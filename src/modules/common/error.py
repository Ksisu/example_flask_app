from dataclasses import dataclass


@dataclass
class ApplicationError:
    error_code: int
    message: str
