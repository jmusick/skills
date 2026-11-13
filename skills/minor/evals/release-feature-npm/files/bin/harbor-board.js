#!/usr/bin/env node
const { formatBoard } = require("../lib/board");

const args = process.argv.slice(2);
const sortArg = args.find((a) => a.startsWith("--sort="));
const arrivals = [
  { time: "14:10", vessel: "Lady Kelleys" },
  { time: "09:45", vessel: "Erie Wind" },
];
console.log(formatBoard(arrivals, { sort: sortArg ? sortArg.slice(7) : "none" }));
