from dataclasses import dataclass


@dataclass
class ListRequest:
    page: int
    size: int
