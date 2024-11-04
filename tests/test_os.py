import sys
import os

def test_rec():
    piper_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../piper/piper'))
    print("path->", piper_file)
    print("__file__", __file__)