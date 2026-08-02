from app.core.config import settings

# This file acts as a simplified export module for settings,
# in case we want to separate instantiation from definition in the future.
# Currently, it just re-exports the instantiated settings object.

__all__ = ["settings"]
