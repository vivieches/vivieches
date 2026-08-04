# GitHub Profile README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build Vitória Ferreira's responsive English-language GitHub profile README with theme-aware banners, an honest technology roadmap, Spotify preparation, a Bomberman contribution graph, social links, and a profile-view counter.

**Architecture:** The root `README.md` composes local theme-aware banner SVGs and documented remote image services. A minimal GitHub Actions workflow generates light and dark Bomberman SVGs daily and publishes them to the existing `output` branch. Validation is performed with XML/YAML parsers and targeted content scans because the repository contains static profile assets rather than an application test suite.

**Tech Stack:** GitHub-flavored Markdown, HTML `<picture>`, SVG 1.1-compatible XML, GitHub Actions YAML, spotify-github-profile, Skill Icons, pacman-contribution-graph v5.0.0, ghaction-github-pages v5, Komarev profile views.

## Global Constraints

- Change only the `vivieches/vivieches` profile repository.
- Keep all visitor-facing text, image alternative text, workflow names, and comments in English.
- Present Vitória Ferreira as a Computer Engineering student, never as an expert, specialist, senior developer, software engineer, or security engineer.
- Use `SPOTIFY_UID` as the sole intentional placeholder and do not store any Spotify credential or token.
- Use `vivieches` for every static username occurrence and `${{ github.repository_owner }}` inside the workflow.
- Generate only Bomberman using `games: "bomberman"`.
- Preserve the confirmed LinkedIn, Instagram, TikTok, and YouTube URLs.
- Avoid unnecessary statistics, generic motivational copy, excessive badges, and unsupported technology icons.

---

### Task 1: Theme-aware profile banners

**Files:**
- Create: `assets/banner-dark.svg`
- Create: `assets/banner-light.svg`

**Interfaces:**
- Consumes: The approved name, subtitle, career-direction sentence, and black/violet visual direction.
- Produces: Two responsive SVG files with identical geometry and a `viewBox="0 0 1200 360"` interface for the README `<picture>` element.

- [ ] **Step 1: Create the dark banner**

Create a script-free SVG with a near-black gradient, restrained violet glows, circuit-inspired lines, and these exact visible strings:

```text
Vitória Ferreira
Computer Engineering · Cybersecurity · Python
Building toward a career in cybersecurity, application security and cloud security.
```

Use system font stacks only, a `1200 × 360` view box, rounded outer geometry, and text positions that keep the complete copy inside the view box.

- [ ] **Step 2: Create the light banner**

Mirror the dark banner's element positions, sizes, and strings. Replace the palette with a gray-lavender gradient, dark purple text, and restrained violet/lilac accents while retaining sufficient contrast.

- [ ] **Step 3: Parse and inspect both SVG files**

Run:

```bash
python - <<'PY'
from pathlib import Path
from xml.etree import ElementTree as ET

required = {
    "Vitória Ferreira",
    "Computer Engineering · Cybersecurity · Python",
    "Building toward a career in cybersecurity, application security and cloud security.",
}
for path in (Path("assets/banner-dark.svg"), Path("assets/banner-light.svg")):
    root = ET.parse(path).getroot()
    assert root.attrib["viewBox"] == "0 0 1200 360"
    text = " ".join("".join(node.itertext()) for node in root.iter())
    assert required <= {item.strip() for item in text.split("\n") if item.strip()}
    raw = path.read_text()
    assert "<script" not in raw.lower()
    assert "<foreignObject" not in raw
print("Banner SVG validation passed")
PY
```

Expected: `Banner SVG validation passed`.

- [ ] **Step 4: Commit the banners**

```bash
git add assets/banner-dark.svg assets/banner-light.svg
git commit -m "feat: add theme-aware profile banners"
```

### Task 2: Editorial profile README

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: `assets/banner-dark.svg`, `assets/banner-light.svg`, username `vivieches`, confirmed social URLs, and the service URLs in Global Constraints.
- Produces: The complete visitor-facing profile document and references to the two future Bomberman files on the `output` branch.

