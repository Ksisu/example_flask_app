import os
from dataclasses import dataclass

import jwt


@dataclass
class JwtServiceConfig:
    algorithm: str
    coding_key: str

    @staticmethod
    def read_from_env():
        algorithm = os.getenv("JWT_ALGORITHM")
        coding_key = os.getenv("JWT_CODING_KEY")
        return JwtServiceConfig(algorithm, coding_key)


class JwtService:
    def __init__(self, config: JwtServiceConfig):
        self._config = config

    def decode(self, raw) -> dict | None:
        try:
            return jwt.decode(raw, self._config.coding_key, [self._config.algorithm])
        except:
            return None
