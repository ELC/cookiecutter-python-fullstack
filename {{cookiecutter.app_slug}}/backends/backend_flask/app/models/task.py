from typing import NamedTuple, Optional

class Task(NamedTuple):
    id: int
    text: Optional[str] = None
    day: Optional[str] = None
    reminder: Optional[bool] = None