- [ ] **Step 1: Replace the existing README composition**

Build the document in this exact order:

```text
theme-aware banner
Hi, I'm Vitória
professional direction and four social links
Currently playing
My Tech Journey
  Learning now
  Next on my roadmap
  Long-term focus
My contribution graph
profile views
```

Use the approved short introduction and these exact journey lists:

```text
Learning now: Java, Python, SQL, Linux, Git
Next on my roadmap: Spring Boot, PowerShell, Docker, Azure, AWS, Go
Long-term focus: C#/.NET, C, Rust, Kubernetes, Terraform, Application Security, DevSecOps, Cloud Security, Identity and Access Management
```

Use theme-aware Skill Icons rows with these supported IDs:

```text
java,py,mysql,linux,git
spring,powershell,docker,azure,aws,go
cs,dotnet,c,rust,kubernetes,terraform
```

Keep conceptual security areas as plain text. Add an English comment immediately before the Spotify card:

```html
<!-- Replace SPOTIFY_UID after connecting the account through spotify-github-profile -->
```

The Spotify URL must contain:

```text
https://spotify-github-profile.kittinanx.com/api/view?uid=SPOTIFY_UID&cover_image=true&theme=compact&background_color=0d0d0f&bar_color=8b5cf6&bar_color_cover=false&border_radius=12&show_offline=true
```

The Spotify link target is `https://open.spotify.com/`. Use the four preserved social URLs and a restrained `flat-square` badge style. End with:

```text
https://komarev.com/ghpvc/?username=vivieches&label=PROFILE+VIEWS&color=7c3aed&style=flat-square&abbreviated=true
```

- [ ] **Step 2: Validate structure, content, usernames, and URLs**

Run:

```bash
python - <<'PY'
from pathlib import Path

text = Path("README.md").read_text()
required = [
    "Vitória Ferreira", "Computer Engineering student", "### 🎧 Currently playing",
    "### My Tech Journey", "#### Learning now", "#### Next on my roadmap",
    "#### Long-term focus", "### 💣 My contribution graph", "SPOTIFY_UID",
    "vivieches/vivieches/output/bomberman-contribution-graph.svg",
    "vivieches/vivieches/output/bomberman-contribution-graph-dark.svg",
    "https://linkedin.com/in/vitória-ferreira-162643281",
    "https://instagram.com/viviexec.es", "https://tiktok.com/@viviexec.es",
    "https://www.youtube.com/@viviwsd",
]
for value in required:
    assert value in text, value
for forbidden in ["Sobre mí", "Stack Tecnológico", "Trofeos", "Proyectos Destacados", "Actualmente Construyendo", "Vitoria Ferreira", "USERNAME", "YOUR_UID"]:
    assert forbidden not in text, forbidden
assert text.count("SPOTIFY_UID") == 2
print("README validation passed")
PY
```

Expected: `README validation passed`.

- [ ] **Step 3: Commit the README**

```bash
git add README.md
git commit -m "feat: rebuild GitHub profile README"
```

### Task 3: Bomberman contribution automation

**Files:**
- Create: `.github/workflows/bomberman.yml`
- Delete: `.github/workflows/snake.yml`

**Interfaces:**
- Consumes: GitHub's `${{ github.repository_owner }}`, `${{ secrets.GITHUB_TOKEN }}`, and the `main` and `output` branches.
- Produces: `dist/bomberman-contribution-graph.svg` and `dist/bomberman-contribution-graph-dark.svg`, published at the raw URLs already consumed by `README.md`.

- [ ] **Step 1: Replace the Snake workflow with Bomberman**

