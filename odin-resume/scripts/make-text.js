const fs = require("node:fs");
const path = require("node:path");

const htmlPath = path.join(__dirname, "..", "resume.html");
const outputPath = path.join(__dirname, "..", "resume-ats.txt");

let html = fs.readFileSync(htmlPath, "utf8");

html = html
  .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, "")
  .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, "")
  .replace(/<!--[\s\S]*?-->/g, "")
  .replace(
    /<a\b[^>]*href=["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/gi,
    (_, url, content) => `${content} (${url})`,
  );

const text = html
  .replace(/<br\s*\/?>/gi, "\n")
  .replace(/<\/(h1|h2|h3|p|div|section|article|header)>/gi, "\n")
  .replace(/<[^>]+>/g, "")
  .replace(/&nbsp;/g, " ")
  .replace(/&amp;/g, "&")
  .replace(/&lt;/g, "<")
  .replace(/&gt;/g, ">")
  .replace(/&quot;/g, '"')
  .replace(/&#39;/g, "'")
  .replace(/[ \t]+/g, " ")
  .replace(/\n\s*\n+/g, "\n\n")
  .trim();

fs.writeFileSync(outputPath, text, "utf8");

console.log("ATS text file updated successfully.");
console.log("\n===== EXTRACTED RESUME TEXT =====\n");
console.log(text);
