const test = require("node:test");
const assert = require("node:assert");
const { formatBoard } = require("../lib/board");

const arrivals = [
  { time: "14:10", vessel: "Lady Kelleys" },
  { time: "09:45", vessel: "Erie Wind" },
];

test("keeps input order by default", () => {
  assert.strictEqual(formatBoard(arrivals), "14:10  Lady Kelleys\n09:45  Erie Wind");
});

test("sorts by time", () => {
  assert.strictEqual(formatBoard(arrivals, { sort: "time" }), "09:45  Erie Wind\n14:10  Lady Kelleys");
});
