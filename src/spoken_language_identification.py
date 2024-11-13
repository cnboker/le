# Install SpeechBrain if you haven't already
import io
import torchaudio
from speechbrain.inference.classifiers import EncoderClassifier

# Load the language identification model
classifier = EncoderClassifier.from_hparams(source="speechbrain/lang-id-commonlanguage_ecapa", savedir="pretrained_models/lang-id-commonlanguage_ecapa")


def lang_identify(audio_file):   
    out_prob, score, index, text_lab = classifier.classify_file(audio_file)
    print("text_lab", text_lab)
    return text_lab[0]

