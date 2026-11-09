import os
import wave
import tempfile
import win32com.client
import lameenc

# Audio output directory
out_dir = os.path.join(os.path.dirname(__file__), "..", "materials", "audio", "eating-ice-vocab-fill-quiz")
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
    # Intro
    ("intro.mp3", "第一大題：生字語詞，句子填充題。請從語詞盒中選出合適的語詞，填入句子空格中。語詞盒有：黯然失色、五花八門、遜色、貨真價實、垂涎三尺、名聞遐邇、俄頃、消失殆盡。"),
    
    # Word bank
    ("word-1.mp3", "語詞一：黯然失色。"),
    ("word-2.mp3", "語詞二：五花八門。"),
    ("word-3.mp3", "語詞三：遜色。"),
    ("word-4.mp3", "語詞四：貨真價實。"),
    ("word-5.mp3", "語詞五：垂涎三尺。"),
    ("word-6.mp3", "語詞六：名聞遐邇。"),
    ("word-7.mp3", "語詞七：俄頃。"),
    ("word-8.mp3", "語詞八：消失殆盡。"),
    
    # 8 Questions (Blank is read as "空格", NO answers revealed)
    ("q01-question.mp3", "第1題。這家老字號的麵店以空格、料多實在聞名，大家都愛去吃。提示：形容東西是真貨，價格也實在，講求信用。"),
    ("q02-question.mp3", "第2題。這位明星的歌聲和表演十分出色，相較之下，其他表演者都空格。提示：形容失去光彩與吸引力，顯得不夠亮眼。"),
    ("q03-question.mp3", "第3題。廚房裡傳來烤麵包的陣陣香味，讓門口的小狗看得空格。提示：形容非常想吃的樣子，口水都快流下來了。"),
    ("q04-question.mp3", "第4題。百貨公司裡的玩具商品空格，讓小明看得眼花撩亂，不知道選哪一個。提示：形容花樣繁多，變化非常多。"),
    ("q05-question.mp3", "第5題。這家糖廠的紅豆冰棒在當地空格，很多遊客專程開車來買。提示：名聲非常大，遠近的人都知道。"),
    ("q06-question.mp3", "第6題。剛才天空還出大太陽，空格便下起了大雨。提示：形容時間很短，一會兒的時間。"),
    ("q07-question.mp3", "第7題。以前住在這裡的老鄰居都搬走了，當年的老街景象已經空格。提示：形容大多消失，所剩不多。"),
    ("q08-question.mp3", "第8題。雖然新手機的功能很多，但就耐用度來說，可能比舊款手機還空格。提示：比不上別人，顯得比較差。")
]

print(f"Generating {len(audio_items)} audio clips...")
for filename, text in audio_items:
    tts_to_mp3(text, filename)

print("Audio generation complete!")
