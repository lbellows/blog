import os
import shutil
import unittest
from pathlib import Path

import frontmatter

from scripts.generate_post_websearch import (
    FOUNDARY_MODELS_DEFAULT,
    ask_azure_foundry_with_web_search,
    write_post,
)


REQUIRED_ENV_VARS = ("FOUNDARY_API_KEY", "ENDPOINT_URL")


def _has_required_env() -> bool:
    return all(os.getenv(name) for name in REQUIRED_ENV_VARS)


@unittest.skipUnless(_has_required_env(), "FOUNDARY_API_KEY and ENDPOINT_URL must be configured for live model tests.")
class FoundryModelPostTests(unittest.TestCase):
    def setUp(self):
        self.tests_root = Path(__file__).resolve().parent
        self.posts_root = self.tests_root / "posts"
        self.posts_root.mkdir(parents=True, exist_ok=True)
        env_models = [m.strip() for m in os.getenv("FOUNDARY_MODELS", "").split(",") if m.strip()]
        models = env_models or FOUNDARY_MODELS_DEFAULT
        for model in models:
            target = self.posts_root / model
            if target.exists():
                shutil.rmtree(target)

    def test_each_model_generates_preview_post(self):
        env_models = [m.strip() for m in os.getenv("FOUNDARY_MODELS", "").split(",") if m.strip()]
        models = env_models or FOUNDARY_MODELS_DEFAULT

        for model in models:
            with self.subTest(model=model):
                try:
                    markdown_body = ask_azure_foundry_with_web_search(foundry_model=model)
                except RuntimeError as err:
                    msg = str(err)
                    if "DeploymentNotFound" in msg or "404" in msg:
                        self.skipTest(f"{model} deployment not found in Azure Foundry.")
                    raise

                output_dir = self.posts_root / model
                write_post(markdown_body, used_model=model, output_dir=output_dir)

                created = list(output_dir.glob("*.md"))
                self.assertTrue(created, f"Expected a post file for model {model}")

                post_path = max(created, key=lambda p: p.stat().st_mtime)
                post = frontmatter.load(post_path)

                self.assertEqual(post.get("llm_model"), model)
                self.assertIn(model, post.get("author", ""))

                lines = [line.strip() for line in post.content.splitlines() if line.strip()]
                self.assertTrue(lines, "Post content should not be empty")

                has_heading = any(
                    line.lstrip().startswith("#") or " # " in line or line.lower().startswith("h1:")
                    for line in lines
                )
                self.assertTrue(has_heading, "Post should include an H1 title at the top.")

                self.assertTrue(any("TL;DR" in line for line in lines), "Post should include a TL;DR section")
                self.assertTrue(
                    any("Further reading" in line for line in lines),
                    "Post should include a Further reading section",
                )


if __name__ == "__main__":
    unittest.main()
