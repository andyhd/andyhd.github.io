import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def initialized(pelican):
    from pelican.settings import DEFAULT_CONFIG

    DEFAULT_CONFIG.setdefault("COMMENTS_PATH", "comments")
    if pelican:
        pelican.settings.setdefault("COMMENTS_PATH", "comments")


def add_comments(generator, metadata):
    post_slug = metadata.get("slug")
    if post_slug:
        comments_dir = Path(generator.settings.get("COMMENTS_PATH", "comments")) / post_slug

        comments = {}
        metadata["comments"] = {}

        for comment_file in sorted(comments_dir.glob("*.json")):
            try:
                data = json.loads(comment_file.read_text())
                logger.info(f"Loaded comment {comment_file.stem} for post {post_slug}")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON from {comment_file}: {e}")
                continue

            timestamp, _, author_hash = comment_file.stem.partition("_")
            comment = {
                "id": comment_file.stem,
                "author": data["author"],
                "author_hash": author_hash,
                "text": data["text"],
                "datetime": datetime.strptime(timestamp, "%Y%m%d%H%M%S"),
                "in_reply_to": data.get("in_reply_to"),
            }
            comments[comment["id"]] = comment

            if comment["in_reply_to"]:
                comments[comment["in_reply_to"]].setdefault("replies", []).append(comment)
            else:
                metadata["comments"][comment["id"]] = comment

        metadata["num_comments"] = (
            len(metadata["comments"])
            + sum(len(c.get("replies", [])) for c in metadata["comments"].values())
        )


def register():
    from pelican import signals

    signals.initialized.connect(initialized)
    signals.article_generator_context.connect(add_comments)
