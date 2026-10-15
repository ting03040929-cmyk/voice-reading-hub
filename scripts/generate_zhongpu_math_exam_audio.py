import os
import wave
import tempfile
import win32com.client
import lameenc

out_dir = os.path.join(os.path.dirname(__file__), "..", "materials", "audio", "zhongpu-115-math-exam1")
out_dir = os.path.abspath(out_dir)
os.makedirs(out_dir, exist_ok=True)
print(f"Output directory: {out_dir}")

# Initialize SAPI SpVoice
voice = win32com.client.Dispatch("SAPI.SpVoice")
voice.Rate = -1  # slightly slower for special education students

# Choose best Taiwan voice (Yating or Hanhan)
installed_voices = voice.GetVoices()
selected_token = None
for token in installed_voices:
    desc = token.GetDescription().lower()
    tid = token.Id.lower()
    if "yating" in desc or "yating" in tid:
        selected_token = token
        break
    if "hanhan" in desc or "hanhan" in tid:
        selected_token = token

if selected_token:
    voice.Voice = selected_token
    print(f"Using SAPI Voice: {selected_token.GetDescription()}")
else:
    print("Using default SAPI Voice")

def tts_to_mp3(text: str, filename: str):
    target_mp3 = os.path.join(out_dir, filename)
    if os.path.exists(target_mp3) and os.path.getsize(target_mp3) > 0:
        return

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_wav = tmp.name

    try:
        file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
        file_stream.Open(tmp_wav, 3)  # 3 = SSFMCreateForWrite
        voice.AudioOutputStream = file_stream
        voice.Speak(text)
        file_stream.Close()
        voice.AudioOutputStream = None

        with wave.open(tmp_wav, "rb") as w:
            n_channels = w.getnchannels()
            sample_rate = w.getframerate()
            pcm_data = w.readframes(w.getnframes())

        encoder = lameenc.Encoder()
        encoder.set_bit_rate(128)
        encoder.set_in_sample_rate(sample_rate)
        encoder.set_channels(n_channels)
        encoder.set_quality(2)
        mp3_data = encoder.encode(pcm_data) + encoder.flush()

        with open(target_mp3, "wb") as f:
            f.write(mp3_data)
        print(f"Generated: {filename} ({len(mp3_data):,} bytes)")
    finally:
        if os.path.exists(tmp_wav):
            try:
                os.remove(tmp_wav)
            except Exception:
                pass

