from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "refresh_strict_original_memory.py"


def load_module():
    spec = importlib.util.spec_from_file_location("refresh_strict_original_memory", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n"
    path.write_text(payload, encoding="utf-8")


class StrictOriginalMemoryTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.tempdir = tempfile.TemporaryDirectory()
        self.base = Path(self.tempdir.name)
        self.workspace = self.base / "workspace"
        self.workspace.mkdir()
        self.codex_home = self.base / ".codex"
        self.memory_home = self.base / "global-memory"
        self.workspace_memory_home = self.module.workspace_memory_home(self.memory_home, self.workspace)
        (self.codex_home / "sessions" / "2026" / "04" / "02").mkdir(parents=True)

    def tearDown(self):
        self.tempdir.cleanup()

    def run_script(self, *extra_args):
        return self.run_script_for_workspace(self.workspace, *extra_args)

    def run_script_for_workspace(self, workspace: Path, *extra_args):
        old_argv = sys.argv
        try:
            sys.argv = [
                str(SCRIPT_PATH),
                "--workspace-root",
                str(workspace),
                "--codex-home",
                str(self.codex_home),
                "--memory-home",
                str(self.memory_home),
                *extra_args,
            ]
            return self.module.main()
        finally:
            sys.argv = old_argv

    def write_default_config(self):
        payload = {
            "version": 1,
            "context_window_tokens": 80,
            "reserve_tokens": 10,
            "index_max_lines": 50,
            "index_max_chars_per_entry": 100,
            "dream": {"min_hours_since_last": 24, "min_sessions_since_last": 1},
            "global_dream": {"min_hours_since_last": 72, "min_workspace_updates_since_last": 1},
            "candidate_governance": {"global": {"max_per_type": 2, "archive_after_days": 1, "keep_per_key": 1}},
            "compression": {"quote_limit": 2, "recent_session_limit": 4},
            "promotion": {
                "feedback_min_confidence": 0.85,
                "project_min_confidence": 0.8,
                "reference_min_confidence": 0.8,
                "user_min_confidence": 0.85,
                "reference_max_promoted_per_source": 3,
            },
            "memory_types": {
                "user": True,
                "feedback": True,
                "project": True,
                "reference": True,
                "open_loop": True,
            },
            "runtime": {"focus_session_limit": 2},
        }
        for config_path in (
            self.workspace_memory_home / "config.json",
            self.memory_home / "global" / "config.json",
        ):
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(
                json.dumps(
                    payload,
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

    def test_parse_memory_file_supports_yaml_list_metadata(self):
        target = self.base / "candidate.md"
        target.write_text(
            "\n".join(
                [
                    "---",
                    "id: reference-2026-04-10-abc123",
                    "scope: workspace",
                    "type: reference",
                    "source_runs:",
                    "  - run-1",
                    "  - run-2",
                    "source_workspaces:",
                    "  - workspace-a",
                    "  - workspace-b",
                    "---",
                    "# Title",
                    "",
                    "## Reference takeaway",
                    "Fact",
                    "",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        parsed = self.module.parse_memory_file(target)

        self.assertEqual(self.module.parse_metadata_list(parsed.metadata["source_runs"]), ["run-1", "run-2"])
        self.assertEqual(
            self.module.parse_metadata_list(parsed.metadata["source_workspaces"]),
            ["workspace-a", "workspace-b"],
        )

    def test_stages_candidates_and_promotes_only_durable_items(self):
        rows = [
            {
                "type": "session_meta",
                "timestamp": "2026-04-02T10:00:00+00:00",
                "payload": {
                    "id": "session-1",
                    "cwd": str(self.workspace),
                    "timestamp": "2026-04-02T10:00:00+00:00",
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"text": "原文真正值得仿造的是把记忆做成分层、可审查、会压缩、能纠偏的系统。"}],
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "user",
                    "content": [
                        {
                            "text": "我现在常用 Codex App。以后都不要 install.sh，写到 README.md 里。"
                            " 这个仓库默认按单 worker 运行。参考 https://example.com/memory 文章。"
                            " 我要睡觉了，你继续做，不要停，直到这轮全部完成。"
                        }
                    ],
                },
            },
        ]
        session_path = self.codex_home / "sessions" / "2026" / "04" / "02" / "session-1.jsonl"
        write_jsonl(session_path, rows)
        self.write_default_config()
        exit_code = self.run_script("--force-dream")

        self.assertEqual(exit_code, 0)

        root = self.workspace_memory_home
        self.assertTrue((self.memory_home / "instructions" / "company" / "GUIDE.md").exists())
        self.assertTrue((self.memory_home / "instructions" / "user" / "GUIDE.md").exists())
        self.assertTrue((self.memory_home / "instructions" / "local" / "GUIDE.md").exists())
        self.assertTrue((root / "instructions" / "repo" / "GUIDE.md").exists())
        self.assertTrue((root / "candidates" / "feedback").exists())
        self.assertTrue((root / "memories" / "user").exists())
        self.assertTrue((root / "memories" / "feedback").exists())
        self.assertTrue((root / "memories" / "project").exists())
        self.assertTrue((root / "memories" / "reference").exists())
        self.assertTrue((root / "memories" / "MEMORY.md").exists())
        self.assertTrue((root / "runtime" / "active_context.md").exists())
        self.assertTrue((root / "runtime" / "compression" / "latest.md").exists())
        self.assertTrue((root / "dream" / "state.json").exists())

        global_root = self.memory_home / "global"
        user_files = list((global_root / "memories" / "user").glob("*.md"))
        feedback_files = list((root / "memories" / "feedback").glob("*.md"))
        feedback_candidates = list((root / "candidates" / "feedback").glob("*.md"))
        user_candidates = list((root / "candidates" / "user").glob("*.md"))
        project_files = list((root / "memories" / "project").glob("*.md"))
        reference_files = list((root / "memories" / "reference").glob("*.md"))

        self.assertGreaterEqual(len(user_files), 1)
        self.assertGreaterEqual(len(user_candidates), 1)
        self.assertGreaterEqual(len(feedback_files), 1)
        self.assertGreaterEqual(len(feedback_candidates), 1)
        self.assertGreaterEqual(len(project_files), 1)
        self.assertGreaterEqual(len(reference_files), 1)

        active_feedback_text = "\n".join(path.read_text(encoding="utf-8") for path in feedback_files)
        candidate_feedback_text = "\n".join(path.read_text(encoding="utf-8") for path in feedback_candidates)
        self.assertIn("以后都不要 install.sh", active_feedback_text)
        self.assertNotIn("我要睡觉了，你继续做，不要停", active_feedback_text)
        self.assertIn("我要睡觉了，你继续做，不要停", candidate_feedback_text)

        reference_text = "\n".join(path.read_text(encoding="utf-8") for path in reference_files)
        self.assertIn("原文真正值得仿造的是把记忆做成分层、可审查、会压缩、能纠偏的系统", reference_text)
        self.assertNotIn("学习下这篇文章", reference_text)

        memory_index = (root / "memories" / "MEMORY.md").read_text(encoding="utf-8")
        self.assertIn("# MEMORY", memory_index)
        self.assertIn("[feedback]", memory_index)
        global_memory_index = (global_root / "memories" / "MEMORY.md").read_text(encoding="utf-8")
        self.assertIn("[user]", global_memory_index)
        global_context = (global_root / "runtime" / "global_context.md").read_text(encoding="utf-8")
        self.assertIn("## User Defaults", global_context)

        active_context = (root / "runtime" / "active_context.md").read_text(encoding="utf-8")
        self.assertIn("## Current Goal", active_context)
        self.assertIn("## Confirmed Feedback", active_context)

        run_root = self.memory_home / "runs" / self.module.workspace_key(self.workspace) / "session-1"
        self.assertTrue((run_root / "status.json").exists())
        self.assertTrue((run_root / "summary.md").exists())
        self.assertTrue((run_root / "handoff.md").exists())
        self.assertTrue((run_root / "extracted.json").exists())

        dream_state = json.loads((root / "dream" / "state.json").read_text(encoding="utf-8"))
        self.assertIsNotNone(dream_state["last_dream_at"])
        report_path = Path(dream_state["last_report"])
        self.assertTrue(report_path.exists())
        global_dream_state = json.loads((global_root / "dream" / "state.json").read_text(encoding="utf-8"))
        self.assertIsNotNone(global_dream_state["last_dream_at"])

    def test_question_like_project_memory_is_rejected(self):
        rows = [
            {
                "type": "session_meta",
                "timestamp": "2026-04-02T10:00:00+00:00",
                "payload": {
                    "id": "session-question",
                    "cwd": str(self.workspace),
                    "timestamp": "2026-04-02T10:00:00+00:00",
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "user",
                    "content": [{"text": "你建议单worker还是多worker共享记忆"}],
                },
            },
        ]
        write_jsonl(self.codex_home / "sessions" / "2026" / "04" / "02" / "session-question.jsonl", rows)
        self.write_default_config()
        self.assertEqual(self.run_script("--force"), 0)

        root = self.workspace_memory_home
        self.assertEqual(list((root / "memories" / "project").glob("*.md")), [])
        self.assertEqual(list((root / "candidates" / "project").glob("*.md")), [])

    def test_disabled_user_and_feedback_archive_legacy_recall_and_keep_context_clear(self):
        self.write_default_config()

        for config_path in (
            self.workspace_memory_home / "config.json",
            self.memory_home / "global" / "config.json",
        ):
            payload = json.loads(config_path.read_text(encoding="utf-8"))
            payload["memory_types"]["user"] = False
            payload["memory_types"]["feedback"] = False
            config_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        workspace_feedback = self.workspace_memory_home / "memories" / "feedback" / "rule.md"
        workspace_feedback.parent.mkdir(parents=True, exist_ok=True)
        workspace_feedback.write_text(
            "\n".join(
                [
                    "---",
                    "id: feedback-2026-04-21-rule",
                    "key: feedback-rule",
                    "scope: workspace",
                    "type: feedback",
                    "created_at: 2026-04-21T00:00:00+00:00",
                    "last_confirmed_at: 2026-04-21T00:00:00+00:00",
                    "status: active",
                    "---",
                    "# Rule",
                    "",
                    "## Rule",
                    "以后默认只给文件名和链接。",
                    "",
                    "## Why",
                    "Legacy feedback memory.",
                    "",
                    "## How to apply",
                    "Apply by default.",
                    "",
                    "## Evidence",
                    "Workspace test fixture.",
                    "",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        workspace_user_candidate = self.workspace_memory_home / "candidates" / "user" / "pref.md"
        workspace_user_candidate.parent.mkdir(parents=True, exist_ok=True)
        workspace_user_candidate.write_text(
            "\n".join(
                [
                    "---",
                    "id: user-2026-04-21-pref",
                    "key: user-pref",
                    "scope: workspace",
                    "type: user",
                    "created_at: 2026-04-21T00:00:00+00:00",
                    "last_confirmed_at: 2026-04-21T00:00:00+00:00",
                    "status: candidate",
                    "---",
                    "# Preference",
                    "",
                    "## Fact",
                    "新文档默认中英文双语。",
                    "",
                    "## Why it matters",
                    "Legacy user preference.",
                    "",
                    "## How to use",
                    "Use by default.",
                    "",
                    "## Evidence",
                    "Workspace test fixture.",
                    "",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        global_user = self.memory_home / "global" / "memories" / "user" / "pref.md"
        global_user.parent.mkdir(parents=True, exist_ok=True)
        global_user.write_text(
            "\n".join(
                [
                    "---",
                    "id: user-2026-04-21-global-pref",
                    "key: global-user-pref",
                    "scope: global",
                    "type: user",
                    "created_at: 2026-04-21T00:00:00+00:00",
                    "last_confirmed_at: 2026-04-21T00:00:00+00:00",
                    "status: active",
                    "---",
                    "# Global Preference",
                    "",
                    "## Fact",
                    "默认使用 README 驱动安装说明。",
                    "",
                    "## Why it matters",
                    "Legacy global user preference.",
                    "",
                    "## How to use",
                    "Use by default.",
                    "",
                    "## Evidence",
                    "Global test fixture.",
                    "",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        global_feedback_candidate = self.memory_home / "global" / "candidates" / "feedback" / "rule.md"
        global_feedback_candidate.parent.mkdir(parents=True, exist_ok=True)
        global_feedback_candidate.write_text(
            "\n".join(
                [
                    "---",
                    "id: feedback-2026-04-21-global-rule",
                    "key: global-feedback-rule",
                    "scope: global",
                    "type: feedback",
                    "created_at: 2026-04-21T00:00:00+00:00",
                    "last_confirmed_at: 2026-04-21T00:00:00+00:00",
                    "status: candidate",
                    "---",
                    "# Global Rule",
                    "",
                    "## Rule",
                    "以后回答里不要展开大段文件清单。",
                    "",
                    "## Why",
                    "Legacy global feedback memory.",
                    "",
                    "## How to apply",
                    "Apply by default.",
                    "",
                    "## Evidence",
                    "Global test fixture.",
                    "",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        self.assertEqual(self.run_script("--force"), 0)
        self.assertFalse(workspace_feedback.exists())
        self.assertFalse(workspace_user_candidate.exists())
        self.assertFalse(global_user.exists())
        self.assertFalse(global_feedback_candidate.exists())

        self.assertTrue((self.workspace_memory_home / "archive" / "disabled" / "memories" / "feedback" / "rule.md").exists())
        self.assertTrue((self.workspace_memory_home / "archive" / "disabled" / "candidates" / "user" / "pref.md").exists())
        self.assertTrue((self.memory_home / "global" / "archive" / "disabled" / "memories" / "user" / "pref.md").exists())
        self.assertTrue((self.memory_home / "global" / "archive" / "disabled" / "candidates" / "feedback" / "rule.md").exists())

        memory_index = (self.workspace_memory_home / "memories" / "MEMORY.md").read_text(encoding="utf-8")
        self.assertNotIn("[feedback]", memory_index)
        global_memory_index = (self.memory_home / "global" / "memories" / "MEMORY.md").read_text(encoding="utf-8")
        self.assertNotIn("[user]", global_memory_index)
        self.assertNotIn("[feedback]", global_memory_index)

        active_context = (self.workspace_memory_home / "runtime" / "active_context.md").read_text(encoding="utf-8")
        self.assertIn("native memories own common corrections and convenience recall", active_context)

        global_context = (self.memory_home / "global" / "runtime" / "global_context.md").read_text(encoding="utf-8")
        self.assertIn("native memories own personal preference recall", global_context)
        self.assertIn("native memories own common corrections and convenience recall", global_context)

    def test_disabled_global_recall_rebuilds_indexes_without_new_sessions(self):
        self.write_default_config()

        for config_path in (
            self.workspace_memory_home / "config.json",
            self.memory_home / "global" / "config.json",
        ):
            payload = json.loads(config_path.read_text(encoding="utf-8"))
            payload["memory_types"]["user"] = False
            payload["memory_types"]["feedback"] = False
            config_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        global_feedback = self.memory_home / "global" / "memories" / "feedback" / "rule.md"
        global_feedback.parent.mkdir(parents=True, exist_ok=True)
        global_feedback.write_text(
            "\n".join(
                [
                    "---",
                    "id: feedback-2026-04-21-global-rule",
                    "key: global-feedback-rule",
                    "scope: global",
                    "type: feedback",
                    "created_at: 2026-04-21T00:00:00+00:00",
                    "last_confirmed_at: 2026-04-21T00:00:00+00:00",
                    "status: active",
                    "---",
                    "# Global Rule",
                    "",
                    "## Rule",
                    "以后回答里不要展开大段文件清单。",
                    "",
                    "## Why",
                    "Legacy global feedback memory.",
                    "",
                    "## How to apply",
                    "Apply by default.",
                    "",
                    "## Evidence",
                    "Global test fixture.",
                    "",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        self.assertEqual(self.run_script(), 0)
        self.assertFalse(global_feedback.exists())

        global_memory_index = (self.memory_home / "global" / "memories" / "MEMORY.md").read_text(encoding="utf-8")
        self.assertNotIn("[feedback]", global_memory_index)

        global_context = (self.memory_home / "global" / "runtime" / "global_context.md").read_text(encoding="utf-8")
        self.assertIn("native memories own common corrections and convenience recall", global_context)
        self.assertNotIn("以后回答里不要展开大段文件清单", global_context)

    def test_content_keys_prevent_confirmed_slug_collision(self):
        rows_a = [
            {
                "type": "session_meta",
                "timestamp": "2026-04-02T10:00:00+00:00",
                "payload": {
                    "id": "session-a",
                    "cwd": str(self.workspace),
                    "timestamp": "2026-04-02T10:00:00+00:00",
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "user",
                    "content": [{"text": "可以，就按 README 驱动安装，以后都这样。"}],
                },
            },
        ]
        rows_b = [
            {
                "type": "session_meta",
                "timestamp": "2026-04-02T11:00:00+00:00",
                "payload": {
                    "id": "session-b",
                    "cwd": str(self.workspace),
                    "timestamp": "2026-04-02T11:00:00+00:00",
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "user",
                    "content": [{"text": "可以，就按 README 读取安装，以后都这样。"}],
                },
            },
        ]
        write_jsonl(self.codex_home / "sessions" / "2026" / "04" / "02" / "session-a.jsonl", rows_a)
        write_jsonl(self.codex_home / "sessions" / "2026" / "04" / "02" / "session-b.jsonl", rows_b)
        self.write_default_config()
        self.assertEqual(self.run_script("--force"), 0)

        root = self.workspace_memory_home
        feedback_files = sorted((root / "memories" / "feedback").glob("*.md"))
        self.assertEqual(len(feedback_files), 2)
        names = [path.name for path in feedback_files]
        self.assertTrue(all(len(name.split("-")) >= 4 for name in names))

    def test_repeat_run_is_incremental(self):
        rows = [
            {
                "type": "session_meta",
                "timestamp": "2026-04-02T10:00:00+00:00",
                "payload": {
                    "id": "session-2",
                    "cwd": str(self.workspace),
                    "timestamp": "2026-04-02T10:00:00+00:00",
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "user",
                    "content": [{"text": "我常用 Codex App。"}],
                },
            },
        ]
        session_path = self.codex_home / "sessions" / "2026" / "04" / "02" / "session-2.jsonl"
        write_jsonl(session_path, rows)
        self.write_default_config()

        first = self.run_script()
        second = self.run_script()

        self.assertEqual(first, 0)
        self.assertEqual(second, 0)

        registry = json.loads((self.workspace_memory_home / "registry.json").read_text(encoding="utf-8"))
        normalized_keys = {self.module.normalize_path(key) for key in registry["processed_sessions"]}
        self.assertIn(self.module.normalize_path(str(session_path)), normalized_keys)
        root = self.workspace_memory_home
        self.assertEqual(len(list((root / "candidates" / "user").glob("*.md"))), 1)
        self.assertEqual(len(list((self.memory_home / "global" / "memories" / "user").glob("*.md"))), 1)

    def test_reference_promotion_is_capped_per_source(self):
        assistant_text = (
            "原文第一条结论是记忆要分层。"
            " 原文第二条结论是反馈要同时记录纠正和确认。"
            " 原文第三条结论是用文件系统保存长期记忆。"
            " 原文第四条结论是 Dream 负责修正漂移。"
        )
        rows = [
            {
                "type": "session_meta",
                "timestamp": "2026-04-02T10:00:00+00:00",
                "payload": {
                    "id": "session-ref-cap",
                    "cwd": str(self.workspace),
                    "timestamp": "2026-04-02T10:00:00+00:00",
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"text": assistant_text}],
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "user",
                    "content": [{"text": "参考 https://example.com/article 这篇文章，分析总结给我。"}],
                },
            },
        ]
        write_jsonl(self.codex_home / "sessions" / "2026" / "04" / "02" / "session-ref-cap.jsonl", rows)
        self.write_default_config()
        self.assertEqual(self.run_script("--force"), 0)

        root = self.workspace_memory_home
        active_reference_files = list((root / "memories" / "reference").glob("*.md"))
        candidate_reference_files = list((root / "candidates" / "reference").glob("*.md"))
        self.assertEqual(len(active_reference_files), 3)
        self.assertEqual(len(candidate_reference_files), 4)

    def test_runtime_context_uses_focus_sessions(self):
        (self.workspace / "old.py").write_text("old\n", encoding="utf-8")
        (self.workspace / "mid.py").write_text("mid\n", encoding="utf-8")
        (self.workspace / "new.py").write_text("new\n", encoding="utf-8")
        rows_old = [
            {
                "type": "session_meta",
                "timestamp": "2026-04-02T08:00:00+00:00",
                "payload": {
                    "id": "session-old",
                    "cwd": str(self.workspace),
                    "timestamp": "2026-04-02T08:00:00+00:00",
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"text": f"Old error happened. Changed {self.workspace}/old.py"}],
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "user",
                    "content": [{"text": "旧任务，已经完成。"}],
                },
            },
        ]
        rows_mid = [
            {
                "type": "session_meta",
                "timestamp": "2026-04-02T09:00:00+00:00",
                "payload": {
                    "id": "session-mid",
                    "cwd": str(self.workspace),
                    "timestamp": "2026-04-02T09:00:00+00:00",
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"text": f"Middle failure occurred. Changed {self.workspace}/mid.py"}],
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "user",
                    "content": [{"text": "中间任务。"}],
                },
            },
        ]
        rows_new = [
            {
                "type": "session_meta",
                "timestamp": "2026-04-02T10:00:00+00:00",
                "payload": {
                    "id": "session-new",
                    "cwd": str(self.workspace),
                    "timestamp": "2026-04-02T10:00:00+00:00",
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"text": f"New failure occurred. Changed {self.workspace}/new.py"}],
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "user",
                    "content": [{"text": "当前任务继续。"}],
                },
            },
        ]
        write_jsonl(self.codex_home / "sessions" / "2026" / "04" / "02" / "session-old.jsonl", rows_old)
        write_jsonl(self.codex_home / "sessions" / "2026" / "04" / "02" / "session-mid.jsonl", rows_mid)
        write_jsonl(self.codex_home / "sessions" / "2026" / "04" / "02" / "session-new.jsonl", rows_new)
        self.write_default_config()
        self.assertEqual(self.run_script("--force"), 0)

        active_context = (self.workspace_memory_home / "runtime" / "active_context.md").read_text(encoding="utf-8")
        self.assertIn("new.py", active_context)
        self.assertIn("mid.py", active_context)
        self.assertNotIn("old.py", active_context)

    def test_metadata_migration_backfills_workspace_origins_conservatively(self):
        other_workspace = self.base / "workspace-copy"
        other_workspace.mkdir()
        self.write_default_config()

        root_a = self.workspace_memory_home / "memories" / "feedback"
        root_b = self.module.workspace_memory_home(self.memory_home, other_workspace) / "memories" / "feedback"
        root_a.mkdir(parents=True, exist_ok=True)
        root_b.mkdir(parents=True, exist_ok=True)
        legacy_text = """---
id: feedback-legacy
type: feedback
created_at: 2026-04-01T10:00:00+00:00
last_confirmed_at: 2026-04-01T10:00:00+00:00
status: active
confidence: 0.90
---
# Legacy Rule

## Rule
不要跑 install.sh

## Why
legacy

## How to apply
legacy

## Evidence
legacy
"""
        (root_a / "legacy-a.md").write_text(legacy_text, encoding="utf-8")
        (root_b / "legacy-b.md").write_text(legacy_text, encoding="utf-8")

        self.assertEqual(self.run_script("--force"), 0)

        migrated_a = self.module.parse_memory_file(root_a / "legacy-a.md")
        migrated_b = self.module.parse_memory_file(root_b / "legacy-b.md")
        expected_origin = sorted(
            [self.module.workspace_key(self.workspace), self.module.workspace_key(other_workspace)]
        )[:1]
        self.assertEqual(self.module.parse_metadata_list(migrated_a.metadata.get("source_workspaces")), expected_origin)
        self.assertEqual(self.module.parse_metadata_list(migrated_b.metadata.get("source_workspaces")), expected_origin)
        self.assertEqual(self.module.parse_metadata_list(migrated_a.metadata.get("source_runs")), ["feedback-legacy"])
        self.assertEqual(self.module.parse_metadata_list(migrated_b.metadata.get("source_runs")), ["feedback-legacy"])

    def test_global_candidate_governance_archives_promoted_and_overflow_items(self):
        self.write_default_config()
        global_candidates = self.memory_home / "global" / "candidates" / "feedback"
        global_active = self.memory_home / "global" / "memories" / "feedback"
        archived_root = self.memory_home / "global" / "candidates_archive" / "feedback"
        global_candidates.mkdir(parents=True, exist_ok=True)
        global_active.mkdir(parents=True, exist_ok=True)

        active_text = """---
id: feedback-2026-04-03-rule-active
key: rule-active
scope: global
type: feedback
created_at: 2026-04-03T10:00:00+00:00
last_confirmed_at: 2026-04-03T10:00:00+00:00
status: active
confidence: 0.95
source_runs: [\"run-a\"]
source_workspaces: [\"workspace-a\"]
---
# Active Rule

## Rule
不要跑 install.sh

## Why
active

## How to apply
active

## Evidence
active
"""
        candidate_promoted = active_text.replace("status: active", "status: candidate").replace("# Active Rule", "# Candidate Promoted")
        candidate_overflow_1 = candidate_promoted.replace("rule-active", "rule-overflow").replace("不要跑 install.sh", "统一先读 README").replace("run-a", "run-b").replace("workspace-a", "workspace-b")
        candidate_overflow_2 = candidate_overflow_1.replace("Candidate Promoted", "Candidate Overflow 2").replace("2026-04-03T10:00:00+00:00", "2026-04-01T10:00:00+00:00")
        candidate_overflow_3 = candidate_overflow_1.replace("Candidate Promoted", "Candidate Overflow 3").replace("2026-04-03T10:00:00+00:00", "2026-03-01T10:00:00+00:00").replace("run-b", "run-c")

        (global_active / "active.md").write_text(active_text, encoding="utf-8")
        (global_candidates / "promoted.md").write_text(candidate_promoted, encoding="utf-8")
        (global_candidates / "overflow-1.md").write_text(candidate_overflow_1, encoding="utf-8")
        (global_candidates / "overflow-2.md").write_text(candidate_overflow_2, encoding="utf-8")
        (global_candidates / "overflow-3.md").write_text(candidate_overflow_3, encoding="utf-8")

        self.assertEqual(self.run_script("--force-dream"), 0)

        remaining = sorted(path.name for path in global_candidates.glob("*.md"))
        archived = sorted(path.name for path in archived_root.glob("*.md"))
        self.assertNotIn("promoted.md", remaining)
        self.assertIn("promoted.md", archived)
        self.assertLessEqual(len(remaining), 2)

    def test_global_conflict_queue_captures_cross_workspace_feedback_conflict(self):
        other_workspace = self.base / "workspace-b"
        other_workspace.mkdir()
        other_workspace_memory_home = self.module.workspace_memory_home(self.memory_home, other_workspace)
        self.write_default_config()
        other_workspace_memory_home.mkdir(parents=True, exist_ok=True)
        (other_workspace_memory_home / "config.json").write_text(
            (self.workspace_memory_home / "config.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )

        rows_a = [
            {
                "type": "session_meta",
                "timestamp": "2026-04-02T10:00:00+00:00",
                "payload": {
                    "id": "session-global-a",
                    "cwd": str(self.workspace),
                    "timestamp": "2026-04-02T10:00:00+00:00",
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "user",
                    "content": [{"text": "以后所有项目都不要用 install.sh。"}],
                },
            },
        ]
        rows_b = [
            {
                "type": "session_meta",
                "timestamp": "2026-04-02T11:00:00+00:00",
                "payload": {
                    "id": "session-global-b",
                    "cwd": str(other_workspace),
                    "timestamp": "2026-04-02T11:00:00+00:00",
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "user",
                    "content": [{"text": "以后所有项目都要用 install.sh。"}],
                },
            },
        ]
        day_dir = self.codex_home / "sessions" / "2026" / "04" / "02"
        write_jsonl(day_dir / "session-global-a.jsonl", rows_a)
        write_jsonl(day_dir / "session-global-b.jsonl", rows_b)

        self.assertEqual(self.run_script_for_workspace(self.workspace, "--force-dream"), 0)
        self.assertEqual(self.run_script_for_workspace(other_workspace, "--force-dream"), 0)

        conflict_files = list((self.memory_home / "global" / "conflicts" / "open").glob("*.md"))
        self.assertEqual(len(conflict_files), 1)
        conflict_text = conflict_files[0].read_text(encoding="utf-8")
        self.assertIn("scope_split", conflict_text)
        self.assertIn("install.sh", conflict_text)


if __name__ == "__main__":
    unittest.main()
