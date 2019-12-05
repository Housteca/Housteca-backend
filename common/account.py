from typing import Optional


class Account:
    def __init__(self, address: str, private_key: bytes, index: Optional[int] = None) -> None:
        self.__address = address
        self.__private_key = private_key
        self.__index = index

    @property
    def address(self) -> str:
        return self.__address

    @property
    def private_key(self) -> bytes:
        return self.__private_key

    @property
    def index(self) -> Optional[int]:
        return self.__index
