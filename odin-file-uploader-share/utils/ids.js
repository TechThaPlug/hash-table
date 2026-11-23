// Plain positive whole numbers that fit in a Postgres integer
function parseId(value) {
  const text = String(value ?? "");
  return /^[1-9]\d{0,8}$/.test(text) ? Number(text) : null;
}

function isUuid(value) {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(
    String(value ?? ""),
  );
}

module.exports = { parseId, isUuid };
