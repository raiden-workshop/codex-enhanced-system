#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

DEFAULT_CODEX_HOME = Path.home() / ".codex"
DEFAULT_MEMORY_HOME = DEFAULT_CODEX_HOME / "memory"
INSTRUCTION_FILE_NAME = "GUIDE.md"
INSTRUCTIONS_REL = Path("instructions")
WORKSPACES_REL = Path("workspaces")
GLOBAL_REL = Path("global")
RUNS_REL = Path("runs")
CANDIDATES_REL = Path("candidates")
MEMORIES_REL = Path("memories")
RUNTIME_REL = Path("runtime")
DREAM_REL = Path("dream")
CONFIG_REL = Path("config.json")
REGISTRY_REL = Path("registry.json")
WORKSPACE_INDEX_REL = WORKSPACES_REL / "index.json"
MEMORY_INDEX_REL = MEMORIES_REL / "MEMORY.md"
ACTIVE_CONTEXT_REL = RUNTIME_REL / "active_context.md"
LATEST_COMPRESSION_REL = RUNTIME_REL / "compression" / "latest.md"
COMPRESSION_ARCHIVE_REL = RUNTIME_REL / "compression" / "archive"
DREAM_STATE_REL = DREAM_REL / "state.json"
DREAM_REPORTS_REL = DREAM_REL / "reports"
GLOBAL_CANDIDATES_REL = GLOBAL_REL / "candidates"
GLOBAL_CANDIDATES_ARCHIVE_REL = GLOBAL_REL / "candidates_archive"
GLOBAL_MEMORIES_REL = GLOBAL_REL / "memories"
GLOBAL_RUNTIME_REL = GLOBAL_REL / "runtime"
GLOBAL_CONTEXT_REL = GLOBAL_RUNTIME_REL / "global_context.md"
GLOBAL_CONFLICTS_REL = GLOBAL_REL / "conflicts"
GLOBAL_CONFLICTS_OPEN_REL = GLOBAL_CONFLICTS_REL / "open"
GLOBAL_CONFLICTS_RESOLVED_REL = GLOBAL_CONFLICTS_REL / "resolved"
GLOBAL_CONFLICTS_ARCHIVED_REL = GLOBAL_CONFLICTS_REL / "archived"
GLOBAL_DREAM_REL = GLOBAL_REL / "dream"
GLOBAL_DREAM_STATE_REL = GLOBAL_DREAM_REL / "state.json"
GLOBAL_DREAM_REPORTS_REL = GLOBAL_DREAM_REL / "reports"
GLOBAL_CONFIG_REL = GLOBAL_REL / "config.json"
GLOBAL_REGISTRY_REL = GLOBAL_REL / "registry.json"
GLOBAL_MEMORY_INDEX_REL = GLOBAL_MEMORIES_REL / "MEMORY.md"

MEMORY_TYPES = ("user", "feedback", "project", "reference", "open_loop")
GLOBAL_MEMORY_TYPES = ("user", "feedback", "reference")
WORKSPACE_SCOPES = ("company", "user", "repo", "local")

DEFAULT_CONFIG: Dict[str, Any] = {
    "version": 1,
    "context_window_tokens": 200000,
    "reserve_tokens": 13000,
    "index_max_lines": 200,
    "index_max_chars_per_entry": 150,
    "dream": {
        "min_hours_since_last": 24,
        "min_sessions_since_last": 5,
    },
    "global_dream": {
        "min_hours_since_last": 72,
        "min_workspace_updates_since_last": 3,
    },
    "candidate_governance": {
        "global": {
            "max_per_type": 50,
            "archive_after_days": 30,
            "keep_per_key": 1,
        }
    },
    "compression": {
        "quote_limit": 3,
        "recent_session_limit": 8,
    },
    "promotion": {
        "feedback_min_confidence": 0.85,
        "project_min_confidence": 0.8,
        "reference_min_confidence": 0.8,
        "user_min_confidence": 0.85,
        "reference_max_promoted_per_source": 3,
    },
    "runtime": {
        "focus_session_limit": 2,
    },
}

LOW_SIGNAL_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"^继续$",
        r"^可以$",
        r"^好的?$",
        r"^收到$",
        r"^对$",
    )
]

RELATIVE_WEEKDAY_MAP = {
    "一": 0,
    "二": 1,
    "三": 2,
    "四": 3,
    "五": 4,
    "六": 5,
    "日": 6,
    "天": 6,
}

ABSOLUTE_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
URL_RE = re.compile(r"https?://[^\s)>\]]+")
FILE_LINK_RE = re.compile(r"\[[^\]]+\]\((/[^)]+)\)")
ABS_FILE_RE = re.compile(r"(/[A-Za-z0-9._ \-\u4e00-\u9fff/]+?\.[A-Za-z0-9]+)")
ERROR_RE = re.compile(r"(error|failed|failure|traceback|exception|报错|失败|异常|超时)", re.IGNORECASE)
DECISION_RE = re.compile(r"(决定|采用|改成|默认|优先|use|prefer|switch to)", re.IGNORECASE)

USER_MEMORY_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"我现在常用",
        r"我常用",
        r"我是重度",
        r"我更看重",
        r"我习惯",
    )
]

FEEDBACK_CORRECTION_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"不要",
        r"别再",
        r"别 ",
        r"改成",
        r"以后都",
        r"优先",
    )
]

FEEDBACK_CONFIRMATION_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"可以",
        r"就这样",
        r"先这样",
        r"没问题",
        r"对，就",
        r"可以，就",
    )
]

PROJECT_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"当前工作区",
        r"这个工作区",
        r"当前仓库",
        r"这个仓库",
        r"BuddyPulse",
        r"默认按",
        r"只负责",
        r"不负责",
        r"不维护",
        r"单 worker",
        r"single worker",
    )
]

REFERENCE_HINT_RE = re.compile(r"(参考|文章|文档|源码|链接)", re.IGNORECASE)
REFERENCE_REQUEST_RE = re.compile(r"(学习下|仔细学习|分析总结|看这篇|读这篇|这篇文章|这篇文档|这个链接)", re.IGNORECASE)
REFERENCE_SUMMARY_HINT_RE = re.compile(r"(核心|结论|关键|真正|值得|建议|原则|不是.+而是|一句话总结|最重要|严格模仿|记忆系统)", re.IGNORECASE)
REFERENCE_CONTEXT_RE = re.compile(r"(原文|文章|源码|文档|这篇|作者|Claude Code|外部|参考|来源|链接)", re.IGNORECASE)
QUESTION_PREFIX_RE = re.compile(r"^(为什么|怎么|如何|是否|是不是|要不要|能不能|可不可以|需不需要|什么时候|哪个|哪些|多少|谁|哪里|你建议|该不该|能否|会不会|怎么解决|如何解决)", re.IGNORECASE)
QUESTION_SUFFIX_RE = re.compile(r"(吗|么|呢)$", re.IGNORECASE)
EXPLICIT_GLOBAL_RE = re.compile(r"(全局|所有项目|整个codex|整个 codex|整个app|整个 app|跨项目|以后都|统一默认)", re.IGNORECASE)
NEGATION_RE = re.compile(r"(不要|别|禁止|not|never|avoid)", re.IGNORECASE)
PROJECT_SPECIFIC_RE = re.compile(r"(当前工作区|这个工作区|当前仓库|这个仓库|repo|仓库|项目里|这个项目|本项目)", re.IGNORECASE)
POLARITY_STRIP_RE = re.compile(r"(不要|别|禁止|应该|必须|优先|默认|统一|全局|要用|不用|使用|用|use|prefer|avoid|not|never|always)", re.IGNORECASE)
TASK_SCOPED_RE = re.compile(
    r"(我要睡觉了|继续做|不要停|直到.*完成|本轮|这轮|这次|本次|今天|做完|全部完成|这一轮|按一次|步骤|1、|2、|3、|4、|5、|6、)",
    re.IGNORECASE,
)
DURABLE_FEEDBACK_RE = re.compile(r"(以后|默认|优先|一律|统一|记住|都用|以.+为准|不要跑|不要用|先读|固定)", re.IGNORECASE)
ASSISTANT_META_RE = re.compile(
    r"^(我(已经|先|再|现在|会|把|用|看完了|看到|发现|看一下)|下面|接下来|如果你要|我可以继续|我建议下一步|我先)",
    re.IGNORECASE,
)
REFERENCE_META_EXCLUSION_RE = re.compile(
    r"(当前卡点|本机|远程调试|Chrome|CDP|这轮|测试覆盖|我看到|我发现|我看一下|我先|我再|我现在)",
    re.IGNORECASE,
)
NOISE_FRAGMENT_RE = re.compile(
    r"^(我先|我再|我现在开始|我准备|我已经|接下来|下一步|最后|然后|这一轮|这轮|继续|开始|自动化检查|单测|review|qa|设计文档|开发文档)",
    re.IGNORECASE,
)
WHITESPACE_RE = re.compile(r"\s+")
ENVIRONMENT_BLOCK_RE = re.compile(r"<environment_context>.*?</environment_context>", re.DOTALL | re.IGNORECASE)

SECTION_KEYS = {
    "user": ("Fact", "Why it matters", "How to use", "Evidence"),
    "feedback": ("Rule", "Why", "How to apply", "Evidence"),
    "project": ("Project fact", "Why it matters", "When relevant", "Evidence"),
    "reference": ("Reference takeaway", "Why it matters", "How to reuse", "Source"),
    "open_loop": ("Summary", "Next Check", "Evidence"),
}

INSTRUCTION_TEMPLATES = {
    "company": "# Company Guide\n\n- Put organization-wide defaults here.\n",
    "user": "# User Guide\n\n- Put cross-project personal defaults here.\n",
    "repo": "# Repo Guide\n\n- Put repository-shared guidance here.\n",
    "local": "# Local Guide\n\n- Put machine-local private guidance here.\n",
}


@dataclass
class CandidateMemory:
    scope: str
    memory_type: str
    title: str
    sections: Dict[str, str]
    created_at: str
    last_confirmed_at: str
    source_session_id: str
    source_path: str
    source_url: str | None = None
    key: str = ""
    status: str = "candidate"
    confidence: float = 0.5
    auto_promote: bool = False
    source_runs: List[str] | None = None
    source_workspaces: List[str] | None = None


@dataclass
class SessionRecord:
    session_id: str
    started_at: str
    day: str
    cwd: str
    path: Path
    user_turns: List[str]
    assistant_turns: List[str]
    summary: str
    low_signal: bool
    files_changed: List[str]
    errors: List[str]
    decisions: List[str]
    quotes: List[str]
    current_goal: str
    candidates: List[CandidateMemory]


