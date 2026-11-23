const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const htmlFiles = ["index.html", "blog.html"];

const errors = [];
const warnings = [];

for (const file of htmlFiles) {
  const filePath = path.join(root, file);

  if (!fs.existsSync(filePath)) {
    errors.push(`Missing file: ${file}`);
    continue;
  }

  const html = fs.readFileSync(filePath, "utf8");

  console.log(`\nChecking ${file}...`);

  if (html.includes("YOUR_EMAIL_HERE")) {
    errors.push(`${file}: Contact email placeholder remains.`);
  }

  if (/href\s*=\s*["']#["']/.test(html)) {
    warnings.push(`${file}: Empty placeholder link found.`);
  }

  const references = html.matchAll(/(?:href|src)=["']([^"']+)["']/g);

  for (const match of references) {
    const url = match[1];

    if (
      !url ||
      url.startsWith("#") ||
      url.startsWith("http://") ||
      url.startsWith("https://") ||
      url.startsWith("mailto:") ||
      url.startsWith("tel:") ||
      url.startsWith("data:") ||
      url.startsWith("javascript:")
    ) {
      continue;
    }

    const localPath = path.join(root, url.split(/[?#]/)[0]);

    if (!fs.existsSync(localPath)) {
      errors.push(`${file}: Missing local file: ${url}`);
    }
  }

  console.log("Finished checking " + file);
}

console.log("\n========== WEBSITE CHECK ==========");

if (warnings.length) {
  console.log("\nWARNINGS:");
  warnings.forEach((item) => console.log("WARNING:", item));
}

if (errors.length) {
  console.log("\nERRORS:");
  errors.forEach((item) => console.log("ERROR:", item));
  console.log("\nWebsite check FAILED.");
  process.exitCode = 1;
} else {
  console.log("\nNo missing local files or contact placeholders found.");
  console.log("Website check PASSED.");
}
