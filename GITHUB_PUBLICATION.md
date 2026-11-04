# Publishing the prepared project folder

No repository was supplied for this assignment, and no GitHub write connection was available in this session. No existing repository was modified. Choose a new assignment repository rather than assuming that an unrelated existing repository is the destination.

## Website upload route

1. Create a repository in your GitHub account with a clear assignment name.
2. Extract the ZIP and upload the contents of cmpe-methodologies/ so README.md and the three project directories appear in the repository root. GitHub cannot display folders contained only inside an uploaded ZIP, so extract it first.
3. Include the notebooks, reports, generated tables/figures, scorers, fitted models, and genuine review evidence once obtained. The source data loader handles the source CSVs.
4. Confirm notebook previews show outputs and that relative report/article image links resolve.
5. Replace pending entries in SUBMISSION_LINKS.md with real URLs.

## Git command route

Create an empty repository on GitHub, open a terminal in the extracted folder, and use the exact repository URL you created:

```bash
git init
git add .
git commit -m "Add CRISP-DM, SEMMA, and KDD assignment projects"
git branch -M main
git remote add origin YOUR_NEW_REPOSITORY_URL
git push -u origin main
```

YOUR_NEW_REPOSITORY_URL is a placeholder, not a working command value. Do not reuse these commands inside an unrelated existing checkout. Each fitted artifact in this package is well below GitHub's usual individual-file size limit; inspect newly generated replacements before later uploads.

For Colab, either upload each .ipynb directly or open the actual notebook path from your published GitHub repository in Colab. Add real “Open in Colab” links only after the owner/repository/branch paths exist.
