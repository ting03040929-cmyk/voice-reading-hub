import os
import wave
import tempfile
import win32com.client
import lameenc

out_dir = os.path.join(os.path.dirname(__file__), "..", "materials", "audio", "zhongpu-115-exam1")
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

# 大題與導讀音訊
intros = [
    ("sec-fill-a-intro.mp3", "三大題第一部分，課文詞語選填。請從詞語框中選出適當的詞語，填入空格。"),
    ("word-jiedeng.mp3", "詞語：街燈"),
    ("word-tianye.mp3", "詞語：田野"),
    ("word-mitang.mp3", "詞語：蜜糖"),
    ("word-menglong.mp3", "詞語：朦朧"),
    ("sec-fill-b-intro.mp3", "三大題第二部分，語詞填充。請從下面的語詞中選出適當的答案填入空格。"),
    ("word-shushao.mp3", "語詞：樹梢"),
    ("word-zhenzhu.mp3", "語詞：珍珠"),
    ("word-liangshuang.mp3", "語詞：涼爽"),
    ("word-mengxiang.mp3", "語詞：夢鄉"),
    ("word-shanluan.mp3", "語詞：山巒"),
    ("word-tengman.mp3", "語詞：藤蔓"),
    ("sec-choice-intro.mp3", "五、選擇題，注釋。每題2分，共16分。請選出正確的答案。"),
    ("sec-reading-intro.mp3", "六、閱讀理解。請根據夏夜課文回答問題。每題2分，共20分。"),
    ("sec-literacy-intro.mp3", "七、素養題。共8分。請仔細閱讀並回答問題。"),
    ("poster-info.mp3", "閱讀資料：中埔國中夏夜星空草地音樂會。時間：晚上7點開始。地點：學校大操場草坪。注意事項：第一，請準時入場，安靜坐好欣賞表演。第二，請勿大聲聊天，禁止在場內跑步。歡迎全校親師生一起來享受美麗夏夜！")
]

# 填充題 A 部分共用選項音訊 (Q01~Q04)
fill_a_options = [
    ("fill-a-opt-a.mp3", "選項A，街燈"),
    ("fill-a-opt-b.mp3", "選項B，田野"),
    ("fill-a-opt-c.mp3", "選項C，蜜糖"),
    ("fill-a-opt-d.mp3", "選項D，朦朧")
]

# 填充題 B 部分共用選項音訊 (Q05~Q12)
fill_b_options = [
    ("fill-b-opt-a.mp3", "選項A，田野"),
    ("fill-b-opt-b.mp3", "選項B，樹梢"),
    ("fill-b-opt-c.mp3", "選項C，珍珠"),
    ("fill-b-opt-d.mp3", "選項D，涼爽"),
    ("fill-b-opt-e.mp3", "選項E，夢鄉"),
    ("fill-b-opt-f.mp3", "選項F，朦朧"),
    ("fill-b-opt-g.mp3", "選項G，山巒"),
    ("fill-b-opt-h.mp3", "選項H，藤蔓")
]

