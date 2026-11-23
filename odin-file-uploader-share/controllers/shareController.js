const prisma = require("../db/prisma");
const { isUuid, parseId } = require("../utils/ids");
const { notFound } = require("../utils/http");
const { sendDownload } = require("../utils/download");
const { redirectWith } = require("../utils/flash");

const DAY = 24 * 60 * 60 * 1000;
const DURATIONS = { "1d": 1, "3d": 3, "7d": 7, "10d": 10, "30d": 30 };

async function create(req, res, next) {
  const back = `/folders/${req.folder.id}`;
  const choice = String(req.body.duration ?? "");

  if (!Object.hasOwn(DURATIONS, choice)) {
    return redirectWith(
      req,
      res,
      next,
      back,
      "error",
      "Please choose how long the link should last.",
    );
  }

  await prisma.shareLink.create({
    data: {
      folderId: req.folder.id,
      expiresAt: new Date(Date.now() + DURATIONS[choice] * DAY),
    },
  });

  redirectWith(
    req,
    res,
    next,
    back,
    "success",
    `Share link created. It works for ${choice}.`,
  );
}

async function revoke(req, res, next) {
  const id = String(req.params.id ?? "");

  const link = isUuid(id)
    ? await prisma.shareLink.findFirst({
        where: { id, folder: { userId: req.user.id } },
      })
    : null;

  if (!link) {
    return notFound(res, "That link doesn't exist.");
  }

  await prisma.shareLink.delete({ where: { id: link.id } });
  redirectWith(
    req,
    res,
    next,
    `/folders/${link.folderId}`,
    "success",
    "Share link removed.",
  );
}

// Public pages: a valid, unexpired link is the only permission needed
async function findActiveLink(id) {
  if (!isUuid(id)) {
    return null;
  }

  return prisma.shareLink.findFirst({
    where: { id, expiresAt: { gt: new Date() } },
    include: {
      folder: { include: { files: { orderBy: { uploadedAt: "desc" } } } },
    },
  });
}

async function showPublic(req, res) {
  const link = await findActiveLink(req.params.id);

  if (!link) {
    return notFound(res, "This link has expired or doesn't exist.");
  }

  res.render("share/show", {
    title: link.folder.name,
    link,
    folder: link.folder,
  });
}

async function downloadPublic(req, res, next) {
  const link = await findActiveLink(req.params.id);
  const fileId = parseId(req.params.fileId);

  if (!link || fileId === null) {
    return notFound(res, "This link has expired or doesn't exist.");
  }

  // The file must belong to the shared folder
  const file = await prisma.file.findFirst({
    where: { id: fileId, folderId: link.folderId },
  });

  if (!file) {
    return notFound(res, "That file isn't in this shared folder.");
  }

  const sent = await sendDownload(res, file);

  if (!sent) {
    redirectWith(
      req,
      res,
      next,
      `/share/${link.id}`,
      "error",
      "That file could not be fetched right now.",
    );
  }
}

module.exports = { create, revoke, showPublic, downloadPublic };
