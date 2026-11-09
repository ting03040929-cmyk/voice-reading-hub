import os
import wave
import tempfile
import win32com.client
import lameenc

out_dir = os.path.join(os.path.dirname(__file__), "..", "materials", "audio", "eating-ice-concept-matching-quiz")
out_dir = os.path.abspath(out_dir)
os.makedirs(out_dir, exist_ok=True)

voice = win32com.client.Dispatch("SAPI.SpVoice")
voice.Rate = -1

for token in voice.GetVoices():
    desc = token.GetDescription().lower()
    tid = token.Id.lower()
    if "yating" in desc or "yating" in tid:
        voice.Voice = token
        break
    if "hanhan" in desc or "hanhan" in tid:
        voice.Voice = token

print(f"Using SAPI Voice: {voice.Voice.GetDescription()}")

def tts_to_mp3(text: str, filename: str):
    target_mp3 = os.path.join(out_dir, filename)
    if os.path.exists(target_mp3) and os.path.getsize(target_mp3) > 0:
        print(f"Skipping existing: {filename}")
        return

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_wav = tmp.name

    try:
        file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
        file_stream.Open(tmp_wav, 3)
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

sec2_items = [
    ("intro.mp3", "第二大題：生字語詞，句子概念配對。請將生字語詞，配對到最符合句子意思的選項。選項有：A 黯然失色、B 五花八門、C 遜色、D 貨真價實、E 垂涎三尺、F 名聞遐邇、G 俄頃、H 消失殆盡。"),
    ("opt-A.mp3", "選項A：黯然失色。"),
    ("opt-B.mp3", "選項B：五花八門。"),
    ("opt-C.mp3", "選項C：遜色。"),
    ("opt-D.mp3", "選項D：貨真價實。"),
    ("opt-E.mp3", "選項E：垂涎三尺。"),
    ("opt-F.mp3", "選項F：名聞遐邇。"),
    ("opt-G.mp3", "選項G：俄頃。"),
    ("opt-H.mp3", "選項H：消失殆盡。"),
    ("q01.mp3", "第1題。括號，形容東西真材實料，價格公道，誠實不騙人。提示：與信用、實在有關的詞。"),
    ("q02.mp3", "第2題。括號，一會兒、很短的時間。課文用來形容刨冰很快堆成小冰山。提示：與時間非常短暫有關的詞。"),
    ("q03.mp3", "第3題。括號，失去光彩，課文用來形容如果童年少了吃冰，生活就會變得無趣。提示：與失去光彩、不好看有關的詞。"),
    ("q04.mp3", "第4題。括號，看見美食非常想吃，口水流了三尺長的樣子。提示：與想吃東西流口水有關的詞。"),
    ("q05.mp3", "第5題。括號，遠近皆知，很有名氣。課文用來形容糖廠的冰水和冰棒很有名。提示：與名氣很大、很有名有關的詞。"),
    ("q06.mp3", "第6題。括號，種類繁多，各式各樣。課文用來形容現代社會富裕，冰品選擇很多。提示：與各式各樣、花樣繁多有關的詞。"),
    ("q07.mp3", "第7題。括號，已經大多消失，所剩不多。課文用來形容童年吃冰記憶如今大多消失了。提示：與大多消失、所剩不多有關的詞。"),
    ("q08.mp3", "第8題。括號，比較差、比不上。課文用來形容現代冰品口味可能不如早期的。提示：與比較差、比下去有關的詞。")
]

print(f"Generating {len(sec2_items)} audio clips...")
for fn, text in sec2_items:
    tts_to_mp3(text, fn)

print("Audio generation complete!")
