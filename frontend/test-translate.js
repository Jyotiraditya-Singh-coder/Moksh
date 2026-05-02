const translate = require('googletrans').default;

async function test() {
  try {
    const res = await translate('Hello world', 'es');
    console.log('Translate result:', res);
  } catch (err) {
    console.error('Error:', err);
  }
}

test();
