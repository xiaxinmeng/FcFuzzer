@dataclass(hash=True, eq=False, frozen=False)
class A:
    i: int
    def __eq__(self, other): ...