const prisma = require("../db/prisma");
const { parseId } = require("../utils/ids");
const { notFound } = require("../utils/http");

// Loads the file only if its folder belongs to the logged-in user
async function loadFile(req, res, next) {
  const id = parseId(req.params.id);

  const file =
    id === null
      ? null
      : await prisma.file.findFirst({
          where: { id, folder: { userId: req.user.id } },
          include: { folder: true },
        });

  if (!file) {
    return notFound(res, "That file doesn't exist.");
  }

  req.storedFile = file;
  next();
}

module.exports = { loadFile };
