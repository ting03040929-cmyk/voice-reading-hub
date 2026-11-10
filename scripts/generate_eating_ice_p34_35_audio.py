import os
import wave
import tempfile
import win32com.client
import lameenc

out_dir = os.path.join(os.path.dirname(__file__), "..", "materials", "audio", "eating-ice-p34-35-concept-quiz")
out_dir = os.path.abspath(out_dir)
os.makedirs(out_dir, exist_ok=True)
print(f"Output directory: {out_dir}")

# Initialize SAPI SpVoice
voice = win32com.client.Dispatch("SAPI.SpVoice")
voice.Rate = -1

# Choose best Taiwan voice (Yating preferred, then Hanhan)
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

def tts_to_mp3(text: str, filename: str, force: bool = True):
    target_mp3 = os.path.join(out_dir, filename)
    if not force and os.path.exists(target_mp3) and os.path.getsize(target_mp3) > 0:
        print(f"Skipping existing: {filename}")
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

audio_items = [
    ("intro.mp3", "第34、35頁。練習題第二大題：生字語詞，句子概念選擇題。請聽題目與選項，選出最符合句意概念的語詞。"),
    ("test-sound.mp3", "語音測試正常，歡迎使用句子概念選擇題聽讀練習。"),

    # Q1
    ("q01-question.mp3", "第1題。括號，當我們想形容一家店的招牌產品「名氣非常大，遠近都知道」時，可以用哪一個詞？提示：與遠近皆知、非常有名有關。"),
    ("q01-optA.mp3", "選項A：俄頃。"),
    ("q01-optB.mp3", "選項B：名聞遐邇。"),
    ("q01-optC.mp3", "選項C：遜色。"),
    ("q01-optD.mp3", "選項D：垂涎三尺。"),
    ("q01-full.mp3", "第1題。括號，當我們想形容一家店的招牌產品「名氣非常大，遠近都知道」時，可以用哪一個詞？提示：與遠近皆知、非常有名有關。選項A：俄頃。選項B：名聞遐邇。選項C：遜色。選項D：垂涎三尺。"),

    # Q2
    ("q02-question.mp3", "第2題。括號，課文中，如果把冰抽離，童年生活會變得「失去光彩、沒有吸引力」，這是指什麼？提示：形容失去原有的光芒與樂趣。"),
    ("q02-optA.mp3", "選項A：黯然失色。"),
    ("q02-optB.mp3", "選項B：五花八門。"),
    ("q02-optC.mp3", "選項C：貨真價實。"),
    ("q02-optD.mp3", "選項D：俄頃。"),
    ("q02-full.mp3", "第2題。括號，課文中，如果把冰抽離，童年生活會變得「失去光彩、沒有吸引力」，這是指什麼？提示：形容失去原有的光芒與樂趣。選項A：黯然失色。選項B：五花八門。選項C：貨真價實。選項D：俄頃。"),

    # Q3
    ("q03-question.mp3", "第3題。括號，媽媽去市場買菜，想稱讚菜販「東西新鮮、價格實在、不騙人」，可以用哪一個詞？提示：形容誠實信用、不偷工減料。"),
    ("q03-optA.mp3", "選項A：遜色。"),
    ("q03-optB.mp3", "選項B：消失殆盡。"),
    ("q03-optC.mp3", "選項C：貨真價實。"),
    ("q03-optD.mp3", "選項D：俄頃。"),
    ("q03-full.mp3", "第3題。括號，媽媽去市場買菜，想稱讚菜販「東西新鮮、價格實在、不騙人」，可以用哪一個詞？提示：形容誠實信用、不偷工減料。選項A：遜色。選項B：消失殆盡。選項C：貨真價實。選項D：俄頃。"),

    # Q4
    ("q04-question.mp3", "第4題。括號，課文中，小老闆飛快地操作刨冰機，冰屑「很快、在極短時間內」堆成小山，這是指什麼？"),
    ("q04-optA.mp3", "選項A：俄頃。"),
    ("q04-optB.mp3", "選項B：遜色。"),
    ("q04-optC.mp3", "選項C：消失殆盡。"),
    ("q04-optD.mp3", "選項D：名聞遐邇。"),
    ("q04-full.mp3", "第4題。括號，課文中，小老闆飛快地操作刨冰機，冰屑「很快、在極短時間內」堆成小山，這是指什麼？選項A：俄頃。選項B：遜色。選項C：消失殆盡。選項D：名聞遐邇。"),

    # Q5
    ("q05-question.mp3", "第5題。括號，課文中，現代冰品在口味上「比不上」臺灣早年的冰製品，這是指什麼？提示：形容比起別的產品顯得比較差。"),
    ("q05-optA.mp3", "選項A：貨真價實。"),
    ("q05-optB.mp3", "選項B：遜色。"),
    ("q05-optC.mp3", "選項C：五花八門。"),
    ("q05-optD.mp3", "選項D：名聞遐邇。"),
    ("q05-full.mp3", "第5題。括號，課文中，現代冰品在口味上「比不上」臺灣早年的冰製品，這是指什麼？提示：形容比起別的產品顯得比較差。選項A：貨真價實。選項B：遜色。選項C：五花八門。選項D：名聞遐邇。"),

    # Q6
    ("q06-question.mp3", "第6題。括號，當我們看到美味的大餐，心裡「非常想吃，連口水都快流下來」，這個狀態叫什麼？提示：形容極度渴望美食的樣子。"),
    ("q06-optA.mp3", "選項A：黯然失色。"),
    ("q06-optB.mp3", "選項B：垂涎三尺。"),
    ("q06-optC.mp3", "選項C：消失殆盡。"),
    ("q06-optD.mp3", "選項D：俄頃。"),
    ("q06-full.mp3", "第6題。括號，當我們看到美味的大餐，心裡「非常想吃，連口水都快流下來」，這個狀態叫什麼？提示：形容極度渴望美食的樣子。選項A：黯然失色。選項B：垂涎三尺。選項C：消失殆盡。選項D：俄頃。"),

    # Q7
    ("q07-question.mp3", "第7題。括號，課文中，隨著社會發達，我們現在吃冰的選擇「各式各樣、種類繁多」，這是什麼意思？提示：形容花樣繁多，應有盡有。"),
    ("q07-optA.mp3", "選項A：五花八門。"),
    ("q07-optB.mp3", "選項B：遜色。"),
    ("q07-optC.mp3", "選項C：俄頃。"),
    ("q07-optD.mp3", "選項D：貨真價實。"),
    ("q07-full.mp3", "第7題。括號，課文中，隨著社會發達，我們現在吃冰的選擇「各式各樣、種類繁多」，這是什麼意思？提示：形容花樣繁多，應有盡有。選項A：五花八門。選項B：遜色。選項C：俄頃。選項D：貨真價實。"),

    # Q8
    ("q08-question.mp3", "第8題。括號，課文中，作者感嘆童年那些吃冰的快樂記憶，現在已經「大多消失、所剩不多」，這是指什麼？提示：形容大多消失、所剩不多。"),
    ("q08-optA.mp3", "選項A：消失殆盡。"),
    ("q08-optB.mp3", "選項B：五花八門。"),
    ("q08-optC.mp3", "選項C：名聞遐邇。"),
    ("q08-optD.mp3", "選項D：貨真價實。"),
    ("q08-full.mp3", "第8題。括號，課文中，作者感嘆童年那些吃冰的快樂記憶，現在已經「大多消失、所剩不多」，這是指什麼？提示：形容大多消失、所剩不多。選項A：消失殆盡。選項B：五花八門。選項C：名聞遐邇。選項D：貨真價實。")
]

print(f"Generating {len(audio_items)} audio clips for eating-ice-p34-35-concept-quiz...")
for filename, text in audio_items:
    tts_to_mp3(text, filename, force=True)

print("All audio clips generated successfully!")
