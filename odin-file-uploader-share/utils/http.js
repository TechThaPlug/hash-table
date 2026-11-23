function notFound(res, message = "That page doesn't exist.") {
  res.status(404).render("404", { title: "Not found", message });
}

module.exports = { notFound };
