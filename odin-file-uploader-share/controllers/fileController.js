const prisma = require("../db/prisma");
const { inspectFile, cleanFileName } = require("../utils/fileCheck");
const { uploadBuffer, deleteStored } = require("../utils/storage");
const { sendDownload } = require("../utils/download");
const { redirectWith } = require("../utils/flash");

async function create(req, res, next) {
  const folder = req.folder;
  const back = `/folders/${folder.id}`;
  const file = req.file;

  if (!file) {
    return redirectWith(
      req,
      res,
      next,
      back,
      "error",
      "Please choose a file to upload.",
    );
  }

  const check = inspectFile(file);
  if (!check.ok) {
    return redirectWith(req, res, next, back, "error", check.message);
  }

  let result;

  try {
    result = await uploadBuffer(file.buffer, req.user.id);
  } catch (error) {
    console.error(error);
    return redirectWith(
      req,
      res,
      next,
      back,
      "error",
      "Could not store the file. Please try again.",
    );
  }

  const name = cleanFileName(file.originalname);

  try {
    await prisma.file.create({
      data: {
        name,
        size: file.size,
        mimeType: file.mimetype,
        url: result.secure_url,
        publicId: result.public_id,
        resourceType: result.resource_type,
        folderId: folder.id,
      },
    });
  } catch (error) {
    // Don't leave an orphan copy in storage
    await deleteStored({
      publicId: result.public_id,
      resourceType: result.resource_type,
    }).catch(() => {});
    throw error;
  }

  redirectWith(req, res, next, back, "success", `Uploaded "${name}".`);
}

function show(req, res) {
  const file = req.storedFile;
  res.render("files/show", { title: file.name, file });
}

async function download(req, res, next) {
  const file = req.storedFile;
  const sent = await sendDownload(res, file);

  if (!sent) {
    redirectWith(
      req,
      res,
      next,
      `/files/${file.id}`,
      "error",
      "The stored file could not be fetched right now.",
    );
  }
}

async function remove(req, res, next) {
  const file = req.storedFile;

  await deleteStored(file).catch((error) => console.error(error));
  await prisma.file.delete({ where: { id: file.id } });

  redirectWith(
    req,
    res,
    next,
    `/folders/${file.folderId}`,
    "success",
    `Deleted "${file.name}".`,
  );
}

module.exports = { create, show, download, remove };
