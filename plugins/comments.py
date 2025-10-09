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
    if post_slug := metadata.get("slug"):
        comments_dir = Path(generator.settings.get("COMMENTS_PATH", "comments")) / post_slug

        comments = []

        for i, comment_file in enumerate(sorted(comments_dir.glob("*.json"))):
            try:
                comment = json.loads(comment_file.read_text())
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON from {comment_file}: {e}")
                continue

            if not comment:
                continue

            comment["timestamp"] = datetime.strptime(comment["timestamp"], "%Y%m%d%H%M%S")

            comment["replies"] = []

            if in_reply_to := comment.get("in_reply_to"):
                comments[in_reply_to - 1]["replies"].append(comment)
            else:
                comments.append(comment)

        metadata["comments"] = comments
        metadata["num_comments"] = i + 1 if comments else 0


def register():
    from pelican import signals

    signals.initialized.connect(initialized)
    signals.article_generator_context.connect(add_comments)
