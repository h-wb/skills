# skills: instructions for agents

The shared skills of every agent in the homelab. Start with the [handbook](https://github.com/h-wb/handbook) and this repo's [README](README.md).

- This repo is public and every scope reads it: no personal details, no domain, no secrets, no private tool's data.
- One folder per skill, `skills/<name>/SKILL.md`, `name` equal to the folder. Rename a skill only with the places that declare it (dotfiles, home-ops) in the same change.
- A skill is a map: it links the handbook page or repo page that holds a rule, and never restates it.
- Run `mise run check` before each commit.
- Branch and pull request; the default branch is `main`. A pull request names its task (`HOMEL-<n>`).
