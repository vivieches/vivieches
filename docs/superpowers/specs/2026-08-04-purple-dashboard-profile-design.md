# Purple Dashboard GitHub Profile Design

## Goal

Transform Vitória Ferreira's GitHub profile from a text-heavy document into a structured black-and-purple dashboard inspired by the supplied references. Preserve the illustrated banner, confirmed contact links, honest technical positioning, real public projects, and Bomberman contribution graph.

## Visual System

Use GitHub-native Markdown and supported HTML so the profile remains reliable. Section titles use a small diamond marker and horizontal rules. The palette is near-black, graphite, violet, purple, and lilac. Content remains in English. Layouts must remain readable in GitHub light and dark modes and on mobile.

## Structure

The README follows this order:

1. Existing illustrated banner.
2. Short introduction and contact badges.
3. Compact music badge.
4. Visual Tech Stack dashboard.
5. Focus summary.
6. Featured Projects grid.
7. Currently Building status panel.
8. Bomberman contribution graph.

## Music Badge

Replace the sparse `compact` Spotify theme with the documented `natemoo-re` theme. Keep the connected Spotify UID, `cover_image=false`, `background_color=0d0d0f`, `bar_color=8b5cf6`, `bar_color_cover=false`, `border_radius=10`, and `show_offline=true`. The result is a centered 320 × 84 pixel black-and-purple badge with artist, track, and animated purple equalizer. It remains clickable and contains no iframe, autoplay, credentials, tokens, or album artwork.

SpotiBadge is not used because its current self-service mode places encrypted Spotify application credentials in the generated widget URL, conflicting with the requirement that credentials never appear in the README.

## Tech Stack Dashboard

Replace long technology paragraphs with centered visual groups:

- `Languages`: Java, Python, Go, C#/.NET, SQL, PowerShell, Bash, C, and Rust through official Skill Icons.
- `Systems & Cloud`: Linux, Windows, Azure, AWS, Docker, Kubernetes, and Terraform through official Skill Icons.
- `Security & Identity`: Application Security, DevSecOps, Cloud Security, Active Directory, Microsoft Entra ID, and Identity & Access Management through compact purple badges.

The icons remain grouped under their category names. Supported icons use theme-aware Skill Icons sources with encoded `srcset` commas to avoid the earlier GitHub rendering bug.

## Featured Projects

Use a native two-column Markdown table styled by GitHub instead of unreliable external project-card services. The cards feature only real public repositories:

- Open Studio: repository description, TypeScript/Next.js/React tags, dynamic repository link, and active status.
- OpenClaw AI Agents: factual role-based automation description, Python/Shell/TypeScript tags, dynamic repository link, and maintained status.

The grid uses emojis, purple shields, concise copy, and clickable repository links. It avoids unsupported professional claims.

## Currently Building

Show Open Studio and OpenClaw AI Agents as active work using compact status badges and concise descriptions. Do not display invented completion percentages. The panel is visual but remains factual and easy to update.

## Reliability Decisions

Do not add GitHub Profile Trophy or GitHub Readme Stats widgets. Their public endpoints returned HTTP 402 and 503 during validation, and the trophy in the supplied reference was visibly broken. Native tables, Skill Icons, Shields.io, the connected Spotify service, and the existing Bomberman workflow provide a more reliable result.

## Verification

Automated tests enforce section order, music size and parameters, complete icon groups, purple security badges, real project links, factual status content, no credentials, and no broken external trophy/stat widgets. GitHub's Markdown API validates that the final HTML is not escaped. Every external image endpoint must return HTTP 200 before publication.