audio_tasks = [
    # 觀念整理與大題說明
    ("concept-intro.mp3", "觀念引導：正負數家族與相反詞整理。加號家族代表增加、變多、正向，例如：賺錢、收入、上升、往上、贏了、向東。減號家族代表減少、變少、負向，例如：花錢、支出、下降、往下、輸了、向西。指南針指向東邊記作加號，指向西邊記作減號。氣溫比零度低記作負數。"),
    ("sec-choice-intro.mp3", "一大題，選擇題。共12題。請觀察題目與生活關鍵字，選出正確的選項。"),
    ("sec-fill-intro.mp3", "二大題，填充題。共10題。請根據題目中的關鍵字，參考上面的圖片，填入正確的數字，記得要寫正號或負號喔！"),

    # 一、選擇題 (1~12)
    # 第 1 題
    ("choice-q1-question.mp3", "第1題。圖片中，黃色的加號家族代表什麼意思？"),
    ("choice-q1-opt1.mp3", "選項1，減少、變少"),
    ("choice-q1-opt2.mp3", "選項2，增加、變多"),
    ("choice-q1-opt3.mp3", "選項3，不動"),
    ("choice-q1-full.mp3", "第1題。圖片中，黃色的加號家族代表什麼意思？選項1，減少、變少。選項2，增加、變多。選項3，不動。"),

    # 第 2 題
    ("choice-q2-question.mp3", "第2題。圖片中，藍色的減號家族代表什麼意思？"),
    ("choice-q2-opt1.mp3", "選項1，減少、變少"),
    ("choice-q2-opt2.mp3", "選項2，增加、變多"),
    ("choice-q2-opt3.mp3", "選項3，變大"),
    ("choice-q2-full.mp3", "第2題。圖片中，藍色的減號家族代表什麼意思？選項1，減少、變少。選項2，增加、變多。選項3，變大。"),

    # 第 3 題
    ("choice-q3-question.mp3", "第3題。如果看到錢袋旁邊寫著「賺錢」，我們應該用哪一個符號？"),
    ("choice-q3-opt1.mp3", "選項1，加號"),
    ("choice-q3-opt2.mp3", "選項2，減號"),
    ("choice-q3-opt3.mp3", "選項3，乘號"),
    ("choice-q3-full.mp3", "第3題。如果看到錢袋旁邊寫著「賺錢」，我們應該用哪一個符號？選項1，加號。選項2，減號。選項3，乘號。"),

    # 第 4 題
    ("choice-q4-question.mp3", "第4題。「花錢」買果汁用了 25 元，應該記作什麼？"),
    ("choice-q4-opt1.mp3", "選項1，正25"),
    ("choice-q4-opt2.mp3", "選項2，負25"),
    ("choice-q4-opt3.mp3", "選項3，0"),
    ("choice-q4-full.mp3", "第4題。「花錢」買果汁用了 25 元，應該記作什麼？選項1，正25。選項2，負25。選項3，0。"),

    # 第 5 題
    ("choice-q5-question.mp3", "第5題。氣溫「下降」了 5 度，這屬於哪一個家族？"),
    ("choice-q5-opt1.mp3", "選項1，加號家族"),
    ("choice-q5-opt2.mp3", "選項2，減號家族"),
    ("choice-q5-opt3.mp3", "選項3，以上都不是"),
    ("choice-q5-full.mp3", "第5題。氣溫「下降」了 5 度，這屬於哪一個家族？選項1，加號家族。選項2，減號家族。選項3，以上都不是。"),

    # 第 6 題
    ("choice-q6-question.mp3", "第6題。指南針指向 E，東邊，圖片說這要記作什麼？"),
    ("choice-q6-opt1.mp3", "選項1，向東加號"),
    ("choice-q6-opt2.mp3", "選項2，向東減號"),
    ("choice-q6-opt3.mp3", "選項3，向東乘號"),
    ("choice-q6-full.mp3", "第6題。指南針指向 E，東邊，圖片說這要記作什麼？選項1，向東加號。選項2，向東減號。選項3，向東乘號。"),

    # 第 7 題
    ("choice-q7-question.mp3", "第7題。看到獎盃且寫著「贏了」 10 分，正確的記法是？"),
    ("choice-q7-opt1.mp3", "選項1，負10"),
    ("choice-q7-opt2.mp3", "選項2，正10"),
    ("choice-q7-opt3.mp3", "選項3，10加"),
    ("choice-q7-full.mp3", "第7題。看到獎盃且寫著「贏了」 10 分，正確的記法是？選項1，負10。選項2，正10。選項3，10加。"),

    # 第 8 題
    ("choice-q8-question.mp3", "第8題。「收入」 100 元與「支出」 100 元，哪一個要用減號？"),
    ("choice-q8-opt1.mp3", "選項1，收入"),
    ("choice-q8-opt2.mp3", "選項2，支出"),
    ("choice-q8-opt3.mp3", "選項3，兩個都要"),
    ("choice-q8-full.mp3", "第8題。「收入」 100 元與「支出」 100 元，哪一個要用減號？選項1，收入。選項2，支出。選項3，兩個都要。"),

    # 第 9 題
    ("choice-q9-question.mp3", "第9題。小兔子「往下」移動 3 層樓，應該選哪一個？"),
    ("choice-q9-opt1.mp3", "選項1，正3"),
    ("choice-q9-opt2.mp3", "選項2，負3"),
    ("choice-q9-opt3.mp3", "選項3，往下 0"),
    ("choice-q9-full.mp3", "第9題。小兔子「往下」移動 3 層樓，應該選哪一個？選項1，正3。選項2，負3。選項3，往下 0。"),

    # 第 10 題
    ("choice-q10-question.mp3", "第10題。下列哪一個屬於加號家族的關鍵字？"),
    ("choice-q10-opt1.mp3", "選項1，下降"),
    ("choice-q10-opt2.mp3", "選項2，向西"),
    ("choice-q10-opt3.mp3", "選項3，上升"),
    ("choice-q10-full.mp3", "第10題。下列哪一個屬於加號家族的關鍵字？選項1，下降。選項2，向西。選項3，上升。"),

    # 第 11 題
    ("choice-q11-question.mp3", "第11題。冰箱冷凍庫的溫度，設定為比 0 度還要低 12 度。請問冷凍庫是多少度？"),
    ("choice-q11-opt1.mp3", "選項A，負12度C"),
    ("choice-q11-opt2.mp3", "選項B，12度C"),
    ("choice-q11-opt3.mp3", "選項C，0度C"),
    ("choice-q11-full.mp3", "第11題。冰箱冷凍庫的溫度，設定為比 0 度還要低 12 度。請問冷凍庫是多少度？選項A，負12度C。選項B，12度C。選項C，0度C。"),

    # 第 12 題
    ("choice-q12-question.mp3", "第12題。在高山上非常冷，氣溫比 0 度還要低 3 度。請問山上的溫度是多少度？"),
    ("choice-q12-opt1.mp3", "選項A，0度C"),
    ("choice-q12-opt2.mp3", "選項B，3度C"),
    ("choice-q12-opt3.mp3", "選項C，負3度C"),
    ("choice-q12-full.mp3", "第12題。在高山上非常冷，氣溫比 0 度還要低 3 度。請問山上的溫度是多少度？選項A，0度C。選項B，3度C。選項C，負3度C。"),

    # 二、填充題 (1~10)
    ("fill-q1-question.mp3", "第1題。媽媽給我 50 元當零用錢，這是一筆收入，可以記作空格元。"),
    ("fill-q2-question.mp3", "第2題。我去文具店買鉛筆花錢花了 20 元，可以記作空格元。"),
    ("fill-q3-question.mp3", "第3題。今天的天氣很熱，氣溫上升了 3 度，可以記作空格度。"),
    ("fill-q4-question.mp3", "第4題。大隊接力比賽，我們班最後輸了 5 秒，可以記作空格秒。"),
    ("fill-q5-question.mp3", "第5題。小明在操場跑步，向東走了 100 公尺，可以記作空格公尺。"),
    ("fill-q6-question.mp3", "第6題。爸爸在路邊幫忙修車賺錢賺了 500 元，可以記作空格元。"),
    ("fill-q7-question.mp3", "第7題。因為很久沒下雨，水庫的水位下降了 2 公尺，可以記作空格公尺。"),
    ("fill-q8-question.mp3", "第8題。搭電梯要去地下室，電梯往下移動了 1 層樓，可以記作空格層。"),
    ("fill-q9-question.mp3", "第9題。這星期買早餐的總支出是 300 元，可以記作空格元。"),
    ("fill-q10-question.mp3", "第10題。小華騎腳踏車向西前進了 5 公里，可以記作空格公里。"),
]

print(f"Total audio files to generate: {len(audio_tasks)}")
for fn, text in audio_tasks:
    tts_to_mp3(text, fn)

print("Audio generation completed successfully!")
