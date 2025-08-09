"""
Database models for Influenceur IA
"""

from .user import User  # noqa: F401
from .influenceuse import Influenceuse  # noqa: F401
from .content import Content, ContentType  # noqa: F401
from .conversation import Conversation, Message  # noqa: F401

# Optional modules (present in future phases). Import lazily if available.
try:  # noqa: SIM105
    from .platform import Platform, PlatformAccount  # type: ignore  # noqa: F401
except Exception:  # pragma: no cover
    Platform = None  # type: ignore
    PlatformAccount = None  # type: ignore

try:  # noqa: SIM105
    from .analytics import Analytics, Metrics  # type: ignore  # noqa: F401
except Exception:  # pragma: no cover
    Analytics = None  # type: ignore
    Metrics = None  # type: ignore

try:  # noqa: SIM105
    from .sales import Sale, Pack, Transaction  # type: ignore  # noqa: F401
except Exception:  # pragma: no cover
    Sale = None  # type: ignore
    Pack = None  # type: ignore
    Transaction = None  # type: ignore

__all__ = [
    "User",
    "Influenceuse",
    "Content",
    "ContentType",
    "Conversation",
    "Message",
]
