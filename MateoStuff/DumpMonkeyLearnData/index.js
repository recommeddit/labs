require('dotenv').config();

const jetpack = require("fs-jetpack");
const truncate = require("just-truncate");
const { chromium } = require('playwright');
const delay = require('delay');

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

  const authFileExists = await jetpack.existsAsync('auth.json');
  let authLastModified;
  let envLastModified;
  let skipAuth;
  if (authFileExists) {
    authLastModified = (await jetpack.inspectAsync("auth.json", { times: true })).modifyTime;
    envLastModified = (await jetpack.inspectAsync(".env", { times: true })).modifyTime;
    skipAuth = (authLastModified > envLastModified);
  } else {
    skipAuth = false;
  }

  let context;
  if (skipAuth) {
    console.log("auth.json file detected and up-to-date. Setting cookies and localstorage to it...");
    context = await browser.newContext({ storageState: "auth.json" });
  } else {
    if (!authFileExists) {
      console.log("auth.json file missing!");
    } else {
      console.log(`auth.json file (${authLastModified}) out-of-date compared to .env (${envLastModified})...`);
    }
    console.log("Generating empty browser context...");
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

  await page.click('text=My Models');

  // Click on model (e.g., Recommendation Extractor)
  const modelName = process.env.MODEL_NAME;
  console.log(`Clicking on the appropriate model (${modelName})`);
  await page.click(`text=${process.env.MODEL_NAME}`);

  console.log("Navigating to data list...");
  // e.g., /main/extractors/ex_Zcaa6vKA/ -> /main/extractors/ex_Zcaa6vKA/tab/build
  await page.click('text=Build');

  const numLabeledExamples = Number(await page.innerText('[data-bind="number: numberOfStep"]'));

  console.log(`I see there is a total of ${numLabeledExamples} labeled examples! I'll keep this in mind...`);

  // /main/extractors/ex_Zcaa6vKA/tab/build -> /main/extractors/ex_Zcaa6vKA/tab/data/
  await page.click('text=Data');

  console.log(`Selecting the oldest ${numLabeledExamples} examples...`);
  await page.locator('text=Sort By').click();
  await page.locator('text=Oldest').click();

  console.log("Selecting current page data...");

  console.log("Waiting three seconds for good measure...");

  await delay(3000);

  // Select current page of data
  await page.click('.select-all checkbox div');

  console.log("Selecting all data...");

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

  const dataset = [];

  const totalExamples = Number(await page.innerText('[data-bind="text: selectedSamplesToGo"]'));

  for (let i = 0; i < numLabeledExamples; i++) {
    // Use a glob URL pattern
    console.log(`\nExample ${i + 1} of ${numLabeledExamples}:`);
    console.log('Waiting on API for text and labels...');
    const [res] = await Promise.all([page.waitForResponse('**/sample_to_tag/**'), page.click(
      'text=SKIP')]);
    console.log('Got the text and labels! Processing...');
    const { data } = await res.json();
    const { sample } = data;
    const { text, annotations } = sample;

    dataset.push({
      text,
      annotations: annotations.map(({ start_char: start_idx, end_char: end_idx }) => ({
        text: text.substring(start_idx, end_idx),
        start_idx,
        end_idx,
      })),
    });
    console.log(`Successfully stored "${truncate(text, MAX_LEN).replace(/\n/g, "\\n")}" to array!`);
  }

  console.log("\nDone iterating over the dataset! Writing to json...");

  (async () => {
    await jetpack.writeAsync(`./${process.env.OUTPUT_FILENAME}`, JSON.stringify(dataset, null, 2));
    console.log("Successfully wrote dataset to dataset.json!");
  })();

  console.log("Double-checking that we have labeled the number of examples we expected...");
  const numExamplesLeft = Number(await page.innerText('[data-bind="text: selectedSamplesToGo"]'));
  if (totalExamples - numExamplesLeft !== numLabeledExamples) {
    console.log("Something went wrong! We didn't label the expected number of examples!");
    console.log(`Expected ${totalExamples - numLabeledExamples} examples left, but got ${numExamplesLeft} instead!`);
    console.log("Writing screenshot of current page to error.png...");
    await page.screenshot({ path: 'error.png' });
    console.log("Successfully wrote screenshot to error.png");
  } else {
    console.log("It appears we did! Excellent. 😎")
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
