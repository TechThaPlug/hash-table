const multer = require("multer");
const { redirectWith } = require("../utils/flash");
const { MAX_FILE_SIZE } = require("../utils/fileCheck");

const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: MAX_FILE_SIZE, files: 1 },
});

// Runs multer, and turns its errors into friendly messages
function handleUpload(req, res, next) {
  upload.single("file")(req, res, (error) => {
    if (!error) {
      return next();
    }

    const back = `/folders/${req.folder.id}`;

    if (
      error instanceof multer.MulterError &&
      error.code === "LIMIT_FILE_SIZE"
    ) {
      return redirectWith(
        req,
        res,
        next,
        back,
        "error",
        "That file is larger than 5 MB.",
      );
    }

    console.error(error);
    redirectWith(
      req,
      res,
      next,
      back,
      "error",
      "The upload failed. Please try again.",
    );
  });
}

module.exports = { handleUpload };
