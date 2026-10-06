"""In-memory virtual file system loaded from CSV."""

import base64
import binascii
import csv
from dataclasses import dataclass, field
from pathlib import Path


MIN_SIZE = 0


class VfsError(ValueError):
    """Raised when a VFS cannot be loaded or accessed."""


@dataclass
class VfsNode:
    """Represent one VFS file or directory."""

    name: str
    node_type: str
    size: int = 0
    owner: str = "root"
    data: bytes = b""
    parent: "VfsNode | None" = None
    children: dict[str, "VfsNode"] = field(default_factory=dict)

    @property
    def is_dir(self) -> bool:
        """Return True when the node is a directory."""
        return self.node_type == "dir"


class Vfs:
    """Manage a virtual file tree entirely in memory."""

    HEADER = ["path", "type", "size", "owner", "content_base64"]

    def __init__(self, name: str = "VFS") -> None:
        """Create an empty VFS with a root directory."""
        self.name = name
        self.root = VfsNode("/", "dir")

    @classmethod
    def from_csv(cls, path: str) -> "Vfs":
        """Load a VFS from a CSV file without modifying that file."""
        source = Path(path)
        if not source.is_file():
            raise VfsError(f"VFS-файл не найден: {path}")
        vfs = cls(source.stem)
        try:
            with source.open("r", encoding="utf-8", newline="") as file:
                reader = csv.DictReader(file)
                cls._check_header(reader.fieldnames)
                rows = list(reader)
        except (OSError, UnicodeError, csv.Error) as exc:
            raise VfsError(f"Ошибка чтения VFS: {exc}") from exc
        vfs._load_rows(rows)
        return vfs

    @classmethod
    def _check_header(cls, fieldnames: list[str] | None) -> None:
        """Validate required CSV columns."""
        if fieldnames != cls.HEADER:
            raise VfsError("Неверный формат CSV VFS.")

    def _load_rows(self, rows: list[dict[str, str | None]]) -> None:
        """Build the in-memory tree from CSV rows."""
        normalized = [self._parse_row(row) for row in rows]
        normalized.sort(key=lambda item: (item[0].count("/"), item[0]))
        for path, node_type, size, owner, data in normalized:
            self._insert(path, node_type, size, owner, data)

    @staticmethod
    def _parse_row(row: dict[str, str | None]) -> tuple[
        str, str, int, str, bytes
    ]:
        """Validate and decode one CSV row."""
        path = row.get("path") or ""
        node_type = row.get("type") or ""
        size_text = row.get("size") or "0"
        owner = row.get("owner") or "root"
        content = row.get("content_base64") or ""
        if not path.startswith("/") or node_type not in {"dir", "file"}:
            raise VfsError("Некорректная строка VFS.")
        try:
            size = int(size_text)
        except ValueError as exc:
            raise VfsError(f"Некорректный размер: {path}") from exc
        if size < MIN_SIZE:
            raise VfsError(f"Отрицательный размер: {path}")
        if node_type == "dir" and content:
            raise VfsError(f"Каталог содержит данные: {path}")
        if node_type == "file":
            try:
                data = base64.b64decode(content, validate=True)
            except (ValueError, binascii.Error) as exc:
                raise VfsError(f"Некорректный base64: {path}") from exc
            if size != len(data):
                raise VfsError(f"Размер не совпадает: {path}")
        else:
            data = b""
        return path, node_type, size, owner, data

    def _insert(
        self,
        path: str,
        node_type: str,
        size: int,
        owner: str,
        data: bytes,
    ) -> None:
        """Insert one node into the tree."""
        if path == "/":
            if node_type != "dir" or self.root.children:
                raise VfsError("Некорректное описание корня VFS.")
            self.root.owner = owner
            return
        parts = [part for part in path.split("/") if part]
        parent = self.resolve("/" + "/".join(parts[:-1]))
        if parent is None or not parent.is_dir:
            raise VfsError(f"Не найден родитель: {path}")
        name = parts[-1]
        if name in parent.children:
            raise VfsError(f"Дубликат пути: {path}")
        parent.children[name] = VfsNode(
            name=name,
            node_type=node_type,
            size=size if node_type == "file" else 0,
            owner=owner,
            data=data,
            parent=parent,
        )

    def resolve(
        self, path: str, current: VfsNode | None = None
    ) -> VfsNode | None:
        """Resolve a VFS path from the current node."""
        start = self.root if path.startswith("/") else current or self.root
        parts = [part for part in path.split("/") if part]
        node = start
        for part in parts:
            if part == ".":
                continue
            if part == "..":
                node = node.parent or self.root
                continue
            node = node.children.get(part)
            if node is None:
                return None
        return node

    @staticmethod
    def path_of(node: VfsNode) -> str:
        """Return the absolute path of a node."""
        if node.parent is None:
            return "/"
        parts: list[str] = []
        current = node
        while current.parent is not None:
            parts.append(current.name)
            current = current.parent
        return "/" + "/".join(reversed(parts))

    def total_size(self, node: VfsNode) -> int:
        """Return the recursive byte size of a node."""
        if not node.is_dir:
            return node.size
        return sum(self.total_size(child) for child in node.children.values())

    def walk(self, node: VfsNode | None = None) -> list[VfsNode]:
        """Return nodes below a directory in depth-first order."""
        start = node or self.root
        result = [start]
        if start.is_dir:
            children = sorted(
                start.children.values(),
                key=lambda item: item.name,
            )
            for child in children:
                result.extend(self.walk(child))
        return result
