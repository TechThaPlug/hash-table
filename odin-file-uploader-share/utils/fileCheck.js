const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB

const ascii = (buffer, start, end) =>
  buffer.subarray(start, end).toString("latin1");

// Each allowed type, with a check of the file's real first bytes
const ALLOWED_TYPES = {
  "image/jpeg": (b) => b[0] === 0xff && b[1] === 0xd8 && b[2] === 0xff,
  "image/png": (b) =>
    b[0] === 0x89 && ascii(b, 1, 4) === "PNG" && b[4] === 0x0d && b[5] === 0x0a,
  "image/gif": (b) => ascii(b, 0, 4) === "GIF8",
  "image/webp": (b) => ascii(b, 0, 4) === "RIFF" && ascii(b, 8, 12) === "WEBP",
  "application/pdf": (b) => ascii(b, 0, 5) === "%PDF-",
  "text/plain": (b) => !b.includes(0),
};

const ALLOWED_MESSAGE =
  "Allowed files: JPEG, PNG, GIF, WebP, PDF, and plain text.";

function cleanFileName(name) {
  const base = String(name ?? "")
    .split(/[\\/]/)
    .pop();
  const cleaned = base
    .replace(/[\u0000-\u001f\u007f]/g, "")
    .trim()
    .slice(0, 150);
  return cleaned || "file";
}

function inspectFile(file) {
  if (file.size === 0) {
    return { ok: false, message: "That file is empty." };
  }

  const matches = ALLOWED_TYPES[file.mimetype];

  if (typeof matches !== "function") {
    return { ok: false, message: ALLOWED_MESSAGE };
  }

  if (!matches(file.buffer)) {
    return {
      ok: false,
      message: "That file's contents don't match its type. " + ALLOWED_MESSAGE,
    };
  }

  return { ok: true };
}

module.exports = { MAX_FILE_SIZE, inspectFile, cleanFileName };
