"""Décorateur pour sécuriser les slots PySide6.

Attrape les exceptions métier et les affiche proprement,
sans jamais faire planter l'application.
"""
import functools
import logging

from PySide6.QtWidgets import QMessageBox

from services.exceptions import ValidationError, NotFoundError

log = logging.getLogger(__name__)


def safe_slot(func):
    """Décorateur pour les slots : attrape les erreurs et affiche un message.

    Usage :
        @safe_slot
        def on_click(self):
            ...
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except (ValidationError, NotFoundError) as e:
            QMessageBox.warning(self, "Erreur", str(e))
        except Exception as e:
            log.exception("Erreur dans %s", func.__name__)
            QMessageBox.critical(
                self, "Erreur inattendue",
                f"Une erreur est survenue :\n{e}"
            )
    return wrapper