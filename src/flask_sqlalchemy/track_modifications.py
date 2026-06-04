from __future__ import annotations

import typing as t

import sqlalchemy as sa
import sqlalchemy.event as sa_event
import sqlalchemy.orm as sa_orm
from flask import current_app
from flask import has_app_context
from flask.signals import Namespace  # type: ignore[attr-defined]

if t.TYPE_CHECKING:
    from .session import Session

_signals = Namespace()

models_committed = _signals.signal("models-committed")
"""This Blinker signal is sent after the session is committed if there were changed
models in the session.

The sender is the application that emitted the changes. The receiver is passed the
``changes`` argument with a list of tuples in the form ``(instance, operation)``.
The operations are ``"insert"``, ``"update"``, and ``"delete"``.
"""

before_models_committed = _signals.signal("before-models-committed")
"""This signal works exactly like :data:`models_committed` but is emitted before the
commit takes place.
"""










