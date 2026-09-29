import os
import asyncio
import edge_tts

questions_section1 = [
    {
        "id": 1,
        "tts_q": "第1題。躺在舒服的床上，小明閉上眼睛，很快就進入了空格。提示：睡著後作夢的世界。",
        "options": [
            ("a", "A，涼爽"),
            ("b", "B，夢鄉"),
            ("c", "C，藤蔓"),
            ("d", "D，樹梢")
        ]
    },
    {
        "id": 2,
        "tts_q": "第2題。下課時，我看到操場邊的小鳥停在很高很高的空格上唱歌。提示：樹木的末端、最高最尖的地方。",
        "options": [
            ("a", "A，田野"),
            ("b", "B，朦朧"),
            ("c", "C，樹梢"),
            ("d", "D，涼爽")
        ]
    },
    {
        "id": 3,
        "tts_q": "第3題。媽媽脖子上戴著一串白白亮亮的空格項鍊，看起來好高貴。提示：一種在貝殼裡面長出來、圓圓亮亮像寶石的東西。",
        "options": [
            ("a", "A，珍珠"),
            ("b", "B，夢鄉"),
            ("c", "C，山巒"),
            ("d", "D，藤蔓")
        ]
    },
    {
        "id": 4,
        "tts_q": "第4題。阿公在鄉下的空格裡種了很多綠油油的蔬菜和稻米。提示：長滿農作物的大片土地、田地。",
        "options": [
            ("a", "A，夢鄉"),
            ("b", "B，山巒"),
            ("c", "C，田野"),
            ("d", "D，樹梢")
        ]
    },
    {
        "id": 5,
        "tts_q": "第5題。剛睡醒的時候，小華的眼睛覺得空格的，看時鐘都看不清楚。提示：光線不充足或眼睛看過去糊糊的、不夠清楚。",
        "options": [
            ("a", "A，涼爽"),
            ("b", "B，朦朧"),
            ("c", "C，藤蔓"),
            ("d", "D，珍珠")
        ]
    },
    {
        "id": 6,
        "tts_q": "第6題。遠遠望去，那一整排高低起伏、連在一起的空格真漂亮。提示：一座接一座連在一起的山。",
        "options": [
            ("a", "A，山巒"),
            ("b", "B，田野"),
            ("c", "C，樹梢"),
            ("d", "D，夢鄉")
        ]
    },
    {
        "id": 7,
        "tts_q": "第7題。陽台上的牽牛花伸出細細長長的空格，順著鐵窗往上爬。提示：植物細細長長、會抓著東西爬牆的莖。",
        "options": [
            ("a", "A，樹梢"),
            ("b", "B，藤蔓"),
            ("c", "C，涼爽"),
            ("d", "D，朦朧")
        ]
    },
    {
        "id": 8,
        "tts_q": "第8題。吹冷氣的時候，教室裡感覺非常空格，大家上課更有精神。提示：天氣或環境很涼快、舒服，不會讓人滿頭大汗。",
        "options": [
            ("a", "A，涼爽"),
            ("b", "B，田野"),
            ("c", "C，珍珠"),
            ("d", "D，山巒")
        ]
    }
]

questions_section2 = [
    {
        "id": 9,
        "tts_q": "第9題。括號。很多座高高低低的山連在一起，在黑夜裡像靜靜睡著了一樣。提示：和許多座山連在一起有關的詞。"
    },
    {
        "id": 10,
        "tts_q": "第10題。括號。一大片綠色的農田，看過去非常寬廣，常有牛羊在那裡吃草。提示：和大片農田土地有關的詞。"
    },
    {
        "id": 11,
        "tts_q": "第11題。括號。樹木最高、最頂端的地方，課文用來形容夏夜從這裡爬下來。提示：和樹木最高處有關的詞。"
    },
    {
        "id": 12,
        "tts_q": "第12題。括號。植物像繩子一樣細細長長的莖，會抱著架子一直往屋頂上爬。提示：和會爬牆的植物器官有關的詞。"
    },
    {
        "id": 13,
        "tts_q": "第13題。括號。圓圓亮亮的東西，課文用來比喻夜空中一閃一閃的滿天星星。提示：和圓圓亮亮的寶石物品有關的詞。"
    },
    {
        "id": 14,
        "tts_q": "第14題。括號。吹到皮膚上覺得很舒服、很涼快，身體不會流汗的溫度。提示：和舒服涼快的天氣感覺有關的詞。"
    },
    {
        "id": 15,
        "tts_q": "第15題。括號。小朋友躺在床上闔上眼睛睡著了，開始在腦海裡開心作夢的地方。提示：和睡覺與作夢世界有關的詞。"
    },
    {
        "id": 16,
        "tts_q": "第16題。括號。眼睛看過去糊糊的、不清楚，好像有一層霧擋在前面一樣。提示：和景物糊糊的、看不清楚有關的詞。"
    }
]

vocab_options_section2 = [
    ("a", "A，田野"),
    ("b", "B，山巒"),
    ("c", "C，樹梢"),
    ("d", "D，藤蔓"),
    ("e", "E，珍珠"),
    ("f", "F，涼爽"),
    ("g", "G，夢鄉"),
    ("h", "H，朦朧")
]

section2_intro_tts = "第二大題：生字語詞－句子概念配對。請將生字語詞，配對到最符合句子意思的選項。選項A，田野。選項B，山巒。選項C，樹梢。選項D，藤蔓。選項E，珍珠。選項F，涼爽。選項G，夢鄉。選項H，朦朧。"

async def main():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "materials", "audio", "summer-night-vocab-quiz")
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    print(f"Output directory: {out_dir}")

    sem = asyncio.Semaphore(5)

    async def synth(text, filename):
        filepath = os.path.join(out_dir, filename)
        async with sem:
            tts = edge_tts.Communicate(text, voice="zh-TW-HsiaoChenNeural", rate="-4%")
            await tts.save(filepath)
            print(f"Generated: {filename} ({len(text)} chars)")

    tasks = []

    # Section 1
    for q in questions_section1:
        qid_str = f"q{q['id']:02d}"
        tasks.append(synth(q["tts_q"], f"{qid_str}-question.mp3"))
        for opt_key, opt_text in q["options"]:
            tasks.append(synth(opt_text, f"{qid_str}-{opt_key}.mp3"))

    # Section 2 questions
    for q in questions_section2:
        qid_str = f"q{q['id']:02d}"
        tasks.append(synth(q["tts_q"], f"{qid_str}-question.mp3"))

    # Section 2 common vocab options (A~H)
    for opt_key, opt_text in vocab_options_section2:
        tasks.append(synth(opt_text, f"vocab-{opt_key}.mp3"))

    # Section 2 intro
    tasks.append(synth(section2_intro_tts, "section2-intro.mp3"))

    print(f"Total audio clips to generate: {len(tasks)}")
    await asyncio.gather(*tasks)
    print("All audio clips generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
