import fs from 'fs';
import path from 'path';

const ROOT = process.cwd();
const INSIGHT_DIR = path.join(ROOT, 'src', 'content', 'insight');
const RULES_FILE = path.join(ROOT, 'content-rules.json');

console.log('--- [wiseaiwiseu pre-build validation] ---');

// 1. Load content rules
let forbiddenPhrases = [];
if (fs.existsSync(RULES_FILE)) {
  const rules = JSON.parse(fs.readFileSync(RULES_FILE, 'utf-8'));
  forbiddenPhrases = rules.forbidden_phrases || [];
}

let hasError = false;

if (fs.existsSync(INSIGHT_DIR)) {
  const files = fs.readdirSync(INSIGHT_DIR).filter(f => f.endsWith('.md') || f.endsWith('.mdx'));
  
  for (const file of files) {
    const fullPath = path.join(INSIGHT_DIR, file);
    let content = fs.readFileSync(fullPath, 'utf-8');
    if (content.charCodeAt(0) === 0xFEFF) {
      content = content.slice(1);
    }

    // Split frontmatter and body
    const parts = content.split(/^---\s*$/m);
    if (parts.length < 3) {
      console.warn(`[WARN] ${file}: Missing valid frontmatter structure.`);
      continue;
    }

    const fm = parts[1];
    const body = parts.slice(2).join('---');

    // Rule 1: Check generated_by vs reviewed_by
    const genMatch = fm.match(/generated_by:\s*["']?([^"'\r\n]+)["']?/);
    const revMatch = fm.match(/reviewed_by:\s*["']?([^"'\r\n]+)["']?/);
    const approvedMatch = fm.match(/human_approved:\s*(true|false)/);

    if (genMatch && revMatch) {
      const gen = genMatch[1].trim();
      const rev = revMatch[1].trim();
      if (gen === rev) {
        console.error(`[ERROR] ${file}: generated_by and reviewed_by must not be identical (${gen})`);
        hasError = true;
      }
    }

    if (approvedMatch && approvedMatch[1].trim() === 'false') {
      console.error(`[ERROR] ${file}: human_approved is false. Unapproved documents cannot be published.`);
      hasError = true;
    }

    // Rule 2: Check forbidden investment advice phrases (Section 7.3)
    for (const phrase of forbiddenPhrases) {
      if (body.includes(phrase)) {
        console.error(`[ERROR] ${file}: Contains forbidden investment recommendation phrase: "${phrase}"`);
        hasError = true;
      }
    }
  }
}

if (hasError) {
  console.error('\nPre-build validation FAILED. Aborting build.\n');
  process.exit(1);
} else {
  console.log('Pre-build validation PASSED.\n');
}