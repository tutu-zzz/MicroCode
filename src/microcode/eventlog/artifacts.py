"""Content-addressed storage for large durable payloads."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field


class ArtifactRef(BaseModel):
    model_config = ConfigDict(frozen=True)
    digest: str
    size: int = Field(ge=0)
    media_type: str


class ArtifactStore(Protocol):
    def put_bytes(self, data: bytes, media_type: str) -> ArtifactRef: ...
    def get_bytes(self, ref: ArtifactRef) -> bytes: ...


class FileArtifactStore:
    """SHA-256 file store implemented in M2."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def put_bytes(self, data: bytes, media_type: str) -> ArtifactRef:
        del data, media_type
        raise NotImplementedError("Implement atomic content-addressed writes in M2")

    def get_bytes(self, ref: ArtifactRef) -> bytes:
        del ref
        raise NotImplementedError("Implement digest-verified reads in M2")
