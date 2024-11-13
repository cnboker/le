from src.gminigpt import chat_with_Gemin

def test_call_gmini():
    text = chat_with_Gemin("中国有多少人")
    print(f"gmini_resposne:{text}")