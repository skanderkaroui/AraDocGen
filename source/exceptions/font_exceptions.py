class FontException(Exception):
    def __init__(self, fonttype):
        message = f"Wrong font: {fonttype}"
        self.error_code = 500