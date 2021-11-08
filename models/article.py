import dataclasses

@dataclasses.dataclass
class Article(object):
    url: str
    name: str
    price: str
    series: str
    marca: str
    usos: str
    pantalla: str
    sistema_operativo: str
    entrada_interfaz: str
    fabricante_cpu: str

    def to_dict(self):
        return {
            'url': self.url,
            'name': self.name,
            'price': self.price,
            'series': self.series,
            'marca': self.marca,
            'usos': self.usos,
            'pantalla': self.pantalla,
            'sistema_operativo': self.sistema_operativo,
            'entrada_interfaz': self.entrada_interfaz,
            'fabricante_cpu': self.fabricante_cpu
        }




