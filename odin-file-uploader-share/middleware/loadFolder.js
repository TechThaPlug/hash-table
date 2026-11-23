const prisma = require("../db/prisma");
const { parseId } = require("../utils/ids");
const { notFound } = require("../utils/http");

// Loads the folder only if it belongs to the logged-in user
async function loadFolder(req, res, next) {
  const id = parseId(req.params.id);

  const folder =
    id === null
      ? null
      : await prisma.folder.findFirst({ where: { id, userId: req.user.id } });

  if (!folder) {
    return notFound(res, "That folder doesn't exist.");
  }

  req.folder = folder;
  next();
}

module.exports = { loadFolder };