# 題目清單
questions = [
    # 三、填充 Part A
    {
        "id": 1,
        "q": "第1題。蝴蝶和蜜蜂們帶著花朵的空格回來了。",
        "opts": []
    },
    {
        "id": 2,
        "q": "第2題。羊隊和牛群告別了空格回家了。",
        "opts": []
    },
    {
        "id": 3,
        "q": "第3題。空格地山巒靜靜地睡了。",
        "opts": []
    },
    {
        "id": 4,
        "q": "第4題。當空格亮起來向村莊道過晚安，夏天的夜就輕輕地來了。",
        "opts": []
    },

    # 三、填充 Part B
    {
        "id": 5,
        "q": "第5題。小朋友睡著後，快樂地進入了空格。提示：睡覺、作夢的世界。",
        "opts": []
    },
    {
        "id": 6,
        "q": "第6題。遠遠看去，一座一座連在一起的空格很漂亮。提示：很多座山連在一起。",
        "opts": []
    },
    {
        "id": 7,
        "q": "第7題。夜裡有霧，遠處的山看起來空格的。提示：看不清楚、糊糊的。",
        "opts": []
    },
    {
        "id": 8,
        "q": "第8題。小鳥停在高高的空格上唱歌。提示：樹木最高的地方。",
        "opts": []
    },
    {
        "id": 9,
        "q": "第9題。南瓜伸長了空格，慢慢爬上瓜架。提示：植物細長、會爬的莖。",
        "opts": []
    },
    {
        "id": 10,
        "q": "第10題。風吹過來，晚上感覺很空格。提示：涼快、舒服。",
        "opts": []
    },
    {
        "id": 11,
        "q": "第11題。羊隊和牛群在大片的空格吃草。提示：大片的農田。",
        "opts": []
    },
    {
        "id": 12,
        "q": "第12題。天空中閃閃發亮的星星，好像一顆顆空格。提示：圓圓亮亮的寶石。",
        "opts": []
    },

    # 五、選擇題，注釋
    {
        "id": 13,
        "q": "第13題。樹梢是指樹木的哪裡？",
        "opts": [("a", "選項A，樹根"), ("b", "選項B，樹木最高的地方"), ("c", "選項C，樹幹"), ("d", "選項D，樹葉下面")]
    },
    {
        "id": 14,
        "q": "第14題。田野是指什麼地方？",
        "opts": [("a", "選項A，寬廣的農田"), ("b", "選項B，熱鬧的市場"), ("c", "選項C，教室"), ("d", "選項D，海邊")]
    },
    {
        "id": 15,
        "q": "第15題。夢鄉是指什麼？",
        "opts": [("a", "選項A，遊樂園"), ("b", "選項B，睡著後作夢的世界"), ("c", "選項C，家鄉"), ("d", "選項D，山上")]
    },
    {
        "id": 16,
        "q": "第16題。朦朧是什麼樣子？",
        "opts": [("a", "選項A，看得很清楚"), ("b", "選項B，又亮又熱"), ("c", "選項C，糊糊的、不清楚"), ("d", "選項D，很吵鬧")]
    },
    {
        "id": 17,
        "q": "第17題。涼爽是什麼感覺？",
        "opts": [("a", "選項A，涼快又舒服"), ("b", "選項B，又熱又渴"), ("c", "選項C，很冷很痛"), ("d", "選項D，很暗")]
    },
    {
        "id": 18,
        "q": "第18題。藤蔓是什麼？",
        "opts": [("a", "選項A，細長、會攀爬的植物莖"), ("b", "選項B，一種昆蟲"), ("c", "選項C，一條小河"), ("d", "選項D，一盞街燈")]
    },
    {
        "id": 19,
        "q": "第19題。珍珠在課文中用來比喻什麼？",
        "opts": [("a", "選項A，雨傘"), ("b", "選項B，天上的星星"), ("c", "選項C，山巒"), ("d", "選項D，月亮")]
    },
    {
        "id": 20,
        "q": "第20題。山巒是指什麼？",
        "opts": [("a", "選項A，一座小橋"), ("b", "選項B，一座座連在一起的山"), ("c", "選項C，一片花園"), ("d", "選項D，一間房子")]
    },

    # 六、閱讀理解
    {
        "id": 21,
        "q": "第21題。誰帶著花朵的蜜糖回來了？",
        "opts": [("a", "選項A，蝴蝶和蜜蜂們"), ("b", "選項B，羊隊和牛群"), ("c", "選項C，小雞和小鴨"), ("d", "選項D，小弟弟和小妹妹")]
    },
    {
        "id": 22,
        "q": "第22題。羊隊和牛群告別了哪裡，準備回家？",
        "opts": [("a", "選項A，山坡"), ("b", "選項B，田野"), ("c", "選項C，村莊"), ("d", "選項D，花園")]
    },
    {
        "id": 23,
        "q": "第23題。火紅的太陽滾著什麼回家了？",
        "opts": [("a", "選項A，火輪子"), ("b", "選項B，大皮球"), ("c", "選項C，一枚銀幣"), ("d", "選項D，一顆珍珠")]
    },
    {
        "id": 24,
        "q": "第24題。街燈亮起來向村莊道晚安後，什麼來了？",
        "opts": [("a", "選項A，白天"), ("b", "選項B，夏天的夜"), ("c", "選項C，大雨"), ("d", "選項D，冬天")]
    },
    {
        "id": 25,
        "q": "第25題。夏夜從椰子樹的哪裡輕輕爬下來？",
        "opts": [("a", "選項A，樹根"), ("b", "選項B，樹梢"), ("c", "選項C，樹幹中間"), ("d", "選項D，樹下的草地")]
    },
    {
        "id": 26,
        "q": "第26題。夏夜在天空撒了滿天的什麼？",
        "opts": [("a", "選項A，糖果"), ("b", "選項B，珍珠"), ("c", "選項C，花瓣"), ("d", "選項D，雨傘")]
    },
    {
        "id": 27,
        "q": "第27題。小弟弟和小妹妹聽完誰的故事後走向夢鄉？",
        "opts": [("a", "選項A，老師"), ("b", "選項B，老祖母"), ("c", "選項C，鄰居"), ("d", "選項D，警察")]
    },
    {
        "id": 28,
        "q": "第28題。大家都睡了，只有哪一種植物還醒著？",
        "opts": [("a", "選項A，南瓜"), ("b", "選項B，水稻"), ("c", "選項C，椰子樹"), ("d", "選項D，玫瑰花")]
    },
    {
        "id": 29,
        "q": "第29題。南瓜伸長了什麼，往屋頂上爬？",
        "opts": [("a", "選項A，樹梢"), ("b", "選項B，藤蔓"), ("c", "選項C，小橋"), ("d", "選項D，街燈")]
    },
    {
        "id": 30,
        "q": "第30題。夜風跟著誰，在美麗的夏夜裡愉快旅行？",
        "opts": [("a", "選項A，提燈的螢火蟲"), ("b", "選項B，羊隊和牛群"), ("c", "選項C，蝴蝶和蜜蜂"), ("d", "選項D，小雞和小鴨")]
    },

    # 七、素養題
    {
        "id": 31,
        "q": "第31題。晚上起霧了，遠遠的山看起來不清楚。這時可以用課文中的哪一個詞？",
        "opts": [("a", "選項A，朦朧"), ("b", "選項B，涼爽"), ("c", "選項C，愉快"), ("d", "選項D，迎接")]
    },
    {
        "id": 32,
        "q": "第32題。小美在田裡看到一隻螢火蟲。根據課文，螢火蟲在夏夜裡做什麼？",
        "opts": [("a", "選項A，睡覺"), ("b", "選項B，提燈旅行"), ("c", "選項C，吃草"), ("d", "選項D，爬上屋頂")]
    },
    {
        "id": 33,
        "q": "第33題。課文把星星寫成滿天的珍珠，這樣寫讓我們感覺夏夜怎麼樣？",
        "opts": [("a", "選項A，美麗、閃亮"), ("b", "選項B，吵鬧、可怕"), ("c", "選項C，寒冷、黑暗"), ("d", "選項D，生氣、難過")]
    },
    {
        "id": 34,
        "q": "第34題。第1小題。音樂會幾點開始？",
        "opts": [("a", "選項A，晚上6點"), ("b", "選項B，晚上7點"), ("c", "選項C，晚上8點")]
    },
    {
        "id": 35,
        "q": "第35題。第2小題。聽音樂會時，怎麼做比較合適？",
        "opts": [("a", "選項A，安靜坐好"), ("b", "選項B，大聲聊天"), ("c", "選項C，在場內跑步")]
    }
]

def main():
    print("Starting MP3 batch generation...")
    # 1. 大題導言
    for filename, text in intros:
        tts_to_mp3(text, filename)

    # 2. 填充題 A 選項
    for filename, text in fill_a_options:
        tts_to_mp3(text, filename)

    # 3. 填充題 B 選項
    for filename, text in fill_b_options:
        tts_to_mp3(text, filename)

    # 4. 題目與個別選項
    for q in questions:
        qid_str = f"q{q['id']:02d}"
        tts_to_mp3(q["q"], f"{qid_str}-question.mp3")
        for opt_key, opt_text in q["opts"]:
            tts_to_mp3(opt_text, f"{qid_str}-{opt_key}.mp3")

    print("All audio clips generated successfully!")

if __name__ == "__main__":
    main()
