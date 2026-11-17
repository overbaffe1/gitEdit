import { build } from 'esbuild';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { execFileSync } from 'node:child_process';
const here = dirname(fileURLToPath(import.meta.url));
await build({
  entryPoints: [join(here, 'app.js')],
  outfile: join(here, '../docs/stage.js'),
  format: 'iife',
  bundle: true,
  minify: true,
  target: 'es2020',
  legalComments: 'eof',
});
execFileSync('python3', [join(here, 'pack.py')], { stdio: 'inherit' });
