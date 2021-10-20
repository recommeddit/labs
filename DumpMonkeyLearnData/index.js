require('dotenv').config();

const jetpack = require("fs-jetpack");

const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: process.env.USE_HEADLESS === "true" });

  const skipAuth = await jetpack.existsAsync('auth.json');

  let context;
  if (skipAuth) {
    context = await browser.newContext({ storageState: "auth.json" });
  } else {
    context = await browser.newContext();
  }

  const page = await context.newPage();

  await page.goto('https://app.monkeylearn.com/');

  if (!skipAuth) {
    await page.fill('[placeholder="Email address"]', process.env.MONKEYLEARN_USERNAME);
    await page.fill('[placeholder="Password"]', process.env.MONKEYLEARN_PASSWORD);
    await page.click('input:has-text("Login")');
  }

  // Click on model (e.g., Recommendation Extractor)
  await page.click(`text=${process.env.MODEL_NAME}`);

  // e.g., /main/extractors/ex_Zcaa6vKA/ -> /main/extractors/ex_Zcaa6vKA/tab/build
  await page.click('text=Build');

  // /main/extractors/ex_Zcaa6vKA/tab/build -> /main/extractors/ex_Zcaa6vKA/tab/data/
  await page.click('text=Data');

  // Select current page of data
  await page.click('checkbox div');

  // Select all data
  await page.click('text=Select all');

  // Start tagging
  await page.click('text=Actions');
  await page.click('text=Tag selected data');

  const numExamples = Number(await page.innerText('[data-bind="text: selectedSamplesToGo"]'));

  const dataset = [];

  for (let i = 0; i < numExamples; i++) {
    // Use a glob URL pattern
    const [res] = await Promise.all([
      page.waitForResponse('**/sample_to_tag/**'),
      page.click('text=SKIP'),
    ]);
    const { data } = await res.json();
    const { sample } = data;
    const { text, annotations } = sample;

    dataset.push({
      text,
      annotations: annotations.map(({ start_char: start_idx, end_char: end_idx }) =>
        ({ text: text.substring(start_idx, end_idx), start_idx, end_idx }))
    })
  }

  jetpack.writeAsync('./dataset.json', JSON.stringify(dataset, null, 2));

  try {
    await page.waitForSelector('text=All your data is tagged. Well done!', { timeout: 5000 });
  } catch {
    console.error("We didn't finish all the examples!");
    await page.screenshot({ path: 'error.png' });
  }

  // ---------------------
  await context.storageState({ path: 'auth.json' });
  await context.close();
  await browser.close();
})();