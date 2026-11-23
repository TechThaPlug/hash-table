const { Readable } = require("node:stream");
const { pipeline } = require("node:stream/promises");

function contentDisposition(name) {
  const fallback = name.replace(/[^\x20-\x7e]/g, "_").replace(/["\\]/g, "_");
  const encoded = encodeURIComponent(name).replace(
    /['()*]/g,
    (char) => "%" + char.charCodeAt(0).toString(16).toUpperCase(),
  );

  return `attachment; filename="${fallback}"; filename*=UTF-8''${encoded}`;
}

// Streams a stored file to the browser. Returns false if the file couldn't be fetched.
async function sendDownload(res, file) {
  const upstream = await fetch(file.url);

  if (!upstream.ok || !upstream.body) {
    return false;
  }

  res.setHeader("Content-Type", file.mimeType);
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("Content-Disposition", contentDisposition(file.name));

  await pipeline(Readable.fromWeb(upstream.body), res);
  return true;
}

module.exports = { sendDownload };
