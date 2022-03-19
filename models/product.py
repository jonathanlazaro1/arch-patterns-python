from uuid import UUID, uuid4


class Product:
    _id: UUID
    name: str
    sku: str

    def __init__(self, name: str, sku: str):
        self._id = uuid4()
        self.name = name
        self.sku = sku

    @property
    def id(self):
        return self._id
