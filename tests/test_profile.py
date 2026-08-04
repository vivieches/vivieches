from pathlib import Path
from html import unescape
import unittest
from xml.etree import ElementTree as ET

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
    def test_dark_banner_is_the_only_safe_responsive_variant(self):
        expected_lines = {
            "Vitória Ferreira",
            "Computer Engineering · Cybersecurity · Python",
            "Building toward a career in cybersecurity, application security and cloud security.",
        }

        path = ROOT / "assets" / "banner-dark.svg"
        root = ET.parse(path).getroot()
        self.assertEqual(root.attrib.get("viewBox"), "0 0 1200 360")
        self.assertEqual(root.attrib.get("role"), "img")
        raw = path.read_text(encoding="utf-8")
        self.assertNotIn("<script", raw.lower())
        self.assertNotIn("<foreignObject", raw)
        visible_lines = {
            "".join(node.itertext()).strip()
            for node in root.iter()
            if node.tag.endswith("text")
        }
        self.assertTrue(expected_lines.issubset(visible_lines))
        self.assertFalse((ROOT / "assets" / "banner-light.svg").exists())


class ReadmeTests(unittest.TestCase):
    def setUp(self):
        self.readme = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_sections_follow_the_approved_editorial_order(self):
        anchors = [
            "./assets/banner-dark.svg",
            "## Hi, I'm Vitória 👋",
            "### 🎧 Currently playing",
            "### My Tech Journey",
            "#### Learning now",
            "#### Next on my roadmap",
            "#### Long-term focus",
            "### 💣 My contribution graph",
            "Profile views",
        ]
        positions = [self.readme.index(anchor) for anchor in anchors]
        self.assertEqual(positions, sorted(positions))

    def test_profile_uses_only_dark_visual_variants(self):
        self.assertNotIn("banner-light.svg", self.readme)
        self.assertNotIn("bomberman-contribution-graph.svg", self.readme)
        self.assertIn("bomberman-contribution-graph-dark.svg", self.readme)

    def test_standalone_images_use_complete_single_line_html_tags(self):
        banner = (
            '<img src="./assets/banner-dark.svg" '
            'alt="Vitória Ferreira — Computer Engineering and Cybersecurity" '
            'width="100%">'
        )
        bomberman = (
            '<img src="https://raw.githubusercontent.com/vivieches/vivieches/'
            'output/bomberman-contribution-graph-dark.svg" '
            'alt="Bomberman animation playing across Vitória\'s GitHub contribution graph" '
            'width="100%">'
        )
        self.assertTrue(self.readme.startswith(banner))
        self.assertIn(bomberman, self.readme)

    def test_readme_uses_real_profile_links_and_connected_spotify_uid(self):
        required = {
            "https://linkedin.com/in/vitória-ferreira-162643281",
            "https://instagram.com/viviexec.es",
            "https://tiktok.com/@viviexec.es",
            "https://www.youtube.com/@viviwsd",
            "uid=31yudueg6i5khowcpdmfcs6pfmga",
            "theme=default",
            "show_offline=false",
            "bar_color=0ba800",
            "vivieches/vivieches/output/bomberman-contribution-graph-dark.svg",
            "username=vivieches",
        }
        for value in required:
            self.assertIn(value, self.readme)
        self.assertNotIn("SPOTIFY_UID", self.readme)
        self.assertNotRegex(self.readme, r"\b(?:USERNAME|YOUR_UID)\b")

    def test_readme_has_honest_journey_copy_and_no_old_professional_claims(self):
        required = {
            "Computer Engineering student",
            "Currently learning: Java, Python, SQL, Linux and cloud fundamentals.",
            "Building toward: Application Security, DevSecOps and Cloud Security.",
            "Application Security · DevSecOps · Cloud Security · Identity and Access Management",
        }
        for value in required:
            self.assertIn(value, self.readme)
        prohibited = (
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

    def test_skill_icon_groups_render_all_icons_in_dark_rows(self):
        decoded_readme = unescape(self.readme)
        groups = (
            "java,py,mysql,linux,git",
            "spring,powershell,docker,azure,aws,go",
            "cs,dotnet,c,rust,kubernetes,terraform",
        )
        for group in groups:
            self.assertIn(f"icons?i={group}&theme=dark", decoded_readme)
            self.assertNotIn(f"icons?i={group}&theme=light", decoded_readme)
        journey = self.readme.split("### My Tech Journey", 1)[1].split(
            "### 💣 My contribution graph", 1
        )[0]
        self.assertNotIn("<source", journey)


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
