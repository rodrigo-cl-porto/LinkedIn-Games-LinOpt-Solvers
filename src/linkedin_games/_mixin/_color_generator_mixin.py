import random


class ColorGeneratorMixin:

    @staticmethod
    def _generate_hex_codes(n:int=1) -> list[str]:
        colors_int = random.sample(range(16777217), n)
        return [f"#{color:06x}" for color in colors_int]

    @staticmethod
    def _generate_hex_code() -> str:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f"#{r:02x}{g:02x}{b:02x}"
