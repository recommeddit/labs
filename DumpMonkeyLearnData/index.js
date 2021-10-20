require('dotenv').config();

const jetpack = require("fs-jetpack");
const truncate = require("just-truncate");
const { chromium } = require('playwright');

const MAX_LEN = 35;

(async () => {
  const isHeadless = process.env.USE_HEADLESS.toLowerCase() === "true";
  if (isHeadless) {
    console.log("Headless mode activated! Launching chromium browser without display...");
  } else {
    console.log("Headless mode disabled! Launching chromium browser with display...");
  }
  const browser = await chromium.launch({ headless: process.env.USE_HEADLESS === "true" });
  console.log("Browser successfully launched!");

  const skipAuth = await jetpack.existsAsync('auth.json');

  let context;
  if (skipAuth) {
    console.log("auth.json file detected. Setting cookies and localstorage to it...");
    context = await browser.newContext({ storageState: "auth.json" });
  } else {
    console.log("auth.json file missing! Generating empty browser context...");
    context = await browser.newContext();
  }

  console.log("Creating new tab...");
  const page = await context.newPage();
  console.log("New tab created!");

  console.log("Visiting MonkeyLearn dashboard website...");
  await page.goto('https://app.monkeylearn.com/');

  if (!skipAuth) {
    console.log("Attempting login filling process...");
    await page.fill('[placeholder="Email address"]', process.env.MONKEYLEARN_USERNAME);
    await page.fill('[placeholder="Password"]', process.env.MONKEYLEARN_PASSWORD);
    await page.click('input:has-text("Login")');
  }

  // Click on model (e.g., Recommendation Extractor)
  const modelName = process.env.MODEL_NAME;
  console.log(`Clicking on the appropriate model (${modelName})`);
  await page.click(`text=${process.env.MODEL_NAME}`);

  console.log("Navigating to data list...");
  // e.g., /main/extractors/ex_Zcaa6vKA/ -> /main/extractors/ex_Zcaa6vKA/tab/build
  await page.click('text=Build');

  // /main/extractors/ex_Zcaa6vKA/tab/build -> /main/extractors/ex_Zcaa6vKA/tab/data/
  await page.click('text=Data');

  console.log("Selecting all data...");
  // Select current page of data
  await page.click('checkbox div');

  // Select all data
  if (isHeadless) {
    console.log("We're in headless mode, so we wait for 'Select all' text to mount, not visible");
    const el = await page.waitForSelector('text=Select all', { state: "attached" });
    console.log("Discovered it mounted. Clicking on it (without waiting for visibility)...");
    await el.click({ force: true });
  } else {
    await page.click('text=Select all');
  }

  console.log("Selected successfully! Starting logging...");
  // Start tagging
  await page.click('text=Actions');
  await page.click('text=Tag selected data');

  const numExamples = Number(await page.innerText('[data-bind="text: selectedSamplesToGo"]'));
  console.log(`Found a total of ${numExamples} entries in the dataset! Beginning to process them...`);

  const dataset = [];

  for (let i = 0; i < numExamples; i++) {
    // Use a glob URL pattern
    console.log(`\nExample ${i + 1} of ${numExamples}:`);
    console.log('Waiting on API for text and labels...');
    const [res] = await Promise.all([
      page.waitForResponse('**/sample_to_tag/**'),
      page.click('text=SKIP'),
    ]);
    console.log('Got the text and labels! Processing...');
    const { data } = await res.json();
    const { sample } = data;
    const { text, annotations } = sample;

    dataset.push({
      text,
      annotations: annotations.map(({ start_char: start_idx, end_char: end_idx }) =>
        ({ text: text.substring(start_idx, end_idx), start_idx, end_idx }))
    });
    console.log(`Successfully stored "${truncate(text, MAX_LEN).replace(/\n/g, "\\n")}" to array!`);
  }

  console.log("\nDone iterating over the dataset! Writing to json...");

  (async () => {
    await jetpack.writeAsync('./dataset.json', JSON.stringify(dataset, null, 2));
    console.log("successfully wrote dataset to dataset.json!");
  })();

  try {
    console.log("Double-checking that we are at the end screen...");
    await page.waitForSelector('text=All your data is tagged. Well done!', { timeout: 5000 });
    console.log("It appears we are! Excellent. 😎")
  } catch {
    console.error("We didn't finish all the examples! ⚠️");
    console.log("Writing screenshot of current page to error.png...");
    await page.screenshot({ path: 'error.png' });
    console.log("Successfully wrote screenshot to error.png");
  }

  // ---------------------
  console.log("Writing current cookies/localstorage to auth.json...");
  await context.storageState({ path: 'auth.json' });
  console.log("Successfully wrote current cookies/localstorage to auth.json");
  console.log("Closing out of context and browser...");
  await context.close();
  await browser.close();
  console.log("Done. Have a nice day!");
})();