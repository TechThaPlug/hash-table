const bcrypt = require("bcryptjs");
const passport = require("passport");
const prisma = require("../db/prisma");

const BCRYPT_ROUNDS = 10;

function validateSignUp(body = {}) {
  const username = String(body.username ?? "")
    .trim()
    .toLowerCase();
  const password = String(body.password ?? "");
  const confirm = String(body.confirmPassword ?? "");
  const errors = [];

  if (!/^[a-z0-9_]{3,30}$/.test(username)) {
    errors.push("Username must be 3 to 30 letters, numbers, or underscores.");
  }

  // bcrypt only uses the first 72 bytes, so we cap the length
  if (password.length < 8 || password.length > 72) {
    errors.push("Password must be 8 to 72 characters.");
  }

  if (password !== confirm) {
    errors.push("The two passwords do not match.");
  }

  return { username, password, errors };
}

function showSignUp(req, res) {
  res.render("sign-up", { title: "Sign up", errors: [], username: "" });
}

async function signUp(req, res, next) {
  const { username, password, errors } = validateSignUp(req.body);

  if (errors.length === 0) {
    try {
      const passwordHash = await bcrypt.hash(password, BCRYPT_ROUNDS);

      const user = await prisma.user.create({
        data: { username, password: passwordHash },
        select: { id: true, username: true },
      });

      return req.login(user, (error) => {
        if (error) {
          return next(error);
        }
        res.redirect("/folders");
      });
    } catch (error) {
      // P2002 = unique constraint: that username is taken
      if (error.code !== "P2002") {
        throw error;
      }
      errors.push("That username is already taken.");
    }
  }

  res.status(400).render("sign-up", { title: "Sign up", errors, username });
}

function showLogIn(req, res) {
  const messages = req.session.messages ?? [];
  req.session.messages = [];

  res.render("log-in", { title: "Log in", messages });
}

const logIn = passport.authenticate("local", {
  successRedirect: "/folders",
  failureRedirect: "/log-in",
  failureMessage: true,
});

function logOut(req, res, next) {
  req.logout((error) => {
    if (error) {
      return next(error);
    }
    res.redirect("/");
  });
}

module.exports = { showSignUp, signUp, showLogIn, logIn, logOut };
