# GitHub Profile Portfolio Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the existing profile README as a compact English technical portfolio with a small connected Spotify badge.

**Architecture:** The root README composes the existing local illustrated banner with remote, image-only GitHub-compatible services for Skill Icons, Spotify, and Bomberman. Python contract tests verify visitor-facing structure, URLs, parameters, copy, and the workflow without adding runtime dependencies.

**Tech Stack:** GitHub-Flavored Markdown, HTML `<picture>`, unittest, PyYAML, Skill Icons, spotify-github-profile, GitHub Actions.

## Global Constraints

- Preserve `assets/banner-dark.png` as the only banner.
- Preserve LinkedIn, Instagram, TikTok, and YouTube links.
- Keep all visible copy and alternative text in English.
- Use the connected Spotify UID without storing credentials or tokens.
- Use a compact card with `cover_image=false`; never add iframe, autoplay, QR codes, history lists, or large album artwork.
- Feature only the public Open Studio and OpenClaw AI Agents repositories.
- Keep the existing Bomberman automation and omit the profile-view counter.

---

### Task 1: Define the README contract

**Files:**
- Modify: `tests/test_profile.py`

**Interfaces:**
- Consumes: The approved redesign specification and current repository assets.
- Produces: Executable assertions for the complete visitor-facing README contract.

- [ ] **Step 1: Replace obsolete journey and counter assertions**

Add tests for the approved section order, exact technology groups, Focus copy, two public projects, compact Spotify parameters, four contacts, theme-aware icons and Bomberman, and prohibited legacy content.

- [ ] **Step 2: Run the tests and verify RED**

Run `python -m unittest discover -s tests -v`.

Expected: README tests fail because the existing document still contains the large Spotify card, journey sections, and counter.

### Task 2: Implement the portfolio README

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: The assertions from Task 1 and the existing connected Spotify UID.
- Produces: The GitHub profile document shown to visitors.

- [ ] **Step 1: Replace the README body**

Write the approved sections in this order: banner, introduction, Connect with me, Listening to, Tech Stack, Focus, Featured Projects, Contribution Graph. Use `cover_image=false`, `theme=compact`, the dark graphite/purple parameters, and the service redirect link. Use percent-encoded commas in `<source srcset>` icon URLs and normal comma-separated `<img src>` fallbacks.

- [ ] **Step 2: Run the tests and verify GREEN**

Run `python -m unittest discover -s tests -v`.

Expected: all tests pass.

### Task 3: Verify GitHub rendering and remote assets

**Files:**
- Verify: `README.md`
- Verify: `.github/workflows/bomberman.yml`

**Interfaces:**
- Consumes: The completed README.
- Produces: Evidence that GitHub renders the document and external images correctly.

- [ ] **Step 1: Render through GitHub's Markdown API**

Run a read-only `gh api markdown` request with the README as context. Assert that banner, Spotify, icon, project, and Bomberman elements are present and that no intended image tag is escaped as text.

- [ ] **Step 2: Check external image endpoints**

Request the compact Spotify SVG, Skill Icons rows, and both Bomberman SVGs. Confirm successful HTTP responses and inspect the Spotify SVG dimensions to ensure it is compact.

- [ ] **Step 3: Review and publish**

Run `git diff --check`, review the diff, commit the scoped files, push `main`, and verify the repository workflow status.
