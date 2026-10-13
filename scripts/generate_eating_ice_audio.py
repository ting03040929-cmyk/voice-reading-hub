import os
import wave
import tempfile
import win32com.client
import lameenc

# Audio output directory
out_dir = os.path.join(os.path.dirname(__file__), "..", "materials", "audio", "eating-ice-vocab-quiz")
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
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_wav = tmp.name

    try:
        # SAPI to temporary WAV
        file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
        file_stream.Open(tmp_wav, 3)  # 3 = SSFMCreateForWrite
        voice.AudioOutputStream = file_stream
        voice.Speak(text)
        file_stream.Close()
        voice.AudioOutputStream = None

        # Convert WAV to MP3 using lameenc
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

# Audio tasks
audio_items = [
    # Section 1
    ("section1-intro.mp3", "第一大題：語詞配意思。在括號裡寫上正確意思的代號。"),
    ("meaning-a.mp3", "選項A。種類很多，有各式各樣的東西。"),
    ("meaning-b.mp3", "選項B。很短的時間，一下子。"),
    ("meaning-c.mp3", "選項C。名氣很大，遠的、近的人都知道。"),
    ("meaning-d.mp3", "選項D。幾乎全部不見了。"),
    ("meaning-e.mp3", "選項E。和別的比起來，變得不精彩。"),
    ("meaning-f.mp3", "選項F。口水流得很長，形容非常想吃。"),
    ("meaning-g.mp3", "選項G。東西是真的，價錢也實在。"),
    ("meaning-h.mp3", "選項H。比不上別人，比較差。"),
    ("q01-question.mp3", "第1題。語詞：黯然失色。請選出正確意思的代號。"),
    ("q02-question.mp3", "第2題。語詞：五花八門。請選出正確意思的代號。"),
    ("q03-question.mp3", "第3題。語詞：遜色。請選出正確意思的代號。"),
    ("q04-question.mp3", "第4題。語詞：貨真價實。請選出正確意思的代號。"),
    ("q05-question.mp3", "第5題。語詞：垂涎三尺。請選出正確意思的代號。"),
    ("q06-question.mp3", "第6題。語詞：名聞遐邇。請選出正確意思的代號。"),
    ("q07-question.mp3", "第7題。語詞：俄頃。請選出正確意思的代號。"),
    ("q08-question.mp3", "第8題。語詞：消失殆盡。請選出正確意思的代號。"),

    # Section 2 Word Bank
    ("section2-intro.mp3", "第二大題：選語詞填句子。從語詞盒裡選出合適的語詞，寫在空格上。每個語詞只用一次。語詞盒有：黯然失色、五花八門、遜色、貨真價實、垂涎三尺、名聞遐邇、俄頃、消失殆盡。"),
    ("bank-word1.mp3", "選項1，黯然失色。"),
    ("bank-word2.mp3", "選項2，五花八門。"),
    ("bank-word3.mp3", "選項3，遜色。"),
    ("bank-word4.mp3", "選項4，貨真價實。"),
    ("bank-word5.mp3", "選項5，垂涎三尺。"),
    ("bank-word6.mp3", "選項6，名聞遐邇。"),
    ("bank-word7.mp3", "選項7，俄頃。"),
    ("bank-word8.mp3", "選項8，消失殆盡。"),

    # Section 2 Questions
    ("q09-question.mp3", "第9題。沒有了煙火，中秋節晚會就空格了。"),
    ("q10-question.mp3", "第10題。百貨公司的玩具空格，有積木、娃娃，還有遙控車。"),
    ("q11-question.mp3", "第11題。我做的蛋糕，一點也不比蛋糕店空格。"),
    ("q12-question.mp3", "第12題。阿嬤種的高麗菜沒有灑農藥，又甜又便宜，真是空格。"),
    ("q13-question.mp3", "第13題。聞到烤肉的香味，弟弟空格，一直在旁邊等。"),
    ("q14-question.mp3", "第14題。日月潭的風景空格，很多遊客專程來玩。"),
    ("q15-question.mp3", "第15題。媽媽才把餅乾放在桌上，空格之間就被吃完了。"),
    ("q16-question.mp3", "第16題。冰淇淋放在太陽下，一下子就融化得空格了。"),

    # Section 3
    ("section3-intro.mp3", "第三大題：畫畫看、寫寫看。選一個你最喜歡的語詞，畫一張圖，或寫一個句子。"),
    ("q17-question.mp3", "第17題。選一個你最喜歡的語詞，畫一張圖，或寫一個句子。我選的語詞是空格。")
]

print(f"Total audio clips to generate: {len(audio_items)}")
for fn, text in audio_items:
    tts_to_mp3(text, fn)

print("All audio files generated successfully!")