Create a workflow named `Generate Bomberman contribution graph` with daily cron `0 0 * * *`, `workflow_dispatch`, and a `push` trigger limited to `main` changes to `README.md`, `assets/**`, and `.github/workflows/bomberman.yml`. Set top-level `permissions: contents: write`, `runs-on: ubuntu-latest`, and `timeout-minutes: 20`.

Use exactly:

```yaml
- name: Generate Bomberman contribution graphs
  uses: abozanona/pacman-contribution-graph@v5.0.0
  with:
    github_user_name: ${{ github.repository_owner }}
    games: "bomberman"
    hide_month_labels: "false"

- name: Publish generated SVG files
  uses: crazy-max/ghaction-github-pages@v5
  with:
    target_branch: output
    build_dir: dist
    keep_history: true
    allow_empty_commit: false
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Delete `.github/workflows/snake.yml` so no other contribution game runs.

- [ ] **Step 2: Parse and assert the workflow contract**

Run with a YAML parser that preserves the `on` key as text:

```bash
python - <<'PY'
from pathlib import Path
import yaml

class Loader(yaml.SafeLoader):
    pass
Loader.yaml_implicit_resolvers = {
    key: [(tag, regex) for tag, regex in value if tag != "tag:yaml.org,2002:bool"]
    for key, value in Loader.yaml_implicit_resolvers.items()
}

path = Path(".github/workflows/bomberman.yml")
data = yaml.load(path.read_text(), Loader=Loader)
assert data["name"] == "Generate Bomberman contribution graph"
assert data["on"]["schedule"][0]["cron"] == "0 0 * * *"
assert "workflow_dispatch" in data["on"]
assert data["permissions"] == {"contents": "write"}
job = data["jobs"]["generate"]
assert job["timeout-minutes"] == 20
generate, publish = job["steps"]
assert generate["uses"] == "abozanona/pacman-contribution-graph@v5.0.0"
assert generate["with"]["games"] == "bomberman"
assert publish["uses"] == "crazy-max/ghaction-github-pages@v5"
assert publish["with"]["target_branch"] == "output"
assert publish["with"]["build_dir"] == "dist"
assert publish["with"]["keep_history"] is True
assert publish["with"]["allow_empty_commit"] is False
assert not Path(".github/workflows/snake.yml").exists()
print("Bomberman workflow validation passed")
PY
```

Expected: `Bomberman workflow validation passed`.

- [ ] **Step 3: Commit the workflow replacement**

```bash
git add .github/workflows/bomberman.yml .github/workflows/snake.yml
git commit -m "ci: generate Bomberman contribution graph"
```

### Task 4: Final repository verification

**Files:**
- Verify: `README.md`
- Verify: `assets/banner-dark.svg`
- Verify: `assets/banner-light.svg`
- Verify: `.github/workflows/bomberman.yml`

**Interfaces:**
- Consumes: All deliverables from Tasks 1–3.
- Produces: Evidence that the profile is complete, internally consistent, and free of unrelated changes.

- [ ] **Step 1: Scan the complete diff**

Run:

```bash
git status --short
git diff origin/main...HEAD -- README.md assets .github/workflows docs/superpowers
```

Expected: only the design, plan, README, two banners, Bomberman workflow, and Snake workflow removal appear.

- [ ] **Step 2: Check required files and forbidden secrets**

Run:

```bash
test -f README.md
test -f assets/banner-dark.svg
test -f assets/banner-light.svg
test -f .github/workflows/bomberman.yml
test ! -f .github/workflows/snake.yml
! rg -n -i 'client[_ -]?secret|access[_ -]?token|refresh[_ -]?token|spotify.{0,20}secret' README.md assets .github/workflows
```

Expected: all commands exit successfully and the secret scan prints nothing.

- [ ] **Step 3: Confirm the branch is ready without publishing**

Run:

```bash
git status --short --branch
git log --oneline --decorate origin/main..HEAD
```

Expected: a clean `main` branch ahead of `origin/main` with the design, plan, banner, README, and workflow commits. Do not push unless explicitly requested.

