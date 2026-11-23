const { Router } = require("express");
const auth = require("../controllers/authController");
const folders = require("../controllers/folderController");
const files = require("../controllers/fileController");
const shares = require("../controllers/shareController");
const { requireLogin } = require("../middleware/auth");
const { loadFolder } = require("../middleware/loadFolder");
const { loadFile } = require("../middleware/loadFile");
const { handleUpload } = require("../middleware/upload");

const router = Router();

router.get("/", (req, res) =>
  req.isAuthenticated()
    ? res.redirect("/folders")
    : res.render("index", { title: "Welcome" }),
);

// Accounts
router.get("/sign-up", auth.showSignUp);
router.post("/sign-up", auth.signUp);
router.get("/log-in", auth.showLogIn);
router.post("/log-in", auth.logIn);
router.post("/log-out", auth.logOut);

// Folders
router.get("/folders", requireLogin, folders.list);
router.post("/folders", requireLogin, folders.create);
router.get("/folders/:id", requireLogin, loadFolder, folders.show);
router.post("/folders/:id/rename", requireLogin, loadFolder, folders.rename);
router.post("/folders/:id/delete", requireLogin, loadFolder, folders.remove);

// Files
router.post(
  "/folders/:id/files",
  requireLogin,
  loadFolder,
  handleUpload,
  files.create,
);
router.get("/files/:id", requireLogin, loadFile, files.show);
router.get("/files/:id/download", requireLogin, loadFile, files.download);
router.post("/files/:id/delete", requireLogin, loadFile, files.remove);

// Sharing (extra credit)
router.post("/folders/:id/share", requireLogin, loadFolder, shares.create);
router.post("/share-links/:id/delete", requireLogin, shares.revoke);
router.get("/share/:id", shares.showPublic);
router.get("/share/:id/files/:fileId/download", shares.downloadPublic);

module.exports = router;
