# Apply this package to `validated-pattern`

```bash
git clone --branch validated-pattern https://github.com/acicrome/ai-optimization.git
cd ai-optimization
unzip -o /path/to/ai-optimization-validated-pattern-helm.zip -d /tmp/ai-optimization-vp
rsync -a --delete --exclude .git /tmp/ai-optimization-vp/ai-optimization/ ./
make validate
git status
git add .
git commit -m "Convert AI Optimization applications to parameterized Helm charts"
git push origin validated-pattern
```

Inspect `git status` and the rendered files under `dist/rendered/` before committing. The package does not include `.git`
and does not push automatically.
