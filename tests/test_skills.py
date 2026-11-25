"""Every skill is a folder with a SKILL.md whose front matter every agent accepts."""
import pathlib, re, unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())


def front_matter(path):
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, f"{path}: no front matter"
    meta = {}
    for line in m.group(1).splitlines():
        if re.match(r"^[a-z_]+:", line):
            key, _, value = line.partition(":")
            meta[key] = value.strip()
    return meta, text[m.end():]


class Skills(unittest.TestCase):
    def test_each_folder_holds_one_skill_named_after_it(self):
        self.assertTrue(SKILLS)
        for folder in SKILLS:
            with self.subTest(folder.name):
                meta, _ = front_matter(folder / "SKILL.md")
                self.assertEqual(folder.name, meta.get("name"))
                self.assertRegex(folder.name, r"^[a-z0-9]+(-[a-z0-9]+)*$")

    def test_descriptions_say_when_and_fit_every_agent(self):
        # Vibe caps a description at 1,024 characters; Claude Code at 1,536.
        for folder in SKILLS:
            with self.subTest(folder.name):
                meta, _ = front_matter(folder / "SKILL.md")
                self.assertGreater(len(meta.get("description", "")), 40)
                self.assertLessEqual(len(meta["description"]), 1024)

    def test_bodies_stay_short(self):
        # A skill is a map, not a copy: it links the page that holds the rule.
        for folder in SKILLS:
            with self.subTest(folder.name):
                _, body = front_matter(folder / "SKILL.md")
                self.assertLessEqual(len(body.splitlines()), 90)

    def test_plugin_manifests_agree(self):
        import json
        claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual(claude, codex)
        self.assertEqual([claude["name"]], [p["name"] for p in market["plugins"]])


if __name__ == "__main__":
    unittest.main()
