from uuid import UUID, uuid4


class Product:
    __id: UUID
    name: str
    sku: str

    def __init__(self, name: str, sku: str):
        self.__id = uuid4()
        self.name = name
        self.sku = sku

    @property
    def id(self):
        return self.__id
