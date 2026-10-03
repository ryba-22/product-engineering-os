from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PMAAdapterTest(unittest.TestCase):
    def test_pma_source_config_is_public_only(self):
        cfg = json.loads((ROOT / "machine/pma-knowledge-source.json").read_text())
        self.assertEqual(cfg["publication_boundary"], "public-only")
        self.assertTrue(cfg["repository"].startswith("https://github.com/"))

    def test_importer_rejects_private_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            registry = {
                "publication_boundary": "public-only",
                "entries": [{"id": "X", "path": "private/source.md"}],
            }
            src = tmp_path / "registry.json"
            out = tmp_path / "out.json"
            src.write_text(json.dumps(registry))
            p = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/import_pma_registry.py"),
                    "--source",
                    str(src),
                    "--output",
                    str(out),
                ],
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(p.returncode, 0)
            self.assertFalse(out.exists())

    def test_importer_accepts_public_registry(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            registry = {
                "publication_boundary": "public-only",
                "entries": [
                    {
                        "id": "PMA-H-1",
                        "path": "content/02-Heuristics/X.md",
                        "type": "heuristic",
                    }
                ],
            }
            src = tmp_path / "registry.json"
            out = tmp_path / "out.json"
            src.write_text(json.dumps(registry))
            p = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/import_pma_registry.py"),
                    "--source",
                    str(src),
                    "--output",
                    str(out),
                ],
                text=True,
                capture_output=True,
            )
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            data = json.loads(out.read_text())
            self.assertEqual(data["entry_count"], 1)
            self.assertEqual(data["entries"][0]["id"], "PMA-H-1")


if __name__ == "__main__":
    unittest.main()
