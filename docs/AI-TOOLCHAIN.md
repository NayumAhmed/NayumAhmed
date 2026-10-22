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


## Expanded capability map (curated, not a pile of overlapping tools)

The goal is broad capability with a small, maintainable core. These projects are candidates to evaluate and add to the account through the repository-discovery workflow; they are not installed or connected merely by listing them here.

### Highest-priority additions to evaluate

| Capability | Repository | Why it earns a place | Integration note |
|---|---|---|---|
| Browser control and UI testing | [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp) | Structured browser interaction, page inspection, and repeatable tests | Prefer this over adding multiple browser MCPs at once |
| Chrome debugging | [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Console, network, performance, and browser debugging | Add only when browser debugging is a real need |
| Browser agent | [Browser Use](https://github.com/browser-use/browser-use) | Agent-driven browsing for sites where permitted | Separate runtime; review authentication and action permissions |
| Agent workflow automation | [n8n](https://github.com/n8n-io/n8n) | Connect APIs and schedule repeatable workflows | Self-hosting and credentials require configuration |
| MCP server development | [FastMCP](https://github.com/jlowin/fastmcp) | Build and test small custom MCP tools | Useful for bridging specific APIs, not a general model upgrade |
| Current code documentation | [Context7](https://github.com/upstash/context7) | Retrieve version-relevant library documentation | Use through a compatible MCP client |
| Structured web extraction | [Scrapling](https://github.com/D4Vinci/Scrapling) | Alternative extraction/crawling engine | Evaluate alongside Crawl4AI; don't run both without a reason |
| Agent evaluation | [promptfoo](https://github.com/promptfoo/promptfoo) | Test prompts, model outputs, and LLM workflows | Keep test datasets free of secrets and private work data |
| Local model runtime | [Ollama](https://github.com/ollama/ollama) | Run supported models locally where hardware allows | Local models have hardware and quality trade-offs |
| Agent framework | [Pydantic AI](https://github.com/pydantic/pydantic-ai) | Build typed, testable Python agents | Choose one main framework rather than collecting many |
| Agent graph orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) | Stateful multi-step agent workflows | Alternative to Pydantic AI; adopt only if graph orchestration is needed |
| Sandboxed coding agent | [OpenHands](https://github.com/All-Hands-AI/OpenHands) | Coding tasks in an isolated agent environment | Keep separate from profile and production projects |

### Already present in this account (reuse before adding duplicates)

- Agent Reach, MCP Video Analyzer, YouTube Skills, Watch Video Skill
- Playwright, Crawl4AI, OpenHands, and a general MCP servers collection
- PentAGI, Reverse Skill, and Arcade Orbit remain separate projects

Repository names can change and projects may have different licences, system requirements, or maintenance status. Before forking or deploying any candidate, check its official repository for recent activity, licence, security policy, supported runtime, required secrets, and installation instructions.

## What "make ChatGPT capable of everything" realistically means

A GitHub repository does not change the ChatGPT model or automatically grant this chat new tools. Capabilities become usable only when a supported host runs the software and exposes its tools to the model. For this account, the practical path is:

1. Use the existing repository-discovery workflow to produce a report of candidate projects.
2. Review the report for duplicates, licences, maintenance, platform fit, and security.
3. Fork only the highest-value candidates within the workflow's 10-forks-per-week limit.
4. Configure and test them on the Windows laptop or another supported host.
5. Connect the running tools to a compatible agent client; check the current ChatGPT plan/workspace requirements separately before assuming direct ChatGPT integration is supported.

The linked GitHub connector available in this chat can inspect and edit repository files, but it does not expose a fork-creation or workflow-dispatch action. Therefore, this update does not claim to have forked repositories or installed software. To run discovery, open [Repository Discovery and Safe Forks](https://github.com/NayumAhmed/NayumAhmed/actions/workflows/repository-discovery.yml), select **Run workflow**, first use `dry_run=true` to inspect candidates, and only then run with `dry_run=false` if the report looks right. The workflow's configured cap is 10 forks per week.

## Security rules

- Never put tokens, passwords, cookies, or private company data in source files, prompts, issues, or logs.
- Use least-privilege tokens and separate test browser profiles.
- Treat web pages, repository READMEs, downloaded scripts, and model outputs as untrusted input.
- Require review before sending messages, submitting forms, deploying, deleting data, or making purchases.
- Keep security-testing tools limited to systems you own or are explicitly authorised to test.


## Verified forks from the October 2026 discovery run

The expected fork URLs from the discovery report were checked against GitHub repository metadata. All ten exist and report `fork: true`, with the following upstream parents. This verifies that the forks exist; it does not mean they are installed, secure, or connected to ChatGPT.

| Your fork | Upstream | Suggested role | Priority |
|---|---|---|---|
| [rea](https://github.com/NayumAhmed/rea) | [morluto/rea](https://github.com/morluto/rea) | Agent-assisted reverse engineering | Specialist; isolate and only use on authorised targets |
| [paperclip](https://github.com/NayumAhmed/paperclip) | [paperclipai/paperclip](https://github.com/paperclipai/paperclip) | Agent task/organisation management | Later; evaluate after the core agent works |
| [ragflow](https://github.com/NayumAhmed/ragflow) | [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | RAG/document knowledge retrieval | Useful if you need a searchable knowledge base |
| [hyperframes](https://github.com/NayumAhmed/hyperframes) | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | HTML-to-video rendering | Useful for generated training/video assets |
| [agno](https://github.com/NayumAhmed/agno) | [agno-agi/agno](https://github.com/agno-agi/agno) | Agent framework/platform | Candidate framework; compare before choosing |
| [SmartTube](https://github.com/NayumAhmed/SmartTube) | [yuliskov/SmartTube](https://github.com/yuliskov/SmartTube) | Android TV media client | Keep separate from the AI agent toolchain |
| [nanoclaw](https://github.com/NayumAhmed/nanoclaw) | [nanocoai/nanoclaw](https://github.com/nanocoai/nanoclaw) | Containerised messaging/agent workflows | High caution; review integrations and permissions before connecting accounts |
| [kestra](https://github.com/NayumAhmed/kestra) | [kestra-io/kestra](https://github.com/kestra-io/kestra) | Workflow orchestration and scheduling | Later; heavier infrastructure than a simple local setup |
| [qwen-code](https://github.com/NayumAhmed/qwen-code) | [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) | Terminal coding agent | Candidate coding interface; choose one primary coding agent |
| [TVAPP](https://github.com/NayumAhmed/TVAPP) | [youhunwl/TVAPP](https://github.com/youhunwl/TVAPP) | Android TV app catalogue | Keep separate; inspect all APK sources carefully |

### Recommended rollout order for this account

Do not try to run all ten at once. The lowest-friction plan is:

1. **First: existing video/research tools + one browser MCP.** Test MCP Video Analyzer, Agent Reach, and Playwright in one supported host. These map directly to video links, research, and browser tasks.
2. **Second: Qwen Code or OpenHands, not both initially.** Pick one coding agent and test it in a disposable repository/branch.
3. **Third: RAGFlow only if you need document retrieval**, or HyperFrames if the immediate goal is video generation.
4. **Later: n8n/Kestra/Paperclip/Agno/NanoClaw** only when there is a specific workflow that justifies the operational complexity.
5. **Keep Rea, SmartTube, TVAPP, PentAGI, Reverse Skill, and Arcade Orbit isolated** from the general agent runtime unless a specific authorised task calls for them.

Before running any fork, read its installation guide and licence, check open issues and releases, use a disposable test environment, and never supply work credentials or personal account tokens until the need and permissions are understood.
