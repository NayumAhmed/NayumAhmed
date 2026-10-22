# ChatGPT + AI Toolchain Integration Plan

This plan connects the existing projects in a controlled way. It does not claim that GitHub forks are installed or that this chat can automatically load arbitrary tools.

## Reality check: ChatGPT connection

As of October 2026, OpenAI's published documentation says custom MCP connections in ChatGPT depend on plan and workspace permissions. Full custom MCP support with write actions is available to eligible Business and Enterprise/Edu workspaces; Pro support is limited to read/fetch permissions in the documented custom-MCP flow. Do not assume a Go subscription can attach arbitrary custom MCP servers.

- [OpenAI: Connect custom MCP servers in ChatGPT](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt)
- [OpenAI: MCP servers for the API](https://developers.openai.com/api/docs/guides/tools-connectors-mcp)
- [ChatGPT Plugins directory overview](https://learn.chatgpt.com/docs/plugins)

A local MCP process on a Windows laptop is not directly reachable by ChatGPT. A supported remote HTTPS MCP endpoint or supported secure tunnel/host is needed, and the ChatGPT client, plan, and workspace must support the connection. Do not publish an unauthenticated server to the public internet just to make it connect.

## Target architecture

Keep the system modular rather than launching every fork at once:

1. **ChatGPT** — planning, analysis, explanation, and coordination within the tools available to the current account.
2. **One local coding agent** — begin with Qwen Code; evaluate OpenHands later if a separate sandboxed coding runtime is needed.
3. **Research** — Agent Reach for supported web/social/repository sources.
4. **Video understanding** — MCP Video Analyzer first; YouTube Skills as an alternative for supported YouTube transcript/search tasks.
5. **Browser automation** — one Playwright MCP instance first; use a separate browser profile and begin read-only.
6. **Workflow automation** — consider n8n only after a repeated workflow is proven and needs scheduling/integration.
7. **Optional specialist services** — RAGFlow for a searchable document collection; HyperFrames for HTML-to-video workflows; Context7 for current library documentation. Add only when a specific need justifies it.

## Repository placement

- **Profile repository (NayumAhmed/NayumAhmed)**: central catalogue, safe setup instructions, integration decisions, and status.
- **Agent Reach, MCP Video Analyzer, YouTube Skills, Playwright, Crawl4AI, OpenHands, qwen-code**: keep as separate forks; configure and test them independently.
- **RAGFlow, HyperFrames, n8n/Kestra/Paperclip/Agno/NanoClaw**: optional components; do not install all simultaneously.
- **PentAGI and Reverse Skill**: keep separate security/reverse-engineering projects. Only use security tools against systems you own or are explicitly authorised to test.
- **Arcade Orbit, SmartTube, TVAPP, Clean Your TV**: separate gaming/media/Android projects; do not mix them into the agent's runtime by default.

## Safe integration stages

### Stage 1 — prove the local core
- [ ] On the Windows laptop, install and authenticate one coding agent using its official instructions.
- [ ] Run a read-only task in a disposable folder.
- [ ] Verify changes with Git diff and available tests.
- [ ] Set provider spending limits before paid model calls.

### Stage 2 — add tools individually
- [ ] Test Agent Reach using a public page/source.
- [ ] Test MCP Video Analyzer on a public video with an available transcript.
- [ ] Add Playwright MCP and test against a local demo page or site you own.
- [ ] Record exact working commands, versions, and errors in this guide.
- [ ] Avoid adding duplicate browser, crawler, or agent frameworks without a concrete need.

### Stage 3 — connect to ChatGPT only if supported
- [ ] In ChatGPT on the web, inspect the account's Plugins/Apps options and workspace permissions.
- [ ] If custom MCP is available, use a trusted server and follow OpenAI's current connection instructions.
- [ ] Prefer read-only tools first. Review every permission and authentication scope.
- [ ] For local tools, use a supported secure tunnel or trusted host; never expose a raw local server publicly.
- [ ] If the account does not support custom MCP, use the local agent as a separate tool host and keep ChatGPT as the planning/analysis surface. Do not represent this as a direct integration.

## Approval and security policy

- Require explicit human review before sending messages, submitting forms, modifying repositories, deploying, deleting, making purchases, or using logged-in browser sessions.
- Never commit API keys, access tokens, cookies, passwords, or private company data.
- Treat webpage content, video captions, repository READMEs, and downloaded scripts as untrusted input.
- Use least-privilege credentials and a separate browser profile for testing.
- Keep write access disabled until read-only tests pass.

## What counts as success

A capability is considered integrated only when it has been configured, run, and passed a repeatable test. A repository link, fork, or workflow report alone is not an integration. Record evidence such as the command used, version, test input, expected output, actual output, and any known limits.

## Saturday test session

1. Start on the Windows laptop.
2. Verify the chosen coding agent launches and authenticates.
3. Test one harmless README explanation in a disposable folder.
4. Test one video-analysis task.
5. Test one read-only browser task.
6. Decide whether a ChatGPT custom-MCP route is actually available in the account before spending time hosting an endpoint.