@dataclass
class MemoryFile:
    path: Path
    metadata: Dict[str, str]
    title: str
    sections: Dict[str, str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh the global Codex memory system from session history.")
    parser.add_argument("--workspace-root", type=Path, default=Path.cwd())
    parser.add_argument("--codex-home", type=Path, default=DEFAULT_CODEX_HOME)
    parser.add_argument("--memory-home", type=Path, default=DEFAULT_MEMORY_HOME)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--force-dream", action="store_true")
    return parser.parse_args()


def normalize_path(path: Path | str) -> str:
    raw = str(path).strip().replace("\\", "/")
    while "//" in raw:
        raw = raw.replace("//", "/")
    if raw.startswith("/private/"):
        raw = raw[len("/private") :]
    if len(raw) > 1:
        raw = raw.rstrip("/")
    return raw.lower()


def clean_path_preserve_case(path: Path | str) -> str:
    raw = str(path).strip().replace("\\", "/")
    while "//" in raw:
        raw = raw.replace("//", "/")
    if raw.startswith("/private/"):
        raw = raw[len("/private") :]
    if len(raw) > 1:
        raw = raw.rstrip("/")
    return raw


def workspace_key(workspace_root: Path | str) -> str:
    display = clean_path_preserve_case(workspace_root)
    name = Path(display).name or "workspace"
    prefix = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "workspace"
    digest = hashlib.sha1(normalize_path(display).encode("utf-8")).hexdigest()[:12]
    return f"{prefix[:40]}-{digest}"


def workspace_memory_home(memory_home: Path, workspace_root: Path) -> Path:
    return memory_home / WORKSPACES_REL / workspace_key(workspace_root)


def explicit_global_signal(text: str) -> bool:
    return bool(EXPLICIT_GLOBAL_RE.search(clean_text(text)))


def is_project_specific_text(text: str) -> bool:
    fragment = clean_text(text)
    if not fragment:
        return False
    if PROJECT_SPECIFIC_RE.search(fragment):
        return True
    return any(pattern.search(fragment) for pattern in PROJECT_PATTERNS)


def conflict_polarity(text: str) -> str:
    if NEGATION_RE.search(clean_text(text)):
        return "negative"
    return "positive"


def conflict_topic_key(text: str) -> str:
    fragment = POLARITY_STRIP_RE.sub(" ", clean_text(text).lower())
    fragment = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", fragment)
    fragment = WHITESPACE_RE.sub(" ", fragment).strip()
    if not fragment:
        fragment = clean_text(text).lower()
    return shorten(fragment, 120)


def metadata_list_value(items: Sequence[str] | None) -> str:
    return json.dumps(list(items or []), ensure_ascii=False)


def parse_metadata_list(raw: str | None) -> List[str]:
    if not raw:
        return []
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        return [raw] if raw else []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def parse_confidence_value(metadata: Dict[str, str]) -> float:
    try:
        return float(metadata.get("confidence", "0") or "0")
    except ValueError:
        return 0.0


def workspace_nodes(memory_home: Path) -> List[Tuple[str, Path]]:
    root = memory_home / WORKSPACES_REL
    nodes: List[Tuple[str, Path]] = []
    if not root.exists():
        return nodes
    for path in sorted(root.iterdir()):
        if not path.is_dir():
            continue
        nodes.append((path.name, path))
    return nodes


def item_origin_workspaces(workspace_key_value: str, item: MemoryFile) -> List[str]:
    values = parse_metadata_list(item.metadata.get("source_workspaces"))
    return values or [workspace_key_value]


def item_origin_runs(item: MemoryFile) -> List[str]:
    values = parse_metadata_list(item.metadata.get("source_runs"))
    return values or [item.metadata.get("id", item.path.stem)]


def path_exists_with_private_alias(path: str) -> bool:
    candidate = Path(path)
    if candidate.exists():
        return True
    if path.startswith("/var/"):
        return Path("/private" + path).exists()
    return False


def deep_merge(base: Any, override: Any) -> Any:
    if isinstance(base, dict) and isinstance(override, dict):
        merged = {key: deep_merge(base[key], override[key]) if key in base else override[key] for key in override}
        for key, value in base.items():
            if key not in merged:
                merged[key] = value
        return merged
    return override


def clean_text(text: str) -> str:
    text = ENVIRONMENT_BLOCK_RE.sub(" ", text)
    text = WHITESPACE_RE.sub(" ", text).strip()
    return text


def looks_like_question(text: str) -> bool:
    fragment = clean_text(text)
    if not fragment:
        return False
    if "?" in fragment or "？" in fragment:
        return True
    if QUESTION_PREFIX_RE.search(fragment):
        return True
    if QUESTION_SUFFIX_RE.search(fragment):
        return True
    if fragment.endswith("吧"):
        return True
    if re.search(r"(怎么解决|如何解决|怎么办)", fragment):
        return True
    if "还是" in fragment and fragment.startswith(("你", "这", "这个", "那", "如果")):
        return True
    return False


def looks_like_reference_request(text: str) -> bool:
    fragment = clean_text(text)
    return bool(REFERENCE_REQUEST_RE.search(fragment) or fragment.startswith(("学习下", "仔细学习", "分析总结", "看下这篇", "读下这篇")))


def is_task_scoped_feedback(text: str) -> bool:
    fragment = clean_text(text)
    if not fragment:
        return False
    if DURABLE_FEEDBACK_RE.search(fragment):
        return False
    return bool(TASK_SCOPED_RE.search(fragment))


def is_durable_feedback(text: str) -> bool:
    fragment = clean_text(text)
    if not fragment or looks_like_question(fragment):
        return False
    if DURABLE_FEEDBACK_RE.search(fragment):
        return True
    if len(fragment) > 120:
        return False
    if is_task_scoped_feedback(fragment):
        return False
    return False


def shorten(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, round(len(text) / 1.6))


def slugify(text: str) -> str:
    ascii_slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if ascii_slug:
        return ascii_slug[:60]
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
    return f"item-{digest}"


def primary_section_name(memory_type: str) -> str:
    return SECTION_KEYS[memory_type][0]


def primary_section_text(memory_type: str, sections: Dict[str, str]) -> str:
    return clean_text(sections.get(primary_section_name(memory_type), ""))


def candidate_identity_key(candidate: CandidateMemory) -> str:
    payload = {
        "type": candidate.memory_type,
        "primary": primary_section_text(candidate.memory_type, candidate.sections),
        "source_url": candidate.source_url or "",
    }
    return hashlib.sha1(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:12]


def memory_file_identity_key(item: MemoryFile) -> str:
    memory_type = item.metadata.get("type") or item.path.parent.name
    payload = {
        "type": memory_type,
        "primary": primary_section_text(memory_type, item.sections) if memory_type in SECTION_KEYS else clean_text(item.title),
        "source_url": item.metadata.get("source", ""),
    }
    return hashlib.sha1(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:12]


def ensure_iso(ts: str) -> str:
    value = ts.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return value


def parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ensure_iso(ts))


def format_date(dt: datetime) -> str:
    return dt.date().isoformat()


