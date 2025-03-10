from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional

class INoteRepository(ABC):
    @abstractmethod
    def create_note(self, title:str, content:str, reminder: datetime = None) -> int: ...

    @abstractmethod
    def get_notes(self) -> List[Dict]: ...

    @abstractmethod
    def delete_notes(self, note_id: int) -> bool: ...

class INotifier(ABC):
    @abstractmethod
    def reminder(self, note_id: int, reminder_time: datetime, message: str)-> None: ...

class INoteService(ABC):
    @abstractmethod
    def add_note(self, title:str, content:str, reminder: datetime = None) -> None: ...

    @abstractmethod
    def get_all_notes(self) -> List[Dict]: ...

    @abstractmethod
    def delete_note(self, note_id:int) -> None: ...