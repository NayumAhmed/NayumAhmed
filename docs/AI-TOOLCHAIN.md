# AI Toolchain: Video, Web Research, Browser Automation & Coding

This guide documents a practical, modular toolchain for Nayum Ahmed's AI projects. It is intentionally separate from Arcade Orbit, Reverse Skill, PentAGI, and the upstream source code of third-party tools.

## What this does — and does not do

- These tools add capabilities to a **separately configured AI agent**. Forking or starring a repository does not install it or change the underlying ChatGPT model.
- A local MCP server is not automatically available inside ChatGPT. ChatGPT custom MCP support depends on account/workspace plan, client, and server transport.
- OpenAI's current help documentation lists custom MCP connections for Business and Enterprise/Edu workspaces, and read/fetch-only custom MCP connections for Pro. Do not assume a ChatGPT Go account can attach arbitrary local MCP servers. Check the current requirements before planning a ChatGPT integration:
  - [Connect custom MCP servers in ChatGPT](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt)
  - [OpenAI MCP server guide](https://developers.openai.com/api/docs/guides/tools-connectors-mcp)
- This toolchain cannot bypass logins, paywalls, DRM, robots policies, or platform access controls. Video access varies by source.

## Recommended architecture

Use one compatible local agent/client (for example, a supported IDE agent or Codex client) as the tool host. Add capabilities gradually:

1. **Agent Reach** — web, social-platform, RSS, and GitHub research routes.
2. **MCP Video Analyzer** — transcripts, keyframes, OCR, and metadata for supported video URLs/files.
3. **Playwright MCP** — browser navigation and testing for sites you are authorised to access.
4. **Crawl4AI** — optional deeper extraction for public websites.
5. **OpenHands** — optional, separate coding-agent environment for repository changes and tests.

Keep YouTube Skills as an alternative route for YouTube transcripts/search. It uses TranscriptAPI and may require account setup/API credits. Avoid configuring several overlapping video tools until you know which one works reliably for your sources.

## Windows-first setup

Run these commands in PowerShell. Check prerequisites first:

```powershell
node --version
npm --version
python --version
git --version
```

For MCP Video Analyzer, the upstream README specifies Node.js 22.12+ and `yt-dlp` for many platform URLs. Install/update the prerequisites using their official instructions:

- Project: https://github.com/guimatheus92/mcp-video-analyzer
- Install `yt-dlp`: https://github.com/yt-dlp/yt-dlp#installation

A compatible MCP client can launch the analyzer with:

```json
{
  "servers": {
    "mcp-video-analyzer": {
      "type": "stdio",
      "command": "npx",
      "args": ["mcp-video-analyzer@latest"]
    }
  }
}
```

The exact configuration file and schema vary by client. The example above follows the project's documented VS Code-style configuration; use the client-specific instructions if using Cursor, Codex, or another host. Restart/reload the client after changing its configuration.

For browser automation, the official Playwright MCP project documents this launch command:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

Again, place this in the configuration format expected by your selected client, not blindly in the video-analyzer configuration file.

## Tool directory

| Tool | Use | Important constraint |
|---|---|---|
| [Agent Reach](https://github.com/NayumAhmed/Agent-Reach) | Web/social/RSS/GitHub research | Follow its current installer and run its diagnostic command; platform support can change |
| [MCP Video Analyzer](https://github.com/NayumAhmed/mcp-video-analyzer) | Video transcripts, frames, OCR, metadata | Platform downloads may fail; install its prerequisites |
| [YouTube Skills](https://github.com/NayumAhmed/youtube-skills) | YouTube transcripts, search, channels/playlists | TranscriptAPI account/credits may be needed |
| [Watch Video Skill](https://github.com/NayumAhmed/watch-video-skill) | Evidence-first local/video URL analysis | Its README says the analysis CLI supports macOS/Linux; use WSL or a supported host on Windows |
| [Playwright](https://github.com/NayumAhmed/playwright) | Browser automation/testing | Use only on sites/accounts you are authorised to access |
| [Crawl4AI](https://github.com/NayumAhmed/crawl4ai) | Structured public-web extraction | Check its current Python/browser requirements |
| [OpenHands](https://github.com/NayumAhmed/OpenHands) | Coding-agent workflows | Run in an isolated environment and review diffs before accepting changes |
| [MCP servers collection](https://github.com/NayumAhmed/servers) | Discover integrations | Vet each server before granting credentials or write access |

These are the user's fork URLs where available; consult each README for its upstream project, current release, and licensing terms.

## Safe rollout order

1. **Start with video analysis** and test one public YouTube video and one local video file. Confirm that the output contains transcript/frame evidence, not only a title or description.
2. **Add Agent Reach** and run its documented diagnostic. Test one public webpage and one search source.
3. **Add Playwright** in a test profile and use it for read-only checks first.
4. **Add Crawl4AI only if needed** for structured extraction that the first research tool cannot handle.
5. **Add OpenHands separately** for coding tasks; start with a disposable test repository or branch.
6. Add API keys only when a tool requires them. Store them in environment variables or the client's secret store; never commit them to Git.
7. Before any write/deploy/delete operation, inspect the proposed diff and require explicit approval.

## Acceptance tests

- [ ] Video summary cites timestamps or points to transcript/frame evidence.
- [ ] Failed or blocked video access is reported as a limitation, not guessed.
- [ ] Web research provides source URLs and separates facts from inference.
- [ ] Browser tests do not change account data or submit forms without approval.
- [ ] Coding-agent changes are isolated on a branch and pass available tests.
- [ ] No API keys, browser cookies, tokens, or private data appear in repository files or logs.

## Important separation rule

Do not merge third-party code into this profile repository, do not overwrite upstream forks as part of this setup, and keep the Arcade Orbit, Reverse Skill, and PentAGI projects independent. This document is an integration guide, not an automatic installer.
