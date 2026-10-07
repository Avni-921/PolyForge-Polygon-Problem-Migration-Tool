from abc import ABC, abstractmethod
import os

class StorageBackend(ABC):
    """Abstract interface for all storage backends."""

    @abstractmethod
    def upload_file(self, key: str, file_obj) -> bool:
        pass

    @abstractmethod
    def download_file(self, key: str) -> bytes:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def list_files(self, prefix: str) -> list[str]:
        pass

    @abstractmethod
    def delete_file(self, key: str) -> bool:
        pass

    def build_input_key(self, problem_id: str, n: int) -> str:
        """Centralized definition of input file key format."""
        return f"test_cases/{problem_id}/{n:02d}"

    def build_output_key(self, problem_id: str, n: int) -> str:
        """Centralized definition of output file key format."""
        return f"test_cases/{problem_id}/{n:02d}.a"
