---
area: "[[Homelab]]"
categories:
  - "[[Repos]]"
summary: Every skill the homelab's agents run, written once, and how each agent takes the ones it wants.
topics:
  - "[[Workshop]]"
  - "[[Assistant]]"
created: 2026-11-25T01:00
---

# skills

The skills every agent here runs, each one folder `skills/<name>/SKILL.md` in the [Agent Skills](https://agentskills.io) format. Written once; every harness reads the same folder. Why skills are kept this way, and which agent takes which: the handbook's [Workshop](https://github.com/h-wb/handbook/blob/main/Systems/Workshop.md#the-shared-skills).

| Skill | For |
| --- | --- |
| [`handbook`](skills/handbook/SKILL.md) | Find the one page that answers; keep pages true after a change |
| [`board`](skills/board/SKILL.md) | Read and update the build board |
| [`tool-gateway`](skills/tool-gateway/SKILL.md) | Find and call a homelab tool |
| [`orchestrate`](skills/orchestrate/SKILL.md) | Plan a change and hand its steps to cheaper agents, in a workshop |
| [`paseo-workspace-hygiene`](skills/paseo-workspace-hygiene/SKILL.md) | One workspace per agent, branch and pull request, in a workshop |

## How an agent gets them

The folder is the contract: every harness reads `SKILL.md` folders natively, so nothing converts them.

| Harness | Reads | Choosing |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/` | a link per chosen skill |
| Codex | `~/.agents/skills/` | a link per chosen skill |
| OpenCode | `~/.agents/skills/`, `~/.claude/skills/`, or the `skills` paths in `opencode.json` | a link per chosen skill |
| Vibe | `~/.agents/skills/`, or `skill_paths` in its `config.toml` | a link per chosen skill, or `enabled_skills` |
| The assistant (Hermes) | the folders its config lists | its skill sync copies the names it declares, at a pinned commit |

On the machines and pods dotfiles sets up, it follows this repo's `main` (a submodule brought up to date at every apply and every pod start) and links the skills each place declares: a merged change reaches them with nothing else to push. The assistant's sync job in home-ops copies its own list at a pinned commit, since it runs in the private scope.

Anywhere else, with no dotfiles:

```sh
claude plugin marketplace add h-wb/skills && claude plugin install h-wb@h-wb   # Claude Code; skills are then named h-wb:<skill>
codex plugin marketplace add h-wb/skills                                       # Codex reads the same manifest
npx skills add h-wb/skills --skill handbook                                     # any other harness
```

## Adding or changing a skill

- One folder, `skills/<name>/SKILL.md`, `name` equal to the folder. The `description` says when to use it, in under 1,024 characters: it is all an agent sees until it loads the skill.
- A skill is a map, not a copy: it says where to look and links the page that holds the rule. Keep the body under about sixty lines.
- Nothing private, no domain, no secrets: this repo is public and every scope reads it.
- A skill only one repo needs stays in that repo (`.agents/skills/`). The assistant's scheduled routines stay beside it in home-ops.
- `mise run check` before a pull request. A new skill reaches an agent only when its place declares it.