def absolutize_relative_dates(text: str, base_dt: datetime) -> str:
    replacements = {
        "今天": format_date(base_dt),
        "昨天": format_date(base_dt - timedelta(days=1)),
        "明天": format_date(base_dt + timedelta(days=1)),
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    def _replace_next_weekday(match: re.Match[str]) -> str:
        token = match.group(1)
        weekday = RELATIVE_WEEKDAY_MAP[token]
        current_weekday = base_dt.weekday()
        days_ahead = (weekday - current_weekday + 7) % 7
        if days_ahead == 0:
            days_ahead = 7
        return format_date(base_dt + timedelta(days=days_ahead + 7))

    def _replace_this_weekday(match: re.Match[str]) -> str:
        token = match.group(1)
        weekday = RELATIVE_WEEKDAY_MAP[token]
        current_weekday = base_dt.weekday()
        days_ahead = (weekday - current_weekday + 7) % 7
        return format_date(base_dt + timedelta(days=days_ahead))

    text = re.sub(r"下周([一二三四五六日天])", _replace_next_weekday, text)
    text = re.sub(r"本周([一二三四五六日天])", _replace_this_weekday, text)
    return text


def iter_session_files(codex_home: Path) -> List[Path]:
    root = codex_home / "sessions"
    if not root.exists():
        return []
    return sorted(root.rglob("*.jsonl"), key=lambda item: item.stat().st_mtime)


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped:
            rows.append(json.loads(stripped))
    return rows


def _extract_text_fragments(content: Any) -> List[str]:
    fragments: List[str] = []
    if isinstance(content, str):
        fragments.append(content)
        return fragments
    if isinstance(content, list):
        for item in content:
            fragments.extend(_extract_text_fragments(item))
        return fragments
    if isinstance(content, dict):
        for key in ("text", "output_text", "input_text"):
            value = content.get(key)
            if isinstance(value, str):
                fragments.append(value)
    return fragments


def split_fragments(turns: Sequence[str]) -> Iterable[str]:
    for turn in turns:
        for fragment in re.split(r"[。！？；;，,\n]", turn):
            cleaned = clean_text(fragment)
            if 3 <= len(cleaned) <= 200:
                yield cleaned


def split_sentences(turns: Sequence[str]) -> Iterable[str]:
    for turn in turns:
        for fragment in re.split(r"[。！？；;\n]", turn):
            cleaned = clean_text(fragment)
            if 3 <= len(cleaned) <= 220:
                yield cleaned


def is_candidate_fragment(fragment: str, *, min_len: int = 6, max_len: int = 120) -> bool:
    if len(fragment) < min_len or len(fragment) > max_len:
        return False
    if fragment.startswith(("-", "*", "#")):
        return False
    if re.match(r"^\d+[\.\u3001)]", fragment):
        return False
    if fragment.endswith("？") or fragment.endswith("?"):
        return False
    if fragment.count("`") >= 2 or fragment.count("[") >= 1 or "](" in fragment:
        return False
    if NOISE_FRAGMENT_RE.search(fragment):
        return False
    return True


def score_user_candidate(fragment: str) -> float:
    if looks_like_question(fragment):
        return 0.0
    score = 0.6
    if any(pattern.search(fragment) for pattern in USER_MEMORY_PATTERNS):
        score += 0.3
    if fragment.startswith("我"):
        score += 0.05
    return min(score, 1.0)


def score_feedback_candidate(fragment: str) -> Tuple[float, bool]:
    score = 0.55
    durable = is_durable_feedback(fragment)
    if durable:
        score += 0.35
    if is_task_scoped_feedback(fragment):
        score -= 0.35
    if len(fragment) > 100:
        score -= 0.1
    return max(0.0, min(score, 1.0)), durable


def score_project_candidate(fragment: str) -> float:
    if looks_like_question(fragment):
        return 0.0
    score = 0.55
    if any(pattern.search(fragment) for pattern in PROJECT_PATTERNS):
        score += 0.25
    if fragment.startswith(("当前", "这个", "本工作区", "该工作区")):
        score += 0.1
    return min(score, 1.0)


def score_reference_candidate(fragment: str) -> float:
    if looks_like_question(fragment) or looks_like_reference_request(fragment):
        return 0.0
    score = 0.55
    if REFERENCE_SUMMARY_HINT_RE.search(fragment):
        score += 0.2
    if not ASSISTANT_META_RE.search(fragment):
        score += 0.1
    if REFERENCE_META_EXCLUSION_RE.search(fragment):
        score -= 0.25
    if 16 <= len(fragment) <= 140:
        score += 0.05
    return min(score, 1.0)


def list_unique(items: Iterable[str], limit: int) -> List[str]:
    result: List[str] = []
    seen: set[str] = set()
    for item in items:
        normalized = item.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
        if len(result) >= limit:
            break
    return result


def is_low_signal(user_turns: Sequence[str]) -> bool:
    if not user_turns:
        return True
    if len(user_turns) == 1 and any(pattern.match(user_turns[0]) for pattern in LOW_SIGNAL_PATTERNS):
        return True
    return len(" ".join(user_turns)) <= 12


def build_summary(user_turns: Sequence[str], assistant_turns: Sequence[str], low_signal: bool) -> str:
    last_user = shorten(user_turns[-1], 90) if user_turns else "无有效用户输入"
    last_assistant = shorten(assistant_turns[-1], 120) if assistant_turns else "无最终答复"
    if low_signal:
        return f"低信息量交互：{last_user}"
    if len(user_turns) > 1:
        return f"本次会话共 {len(user_turns)} 轮，最后用户提到“{last_user}”，系统回应“{last_assistant}”。"
    return f"用户提到“{last_user}”，系统回应“{last_assistant}”。"


def extract_files_changed(texts: Sequence[str], workspace_root: Path) -> List[str]:
    matches: List[str] = []
    workspace_prefix = normalize_path(workspace_root)
    for text in texts:
        for item in FILE_LINK_RE.findall(text):
            if item.startswith("//"):
                continue
            if not item.startswith(("/Users/", "/.codex/", "/tmp/", "/private/")):
                continue
            display_path = clean_path_preserve_case(item)
            normalized = normalize_path(display_path)
            if not (normalized == workspace_prefix or normalized.startswith(workspace_prefix + "/")):
                continue
            if path_exists_with_private_alias(display_path):
                matches.append(display_path)
        for item in ABS_FILE_RE.findall(text):
            if item.startswith("//"):
                continue
            if not item.startswith(("/Users/", "/.codex/", "/tmp/", "/private/")):
                continue
            display_path = clean_path_preserve_case(item)
            normalized = normalize_path(display_path)
            if not (normalized == workspace_prefix or normalized.startswith(workspace_prefix + "/")):
                continue
            if path_exists_with_private_alias(display_path):
                matches.append(display_path)
    return list_unique(matches, 12)


def extract_errors(texts: Sequence[str]) -> List[str]:
    items: List[str] = []
    for text in texts:
        for fragment in split_sentences([text]):
            if not is_candidate_fragment(fragment, min_len=6, max_len=180):
                continue
            if ERROR_RE.search(fragment):
                items.append(shorten(fragment, 180))
    return list_unique(items, 8)


def extract_decisions(texts: Sequence[str]) -> List[str]:
    items: List[str] = []
    for text in texts:
        for fragment in split_sentences([text]):
            if not is_candidate_fragment(fragment, min_len=6, max_len=180):
                continue
            if DECISION_RE.search(fragment):
                items.append(shorten(fragment, 180))
    return list_unique(items, 8)


def extract_quotes(user_turns: Sequence[str]) -> List[str]:
    quotes = [shorten(turn, 180) for turn in user_turns if len(turn) >= 8]
    return list_unique(quotes, 6)


def find_reference_candidates(
    user_turns: Sequence[str],
    assistant_turns: Sequence[str],
    base_dt: datetime,
    session_id: str,
    source_path: Path,
    config: Dict[str, Any],
) -> List[CandidateMemory]:
    candidates: List[CandidateMemory] = []
    seen: set[str] = set()
    urls = list_unique((url for turn in user_turns for url in URL_RE.findall(turn)), 3)
    if not urls:
        return candidates
    if not any(REFERENCE_HINT_RE.search(turn) or looks_like_reference_request(turn) for turn in user_turns):
        return candidates
    threshold = float(config["promotion"]["reference_min_confidence"])
    max_promoted_per_source = int(config["promotion"]["reference_max_promoted_per_source"])
    candidates_by_url: Dict[str, List[CandidateMemory]] = {url: [] for url in urls}
    for fragment in split_sentences(assistant_turns):
        if not is_candidate_fragment(fragment, min_len=12, max_len=160):
            continue
        if looks_like_reference_request(fragment):
            continue
        normalized = shorten(absolutize_relative_dates(clean_text(fragment), base_dt), 180)
        if ASSISTANT_META_RE.search(normalized):
            continue
        if not REFERENCE_CONTEXT_RE.search(normalized):
            continue
        confidence = score_reference_candidate(normalized)
        if confidence < 0.65:
            continue
        for url in urls:
            key = f"{url}|{normalized}"
            if key in seen:
                continue
            seen.add(key)
            candidate = CandidateMemory(
                scope="workspace",
                memory_type="reference",
                title=shorten(normalized, 70),
                sections={
                    "Reference takeaway": normalized,
                    "Why it matters": "This conclusion was extracted from the analysis output of an external source.",
                    "How to reuse": "Reuse the conclusion when a similar implementation or planning question appears.",
                    "Source": url,
                },
                created_at=base_dt.isoformat(),
                last_confirmed_at=base_dt.isoformat(),
                source_session_id=session_id,
                source_path=str(source_path),
                source_url=url,
                confidence=confidence,
                auto_promote=False,
                source_runs=[session_id],
            )
            candidate.key = candidate_identity_key(candidate)
            candidates_by_url[url].append(candidate)
    for url, bucket in candidates_by_url.items():
        bucket.sort(key=lambda item: item.confidence, reverse=True)
        for index, candidate in enumerate(bucket):
            candidate.auto_promote = candidate.confidence >= threshold and index < max_promoted_per_source
            candidates.append(candidate)
    return candidates


def find_user_candidates(
    turns: Sequence[str],
    base_dt: datetime,
    session_id: str,
    source_path: Path,
    config: Dict[str, Any],
) -> List[CandidateMemory]:
    candidates: List[CandidateMemory] = []
    seen: set[str] = set()
    threshold = float(config["promotion"]["user_min_confidence"])
    for fragment in split_fragments(turns):
        if not fragment.startswith("我"):
            continue
        if not is_candidate_fragment(fragment):
            continue
        if not any(pattern.search(fragment) for pattern in USER_MEMORY_PATTERNS):
            continue
        statement = shorten(absolutize_relative_dates(fragment, base_dt), 180)
        if statement in seen:
            continue
        seen.add(statement)
        confidence = score_user_candidate(statement)
        candidate = CandidateMemory(
            scope="workspace",
            memory_type="user",
            title=shorten(statement, 70),
            sections={
                "Fact": statement,
                "Why it matters": "This looks like a durable user fact or long-term preference.",
                "How to use": "Use it as a default assumption in future work unless the user overrides it.",
                "Evidence": f"Explicit user statement in session {session_id}: {statement}",
            },
            created_at=base_dt.isoformat(),
            last_confirmed_at=base_dt.isoformat(),
            source_session_id=session_id,
            source_path=str(source_path),
            confidence=confidence,
            auto_promote=False,
            source_runs=[session_id],
        )
        candidate.key = candidate_identity_key(candidate)
        candidates.append(candidate)
    return candidates


def find_feedback_candidates(
    user_turns: Sequence[str],
    base_dt: datetime,
    session_id: str,
    source_path: Path,
    config: Dict[str, Any],
) -> List[CandidateMemory]:
    candidates: List[CandidateMemory] = []
    seen: set[str] = set()
    threshold = float(config["promotion"]["feedback_min_confidence"])
    for fragment in split_sentences(user_turns):
        if not is_candidate_fragment(fragment, min_len=6, max_len=140):
            continue
        normalized = shorten(absolutize_relative_dates(fragment, base_dt), 180)
        dedupe_key = normalized
        if explicit_global_signal(normalized) and is_durable_feedback(normalized):
            if dedupe_key not in seen:
                seen.add(dedupe_key)
                confidence, durable = score_feedback_candidate(normalized)
                candidate = CandidateMemory(
                    scope="workspace",
                    memory_type="feedback",
                    title=shorten(normalized, 70),
                    sections={
                        "Rule": normalized,
                        "Why": "Derived from an explicit cross-workspace default stated by the user." if durable else "Derived from a potentially cross-workspace instruction that still needs review.",
                        "How to apply": "Use it as a workspace default and allow global dream to decide whether it should become a global rule." if durable else "Keep it in candidate review until the scope is confirmed.",
                        "Evidence": f"Explicit global-scope statement in session {session_id}: {normalized}",
                    },
                    created_at=base_dt.isoformat(),
                    last_confirmed_at=base_dt.isoformat(),
                    source_session_id=session_id,
                    source_path=str(source_path),
                    confidence=confidence,
                    auto_promote=durable and confidence >= threshold,
                    source_runs=[session_id],
                )
                candidate.key = candidate_identity_key(candidate)
                candidates.append(candidate)
        if any(pattern.search(fragment) for pattern in FEEDBACK_CORRECTION_PATTERNS):
            if dedupe_key not in seen:
                seen.add(dedupe_key)
                confidence, durable = score_feedback_candidate(normalized)
                candidate = CandidateMemory(
                    scope="workspace",
                    memory_type="feedback",
                    title=shorten(normalized, 70),
                    sections={
                        "Rule": normalized,
                        "Why": "Derived from an explicit user correction." if durable else "Derived from a task-scoped or ambiguous user instruction that should be reviewed before long-term promotion.",
                        "How to apply": "Apply when a similar planning or implementation choice appears." if durable else "Use only for the current task shape unless it is later confirmed as a durable default.",
                        "Evidence": f"Explicit correction in session {session_id}: {normalized}",
                    },
                    created_at=base_dt.isoformat(),
                    last_confirmed_at=base_dt.isoformat(),
                    source_session_id=session_id,
                    source_path=str(source_path),
                    confidence=confidence,
                    auto_promote=durable and confidence >= threshold,
                    source_runs=[session_id],
                )
                candidate.key = candidate_identity_key(candidate)
                candidates.append(candidate)
        if any(pattern.search(fragment) for pattern in FEEDBACK_CONFIRMATION_PATTERNS):
            if len(normalized) <= 8:
                continue
            rule = normalized
            if dedupe_key not in seen:
                seen.add(dedupe_key)
                confidence, durable = score_feedback_candidate(rule)
                candidate = CandidateMemory(
                    scope="workspace",
                    memory_type="feedback",
                    title=shorten(f"Confirmed: {rule}", 70),
                    sections={
                        "Rule": shorten(rule, 180),
                        "Why": "Derived from an explicit or strongly implied user confirmation." if durable else "Derived from a confirmation that appears task-scoped and should be reviewed before long-term promotion.",
                        "How to apply": "Prefer this approach when future work matches the same decision shape." if durable else "Treat this as current-task guidance unless it is confirmed again as a durable default.",
                        "Evidence": f"Confirmation in session {session_id}: {rule}",
                    },
                    created_at=base_dt.isoformat(),
                    last_confirmed_at=base_dt.isoformat(),
                    source_session_id=session_id,
                    source_path=str(source_path),
                    confidence=confidence,
                    auto_promote=durable and confidence >= threshold,
                    source_runs=[session_id],
                )
                candidate.key = candidate_identity_key(candidate)
                candidates.append(candidate)
    return candidates


def find_project_candidates(
    turns: Sequence[str],
    base_dt: datetime,
    session_id: str,
    source_path: Path,
    config: Dict[str, Any],
) -> List[CandidateMemory]:
    candidates: List[CandidateMemory] = []
    seen: set[str] = set()
    threshold = float(config["promotion"]["project_min_confidence"])
    for fragment in split_sentences(turns):
        if not is_candidate_fragment(fragment, min_len=8, max_len=120):
            continue
        if looks_like_question(fragment):
            continue
        if not any(pattern.search(fragment) for pattern in PROJECT_PATTERNS):
            continue
        statement = shorten(absolutize_relative_dates(fragment, base_dt), 180)
        if statement in seen:
            continue
        seen.add(statement)
        confidence = score_project_candidate(statement)
        candidate = CandidateMemory(
            scope="workspace",
            memory_type="project",
            title=shorten(statement, 70),
            sections={
                "Project fact": statement,
                "Why it matters": "This looks like a persistent project-level fact or constraint.",
                "When relevant": "Use when working inside this repository or planning future tasks here.",
                "Evidence": f"Observed in session {session_id}: {statement}",
            },
            created_at=base_dt.isoformat(),
            last_confirmed_at=base_dt.isoformat(),
            source_session_id=session_id,
            source_path=str(source_path),
            confidence=confidence,
            auto_promote=confidence >= threshold,
            source_runs=[session_id],
        )
        candidate.key = candidate_identity_key(candidate)
        candidates.append(candidate)
    return candidates


def extract_candidates(
    user_turns: Sequence[str],
    assistant_turns: Sequence[str],
    base_dt: datetime,
    session_id: str,
    source_path: Path,
    config: Dict[str, Any],
) -> List[CandidateMemory]:
    candidates = []
    candidates.extend(find_user_candidates(user_turns, base_dt, session_id, source_path, config))
    candidates.extend(find_feedback_candidates(user_turns, base_dt, session_id, source_path, config))
    candidates.extend(find_project_candidates(user_turns, base_dt, session_id, source_path, config))
    candidates.extend(find_reference_candidates(user_turns, assistant_turns, base_dt, session_id, source_path, config))
    deduped: List[CandidateMemory] = []
    seen: set[Tuple[str, str]] = set()
    for candidate in candidates:
        key = (candidate.memory_type, candidate.key or candidate_identity_key(candidate))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(candidate)
    return deduped


def parse_session(path: Path, workspace_root: Path, config: Dict[str, Any]) -> SessionRecord | None:
    rows = read_jsonl(path)
    if not rows:
        return None

    session_meta = rows[0]
    meta_payload = session_meta.get("payload") or {}
    cwd = meta_payload.get("cwd")
    if not isinstance(cwd, str):
        return None
    normalized_cwd = normalize_path(cwd)
    workspace_norm = normalize_path(workspace_root)
    if normalized_cwd != workspace_norm and not normalized_cwd.startswith(workspace_norm + "/"):
        return None

    session_id = meta_payload.get("id") or path.stem
    started_at = meta_payload.get("timestamp") or session_meta.get("timestamp")
    if not isinstance(started_at, str):
        started_at = datetime.now(timezone.utc).isoformat()
    started_dt = parse_iso(started_at)
    day = started_dt.date().isoformat()

    user_turns: List[str] = []
    assistant_turns: List[str] = []

    for row in rows:
        if row.get("type") != "response_item":
            continue
        payload = row.get("payload") or {}
        if payload.get("type") != "message":
            continue
        role = payload.get("role")
        text = clean_text("\n".join(_extract_text_fragments(payload.get("content"))))
        if not text:
            continue
        if role == "user":
            user_turns.append(text)
        elif role == "assistant":
            assistant_turns.append(text)

    if not user_turns:
        return None

    low_signal = is_low_signal(user_turns)
    summary = build_summary(user_turns, assistant_turns, low_signal)
    combined = [*user_turns, *assistant_turns]
    candidates = [] if low_signal else extract_candidates(user_turns, assistant_turns, started_dt, session_id, path, config)

    return SessionRecord(
        session_id=session_id,
        started_at=started_dt.isoformat(),
        day=day,
        cwd=cwd,
        path=path,
        user_turns=user_turns,
        assistant_turns=assistant_turns,
        summary=summary,
        low_signal=low_signal,
        files_changed=extract_files_changed(combined, workspace_root),
        errors=extract_errors(combined),
        decisions=extract_decisions(combined),
        quotes=extract_quotes(user_turns),
        current_goal=shorten(user_turns[-1], 180),
        candidates=candidates,
    )


def load_json(path: Path, default: Dict[str, Any]) -> Dict[str, Any]:
    if not path.exists():
        return json.loads(json.dumps(default))
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_config(workspace_home: Path) -> Dict[str, Any]:
    path = workspace_home / CONFIG_REL
    if not path.exists():
        return json.loads(json.dumps(DEFAULT_CONFIG))
    current = json.loads(path.read_text(encoding="utf-8"))
    return deep_merge(json.loads(json.dumps(DEFAULT_CONFIG)), current)


def load_global_config(memory_home: Path) -> Dict[str, Any]:
    path = memory_home / GLOBAL_CONFIG_REL
    if not path.exists():
        return json.loads(json.dumps(DEFAULT_CONFIG))
    current = json.loads(path.read_text(encoding="utf-8"))
    return deep_merge(json.loads(json.dumps(DEFAULT_CONFIG)), current)


def update_workspace_index(memory_home: Path, workspace_root: Path) -> None:
    path = memory_home / WORKSPACE_INDEX_REL
    current = load_json(path, {"version": 1, "workspaces": {}})
    workspaces = current.setdefault("workspaces", {})
    normalized = normalize_path(workspace_root)
    workspaces[normalized] = {
        "key": workspace_key(workspace_root),
        "path": clean_path_preserve_case(workspace_root),
    }
    save_json(path, current)


def scaffold(memory_home: Path, workspace_root: Path, config: Dict[str, Any]) -> Path:
    for scope in ("company", "user", "local"):
        path = memory_home / INSTRUCTIONS_REL / scope
        path.mkdir(parents=True, exist_ok=True)
        guide = path / INSTRUCTION_FILE_NAME
        if not guide.exists():
            guide.write_text(INSTRUCTION_TEMPLATES[scope], encoding="utf-8")

    for memory_type in GLOBAL_MEMORY_TYPES:
        (memory_home / GLOBAL_CANDIDATES_REL / memory_type).mkdir(parents=True, exist_ok=True)
        (memory_home / GLOBAL_CANDIDATES_ARCHIVE_REL / memory_type).mkdir(parents=True, exist_ok=True)
        (memory_home / GLOBAL_MEMORIES_REL / memory_type).mkdir(parents=True, exist_ok=True)
    for path in (
        memory_home / GLOBAL_RUNTIME_REL,
        memory_home / GLOBAL_CONFLICTS_OPEN_REL,
        memory_home / GLOBAL_CONFLICTS_RESOLVED_REL,
        memory_home / GLOBAL_CONFLICTS_ARCHIVED_REL,
        memory_home / GLOBAL_DREAM_REPORTS_REL,
    ):
        path.mkdir(parents=True, exist_ok=True)
    save_json(memory_home / GLOBAL_CONFIG_REL, load_json(memory_home / GLOBAL_CONFIG_REL, json.loads(json.dumps(DEFAULT_CONFIG))))
    save_json(memory_home / GLOBAL_REGISTRY_REL, load_json(memory_home / GLOBAL_REGISTRY_REL, {"version": 1, "promoted_clusters": {}}))
    save_json(
        memory_home / GLOBAL_DREAM_STATE_REL,
        load_json(
            memory_home / GLOBAL_DREAM_STATE_REL,
            {
                "version": 1,
                "last_dream_at": None,
                "workspaces_since_last_dream": 0,
                "last_report": None,
                "dream_count": 0,
            },
        ),
    )
    global_index = memory_home / GLOBAL_MEMORY_INDEX_REL
    if not global_index.exists():
        global_index.write_text("# MEMORY\n\nShort index of active global memories.\n", encoding="utf-8")
    global_context = memory_home / GLOBAL_CONTEXT_REL
    if not global_context.exists():
        global_context.write_text("# Global Context\n\n## User Defaults\n- None\n", encoding="utf-8")

    workspace_home = workspace_memory_home(memory_home, workspace_root)
    repo_path = workspace_home / INSTRUCTIONS_REL / "repo"
    repo_path.mkdir(parents=True, exist_ok=True)
    repo_guide = repo_path / INSTRUCTION_FILE_NAME
    if not repo_guide.exists():
        repo_guide.write_text(INSTRUCTION_TEMPLATES["repo"], encoding="utf-8")

    for memory_type in MEMORY_TYPES:
        (workspace_home / CANDIDATES_REL / memory_type).mkdir(parents=True, exist_ok=True)
        (workspace_home / MEMORIES_REL / memory_type).mkdir(parents=True, exist_ok=True)

    for path in (
        workspace_home / RUNTIME_REL / "compression" / "archive",
        workspace_home / DREAM_REL / "reports",
    ):
        path.mkdir(parents=True, exist_ok=True)

    save_json(workspace_home / CONFIG_REL, config)
    save_json(workspace_home / REGISTRY_REL, load_json(workspace_home / REGISTRY_REL, {"version": 1, "processed_sessions": {}}))
    save_json(
        workspace_home / DREAM_STATE_REL,
        load_json(
            workspace_home / DREAM_STATE_REL,
            {
                "version": 1,
                "last_dream_at": None,
                "sessions_since_last_dream": 0,
                "last_report": None,
                "dream_count": 0,
            },
        ),
    )
    update_workspace_index(memory_home, workspace_root)
    (memory_home / RUNS_REL / workspace_key(workspace_root)).mkdir(parents=True, exist_ok=True)
    return workspace_home


def render_run_summary(record: SessionRecord) -> str:
    lines = [
        "# Run Summary",
        "",
        f"- Session ID: {record.session_id}",
        f"- Started At: {record.started_at}",
        "",
        "## Summary",
        "",
        record.summary,
        "",
        "## Goal",
        "",
        f"> {record.current_goal}",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def render_run_handoff(record: SessionRecord) -> str:
    lines = [
        "# Handoff",
        "",
        "## Current Goal",
        "",
        record.current_goal,
        "",
        "## Done",
        "",
        f"- {record.summary}",
        "",
        "## Next",
        "",
        "- Review extracted observations and promote durable items.",
        "",
        "## Risks",
        "",
    ]
    lines.extend([f"- {item}" for item in record.errors] or ["- None"])
    return "\n".join(lines).rstrip() + "\n"


def write_run_artifacts(memory_home: Path, workspace_root: Path, record: SessionRecord) -> None:
    run_root = memory_home / RUNS_REL / workspace_key(workspace_root) / record.session_id
    run_root.mkdir(parents=True, exist_ok=True)
    save_json(
        run_root / "status.json",
        {
            "run_id": record.session_id,
            "workspace_key": workspace_key(workspace_root),
            "status": "active",
            "created_at": record.started_at,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "goal": record.current_goal,
            "promoted_to_workspace": any(candidate.auto_promote for candidate in record.candidates),
            "archived": False,
        },
    )
    (run_root / "summary.md").write_text(render_run_summary(record), encoding="utf-8")
    (run_root / "scratch.md").write_text("# Scratch\n\n- Temporary execution notes belong here.\n", encoding="utf-8")
    (run_root / "handoff.md").write_text(render_run_handoff(record), encoding="utf-8")
    save_json(
        run_root / "extracted.json",
        {
            "session_id": record.session_id,
            "files_changed": record.files_changed,
            "errors": record.errors,
            "decisions": record.decisions,
            "quotes": record.quotes,
            "candidate_keys": [candidate.key or candidate_identity_key(candidate) for candidate in record.candidates],
        },
    )


def find_existing_memory_path(collection_root: Path, candidate: CandidateMemory) -> Path | None:
    key = candidate.key or candidate_identity_key(candidate)
    typed_root = collection_root / candidate.memory_type
    matches = sorted(typed_root.glob(f"*-{key}-*.md"))
    if matches:
        return matches[-1]
    candidate_primary = primary_section_text(candidate.memory_type, candidate.sections)
    for path in sorted(typed_root.glob("*.md")):
        existing = parse_memory_file(path)
        if existing.metadata.get("key") == key:
            return path
        if primary_section_text(candidate.memory_type, existing.sections) == candidate_primary:
            return path
    return None


def build_memory_path(collection_root: Path, candidate: CandidateMemory) -> Path:
    existing = find_existing_memory_path(collection_root, candidate)
    if existing is not None:
        return existing
    slug = slugify(candidate.title)
    key = candidate.key or candidate_identity_key(candidate)
    date = candidate.created_at[:10]
    return collection_root / candidate.memory_type / f"{date}-{key}-{slug}.md"


def render_memory(candidate: CandidateMemory, status: str, existing_created_at: str | None = None) -> str:
    slug = slugify(candidate.title)
    created_at = existing_created_at or candidate.created_at
    key = candidate.key or candidate_identity_key(candidate)
    metadata = {
        "id": f"{candidate.memory_type}-{created_at[:10]}-{key}",
        "key": key,
        "scope": candidate.scope,
        "type": candidate.memory_type,
        "created_at": created_at,
        "last_confirmed_at": candidate.last_confirmed_at,
        "status": status,
        "confidence": f"{candidate.confidence:.2f}",
        "source_runs": metadata_list_value(candidate.source_runs),
        "source_workspaces": metadata_list_value(candidate.source_workspaces),
    }
    if candidate.source_url:
        metadata["source"] = candidate.source_url

    lines = ["---"]
    for key, value in metadata.items():
        lines.append(f"{key}: {value}")
    lines.extend(["---", f"# {candidate.title}", ""])
    for section_name in SECTION_KEYS[candidate.memory_type]:
        lines.append(f"## {section_name}")
        lines.append(candidate.sections[section_name])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_memory_file(path: Path) -> MemoryFile:
    text = path.read_text(encoding="utf-8")
    metadata: Dict[str, str] = {}
    body = text
    if text.startswith("---\n"):
        try:
            _, raw_meta, body = text.split("---\n", 2)
            for line in raw_meta.splitlines():
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()
        except ValueError:
            body = text

    title = path.stem
    sections: Dict[str, str] = {}
    current_section = None
    buffer: List[str] = []
    for line in body.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            if current_section is not None:
                sections[current_section] = "\n".join(buffer).strip()
            current_section = line[3:].strip()
            buffer = []
            continue
        if current_section is not None:
            buffer.append(line)
    if current_section is not None:
        sections[current_section] = "\n".join(buffer).strip()
    return MemoryFile(path=path, metadata=metadata, title=title, sections=sections)


def render_memory_file(item: MemoryFile) -> str:
    lines = ["---"]
    for key, value in item.metadata.items():
        lines.append(f"{key}: {value}")
    lines.extend(["---", f"# {item.title}", ""])
    ordered_sections = SECTION_KEYS.get(item.metadata.get("type", ""), tuple(item.sections.keys()))
    emitted: set[str] = set()
    for section_name in ordered_sections:
        if section_name not in item.sections:
            continue
        lines.extend([f"## {section_name}", item.sections[section_name], ""])
        emitted.add(section_name)
    for section_name, value in item.sections.items():
        if section_name in emitted:
            continue
        lines.extend([f"## {section_name}", value, ""])
    return "\n".join(lines).rstrip() + "\n"


def load_memory_files(memory_root: Path) -> List[MemoryFile]:
    files: List[MemoryFile] = []
    for memory_type in MEMORY_TYPES:
        for path in sorted((memory_root / memory_type).glob("*.md")):
            files.append(parse_memory_file(path))
    return files


def write_memory_set(collection_root: Path, items: Sequence[CandidateMemory], *, status: str) -> Dict[str, List[str]]:
    created: List[str] = []
    updated: List[str] = []
    for candidate in items:
        candidate.key = candidate.key or candidate_identity_key(candidate)
        target = build_memory_path(collection_root, candidate)
        existing_created_at = None
        if target.exists():
            existing = parse_memory_file(target)
            existing_created_at = existing.metadata.get("created_at")
            updated.append(str(target))
        else:
            created.append(str(target))
        target.write_text(render_memory(candidate, status=status, existing_created_at=existing_created_at), encoding="utf-8")
    return {"created": created, "updated": updated}


def build_memory_index_file(memory_root: Path, output_path: Path, config: Dict[str, Any], memory_types: Sequence[str], *, title: str) -> int:
    files = [item for item in load_memory_files(memory_root) if item.metadata.get("status", "active") == "active"]
    type_order = {memory_type: index for index, memory_type in enumerate(memory_types)}
    files.sort(key=lambda item: (type_order.get(item.metadata.get("type", ""), 99), item.metadata.get("last_confirmed_at", "")))
    groups: Dict[str, List[MemoryFile]] = {memory_type: [] for memory_type in memory_types}
    for item in sorted(files, key=lambda entry: entry.metadata.get("last_confirmed_at", ""), reverse=True):
        memory_type = item.metadata.get("type", "")
        if memory_type in groups:
            groups[memory_type].append(item)
    max_lines = int(config["index_max_lines"])
    max_chars = int(config["index_max_chars_per_entry"])
    lines = ["# MEMORY", "", title, ""]
    used_lines = len(lines)
    for memory_type in memory_types:
        items = groups[memory_type]
        if not items:
            continue
        section_header = f"## {memory_type.capitalize()}"
        if used_lines + 3 > max_lines:
            break
        lines.extend([section_header, ""])
        used_lines += 2
        for item in items:
            summary = ""
            for section_name in SECTION_KEYS[memory_type]:
                value = item.sections.get(section_name, "").strip()
                if value:
                    summary = value
                    break
            rel_path = item.path.relative_to(memory_root)
            entry = f"- [{memory_type}] {shorten(summary or item.title, max_chars)} ({rel_path.as_posix()})"
            if used_lines + 1 > max_lines:
                break
            lines.append(entry)
            used_lines += 1
        if used_lines + 1 > max_lines:
            break
        lines.append("")
        used_lines += 1
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return len(lines)


def build_memory_index(workspace_home: Path, config: Dict[str, Any]) -> int:
    return build_memory_index_file(
        workspace_home / MEMORIES_REL,
        workspace_home / MEMORY_INDEX_REL,
        config,
        ("feedback", "project", "reference", "open_loop"),
        title="Short index of active workspace memories.",
    )


def build_global_memory_index(memory_home: Path, config: Dict[str, Any]) -> int:
    return build_memory_index_file(
        memory_home / GLOBAL_MEMORIES_REL,
        memory_home / GLOBAL_MEMORY_INDEX_REL,
        config,
        ("user", "feedback", "reference"),
        title="Short index of active global memories.",
    )


def select_recent_sessions(records: Sequence[SessionRecord], config: Dict[str, Any]) -> List[SessionRecord]:
    limit = int(config["compression"]["recent_session_limit"])
    ordered = sorted(records, key=lambda item: item.started_at, reverse=True)
    return ordered[:limit]


def select_focus_sessions(records: Sequence[SessionRecord], config: Dict[str, Any]) -> List[SessionRecord]:
    limit = int(config["runtime"]["focus_session_limit"])
    ordered = sorted(records, key=lambda item: item.started_at, reverse=True)
    return ordered[:limit]


def select_compression_level(raw_tokens: int, config: Dict[str, Any]) -> str:
    trigger = int(config["context_window_tokens"]) - int(config["reserve_tokens"])
    if trigger <= 0:
        return "full"
    if raw_tokens <= trigger * 0.6:
        return "micro"
    if raw_tokens <= trigger:
        return "automatic"
    return "full"


def build_runtime_context(workspace_home: Path, recent_records: Sequence[SessionRecord], config: Dict[str, Any]) -> str:
    feedback_files = [
        item
        for item in load_memory_files(workspace_home / MEMORIES_REL)
        if item.metadata.get("type") == "feedback" and item.metadata.get("status", "active") == "active"
    ]
    feedback_files.sort(key=lambda item: item.metadata.get("last_confirmed_at", ""), reverse=True)

    raw_text = "\n".join(
        [record.summary for record in recent_records]
        + [quote for record in recent_records for quote in record.quotes]
        + [item.sections.get("Rule", "") for item in feedback_files]
    )
    level = select_compression_level(estimate_tokens(raw_text), config)
    if level == "micro":
        file_limit, error_limit, decision_limit, feedback_limit, quote_limit = 10, 6, 6, 6, int(config["compression"]["quote_limit"])
    elif level == "automatic":
        file_limit, error_limit, decision_limit, feedback_limit, quote_limit = 6, 5, 5, 5, max(1, int(config["compression"]["quote_limit"]) - 1)
    else:
        file_limit, error_limit, decision_limit, feedback_limit, quote_limit = 4, 4, 4, 4, 1

    focus_records = select_focus_sessions(recent_records, config)
    latest = focus_records[0] if focus_records else (recent_records[0] if recent_records else None)
    current_goal = latest.current_goal if latest else "No recent active goal."
    files_changed = list_unique((path for record in focus_records for path in record.files_changed), file_limit)
    errors = list_unique((item for record in focus_records for item in record.errors), error_limit)
    decisions = list_unique((item for record in focus_records for item in record.decisions), decision_limit)
    feedback = list_unique((item.sections.get("Rule", "") for item in feedback_files if item.sections.get("Rule")), feedback_limit)
    quotes = list_unique((quote for record in focus_records for quote in record.quotes), quote_limit)
    remaining = [latest.summary] if latest else ["No remaining work captured yet."]

    lines = [
        "# Compressed Context",
        "",
        f"- Compression level: `{level}`",
        "",
        "## Current Goal",
        "",
        f"> {current_goal}",
        "",
        "## Confirmed Feedback",
        "",
    ]
    lines.extend([f"- {item}" for item in feedback] or ["- None"])
    lines.extend(["", "## Files Changed", ""])
    lines.extend([f"- {item}" for item in files_changed] or ["- None"])
    lines.extend(["", "## Errors Encountered", ""])
    lines.extend([f"- {item}" for item in errors] or ["- None"])
    lines.extend(["", "## Decisions Made", ""])
    lines.extend([f"- {item}" for item in decisions] or ["- None"])
    lines.extend(["", "## Remaining Work", ""])
    lines.extend([f"- {item}" for item in remaining] or ["- None"])
    lines.extend(["", "## Important Quotes", ""])
    lines.extend([f"> {item}" for item in quotes] or ["> None"])
    return "\n".join(lines).rstrip() + "\n"


def write_runtime_context(workspace_home: Path, text: str) -> None:
    active_path = workspace_home / ACTIVE_CONTEXT_REL
    latest_path = workspace_home / LATEST_COMPRESSION_REL
    active_path.parent.mkdir(parents=True, exist_ok=True)
    latest_path.parent.mkdir(parents=True, exist_ok=True)
    if latest_path.exists():
        existing = latest_path.read_text(encoding="utf-8")
        if existing != text:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            archive_path = workspace_home / COMPRESSION_ARCHIVE_REL / f"{stamp}.md"
            archive_path.write_text(existing, encoding="utf-8")
    active_path.write_text(text, encoding="utf-8")
    latest_path.write_text(text, encoding="utf-8")


def load_candidate_files(candidate_root: Path) -> List[MemoryFile]:
    files: List[MemoryFile] = []
    for memory_type in MEMORY_TYPES:
        typed_root = candidate_root / memory_type
        if not typed_root.exists():
            continue
        for path in sorted(typed_root.glob("*.md")):
            files.append(parse_memory_file(path))
    return files


def memory_primary_text(item: MemoryFile) -> str:
    memory_type = item.metadata.get("type", "")
    if memory_type in SECTION_KEYS:
        return primary_section_text(memory_type, item.sections)
    return clean_text(item.title)


def build_global_memory_from_group(
    memory_type: str,
    primary_text: str,
    items: Sequence[Tuple[str, MemoryFile]],
    score: float,
) -> CandidateMemory:
    source_runs = sorted({run_id for _, item in items for run_id in item_origin_runs(item)})
    source_workspaces = sorted({origin for workspace_key_value, item in items for origin in item_origin_workspaces(workspace_key_value, item)})
    exemplar = max(items, key=lambda pair: parse_confidence_value(pair[1].metadata))[1]
    if memory_type == "user":
        sections = {
            "Fact": primary_text,
            "Why it matters": "This user preference appears durable across work and is suitable for global defaults.",
            "How to use": "Use it as a cross-workspace default unless a workspace explicitly overrides it.",
            "Evidence": f"Derived from {len(source_workspaces)} workspace(s): {', '.join(source_workspaces)}",
        }
    elif memory_type == "feedback":
        sections = {
            "Rule": primary_text,
            "Why": "This rule was confirmed strongly enough to act as a cross-workspace default.",
            "How to apply": "Apply by default unless the active workspace defines a narrower override.",
            "Evidence": f"Derived from {len(source_workspaces)} workspace(s): {', '.join(source_workspaces)}",
        }
    else:
        sections = {
            "Reference takeaway": primary_text,
            "Why it matters": "This conclusion appears reusable across workspaces.",
            "How to reuse": "Reuse it when a similar design or implementation problem appears in another workspace.",
            "Source": exemplar.metadata.get("source", "workspace-derived"),
        }
    candidate = CandidateMemory(
        scope="global",
        memory_type=memory_type,
        title=shorten(primary_text, 70),
        sections=sections,
        created_at=datetime.now(timezone.utc).isoformat(),
        last_confirmed_at=max((item.metadata.get("last_confirmed_at", "") for _, item in items), default=datetime.now(timezone.utc).isoformat()),
        source_session_id=source_runs[0] if source_runs else "global-dream",
        source_path=str(exemplar.path),
        source_url=exemplar.metadata.get("source"),
        confidence=max(0.0, min(score, 1.0)),
        auto_promote=False,
        source_runs=source_runs,
        source_workspaces=source_workspaces,
    )
    candidate.key = candidate_identity_key(candidate)
    return candidate


def global_cluster_score(memory_type: str, primary_text: str, items: Sequence[Tuple[str, MemoryFile]]) -> float:
    base = max((parse_confidence_value(item.metadata) for _, item in items), default=0.0)
    workspace_count = len({origin for workspace_key_value, item in items for origin in item_origin_workspaces(workspace_key_value, item)})
    score = base
    if memory_type == "user":
        score += 0.2
    if explicit_global_signal(primary_text):
        score += 0.25
    if workspace_count >= 2:
        score += 0.2
    if workspace_count >= 3:
        score += 0.1
    if workspace_count < 2 and memory_type in {"feedback", "reference"} and not explicit_global_signal(primary_text):
        score -= 0.2
    if is_project_specific_text(primary_text):
        score -= 0.35
    return max(0.0, min(score, 1.0))


def render_conflict_item(
    conflict_id: str,
    memory_type: str,
    topic_key: str,
    groups: Sequence[Tuple[str, Sequence[Tuple[str, MemoryFile]]]],
) -> str:
    workspace_keys = sorted(
        {
            origin
            for _, items in groups
            for workspace_key_value, item in items
            for origin in item_origin_workspaces(workspace_key_value, item)
        }
    )
    candidate_ids = [item.metadata.get("id", item.path.stem) for _, items in groups for _, item in items]
    lines = [
        "---",
        f"id: {conflict_id}",
        "status: open",
        f"type: {memory_type}",
        f"created_at: {datetime.now(timezone.utc).isoformat()}",
        f"updated_at: {datetime.now(timezone.utc).isoformat()}",
        f"candidate_ids: {metadata_list_value(candidate_ids)}",
        f"workspace_keys: {metadata_list_value(workspace_keys)}",
        "resolution_mode: pending",
        "---",
        f"# Conflict: {shorten(topic_key, 80)}",
        "",
        "## Conflict",
        "",
    ]
    for polarity_value, items in groups:
        examples = [memory_primary_text(item) for _, item in items][:2]
        lines.append(f"- {polarity_value}: {' | '.join(examples)}")
    lines.extend(
        [
            "",
            "## Why It Is In Queue",
            "",
            "Multiple candidate truths disagree on a potentially global rule, so promotion is blocked until resolution.",
            "",
            "## Proposed Resolution",
            "",
            "- scope_split",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def rebuild_global_conflicts(
    memory_home: Path,
    eligible_groups: Dict[Tuple[str, str], Sequence[Tuple[str, MemoryFile]]],
    scores: Dict[Tuple[str, str], float],
) -> Tuple[set[Tuple[str, str]], List[str]]:
    conflicts_dir = memory_home / GLOBAL_CONFLICTS_OPEN_REL
    conflicts_dir.mkdir(parents=True, exist_ok=True)
    blocked: set[Tuple[str, str]] = set()
    created: List[str] = []
    existing = {path.stem: path for path in conflicts_dir.glob("*.md")}
    topic_groups: Dict[Tuple[str, str], Dict[str, List[Tuple[str, MemoryFile]]]] = {}
    topic_blocked: Dict[Tuple[str, str], set[Tuple[str, str]]] = {}
    for (memory_type, primary_text), items in eligible_groups.items():
        if scores.get((memory_type, primary_text), 0.0) < 0.70:
            continue
        topic_key = conflict_topic_key(primary_text)
        polarity_value = conflict_polarity(primary_text)
        topic_groups.setdefault((memory_type, topic_key), {}).setdefault(polarity_value, []).extend(items)
        topic_blocked.setdefault((memory_type, topic_key), set()).add((memory_type, primary_text))

    active_conflict_ids: set[str] = set()
    for (memory_type, topic_key), grouped in topic_groups.items():
        if len(grouped) < 2:
            continue
        conflict_id = f"conflict-{hashlib.sha1(f'{memory_type}|{topic_key}'.encode('utf-8')).hexdigest()[:12]}"
        active_conflict_ids.add(conflict_id)
        path = conflicts_dir / f"{conflict_id}.md"
        render_groups = sorted(grouped.items(), key=lambda item: item[0])
        path.write_text(render_conflict_item(conflict_id, memory_type, topic_key, render_groups), encoding="utf-8")
        created.append(str(path))
        blocked.update(topic_blocked.get((memory_type, topic_key), set()))

    resolved_dir = memory_home / GLOBAL_CONFLICTS_RESOLVED_REL
    resolved_dir.mkdir(parents=True, exist_ok=True)
    for conflict_id, path in existing.items():
        if conflict_id in active_conflict_ids:
            continue
        target = resolved_dir / path.name
        if target.exists():
            target.unlink()
        path.replace(target)
    return blocked, created


def build_global_context(memory_home: Path) -> str:
    files = [item for item in load_memory_files(memory_home / GLOBAL_MEMORIES_REL) if item.metadata.get("status", "active") == "active"]
    files.sort(key=lambda item: item.metadata.get("last_confirmed_at", ""), reverse=True)
    groups: Dict[str, List[str]] = {"user": [], "feedback": [], "reference": []}
    for item in files:
        memory_type = item.metadata.get("type", "")
        primary = memory_primary_text(item)
        if memory_type in groups and primary:
            groups[memory_type].append(shorten(primary, 140))
    conflict_titles = [parse_memory_file(path).title for path in sorted((memory_home / GLOBAL_CONFLICTS_OPEN_REL).glob("*.md"))[:2]]
    lines = [
        "# Global Context",
        "",
        "## User Defaults",
        "",
    ]
    lines.extend([f"- {item}" for item in groups["user"][:4]] or ["- None"])
    lines.extend(["", "## Confirmed Global Feedback", ""])
    lines.extend([f"- {item}" for item in groups["feedback"][:4]] or ["- None"])
    lines.extend(["", "## Reusable References", ""])
    lines.extend([f"- {item}" for item in groups["reference"][:4]] or ["- None"])
    lines.extend(["", "## Open Global Decisions", ""])
    lines.extend([f"- {item}" for item in conflict_titles] or ["- None"])
    lines.extend(["", "## Last Updated", "", f"- {datetime.now(timezone.utc).date().isoformat()}"])
    return "\n".join(lines).rstrip() + "\n"


def write_global_context(memory_home: Path, text: str) -> None:
    path = memory_home / GLOBAL_CONTEXT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_global_registry(memory_home: Path) -> Dict[str, Any]:
    return load_json(memory_home / GLOBAL_REGISTRY_REL, {"version": 1, "promoted_clusters": {}})


def write_global_registry(memory_home: Path, payload: Dict[str, Any]) -> None:
    save_json(memory_home / GLOBAL_REGISTRY_REL, payload)


def load_global_dream_state(memory_home: Path) -> Dict[str, Any]:
    return load_json(
        memory_home / GLOBAL_DREAM_STATE_REL,
        {
            "version": 1,
            "last_dream_at": None,
            "workspaces_since_last_dream": 0,
            "last_report": None,
            "dream_count": 0,
        },
    )


def save_global_dream_state(memory_home: Path, payload: Dict[str, Any]) -> None:
    save_json(memory_home / GLOBAL_DREAM_STATE_REL, payload)


def archive_memory_file(path: Path, archive_root: Path, reason: str) -> str:
    item = parse_memory_file(path)
    item.metadata["status"] = "archived"
    item.metadata["archived_at"] = datetime.now(timezone.utc).isoformat()
    item.metadata["archive_reason"] = reason
    target_dir = archive_root / (item.metadata.get("type") or path.parent.name)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / path.name
    if target.exists():
        target.unlink()
    target.write_text(render_memory_file(item), encoding="utf-8")
    path.unlink()
    return str(target)


def migrate_existing_metadata(memory_home: Path) -> Dict[str, int]:
    workspace_groups: Dict[Tuple[str, str, str], List[Tuple[str, MemoryFile]]] = {}
    for workspace_key_value, workspace_path in workspace_nodes(memory_home):
        for root_rel in (CANDIDATES_REL, MEMORIES_REL):
            for memory_type in MEMORY_TYPES:
                typed_root = workspace_path / root_rel / memory_type
                if not typed_root.exists():
                    continue
                for path in sorted(typed_root.glob("*.md")):
                    item = parse_memory_file(path)
                    inferred_type = item.metadata.get("type") or memory_type
                    item.metadata.setdefault("type", inferred_type)
                    key = item.metadata.get("key") or memory_file_identity_key(item)
                    primary = primary_section_text(inferred_type, item.sections) if inferred_type in SECTION_KEYS else clean_text(item.title)
                    workspace_groups.setdefault((inferred_type, key, primary), []).append((workspace_key_value, item))

    workspace_updates = 0
    for records in workspace_groups.values():
        existing_origins = sorted(
            {
                origin
                for workspace_key_value, item in records
                for origin in parse_metadata_list(item.metadata.get("source_workspaces"))
            }
        )
        if existing_origins:
            resolved_origins = existing_origins
        else:
            canonical_workspace = min(
                records,
                key=lambda pair: (pair[1].metadata.get("created_at", "9999-12-31T23:59:59+00:00"), pair[0]),
            )[0]
            resolved_origins = [canonical_workspace]
        for workspace_key_value, item in records:
            before = dict(item.metadata)
            memory_type = item.metadata.get("type") or item.path.parent.name
            item.metadata.setdefault("scope", "workspace")
            item.metadata.setdefault("type", memory_type)
            item.metadata.setdefault("key", memory_file_identity_key(item))
            if not parse_metadata_list(item.metadata.get("source_workspaces")):
                item.metadata["source_workspaces"] = metadata_list_value(resolved_origins)
            if not parse_metadata_list(item.metadata.get("source_runs")):
                item.metadata["source_runs"] = metadata_list_value([item.metadata.get("id", item.path.stem)])
            if item.metadata != before:
                item.path.write_text(render_memory_file(item), encoding="utf-8")
                workspace_updates += 1

    global_updates = 0
    for root_rel in (GLOBAL_CANDIDATES_REL, GLOBAL_MEMORIES_REL):
        for memory_type in GLOBAL_MEMORY_TYPES:
            typed_root = memory_home / root_rel / memory_type
            if not typed_root.exists():
                continue
            for path in sorted(typed_root.glob("*.md")):
                item = parse_memory_file(path)
                before = dict(item.metadata)
                item.metadata.setdefault("scope", "global")
                item.metadata.setdefault("type", memory_type)
                item.metadata.setdefault("key", memory_file_identity_key(item))
                if "source_workspaces" not in item.metadata:
                    item.metadata["source_workspaces"] = metadata_list_value(parse_metadata_list(item.metadata.get("source_workspaces")))
                if not parse_metadata_list(item.metadata.get("source_runs")):
                    item.metadata["source_runs"] = metadata_list_value([item.metadata.get("id", item.path.stem)])
                if item.metadata != before:
                    item.path.write_text(render_memory_file(item), encoding="utf-8")
                    global_updates += 1
    return {"workspace_updates": workspace_updates, "global_updates": global_updates}


def candidate_sort_key(item: MemoryFile) -> Tuple[float, str, str]:
    return (
        parse_confidence_value(item.metadata),
        item.metadata.get("last_confirmed_at", ""),
        item.metadata.get("created_at", ""),
    )


def govern_global_candidates(memory_home: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    settings = config.get("candidate_governance", {}).get("global", {})
    max_per_type = int(settings.get("max_per_type", 50))
    archive_after_days = int(settings.get("archive_after_days", 30))
    keep_per_key = int(settings.get("keep_per_key", 1))
    archive_root = memory_home / GLOBAL_CANDIDATES_ARCHIVE_REL
    active_keys = {
        item.metadata.get("key") or memory_file_identity_key(item)
        for item in load_memory_files(memory_home / GLOBAL_MEMORIES_REL)
        if item.metadata.get("status", "active") == "active"
    }
    archived: List[str] = []
    now = datetime.now(timezone.utc)

    for memory_type in GLOBAL_MEMORY_TYPES:
        typed_root = memory_home / GLOBAL_CANDIDATES_REL / memory_type
        if not typed_root.exists():
            continue
        groups: Dict[str, List[MemoryFile]] = {}
        for path in sorted(typed_root.glob("*.md")):
            item = parse_memory_file(path)
            key = item.metadata.get("key") or memory_file_identity_key(item)
            groups.setdefault(key, []).append(item)

        retained: List[MemoryFile] = []
        for key, items in groups.items():
            items.sort(key=candidate_sort_key, reverse=True)
            allowed = 0 if key in active_keys else keep_per_key
            for index, item in enumerate(items):
                if index >= allowed:
                    reason = "promoted" if key in active_keys else "duplicate"
                    archived.append(archive_memory_file(item.path, archive_root, reason))
                    continue
                retained.append(item)

        fresh: List[MemoryFile] = []
        for item in retained:
            timestamp = item.metadata.get("last_confirmed_at") or item.metadata.get("created_at")
            expired = False
            if timestamp:
                try:
                    expired = now - parse_iso(timestamp) >= timedelta(days=archive_after_days)
                except ValueError:
                    expired = False
            if expired:
                archived.append(archive_memory_file(item.path, archive_root, "expired"))
                continue
            fresh.append(item)

        fresh.sort(key=candidate_sort_key, reverse=True)
        for item in fresh[max_per_type:]:
            archived.append(archive_memory_file(item.path, archive_root, "overflow"))

    return {"archived": archived}


def run_global_dream(memory_home: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    eligible_groups: Dict[Tuple[str, str], List[Tuple[str, MemoryFile]]] = {}
    for workspace_key_value, workspace_path in workspace_nodes(memory_home):
        for item in load_candidate_files(workspace_path / CANDIDATES_REL):
            memory_type = item.metadata.get("type", "")
            if memory_type not in GLOBAL_MEMORY_TYPES:
                continue
            primary = memory_primary_text(item)
            if not primary:
                continue
            eligible_groups.setdefault((memory_type, primary), []).append((workspace_key_value, item))
        for item in load_memory_files(workspace_path / MEMORIES_REL):
            memory_type = item.metadata.get("type", "")
            if memory_type not in GLOBAL_MEMORY_TYPES:
                continue
            if item.metadata.get("status", "active") != "active":
                continue
            primary = memory_primary_text(item)
            if not primary:
                continue
            eligible_groups.setdefault((memory_type, primary), []).append((workspace_key_value, item))

    scores = {key: global_cluster_score(key[0], key[1], items) for key, items in eligible_groups.items()}
    blocked, conflicts = rebuild_global_conflicts(memory_home, eligible_groups, scores)
    candidates: List[CandidateMemory] = []
    promoted: List[CandidateMemory] = []
    for (memory_type, primary_text), items in eligible_groups.items():
        score = scores[(memory_type, primary_text)]
        origin_workspace_count = len({origin for workspace_key_value, item in items for origin in item_origin_workspaces(workspace_key_value, item)})
        explicit_global = explicit_global_signal(primary_text)
        reference_ok = memory_type != "reference" or (
            origin_workspace_count >= 2
            and not ASSISTANT_META_RE.search(primary_text)
            and not REFERENCE_META_EXCLUSION_RE.search(primary_text)
        )
        if (memory_type, primary_text) in blocked:
            continue
        candidate = build_global_memory_from_group(memory_type, primary_text, items, score)
        allow_candidate = (memory_type == "user" or explicit_global or origin_workspace_count >= 2) and reference_ok
        if memory_type == "user":
            allow_promote = score >= 0.85
        elif memory_type == "reference":
            allow_promote = origin_workspace_count >= 3 and reference_ok and score >= 0.90
        elif explicit_global:
            allow_promote = score >= 0.82
        else:
            allow_promote = origin_workspace_count >= 2 and score >= 0.88
        if score >= 0.70 and allow_candidate and not allow_promote:
            candidates.append(candidate)
        if allow_promote:
            promoted.append(candidate)

    candidate_results = write_memory_set(memory_home / GLOBAL_CANDIDATES_REL, candidates, status="candidate")
    promoted_results = write_memory_set(memory_home / GLOBAL_MEMORIES_REL, promoted, status="active")
    candidate_governance = govern_global_candidates(memory_home, config)
    promoted_keys = {candidate.key or candidate_identity_key(candidate) for candidate in promoted}
    stale: List[str] = []
    for item in load_memory_files(memory_home / GLOBAL_MEMORIES_REL):
        if item.metadata.get("status", "active") != "active":
            continue
        if item.metadata.get("type", "") not in GLOBAL_MEMORY_TYPES:
            continue
        if (item.metadata.get("key") or slugify(item.title)) in promoted_keys:
            continue
        mark_status(item.path, "stale")
        stale.append(str(item.path))
    index_lines = build_global_memory_index(memory_home, config)
    write_global_context(memory_home, build_global_context(memory_home))
    now = datetime.now(timezone.utc)
    report_path = memory_home / GLOBAL_DREAM_REPORTS_REL / f"{now.strftime('%Y%m%dT%H%M%SZ')}.md"
    report_lines = [
        "# Global Dream Report",
        "",
        f"- Run at: {now.isoformat()}",
        f"- Candidate writes: {len(candidate_results['created']) + len(candidate_results['updated'])}",
        f"- Candidate archives: {len(candidate_governance['archived'])}",
        f"- Promoted writes: {len(promoted_results['created']) + len(promoted_results['updated'])}",
        f"- Stale global memories: {len(stale)}",
        f"- Conflicts open: {len(conflicts)}",
        f"- MEMORY.md line count: {index_lines}",
        "",
        "## Candidate Archives",
        "",
    ]
    report_lines.extend([f"- {item}" for item in candidate_governance["archived"]] or ["- None"])
    report_lines.extend([
        "",
        "## Promoted",
        "",
    ])
    report_lines.extend([f"- {item}" for item in promoted_results["created"] + promoted_results["updated"]] or ["- None"])
    report_lines.extend(["", "## Stale", ""])
    report_lines.extend([f"- {item}" for item in stale] or ["- None"])
    report_lines.extend(["", "## Conflicts", ""])
    report_lines.extend([f"- {item}" for item in conflicts] or ["- None"])
    report_path.write_text("\n".join(report_lines).rstrip() + "\n", encoding="utf-8")
    return {
        "ran": True,
        "report_path": str(report_path),
        "candidate_writes": len(candidate_results["created"]) + len(candidate_results["updated"]),
        "promoted_writes": len(promoted_results["created"]) + len(promoted_results["updated"]),
        "candidate_archived": candidate_governance["archived"],
        "stale": stale,
        "conflicts": conflicts,
        "index_lines": index_lines,
    }


def write_registry(workspace_home: Path, payload: Dict[str, Any]) -> None:
    save_json(workspace_home / REGISTRY_REL, payload)


def load_registry(workspace_home: Path) -> Dict[str, Any]:
    return load_json(workspace_home / REGISTRY_REL, {"version": 1, "processed_sessions": {}})


def load_dream_state(workspace_home: Path) -> Dict[str, Any]:
    return load_json(
        workspace_home / DREAM_STATE_REL,
        {
            "version": 1,
            "last_dream_at": None,
            "sessions_since_last_dream": 0,
            "last_report": None,
            "dream_count": 0,
        },
    )


def save_dream_state(workspace_home: Path, payload: Dict[str, Any]) -> None:
    save_json(workspace_home / DREAM_STATE_REL, payload)


def mark_status(path: Path, status: str) -> None:
    parsed = parse_memory_file(path)
    parsed.metadata["status"] = status
    metadata_lines = ["---"] + [f"{key}: {value}" for key, value in parsed.metadata.items()] + ["---", f"# {parsed.title}", ""]
    body_lines: List[str] = []
    for key, value in parsed.sections.items():
        body_lines.extend([f"## {key}", value, ""])
    path.write_text("\n".join(metadata_lines + body_lines).rstrip() + "\n", encoding="utf-8")


def should_demote_active_memory(item: MemoryFile) -> bool:
    memory_type = item.metadata.get("type", "")
    primary = primary_section_text(memory_type, item.sections) if memory_type in SECTION_KEYS else ""
    if not primary:
        return False
    if memory_type in {"project", "reference"} and looks_like_question(primary):
        return True
    if memory_type == "reference" and looks_like_reference_request(primary):
        return True
    if memory_type == "feedback" and is_task_scoped_feedback(primary) and not is_durable_feedback(primary):
        return True
    return False


def run_dream(workspace_home: Path, config: Dict[str, Any], write_results: Dict[str, List[str]]) -> Dict[str, Any]:
    memory_root = workspace_home / MEMORIES_REL
    files = [item for item in load_memory_files(memory_root) if item.metadata.get("status", "active") == "active"]
    stale: List[str] = []
    for item in files:
        if should_demote_active_memory(item):
            mark_status(item.path, "stale")
            stale.append(str(item.path))
    files = [item for item in load_memory_files(memory_root) if item.metadata.get("status", "active") == "active"]
    groups: Dict[Tuple[str, str], List[MemoryFile]] = {}
    for item in files:
        identity = item.metadata.get("key") or slugify(item.title)
        key = (item.metadata.get("type", ""), identity)
        groups.setdefault(key, []).append(item)

    superseded: List[str] = []
    for group_items in groups.values():
        if len(group_items) <= 1:
            continue
        group_items.sort(key=lambda item: item.metadata.get("last_confirmed_at", ""), reverse=True)
        for duplicate in group_items[1:]:
            mark_status(duplicate.path, "superseded")
            superseded.append(str(duplicate.path))

    index_lines = build_memory_index(workspace_home, config)
    now = datetime.now(timezone.utc)
    report_path = workspace_home / DREAM_REPORTS_REL / f"{now.strftime('%Y%m%dT%H%M%SZ')}.md"
    report_lines = [
        "# Dream Report",
        "",
        f"- Run at: {now.isoformat()}",
        f"- Created memories: {len(write_results['created'])}",
        f"- Updated memories: {len(write_results['updated'])}",
        f"- Stale memories: {len(stale)}",
        f"- Superseded memories: {len(superseded)}",
        f"- MEMORY.md line count: {index_lines}",
        "",
        "## Created",
        "",
    ]
    report_lines.extend([f"- {item}" for item in write_results["created"]] or ["- None"])
    report_lines.extend(["", "## Updated", ""])
    report_lines.extend([f"- {item}" for item in write_results["updated"]] or ["- None"])
    report_lines.extend(["", "## Stale", ""])
    report_lines.extend([f"- {item}" for item in stale] or ["- None"])
    report_lines.extend(["", "## Superseded", ""])
    report_lines.extend([f"- {item}" for item in superseded] or ["- None"])
    report_path.write_text("\n".join(report_lines).rstrip() + "\n", encoding="utf-8")
    return {
        "report_path": str(report_path),
        "stale": stale,
        "superseded": superseded,
        "index_lines": index_lines,
        "ran": True,
    }


def should_run_dream(state: Dict[str, Any], config: Dict[str, Any], processed_count: int, matching_count: int, force_dream: bool) -> bool:
    if force_dream:
        return True
    if processed_count:
        state["sessions_since_last_dream"] = int(state.get("sessions_since_last_dream", 0)) + processed_count
    min_sessions = int(config["dream"]["min_sessions_since_last"])
    if state.get("last_dream_at") is None:
        return int(state.get("sessions_since_last_dream", 0)) >= min_sessions or matching_count >= min_sessions
    last_dream = parse_iso(state["last_dream_at"])
    hours = int(config["dream"]["min_hours_since_last"])
    enough_time = datetime.now(timezone.utc) - last_dream >= timedelta(hours=hours)
    enough_sessions = int(state.get("sessions_since_last_dream", 0)) >= min_sessions
    return enough_time and enough_sessions


def should_run_global_dream(state: Dict[str, Any], config: Dict[str, Any], workspace_updates: int, force_dream: bool) -> bool:
    if force_dream:
        return True
    if workspace_updates:
        state["workspaces_since_last_dream"] = int(state.get("workspaces_since_last_dream", 0)) + workspace_updates
    settings = config.get("global_dream", {})
    min_updates = int(settings.get("min_workspace_updates_since_last", 3))
    if state.get("last_dream_at") is None:
        return int(state.get("workspaces_since_last_dream", 0)) >= min_updates
    last_dream = parse_iso(state["last_dream_at"])
    hours = int(settings.get("min_hours_since_last", 72))
    enough_time = datetime.now(timezone.utc) - last_dream >= timedelta(hours=hours)
    enough_updates = int(state.get("workspaces_since_last_dream", 0)) >= min_updates
    return enough_time and enough_updates


def main() -> int:
    args = parse_args()
    workspace_root = args.workspace_root.resolve()
    codex_home = args.codex_home.resolve()
    memory_home = args.memory_home.resolve()
    workspace_home = workspace_memory_home(memory_home, workspace_root)
    config = load_config(workspace_home)
    scaffold(memory_home, workspace_root, config)
    config = load_config(workspace_home)
    global_config = load_global_config(memory_home)
    migration_result = migrate_existing_metadata(memory_home)

    registry = load_registry(workspace_home)
    processed_sessions = registry.setdefault("processed_sessions", {})
    session_files = iter_session_files(codex_home)
    matching_files: List[Path] = []
    parsed_recent: List[SessionRecord] = []

    for session_path in session_files:
        try:
            parsed = parse_session(session_path, workspace_root, config)
        except Exception:
            continue
        if parsed is None:
            continue
        matching_files.append(session_path)
        parsed_recent.append(parsed)

    if args.limit > 0:
        matching_files = matching_files[-args.limit :]
        parsed_recent = parsed_recent[-args.limit :]

    created: List[str] = []
    updated: List[str] = []
    candidate_created: List[str] = []
    candidate_updated: List[str] = []
    processed_count = 0
    skipped_count = 0
    touched_types: set[str] = set()

    parsed_by_path = {record.path: record for record in parsed_recent}
    for session_path in matching_files:
        stat = session_path.stat()
        record_key = str(session_path)
        previous = processed_sessions.get(record_key)
        if not args.force and previous and previous.get("mtime_ns") == stat.st_mtime_ns:
            skipped_count += 1
            continue
        parsed = parsed_by_path.get(session_path)
        if parsed is None:
            continue
        workspace_origin = workspace_key(workspace_root)
        for candidate in parsed.candidates:
            candidate.source_workspaces = candidate.source_workspaces or [workspace_origin]
        write_run_artifacts(memory_home, workspace_root, parsed)
        candidate_result = write_memory_set(workspace_home / CANDIDATES_REL, parsed.candidates, status="candidate")
        promoted = [candidate for candidate in parsed.candidates if candidate.auto_promote and candidate.memory_type != "user"]
        result = write_memory_set(workspace_home / MEMORIES_REL, promoted, status="active")
        candidate_created.extend(candidate_result["created"])
        candidate_updated.extend(candidate_result["updated"])
        created.extend(result["created"])
        updated.extend(result["updated"])
        for candidate in parsed.candidates:
            touched_types.add(candidate.memory_type)
        processed_sessions[record_key] = {
            "mtime_ns": stat.st_mtime_ns,
            "session_id": parsed.session_id,
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "started_at": parsed.started_at,
        }
        processed_count += 1

    index_lines = build_memory_index(workspace_home, config)
    recent_records = select_recent_sessions(parsed_recent, config)
    runtime_context = build_runtime_context(workspace_home, recent_records, config)
    write_runtime_context(workspace_home, runtime_context)

    dream_state = load_dream_state(workspace_home)
    if processed_count and not args.force_dream:
        dream_state["sessions_since_last_dream"] = int(dream_state.get("sessions_since_last_dream", 0)) + processed_count

    dream_result = {"ran": False, "report_path": None, "superseded": [], "index_lines": index_lines}
    if should_run_dream(dream_state, config, 0, len(matching_files), args.force_dream):
        write_results = {"created": created, "updated": updated}
        dream_result = run_dream(workspace_home, config, write_results)
        dream_state["last_dream_at"] = datetime.now(timezone.utc).isoformat()
        dream_state["sessions_since_last_dream"] = 0
        dream_state["last_report"] = dream_result["report_path"]
        dream_state["dream_count"] = int(dream_state.get("dream_count", 0)) + 1

    save_dream_state(workspace_home, dream_state)
    write_registry(workspace_home, registry)
    global_dream_state = load_global_dream_state(memory_home)
    global_dream_result = {"ran": False, "report_path": None}
    if processed_count and not (args.force_dream or args.force):
        global_dream_state["workspaces_since_last_dream"] = int(global_dream_state.get("workspaces_since_last_dream", 0)) + 1
    if should_run_global_dream(global_dream_state, global_config, 0, args.force_dream or args.force):
        global_dream_result = run_global_dream(memory_home, global_config)
        global_dream_state["last_dream_at"] = datetime.now(timezone.utc).isoformat()
        global_dream_state["workspaces_since_last_dream"] = 0
        global_dream_state["last_report"] = global_dream_result["report_path"]
        global_dream_state["dream_count"] = int(global_dream_state.get("dream_count", 0)) + 1
    save_global_dream_state(memory_home, global_dream_state)
    write_global_registry(memory_home, load_global_registry(memory_home))

    print(
        json.dumps(
            {
                "workspace_root": str(workspace_root),
                "memory_home": str(memory_home),
                "workspace_memory_home": str(workspace_home),
                "metadata_migrated": migration_result,
                "matching_sessions": len(matching_files),
                "processed": processed_count,
                "skipped": skipped_count,
                "candidate_created": len(candidate_created),
                "candidate_updated": len(candidate_updated),
                "created_memories": len(created),
                "updated_memories": len(updated),
                "touched_types": sorted(touched_types),
                "index_lines": index_lines,
                "dream": dream_result,
                "global_dream": global_dream_result,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
