# GitHub Profile README Design

## Goal

Replace the current profile with an honest, premium, black-and-purple presentation of Vitória Ferreira as a Computer Engineering student building toward cybersecurity, application security, DevSecOps, and cloud security. All visitor-facing content must be in English and work in GitHub light and dark modes on desktop and mobile.

## Repository Scope

The only target is the public special profile repository `vivieches/vivieches`. Its root `README.md` will remain the profile entry point. Existing LinkedIn, Instagram, TikTok, and YouTube links will be preserved. Unverified claims about professional roles, expertise, projects, progress percentages, and technologies will be removed. The existing Snake workflow will be replaced by the requested Bomberman workflow; no unrelated repository will be changed.

## Visual Direction

Use a restrained editorial composition with generous spacing and a black, deep-violet, and lilac palette. Two lightweight, script-free SVG banners will share one geometric composition:

- `assets/banner-dark.svg`: near-black gradient, deep violet accents, and subtle lilac circuit-inspired geometry.
- `assets/banner-light.svg`: pale gray-lavender background, dark purple text, and matching violet geometry.

Both banners display `Vitória Ferreira`, `Computer Engineering · Cybersecurity · Python`, and the approved career-direction sentence. A README `<picture>` element chooses the appropriate banner automatically.

## README Structure

The README follows this order:

1. Theme-aware banner.
2. Short introduction identifying Vitória as a Computer Engineering student.
3. Professional direction and current learning statements.
4. Compact Spotify card using the documented `spotify-github-profile.kittinanx.com/api/view` endpoint.
5. `My Tech Journey`, split into `Learning now`, `Next on my roadmap`, and `Long-term focus`.
6. Theme-aware Skill Icons rows for supported technologies; conceptual security areas remain text-only.
7. Theme-aware Bomberman contribution graph loaded from the `output` branch.
8. Discreet purple profile-view counter and confirmed social links.

The Spotify integration intentionally retains only `SPOTIFY_UID`, accompanied by an English technical comment explaining that it must be replaced after account connection. No credential, token, or invented UID is stored.

## Automation

Create `.github/workflows/bomberman.yml` and remove the obsolete `.github/workflows/snake.yml`. The workflow will:

- run daily at midnight UTC, manually, and when relevant profile files change on `main`;
- use `github.repository_owner` and the default `GITHUB_TOKEN`;
- grant only `contents: write`;
- enforce a 20-minute timeout;
- generate only Bomberman with `games: "bomberman"`;
- use stable `abozanona/pacman-contribution-graph@v5.0.0`;
- publish `dist` to `output` with `crazy-max/ghaction-github-pages@v5`;
- preserve output history and disallow empty deployment commits.

The README references `bomberman-contribution-graph.svg` and `bomberman-contribution-graph-dark.svg` under `vivieches/vivieches/output`.

## Compatibility and Failure Behavior

Local SVGs contain no JavaScript, external scripts, embedded HTML, or remote fonts. README images include English alternative text and safe fallback sources. Before Spotify is connected, its remote card may not render because the required UID is deliberately unknown; the nearby comment and handoff instructions make this explicit. Before the first successful Bomberman workflow run, the graph URLs may return no image; a manual first run from GitHub Actions will initialize the files.

## Verification

Verify the final repository by:

- parsing both SVGs as XML and checking their view boxes and visible English text;
- parsing the workflow as YAML and asserting its triggers, permissions, pinned actions, inputs, output settings, and timeout;
- scanning visitor-facing README content for Portuguese or Spanish and for prohibited professional claims;
- checking that every username occurrence is `vivieches` and the only permitted placeholder is `SPOTIFY_UID`;
- checking all required files and important social URLs;
- validating referenced Skill Icons IDs against the official project list;
- reviewing Git diffs to ensure no unrelated content changed.

