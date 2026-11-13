const readings = require("../data/tides.json");

function tides() {
  return readings;
}

module.exports = { tides };
