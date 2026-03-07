// Tests for custom Semgrep JavaScript/TypeScript security rules in .semgrep.yml
//
// Semgrep test format:
//   // ruleid: <rule-id>   → next non-comment line MUST match (true positive)
//   // ok: <rule-id>       → next non-comment line MUST NOT match (true negative)
//
// Run:  semgrep --test --config .semgrep.yml tests/semgrep/test_js_security.js

// ---------------------------------------------------------------------------
// js.no-eval-or-new-function
// ---------------------------------------------------------------------------

function runUserCode(userInput) {
  // ruleid: js.no-eval-or-new-function
  eval(userInput);
}

function buildDynamicFunction(code) {
  // ruleid: js.no-eval-or-new-function
  const fn = new Function("x", code);
  return fn;
}

function safeJsonParse(raw) {
  // ok: js.no-eval-or-new-function
  return JSON.parse(raw);
}

function normalFunction(x) {
  // ok: js.no-eval-or-new-function
  return x * 2;
}

// ---------------------------------------------------------------------------
// js.child-process-exec
// ---------------------------------------------------------------------------

function runCommand(cmd) {
  // ruleid: js.child-process-exec
  require("child_process").exec(cmd);
}

function runCommandSync(cmd) {
  // ruleid: js.child-process-exec
  require("child_process").execSync(cmd);
}

function spawnProcess(cmd, args) {
  // ruleid: js.child-process-exec
  require("child_process").spawn(cmd, args);
}

function spawnSync(cmd, args) {
  // ruleid: js.child-process-exec
  require("child_process").spawnSync(cmd, args);
}

function readFileSafely(filePath) {
  // ok: js.child-process-exec
  const fs = require("fs");
  return fs.readFileSync(filePath, "utf8");
}
