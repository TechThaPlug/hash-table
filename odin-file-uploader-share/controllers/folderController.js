const prisma = require("../db/prisma");
const { deleteStored } = require("../utils/storage");
const { redirectWith } = require("../utils/flash");

const NAME_MAX = 60;

function readName(body = {}) {
  const name = String(body.name ?? "").trim();

  if (!name) {
    return { problem: "Please enter a folder name." };
  }

  if (name.length > NAME_MAX) {
    return { problem: `Folder names must be ${NAME_MAX} characters or fewer.` };
  }

  return { name };
}

async function list(req, res) {
  const folders = await prisma.folder.findMany({
    where: { userId: req.user.id },
    orderBy: { name: "asc" },
    include: { _count: { select: { files: true } } },
  });

  res.render("folders/index", { title: "My folders", folders });
}

async function create(req, res, next) {
  const { name, problem } = readName(req.body);

  if (problem) {
    return redirectWith(req, res, next, "/folders", "error", problem);
  }

  try {
    const folder = await prisma.folder.create({
      data: { name, userId: req.user.id },
    });

    redirectWith(
      req,
      res,
      next,
      `/folders/${folder.id}`,
      "success",
      `Folder "${name}" created.`,
    );
  } catch (error) {
    if (error.code !== "P2002") {
      throw error;
    }
    redirectWith(
      req,
      res,
      next,
      "/folders",
      "error",
      "You already have a folder with that name.",
    );
  }
}

async function show(req, res) {
  const folder = await prisma.folder.findUnique({
    where: { id: req.folder.id },
    include: {
      files: { orderBy: { uploadedAt: "desc" } },
      shares: {
        where: { expiresAt: { gt: new Date() } },
        orderBy: { createdAt: "desc" },
      },
    },
  });

  const baseUrl = `${req.protocol}://${req.get("host")}`;

  const shareLinks = folder.shares.map((share) => ({
    id: share.id,
    url: `${baseUrl}/share/${share.id}`,
    expiresAt: share.expiresAt,
  }));

  res.render("folders/show", { title: folder.name, folder, shareLinks });
}

async function rename(req, res, next) {
  const back = `/folders/${req.folder.id}`;
  const { name, problem } = readName(req.body);

  if (problem) {
    return redirectWith(req, res, next, back, "error", problem);
  }

  try {
    await prisma.folder.update({
      where: { id: req.folder.id },
      data: { name },
    });
    redirectWith(req, res, next, back, "success", "Folder renamed.");
  } catch (error) {
    if (error.code !== "P2002") {
      throw error;
    }
    redirectWith(
      req,
      res,
      next,
      back,
      "error",
      "You already have a folder with that name.",
    );
  }
}

async function remove(req, res, next) {
  const files = await prisma.file.findMany({
    where: { folderId: req.folder.id },
    select: { publicId: true, resourceType: true },
  });

  // Best effort: remove the stored copies, then the database rows
  await Promise.allSettled(files.map(deleteStored));
  await prisma.folder.delete({ where: { id: req.folder.id } });

  redirectWith(
    req,
    res,
    next,
    "/folders",
    "success",
    `Folder "${req.folder.name}" deleted.`,
  );
}

module.exports = { list, create, show, rename, remove };
