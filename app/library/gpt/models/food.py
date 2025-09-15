class Food:
    def __init__(self, name: str, image: bytes):
        self.name = name
        self.image = image
    def __repr__(self):
        return f"<Food(name={self.name!r}, image_length={len(self.image) if self.image else 0})>"
    def getImage(self):
        return self.image
    def getName(self):
        return self.name