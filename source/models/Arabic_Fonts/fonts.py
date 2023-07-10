from enum import Enum


class FontEnum(Enum):
    advertisingBold = "advertisingBold"
    afDiwani = "afDiwani"
    andalus = "andalus"
    arabicTransparent = "arabicTransparent"
    arslanWessamA = "arslanWessamA"
    decotypeNaskh = "decotypeNaskh"
    decotypeThuluth = "decotypeThuluth"
    mUnicodeSara = "mUnicodeSara"
    sakkalMajalla = "sakkalMajalla"
    simplifiedArabic = "simplifiedArabic"
    tahoma = "tahoma"
    traditionalArabic = "traditionalArabic"

    def get_font_path(self):
        return fonts.get(self.value)


fonts = {
    "advertisingBold": r"models\Arabic_Fonts\AdvertisingBold.ttf",
    "afDiwani": r".\source\models\Arabic_Fonts\AfDiwani.ttf",
    "andalus": r".\source\models\Arabic_Fonts\Andalus.ttf",
    "arabicTransparent": r".\source\models\Arabic_Fonts\ArabicTransparent.ttf",
    "arslanWessamA": r".\source\models\Arabic_Fonts\ArslanWessamA.ttf",
    "decotypeNaskh": r".\source\models\Arabic_Fonts\DecotypeNaskh.ttf",
    "decotypeThuluth": r".\source\models\Arabic_Fonts\DecotypeThuluth.ttf",
    "mUnicodeSara": r".\source\models\Arabic_Fonts\MUnicodeSara.ttf",
    "sakkalMajalla": r".\source\models\Arabic_Fonts\SakkalMajalla.ttf",
    "simplifiedArabic": r".\source\models\Arabic_Fonts\SimplifiedArabic.ttf",
    "tahoma": r".\source\models\Arabic_Fonts\Tahoma.ttf",
    "traditionalArabic": r".\source\models\Arabic_Fonts\TraditionalArabic.ttf"
}
