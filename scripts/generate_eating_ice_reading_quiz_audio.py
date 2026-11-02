import os
import wave
import tempfile
import win32com.client
import lameenc

# Audio output directory
out_dir = os.path.join(os.path.dirname(__file__), "..", "materials", "audio", "eating-ice-reading-quiz")
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
    ("intro.mp3", "吃冰的滋味，課文閱讀測驗。請仔細聽題目，選出最適合的答案。"),
    ("test-sound.mp3", "語音測試正常，歡迎使用吃冰的滋味閱讀測驗報讀練習。"),
    # Q1
    ("q01-question.mp3", "第1題。作者認為童年如果沒有冰，生活會變得如何？"),
    ("q01-opt1.mp3", "選項1，更充實。"),
    ("q01-opt2.mp3", "選項2，黯然失色。"),
    ("q01-opt3.mp3", "選項3，沒有變化。"),
    ("q01-opt4.mp3", "選項4，更有動力。"),
    # Q2
    ("q02-question.mp3", "第2題。現在社會富裕了，小孩對於冰品的選擇情況為何？"),
    ("q02-opt1.mp3", "選項1，只有單一口味。"),
    ("q02-opt2.mp3", "選項2，變得越來越少。"),
    ("q02-opt3.mp3", "選項3，五花八門。"),
    ("q02-opt4.mp3", "選項4，沒有任何進步。"),
    # Q3
    ("q03-question.mp3", "第3題。文中提到現代的小孩子對冰的喜愛程度可以用哪個詞形容？"),
    ("q03-opt1.mp3", "選項1，嗜冰如命。"),
    ("q03-opt2.mp3", "選項2，不屑一顧。"),
    ("q03-opt3.mp3", "選項3，偶爾嘗試。"),
    ("q03-opt4.mp3", "選項4，可有可無。"),
    # Q4
    ("q04-question.mp3", "第4題。根據課文，早期的生意人有什麼特質，讓冰品口味值得信賴？"),
    ("q04-opt1.mp3", "選項1，價格昂貴。"),
    ("q04-opt2.mp3", "選項2，只賣外國產品。"),
    ("q04-opt3.mp3", "選項3，貨真價實。"),
    ("q04-opt4.mp3", "選項4，追求包裝華麗。"),
    # Q5
    ("q05-question.mp3", "第5題。作者小時候住在糖廠宿舍，當時最受歡迎的冰品口味是什麼？"),
    ("q05-opt1.mp3", "選項1，芋頭與鳳梨。"),
    ("q05-opt2.mp3", "選項2，巧克力與香草。"),
    ("q05-opt3.mp3", "選項3，草莓與薄荷。"),
    ("q05-opt4.mp3", "選項4，花生與紅豆。"),
    # Q6
    ("q06-question.mp3", "第6題。根據課文，當時一枝冰棒的售價是多少錢？"),
    ("q06-opt1.mp3", "選項1，一毛錢。"),
    ("q06-opt2.mp3", "選項2，一元錢。"),
    ("q06-opt3.mp3", "選項3，五毛錢。"),
    ("q06-opt4.mp3", "選項4，十元錢。"),
    # Q7
    ("q07-question.mp3", "第7題。關於糖廠冰棒的描述，下列何者正確？"),
    ("q07-opt1.mp3", "選項1，含有大量糖精。"),
    ("q07-opt2.mp3", "選項2，使用自來水製成。"),
    ("q07-opt3.mp3", "選項3，使用砂糖，乾淨衛生。"),
    ("q07-opt4.mp3", "選項4，吃起來苦苦的。"),
    # Q8
    ("q08-question.mp3", "第8題。小孩子吃完冰棒後，會把收集起來的竹桿拿來做什麼？"),
    ("q08-opt1.mp3", "選項1，當作柴火。"),
    ("q08-opt2.mp3", "選項2，拿來做遊戲。"),
    ("q08-opt3.mp3", "選項3，拿去賣錢。"),
    ("q08-opt4.mp3", "選項4，當作筷子。"),
    # Q9
    ("q09-question.mp3", "第9題。文中提到的刨冰配料中，包含下列哪一項？"),
    ("q09-opt1.mp3", "選項1，草莓。"),
    ("q09-opt2.mp3", "選項2，巧克力。"),
    ("q09-opt3.mp3", "選項3，芋頭。"),
    ("q09-opt4.mp3", "選項4，愛玉。"),
    # Q10
    ("q10-question.mp3", "第10題。賣芋冰的小販在叫賣時，會發出什麼樣的聲音來吸引注意？"),
    ("q10-opt1.mp3", "選項1，大聲喊叫。"),
    ("q10-opt2.mp3", "選項2，吹奏樂器。"),
    ("q10-opt3.mp3", "選項3，搖動鈴鐺。"),
    ("q10-opt4.mp3", "選項4，播放音樂。"),
    # Q11
    ("q11-question.mp3", "第11題。作者每到夏天吃冰時，心情通常會是如何？"),
    ("q11-opt1.mp3", "選項1，想起童年美好往事。"),
    ("q11-opt2.mp3", "選項2，感到十分悲傷。"),
    ("q11-opt3.mp3", "選項3，擔心冰太甜。"),
    ("q11-opt4.mp3", "選項4，覺得口渴想喝水。"),
    # Q12
    ("q12-question.mp3", "第12題。作者認為雖然冰淇淋味道好，但什麼才是最甜美的？"),
    ("q12-opt1.mp3", "選項1，芋冰的滋味。"),
    ("q12-opt2.mp3", "選項2，轉盤遊戲的獎勵。"),
    ("q12-opt3.mp3", "選項3，童年的記憶。"),
    ("q12-opt4.mp3", "選項4，清脆的鈴鐺聲。"),
    # Q13
    ("q13-question.mp3", "第13題。除了直接購買外，以前的人還能透過哪種方式來得到芋冰？"),
    ("q13-opt1.mp3", "選項1，玩射擊遊戲賭冰。"),
    ("q13-opt2.mp3", "選項2，幫小販推腳踏車。"),
    ("q13-opt3.mp3", "選項3，用玩具交換。"),
    ("q13-opt4.mp3", "選項4，唱歌給小販聽。"),
    # Q14
    ("q14-question.mp3", "第14題。賣芋冰的小販主要是騎乘什麼交通工具沿街叫賣？"),
    ("q14-opt1.mp3", "選項1，摩托車。"),
    ("q14-opt2.mp3", "選項2，腳踏車。"),
    ("q14-opt3.mp3", "選項3，三輪車。"),
    ("q14-opt4.mp3", "選項4，推車。"),
    # Q15
    ("q15-question.mp3", "第15題。根據課文內容，下列關於作者童年吃冰記憶的敘述何者正確？"),
    ("q15-opt1.mp3", "選項1，那種記憶現在隨處可見。"),
    ("q15-opt2.mp3", "選項2，現在的冰淇淋比記憶更甜美。"),
    ("q15-opt3.mp3", "選項3，童年吃冰的記憶多已消失殆盡。"),
    ("q15-opt4.mp3", "選項4，作者不喜歡芋冰的味道。"),
]

print(f"Total audio files to generate: {len(audio_items)}")
for filename, text in audio_items:
    tts_to_mp3(text, filename)
print("Finished audio generation!")
