# Repository Discovery Automation

This workflow discovers repositories for NayumAhmed across AI tools, browser games, developer tools, Android/Google TV, automation agents, and web apps. It screens metadata and is designed for a maximum of 10 fork requests per rolling seven-day window.

## Safety limits

- It never clones, builds, installs, or executes candidate code.
- Candidates need an identifiable SPDX open-source licence, a README, a useful description, at least 100 stars, and a push within the last 180 days.
- Archived/disabled repositories and candidate repositories that are already forks are rejected.
- Existing repositories under your account are skipped.
- Metadata screening is not a malware scan or a guarantee of safety.
- GitHub's fork API is asynchronous. A successful request is not confirmation that the fork has finished appearing in your account.
- Forks preserve the upstream relationship and source attribution. Each project stays in its own repository.

## One-time setup

1. Open this repository's Settings → Secrets and variables → Actions → New repository secret.
2. Name the secret exactly FORK_AUTOMATION_TOKEN.
3. Create a fine-grained personal access token at https://github.com/settings/personal-access-tokens/new. Select your account as the resource owner and set a short practical expiry.
4. Give the token only the minimum repository permissions accepted for the fork endpoint. GitHub documents either Administration: write + Contents: read, or Contents: read + Repository creation: write. Use the least-privilege option accepted by GitHub for your account. Do not use a classic token with broad repo scope unless no narrower supported option is available.
5. Save the token in the GitHub Actions secret field only. Do not commit it, paste it into issues, or share it in ChatGPT.
6. Ensure GitHub Actions are enabled.
7. Run Actions → Repository Discovery and Safe Forks → Run workflow with dry_run=true. Review the report before enabling fork requests.
8. If the report looks appropriate, manually run with dry_run=false. Scheduled runs default to dry-run mode until you explicitly change the workflow's DRY_RUN policy.

## Schedule and cap

- Runs each Monday at 04:30 UTC (10:00 AM India Standard Time).
- Intended maximum: 10 fork requests per rolling seven-day period.
- Minimum 100 stars and last push within 180 days.
- Discovery reports are uploaded as workflow artifacts and committed under reports/.

## Before using a fork

Review the source owner, licence, README, dependencies, release history, security advisories, build scripts, and GitHub Actions workflows before running anything. Treat external repository contents as untrusted input.

## Limitations

GitHub search results and topic labels can be incomplete. Stars are not proof of quality. SPDX metadata can be missing or incorrect; missing/unclear licences are rejected instead of guessed. The automated checks are heuristics, not a security audit. Review the report and verify each fork in your repository list.
