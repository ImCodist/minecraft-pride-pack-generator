"""
Includes the base class for a component, and any classes it may use.
Also includes helper functions for components.
"""


from PIL import Image


class Texture():
    def __init__(self, path: str, image: Image.Image):
        self.path: str = path
        self.image: Image.Image = image


class ComponentBase():
    def __init__(self):
        self.textures: list[Texture] = []
        self.options: dict[str, str] = {}
    
    def generate(self):
        self.textures = self.generate_textures()
    
    def generate_textures(self) -> list[Texture]:
        return []