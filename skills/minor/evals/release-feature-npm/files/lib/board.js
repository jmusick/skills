function formatBoard(arrivals, { sort = "none" } = {}) {
  const rows = [...arrivals];
  if (sort === "time") rows.sort((a, b) => a.time.localeCompare(b.time));
  if (sort === "vessel") rows.sort((a, b) => a.vessel.localeCompare(b.vessel));
  return rows.map((r) => `${r.time}  ${r.vessel}`).join("\n");
}

module.exports = { formatBoard };
