from docassemble.base.util import DAObject

class Organ(DAObject):
    def init(self, *pargs, **kwargs):
        self.initializeAttribute('name', DAObject)
        self.nazev = "orgánu"
        super().init(*pargs, **kwargs)
    def nazev(self):
        return self.name
