const fs = require("node:fs");
const path = require("node:path");

const resumePath = path.join(__dirname, "..", "resume.html");
const cssPath = path.join(__dirname, "..", "resume.css");

const html = fs.readFileSync(resumePath, "utf8");
const css = fs.readFileSync(cssPath, "utf8");

const checks = [];
const add = (name, passed, message) => {
  checks.push({ name, passed, message });
};

add(
  "HTML document declaration",
  /<!doctype html>/i.test(html),
  "HTML5 document declaration",
);

add(
  "Page language",
  /<html lang="en">/i.test(html),
  "English language is declared",
);

add("Page title", /<title>[^<]+<\/title>/i.test(html), "Page has a title");

add(
  "Professional summary",
  /<h2>Professional Summary<\/h2>/i.test(html),
  "Professional summary section exists",
);

add(
  "Technical skills",
  /<h2>Technical Skills<\/h2>/i.test(html),
  "Technical skills section exists",
);

add(
  "Projects section",
  /<h2>Projects<\/h2>/i.test(html),
  "Projects section exists",
);

add(
  "Project entries",
  (html.match(/class="project"/g) || []).length >= 3,
  "At least three project entries exist",
);

add(
  "GitHub profile",
  /https:\/\/github\.com\/TechThaPlug/i.test(html),
  "GitHub profile link exists",
);

add(
  "Portfolio link",
  /https:\/\/techthaplug\.github\.io\//i.test(html),
  "Portfolio link exists",
);

add(
  "Stylesheet",
  /href="resume\.css"/i.test(html),
  "Resume stylesheet is linked",
);

add(
  "A4 print layout",
  /size:\s*A4/i.test(css),
  "A4 print layout is configured",
);

const placeholders = [/\[YOUR FULL NAME\]/i, /\[Add your education/i];

const remainingPlaceholders = placeholders.some((pattern) =>
  pattern.test(html),
);

add(
  "Personal placeholders",
  !remainingPlaceholders,
  remainingPlaceholders
    ? "Replace remaining name and education placeholders"
    : "No known personal placeholders remain",
);

const errors = checks.filter((check) => !check.passed);

console.log("\n===== RESUME QUALITY CHECK =====\n");

for (const check of checks) {
  console.log(
    `${check.passed ? "PASS" : "FAIL"} - ${check.name}: ${check.message}`,
  );
}

console.log(
  `\nResults: ${checks.length - errors.length}/${checks.length} passed`,
);

if (errors.length > 0) {
  process.exitCode = 1;
} else {
  console.log("\nAll automated checks passed.");
}
