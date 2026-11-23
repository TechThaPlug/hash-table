function ensureAuthenticated(req, res, next) {
  if (req.isAuthenticated()) {
    return next();
  }

  req.flash?.("error", "Please log in to continue.");

  return res.redirect("/login");
}

function ensureGuest(req, res, next) {
  if (req.isAuthenticated()) {
    return res.redirect("/dashboard");
  }

  return next();
}

module.exports = {
  ensureAuthenticated,
  ensureGuest,
};
