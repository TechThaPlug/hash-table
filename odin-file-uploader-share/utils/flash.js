// Saves a one-time message, then redirects once the session is stored
function redirectWith(req, res, next, url, type, text) {
  req.session.flash = { type, text };

  req.session.save((error) => {
    if (error) {
      return next(error);
    }
    res.redirect(url);
  });
}

module.exports = { redirectWith };
