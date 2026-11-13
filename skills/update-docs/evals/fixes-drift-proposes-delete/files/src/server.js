const http = require("node:http");
const config = require("./config");
const { tides } = require("./tides");

const server = http.createServer((req, res) => {
  if (req.url === "/tides") return send(res, 200, tides());
  if (req.url === "/health") return send(res, 200, { ok: true });
  send(res, 404, { error: "not found" });
});

function send(res, status, body) {
  res.writeHead(status, { "content-type": "application/json" });
  res.end(JSON.stringify(body));
}

if (require.main === module) server.listen(config.port);
module.exports = { server };
