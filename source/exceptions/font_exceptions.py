from source.models.Arabic_Fonts.fonts import fonts


class FontException(Exception):
    def __init__(self, fonttype):
        message = f"Wrong font: {fonttype}"
        self.error_code = 500


def validate_font(fonttype):
    try:
        if fonttype not in fonts:
            raise FontException(f"Font '{fonttype}' is not valid.")
    except KeyError:
        raise FontException(f"Font '{fonttype}' is not valid.")
