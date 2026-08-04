# GitHub Profile Portfolio Redesign

## Goal

Turn Vitória Ferreira's GitHub profile into a concise English-language technical portfolio while preserving the illustrated black-and-purple banner and all four confirmed social links.

## Composition

The profile follows this order: illustrated banner, short introduction, contact links, compact Spotify badge, Tech Stack, Focus, Featured Projects, and the Bomberman contribution graph. Learning-roadmap language, profile views, large statistics, and unsupported professional claims are removed.

## Music

The preferred SpotiBadge service requires its own Spotify OAuth flow and generated `public_id`, which is not yet available. The immediate implementation therefore uses the explicitly allowed `spotify-github-profile` fallback with the connected Spotify UID and these compact settings: `cover_image=false`, `theme=compact`, `background_color=0d0d0f`, `bar_color=8b5cf6`, `bar_color_cover=false`, `border_radius=10`, and `show_offline=true`. The badge links to the service redirect endpoint, contains no iframe or autoplay, and stores no credentials.

## Technology Presentation

Supported technologies use official Skill Icons in theme-aware rows. Languages are Java, Python, Go, C#/.NET, SQL, PowerShell, Bash, C, and Rust. Systems and cloud technologies are Linux, Windows, Active Directory, Microsoft Entra ID, Azure, AWS, Docker, Kubernetes, and Terraform. Security focus areas remain text because they are concepts rather than official technology icons.

## Portfolio Projects

Only real public repositories are featured: Open Studio and OpenClaw AI Agents. Descriptions remain factual and link directly to their GitHub repositories.

## Compatibility

The README uses GitHub-compatible Markdown and HTML only. Skill Icon `srcset` commas are percent-encoded so GitHub does not truncate icon rows. The black illustrated banner is intentionally retained in both GitHub themes. The Bomberman graph remains theme-aware.

## Verification

Automated tests enforce order, English copy, compact Spotify parameters, complete icon groups, real project links, the absence of prohibited roadmap/statistics content, and the existing workflow contract. GitHub's Markdown rendering API is used to confirm that image tags and links render instead of appearing as escaped text.
