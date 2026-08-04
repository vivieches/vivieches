# Purple Dashboard GitHub Profile Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the profile README as a reliable black-and-purple dashboard with visual technology groups, native project cards, current-work statuses, and an improved compact Spotify badge.

**Architecture:** The root README uses GitHub-native Markdown tables and supported HTML for layout. Stable external image services are limited to Skill Icons, Shields.io, the connected Spotify endpoint, and the existing Bomberman output; Python contract tests validate structure and prevent broken widget regressions.

**Tech Stack:** GitHub-Flavored Markdown, HTML, unittest, PyYAML, Skill Icons, Shields.io, spotify-github-profile, GitHub Actions.

## Global Constraints

- Preserve `assets/banner-dark.png`, all four confirmed contact links, and the existing Bomberman workflow.
- Keep visitor-facing copy and alternative text in English.
- Use a near-black, graphite, violet, purple, and lilac visual system.
- Use only real public repositories and factual descriptions.
- Keep `cover_image=false`; never add Spotify credentials, tokens, iframe, autoplay, or large album artwork.
- Do not use GitHub Profile Trophy or GitHub Readme Stats endpoints.
- Do not display invented project completion percentages.

---

### Task 1: Define the dashboard contract

**Files:**
- Modify: `tests/test_profile.py`

**Interfaces:**
- Consumes: `docs/superpowers/specs/2026-08-04-purple-dashboard-profile-design.md`.
- Produces: Assertions that specify the exact README dashboard behavior.

- [ ] **Step 1: Write failing dashboard tests**

Replace the old `theme=compact` expectation with `theme=natemoo-re` and assert a centered `width="320"` card. Add assertions for `## ◆ Tech Stack`, `— Languages —`, `— Systems & Cloud —`, `— Security & Identity —`, purple Shields.io security badges, a two-column `<table>` project grid, `## ◆ Currently Building`, Open Studio and OpenClaw status badges, and the absence of trophy/readme-stats URLs.

- [ ] **Step 2: Verify RED**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
```

Expected: README tests fail because the current document still uses the sparse compact music theme and text-heavy project sections.

### Task 2: Build the visual README dashboard

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: The contract from Task 1, confirmed social URLs, Spotify UID `31yudueg6i5khowcpdmfcs6pfmga`, and the two verified public repositories.
- Produces: The complete visitor-facing profile dashboard.

- [ ] **Step 1: Build the music and stack blocks**

Use diamond-prefixed section titles. Center the Spotify image and set `theme=natemoo-re`, `cover_image=false`, `background_color=0d0d0f`, `bar_color=8b5cf6`, `bar_color_cover=false`, `border_radius=10`, `show_offline=true`, and `width="320"`. Keep the existing encoded Skill Icons rows. Move Active Directory and Microsoft Entra ID into purple `flat-square` Shields.io badges alongside the four security focus areas.

- [ ] **Step 2: Build project and current-work cards**

Create one native `<table>` with two 50% width cells for Open Studio and OpenClaw AI Agents. Each cell contains its real description, technology badges, a purple status badge, and a purple `View repository` link badge. Add a separate compact table under `## ◆ Currently Building` with one row per project and no percentage values.

- [ ] **Step 3: Verify GREEN**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
```

Expected: all tests pass.

### Task 3: Validate and publish the GitHub rendering

**Files:**
- Verify: `README.md`
- Verify: `.github/workflows/bomberman.yml`

**Interfaces:**
- Consumes: The completed dashboard.
- Produces: Published `main` with validated HTML and external assets.

- [ ] **Step 1: Validate GitHub HTML**

Render the README through `gh api markdown` using context `vivieches/vivieches`. Assert that the output contains the banner, music image, both icon groups, both native tables, project links, and Bomberman, with no escaped intended HTML.

- [ ] **Step 2: Validate external assets**

Request Spotify, Skill Icons, Shields.io, and both Bomberman URLs. Require HTTP 200. Inspect the first Spotify SVG line and require `width="320" height="84"`.

- [ ] **Step 3: Publish and verify**

Run the full tests and `git diff --check`, commit the README, tests, and plan, push `main`, then compare the local commit SHA with the public GitHub SHA and verify the Bomberman workflow completes successfully.
