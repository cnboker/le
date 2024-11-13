from src.spoken_language_identification import lang_identify

def test_rec():
    zh = lang_identify('tests/data/zh.wav')
    en = lang_identify('tests/data/en.wav')
    assert zh == "zh"
    assert en == "en"