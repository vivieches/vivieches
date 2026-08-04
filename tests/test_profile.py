from pathlib import Path
import struct
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


class StringSafeLoader(yaml.SafeLoader):
    """Load YAML 1.1 files without coercing the GitHub Actions `on` key."""


StringSafeLoader.yaml_implicit_resolvers = {
    key: [
        (tag, regex)
        for tag, regex in value
        if tag != "tag:yaml.org,2002:bool"
    ]
    for key, value in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


class BannerTests(unittest.TestCase):
    def test_requested_dark_png_is_the_only_profile_banner(self):
        path = ROOT / "assets" / "banner-dark.png"
        raw = path.read_bytes()
        self.assertEqual(raw[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II", raw[16:24]), (2172, 724))
        self.assertGreater(len(raw), 1_000_000)
        self.assertFalse((ROOT / "assets" / "banner-dark.svg").exists())
        self.assertFalse((ROOT / "assets" / "banner-light.svg").exists())


class ReadmeTests(unittest.TestCase):
    def setUp(self):
        self.readme = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_sections_follow_the_approved_editorial_order(self):
        anchors = [
            "./assets/banner-dark.png",
            "## ◆ About Me",
            "### Connect with me",
            "## ◆ Listening to",
            "## ◆ Tech Stack",
            "— Languages —",
            "— Systems & Cloud —",
            "— Security & Identity —",
            "## ◆ Focus",
            "## ◆ Featured Projects",
            "## ◆ Currently Building",
            "## ◆ Contribution Graph",
        ]
        positions = [self.readme.index(anchor) for anchor in anchors]
        self.assertEqual(positions, sorted(positions))

    def test_profile_keeps_the_requested_black_banner_and_theme_aware_graph(self):
        self.assertNotIn("banner-light.svg", self.readme)
        self.assertNotIn("banner-dark.svg", self.readme)
        self.assertIn("bomberman-contribution-graph.svg", self.readme)
        self.assertIn("bomberman-contribution-graph-dark.svg", self.readme)

    def test_banner_uses_a_complete_single_line_html_tag(self):
        banner = (
            '<img src="./assets/banner-dark.png" '
            'alt="Vitória Ferreira — Computer Engineering, Cybersecurity and Cloud" '
            'width="100%">'
        )
        self.assertTrue(self.readme.startswith(banner))

    def test_readme_preserves_all_confirmed_contact_links(self):
        required = {
            "https://linkedin.com/in/vitória-ferreira-162643281",
            "https://instagram.com/viviexec.es",
            "https://tiktok.com/@viviexec.es",
            "https://www.youtube.com/@viviwsd",
        }
        for value in required:
            self.assertIn(value, self.readme)

    def test_spotify_badge_is_connected_small_purple_and_clickable(self):
        required = {
            "uid=31yudueg6i5khowcpdmfcs6pfmga",
            "cover_image=false",
            "theme=natemoo-re",
            "background_color=0d0d0f",
            "bar_color=8b5cf6",
            "bar_color_cover=false",
            "border_radius=10",
            "show_offline=true",
            "redirect=true",
            'width="320"',
        }
        for value in required:
            self.assertIn(value, self.readme)
        self.assertNotIn("cover_image=true", self.readme)
        self.assertNotIn("theme=compact", self.readme)
        self.assertNotIn("theme=default", self.readme)
        self.assertNotIn("SPOTIFY_UID", self.readme)
        self.assertNotIn("<iframe", self.readme.lower())
        self.assertNotIn("autoplay", self.readme.lower())
        self.assertNotRegex(
            self.readme.lower(),
            r"(?:client_secret|access_token|refresh_token)",
        )
        music = self.readme.split("## ◆ Listening to", 1)[1].split(
            "## ◆ Tech Stack", 1
        )[0]
        self.assertIn('<p align="center">', music)
        self.assertIn("currently playing or recently played Spotify track", music)

    def test_readme_has_visual_technology_groups_without_levels(self):
        required = {
            "— Languages —",
            "— Systems & Cloud —",
            "— Security & Identity —",
        }
        for value in required:
            self.assertIn(value, self.readme)

    def test_security_and_identity_are_compact_purple_badges(self):
        labels = (
            "Application%20Security",
            "DevSecOps",
            "Cloud%20Security",
            "Active%20Directory",
            "Microsoft%20Entra%20ID",
            "Identity%20%26%20Access%20Management",
        )
        for label in labels:
            self.assertRegex(
                self.readme,
                rf"img\.shields\.io/badge/{label}-(?:6d28d9|7c3aed|8b5cf6|a78bfa)",
            )

    def test_skill_icons_show_every_supported_technology_in_two_themes(self):
        icon_groups = (
            "java,py,go,cs,dotnet,postgres,powershell,bash,c,rust",
            "linux,windows,azure,aws,docker,kubernetes,terraform",
        )
        for group in icon_groups:
            encoded_group = group.replace(",", "%2C")
            self.assertIn(f"icons?i={encoded_group}&amp;theme=dark", self.readme)
            self.assertIn(f"icons?i={encoded_group}&amp;theme=light", self.readme)
            self.assertIn(f"icons?i={group}&amp;theme=dark", self.readme)

    def test_focus_copy_is_neutral_and_approved(self):
        required = {
            "Focused on Application Security, DevSecOps, Cloud Security and Identity & Access Management.",
            "Exploring the intersection between software engineering, cloud infrastructure and cybersecurity.",
        }
        for value in required:
            self.assertIn(value, self.readme)

    def test_featured_projects_are_real_public_repositories(self):
        required = {
            "🎬 Open Studio",
            "https://github.com/vivieches/open-studio",
            "🤖 OpenClaw AI Agents",
            "https://github.com/vivieches/openclaw-ai-agents",
            "Open-source creator workspace",
            "role-based multi-agent framework",
        }
        for value in required:
            self.assertIn(value, self.readme)
        projects = self.readme.split("## ◆ Featured Projects", 1)[1].split(
            "## ◆ Currently Building", 1
        )[0]
        self.assertIn("<table>", projects)
        self.assertEqual(projects.count('<td width="50%" valign="top">'), 2)
        self.assertIn("View%20repository", projects)

    def test_currently_building_is_visual_and_has_no_invented_percentages(self):
        current = self.readme.split("## ◆ Currently Building", 1)[1].split(
            "## ◆ Contribution Graph", 1
        )[0]
        self.assertIn("<table>", current)
        self.assertIn("Open Studio", current)
        self.assertIn("OpenClaw AI Agents", current)
        self.assertIn("Active%20development", current)
        self.assertIn("Maintained", current)
        self.assertNotRegex(current, r"\b\d{1,3}%")

    def test_readme_removes_roadmap_statistics_and_old_claims(self):
        prohibited = (
            "Currently learning",
            "Learning now",
            "Next on my roadmap",
            "Long-term focus",
            "My Tech Journey",
            "Profile views",
            "PROFILE VIEWS",
            "ghpvc",
            "github-profile-trophy",
            "github-readme-stats",
            "AI Content Engineer",
            "Full Stack Developer",
            "AI Engineer",
            "Expert in",
            "Specialist in",
            "Sobre mí",
            "Stack Tecnológico",
            "Trofeos",
            "Proyectos Destacados",
            "Actualmente Construyendo",
            "VISITAS AL PERFIL",
        )
        for value in prohibited:
            self.assertNotIn(value, self.readme)

    def test_bomberman_graph_has_light_and_dark_sources(self):
        required = (
            "vivieches/vivieches/output/bomberman-contribution-graph.svg",
            "vivieches/vivieches/output/bomberman-contribution-graph-dark.svg",
            "Bomberman animation across Vitória's GitHub contribution graph",
        )
        for value in required:
            self.assertIn(value, self.readme)


class WorkflowTests(unittest.TestCase):
    def test_workflow_generates_only_bomberman_and_publishes_without_empty_commits(self):
        workflow_path = ROOT / ".github" / "workflows" / "bomberman.yml"
        data = yaml.load(workflow_path.read_text(encoding="utf-8"), Loader=StringSafeLoader)
        self.assertEqual(data["name"], "Generate Bomberman contribution graph")
        self.assertEqual(data["on"]["schedule"], [{"cron": "0 0 * * *"}])
        self.assertIn("workflow_dispatch", data["on"])
        self.assertEqual(data["permissions"], {"contents": "write"})
        job = data["jobs"]["generate"]
        self.assertEqual(job["runs-on"], "ubuntu-latest")
        self.assertEqual(job["timeout-minutes"], 20)
        generate, publish = job["steps"]
        self.assertEqual(generate["uses"], "abozanona/pacman-contribution-graph@v5.0.0")
        self.assertEqual(generate["with"]["github_user_name"], "${{ github.repository_owner }}")
        self.assertEqual(generate["with"]["games"], "bomberman")
        self.assertEqual(publish["uses"], "crazy-max/ghaction-github-pages@v5")
        self.assertEqual(
            publish["with"],
            {
                "target_branch": "output",
                "build_dir": "dist",
                "keep_history": "true",
                "allow_empty_commit": "false",
            },
        )
        self.assertFalse((ROOT / ".github" / "workflows" / "snake.yml").exists())


if __name__ == "__main__":
    unittest.main()
