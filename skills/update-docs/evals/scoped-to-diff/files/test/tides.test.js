const test = require("node:test");
const assert = require("node:assert");
const { tides } = require("../src/tides");

test("returns the day's readings", () => {
  assert.strictEqual(tides().length, 2);
});
