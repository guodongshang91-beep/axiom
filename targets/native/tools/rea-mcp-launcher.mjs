// REA MCP launcher.
// Why this exists: WorkBuddy injects ACC_PRODUCT_CONFIG_V3 (~380k chars, a product
// config JSON) into every child process it spawns. The REA MCP server inherits it,
// and when REA launches Ghidra headless it hands the whole inherited environment to
// CreateProcess. Windows measures that block with a 16-bit length field, so ~788KB
// overflows and the call dies with Win32 87 (ERROR_INVALID_PARAMETER), surfacing as
// "Windows value exceeds the native string limit / Ghidra headless launch failed".
// Keep stdio inherited: MCP speaks JSON-RPC over stdin/stdout, nothing may buffer it.

import { spawn } from 'node:child_process';

// Configure for your machine instead of hard-coding a path.
const REA_ENTRY = process.env.REA_ENTRY;
if (!REA_ENTRY) {
  process.stderr.write('[rea-launcher] set REA_ENTRY to your rea-agents/scripts/rea.mjs path\n');
  process.exit(1);
}

// 20000 chars is far below the 32767 limit but still catches any oversized blob.
const OVERSIZE_CHARS = 20000;

const env = { ...process.env };
const dropped = [];
for (const [key, value] of Object.entries(env)) {
  if (typeof value === 'string' && value.length > OVERSIZE_CHARS) {
    delete env[key];
    dropped.push(`${key}(${value.length})`);
  }
}
if (dropped.length > 0) {
  process.stderr.write(`[rea-launcher] dropped oversized env vars: ${dropped.join(', ')}\n`);
}

const args = process.argv.slice(2);
if (args.length === 0) args.push('mcp');

const child = spawn(process.execPath, [REA_ENTRY, ...args], {
  stdio: 'inherit',
  env,
  windowsHide: true,
});

child.on('error', (err) => {
  process.stderr.write(`[rea-launcher] spawn failed: ${err.message}\n`);
  process.exit(1);
});

child.on('exit', (code, signal) => {
  process.exit(code === null ? (signal ? 1 : 0) : code);
});

for (const signal of ['SIGINT', 'SIGTERM']) {
  process.on(signal, () => {
    try {
      child.kill(signal);
    } catch {
      // child already gone
    }
  });
}
