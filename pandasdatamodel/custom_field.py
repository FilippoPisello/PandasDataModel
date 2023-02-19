from dataclasses import MISSING, Field


class CustomField(Field):
    def __init__(self, default: str, validation=None, **validation_parameters):
        self.validation = validation
        super().__init__(
            default=default,
            default_factory=MISSING,
            init=False,
            repr=True,
            hash=None,
            compare=True,
            metadata=None,
            kw_only=MISSING,
        )
        self.validation_parameters = validation_parameters

    def __repr__(self):
        return (
            "CustomField("
            f"name={self.name!r},"
            f"type={self.type!r},"
            f"default={self.default!r},"
            f"default_factory={self.default_factory!r},"
            f"init={self.init!r},"
            f"repr={self.repr!r},"
            f"hash={self.hash!r},"
            f"compare={self.compare!r},"
            f"metadata={self.metadata!r},"
            f"kw_only={self.kw_only!r},"
            f"_field_type={self._field_type}"
            ")"
        )
