import os
import wave
import tempfile
import win32com.client
import lameenc

out_dir = os.path.join(os.path.dirname(__file__), "..", "materials", "audio", "eating-ice-vocab-fill-quiz")
out_dir = os.path.abspath(out_dir)
os.makedirs(out_dir, exist_ok=True)
print(f"Output directory: {out_dir}")

# Initialize SAPI SpVoice
voice = win32com.client.Dispatch("SAPI.SpVoice")
voice.Rate = -1

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
    ("intro.mp3", "第一大題：生字語詞，句子挖空選擇題。請選出最適合填入句子空格中的語詞。"),
    ("test-sound.mp3", "語音測試正常，歡迎使用生字語詞挖空選擇題聽讀練習。"),

    # Q1
    ("q01-question.mp3", "第1題。糖廠宿舍前大排長龍，因為這裡的紅豆冰棒在當地空格。"),
    ("q01-optA.mp3", "選項A：俄頃。"),
    ("q01-optB.mp3", "選項B：名聞遐邇。"),
    ("q01-optC.mp3", "選項C：遜色。"),
    ("q01-optD.mp3", "選項D：垂涎三尺。"),

    # Q2
    ("q02-question.mp3", "第2題。新開的甜點店裡有空格的蛋糕，每一種看起來都很美味。"),
    ("q02-optA.mp3", "選項A：五花八門。"),
    ("q02-optB.mp3", "選項B：遜色。"),
    ("q02-optC.mp3", "選項C：俄頃。"),
    ("q02-optD.mp3", "選項D：消失殆盡。"),

    # Q3
    ("q03-question.mp3", "第3題。弟弟一看到桌上剛烤好的披薩，忍不住空格，想要立刻咬一口。"),
    ("q03-optA.mp3", "選項A：黯然失色。"),
    ("q03-optB.mp3", "選項B：遜色。"),
    ("q03-optC.mp3", "選項C：垂涎三尺。"),
    ("q03-optD.mp3", "選項D：貨真價實。"),

    # Q4
    ("q04-question.mp3", "第4題。這家手工製鞋店的皮鞋用料實在、價格公道，可說是空格。"),
    ("q04-optA.mp3", "選項A：俄頃。"),
    ("q04-optB.mp3", "選項B：遜色。"),
    ("q04-optC.mp3", "選項C：貨真價實。"),
    ("q04-optD.mp3", "選項D：消失殆盡。"),

    # Q5
    ("q05-question.mp3", "第5題。老闆飛快地操作刨冰機，冰花如雪飛落，空格就堆滿了整盤。"),
    ("q05-optA.mp3", "選項A：俄頃。"),
    ("q05-optB.mp3", "選項B：遜色。"),
    ("q05-optC.mp3", "選項C：黯然失色。"),
    ("q05-optD.mp3", "選項D：名聞遐邇。"),

    # Q6
    ("q06-question.mp3", "第6題。由於環境受到破壞，森林裡的珍貴植物已經空格。"),
    ("q06-optA.mp3", "選項A：名聞遐邇。"),
    ("q06-optB.mp3", "選項B：五花八門。"),
    ("q06-optC.mp3", "選項C：消失殆盡。"),
    ("q06-optD.mp3", "選項D：垂涎三尺。"),

    # Q7
    ("q07-question.mp3", "第7題。如果舞台上的主角沒有燈光照射，他的表演可能就會空格。"),
    ("q07-optA.mp3", "選項A：黯然失色。"),
    ("q07-optB.mp3", "選項B：貨真價實。"),
    ("q07-optC.mp3", "選項C：名聞遐邇。"),
    ("q07-optD.mp3", "選項D：俄頃。"),

    # Q8
    ("q08-question.mp3", "第8題。雖然這件衣服的包裝很精美，但就質料而言，其實比舊的還空格。"),
    ("q08-optA.mp3", "選項A：貨真價實。"),
    ("q08-optB.mp3", "選項B：遜色。"),
    ("q08-optC.mp3", "選項C：名聞遐邇。"),
    ("q08-optD.mp3", "選項D：五花八門。")
]

print(f"Generating {len(audio_items)} audio clips...")
for filename, text in audio_items:
    tts_to_mp3(text, filename, force=True)

print("Audio generation finished successfully!")
