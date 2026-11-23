require("dotenv").config();

const express = require("express");
const session = require("express-session");
const passport = require("passport");
const path = require("path");

const prisma = require("./config/prisma");
const { PrismaSessionStore } = require("@quixo3/prisma-session-store");

const app = express();

// View engine
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// Middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.use(express.static(path.join(__dirname, "public")));

// Sessions
app.use(
  session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    store: new PrismaSessionStore(prisma, {
      checkPeriod: 2 * 60 * 1000,
      dbRecordIdIsSessionId: true,
    }),
    cookie: {
      maxAge: 1000 * 60 * 60 * 24,
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
    },
  }),
);

// Passport
require("./config/passport")(passport);

app.use(passport.initialize());
app.use(passport.session());

// Global template variables
app.use((req, res, next) => {
  res.locals.currentUser = req.user || null;
  next();
});

// Home route
app.get("/", (req, res) => {
  res.redirect(req.isAuthenticated() ? "/dashboard" : "/login");
});

// Temporary routes
app.get("/login", (req, res) => {
  res.send("Login page - coming soon");
});

app.get("/dashboard", (req, res) => {
  if (!req.isAuthenticated()) {
    return res.redirect("/login");
  }

  res.send(`Welcome ${req.user.email}`);
});

// 404 handler
app.use((req, res) => {
  res.status(404).send("Page not found");
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err);

  res.status(500).send("Internal server error");
});

// Start server
const PORT = process.env.PORT || 3000;

const server = app.listen(PORT, () => {
  console.log(`File Uploader running at http://localhost:${PORT}`);
});

// Graceful shutdown
async function shutdown() {
  console.log("Shutting down server...");

  server.close(async () => {
    await prisma.$disconnect();
    process.exit(0);
  });
}

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
