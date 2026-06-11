import json
import os
import csv
from flask import Flask, render_template, request, make_response, redirect, jsonify
from flask_cors import CORS

app = Flask(__name__)

# 🔒 啟用 CORS，允許你的 GitHub 網頁安全地過來抓取 Sana 的資料
# 將來你的 GitHub 網址建立後，可以把 '*' 改成你的 GitHub 專屬網址，安全性更高
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ----------------------------------------------------
# 🪄 SANA 魔法百科專屬：演唱會資料 API 通道
# ----------------------------------------------------
@app.route('/api/sana-wiki/concerts', methods=['GET'])
def get_sana_concerts():
    # 定位到我們剛剛建立的獨立「魔法行李箱」子目錄
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'sana_wiki', 'data', 'concerts.json')

    if not os.path.exists(json_path):
        return jsonify({"error": "魔法文獻遺失，找不到演唱會資料。"}), 404

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            concert_data = json.load(f)
        return jsonify(concert_data)
    except Exception as e:
        return jsonify({"error": f"讀取魔法文獻失敗: {str(e)}"}), 500


# 🔒 密碼守護盾
CORRECT_HASH = "da4cbb4ea92bb3b7b3b9b4a45a33c6ce0fc52cf66236b2f7b1fc68fb110bebc0"

# 🏰 項目時空堡壘：全域記憶體快取大腦 (Global Memory Cache)
GLOBAL_CACHE = {
    "welcome_letter": {},
    "timeline": [],
    "sana_parchment": {},
    "sana_profile": {},
    "media": {},
    "music": {},
    "room": {},
    "secret_letter": {}
}

def load_all_json_to_cache():
    """
    這個函式負責在伺服器啟動的一瞬間，把全站 8 個真實 JSON 檔案全部安全吸進記憶體！
    """
    global GLOBAL_CACHE
    try:
        data_dir = os.path.join(app.root_path, 'data')

        for key in GLOBAL_CACHE.keys():
            file_path = os.path.join(data_dir, f"{key}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    GLOBAL_CACHE[key] = json.load(f)
            else:
                print(f"[⚠️ 快取警告] 找不到檔案: {key}.json，已初始化為空結構防禦。")

        print("[堡壘大腦] 🪐 全站 8 大 JSON 資料庫已完美載入記憶體保險箱！")
    except Exception as e:
        print(f"[💥 快取核心崩潰] 原因: {str(e)}")

# 💡 伺服器啟動一瞬間通電灌錄！
with app.app_context():
    load_all_json_to_cache()


def get_current_language():
    return request.cookies.get('lang', 'zh')


# ==============================================================================
# 🚪 傳統多頁面架構 (MPA) 核心路由安全通電區
# ==============================================================================

@app.route('/')
def home():
    # 1. 先看有沒有點過右上角羅盤留下的 Cookie 令牌
    lang = request.cookies.get('lang')

    # 2. 💡 智慧導航核心：如果是初次進站（沒有 Cookie），Python 自動看他是哪國瀏覽器！
    if not lang:
        browser_lang = request.headers.get('Accept-Language', '')
        if 'ja' in browser_lang:
            lang = 'ja'
        elif 'ko' in browser_lang:
            lang = 'ko'
        else:
            lang = 'zh' # 預設一律奉上最親切的繁體中文

    # 3. 原封不動繼承您原本的快取與渲染結構
    welcome_data = GLOBAL_CACHE.get("welcome_letter", {})
    localized_letter = {}
    if welcome_data:
        localized_letter = {
            "header": welcome_data.get("header", {}).get(lang, ""),
            "sub_header": welcome_data.get("sub_header", {}).get(lang, ""),
            "p1": welcome_data.get("p1", {}).get(lang, ""),
            "p2": welcome_data.get("p2", {}).get(lang, ""),
            "p3": welcome_data.get("p3", {}).get(lang, ""),
            "p4": welcome_data.get("p4", {}).get(lang, ""),
            "p5": welcome_data.get("p5", {}).get(lang, ""),
            "p6": welcome_data.get("p6", {}).get(lang, ""),
            "p7": welcome_data.get("p7", {}).get(lang, ""),
            "btn_magic": welcome_data.get("btn_magic", {}).get(lang, ""),
            "btn_reality": welcome_data.get("btn_reality", {}).get(lang, "")
        }
    return render_template('letter.html', letter=localized_letter, current_lang=lang)


@app.route('/castle')
def castle():
    lang = get_current_language()
    timeline_data = GLOBAL_CACHE.get("timeline", [])
    parchment_data = GLOBAL_CACHE.get("sana_parchment", {})

    localized_timeline = []
    for item in timeline_data:
        localized_timeline.append({
            "year": item["year"],
            "date": item["date"].get(lang, ""),
            "title": item["title"].get(lang, ""),
            "image": item["image"],
            "position": item.get("position", "50% 50%"),
            "fit_mode": item.get("fit_mode", "cover"),
            "event": item["event"].get(lang, ""),
            "achievement": item["achievement"].get(lang, "")
        })

    localized_parchment = {}
    if parchment_data:
        localized_parchment = {
            "reg_title": parchment_data.get("parchment_meta", {}).get("registry_title", {}).get(lang, ""),
            "name": parchment_data.get("core_identity", {}).get("full_name", {}).get(lang, ""),
            "birth": parchment_data.get("core_identity", {}).get("birthday", {}).get(lang, ""),
            "place": parchment_data.get("core_identity", {}).get("birthplace", {}).get(lang, ""),
            "blood": parchment_data.get("core_identity", {}).get("blood_status", {}).get(lang, ""),
            "mbti": parchment_data.get("core_identity", {}).get("mbti_astral", {}).get(lang, ""),
            "names": parchment_data.get("core_identity", {}).get("ancient_aliases", {}).get(lang, ""),
            "core": parchment_data.get("core_identity", {}).get("wand_essence", {}).get(lang, "")
        }
    return render_template('castle.html', timeline=localized_timeline, profile=localized_parchment, current_lang=lang)


@app.route('/charms')
def charms():
    lang = get_current_language()
    full_data = GLOBAL_CACHE.get("music", [])

    localized_music = []
    for item in full_data:
        localized_music.append({
            "id": item["id"],
            "year": item["year"].get(lang, ""),
            "album": item["album"].get(lang, ""),
            "title": item["title"],
            "cover": item["cover"],
            "position": item.get("position", "50% 50%"),
            "type": item["type"].get(lang, ""),
            "description": item["description"].get(lang, ""),
            "magic_effect": item["magic_effect"].get(lang, "")
        })
    return render_template('charms.html', music_books=localized_music, current_lang=lang)


@app.route('/media')
def media():
    """ 4. 全球巡演中控台與儲思盆 (對應：media) """
    lang = get_current_language()

    # 💡 核心優化：從記憶體保險箱提取 media 資料
    full_data = GLOBAL_CACHE.get("media", {})

    # 建立純淨前端網格，準備接受灌錄
    localized_media = {
        "videos": [],
        "concerts": [],
        "history_tours": {"world": [], "physical": [], "online": []}
    }

    if full_data:
        # 🎬 1. 儲思盆影片快取處理
        for vid in full_data.get("videos", []):
            localized_media["videos"].append({
                "id": vid["id"],
                "title": vid.get("title", {}).get(lang, ""),
                "youtube_id": vid.get("youtube_id", ""),
                "description": vid.get("description", {}).get(lang, "")
            })

        # 🗺️ 2. 地圖演唱會錨點座標分配
        for con in full_data.get("concerts", []):
            localized_media["concerts"].append({
                "id": con["id"],
                "name": con.get("name", {}).get(lang, ""),
                "coords": con.get("coords", "50% 50%"),
                "detail": con.get("detail", {}).get(lang, "")
            })

        # 📜 3. 💡 核心修正：100% 嚴絲合縫對齊 media.json 的歷史巡演結構！
        # 直接使用項目下的語系欄位（.get(lang)），徹底擊碎死鎖，讓轉圈圈當場解開！
        for cat in ["world", "physical", "online"]:
            tours_list = full_data.get("history_tours", {}).get(cat, [])
            for tour in tours_list:
                localized_media["history_tours"][cat].append({
                    "year": tour.get("year", ""),
                    "title": tour.get("title", ""),
                    "detail": tour.get(lang, ""),  # 💡 完美對齊您 JSON 裡最純淨的 "zh"/"ja"/"ko" 欄位！
                    "image": tour.get("image", "")
                })

    # 💡 配送 media_data 給前端，滿血對齊 media.html 的 {{ media_data.videos }}
    return render_template('media.html',
                           media_data=localized_media,
                           current_lang=lang)


@app.route('/room')
def room():
    lang = get_current_language()

    # 💡 核心優化：告別硬碟讀取！直接從 GLOBAL_CACHE 記憶體中取出萬應室資料！
    full_data = GLOBAL_CACHE.get("room", [])

    # --- 100% 嚴絲合縫對齊 room.json 結構與 room.html 的變數期待 ---
    localized_items = []
    for item in full_data:
        localized_items.append({
            "id": item["id"],
            "name": item["name"].get(lang, ""),
            "image": item["image"],
            "style": item.get("position", "50% 50%"),  # 完美配送不切臉網格座標
            "fact": item["fact"].get(lang, "")         # 完美配送對應語系秘聞
        })
    # -------------------------------------------------------------------------

    # 💡 配送 room_items 給前端，完美對齊 room.html 的 {% for item in room_items %}
    return render_template('room.html',
                           room_items=localized_items,
                           current_lang=lang)


@app.route('/lounge', methods=['GET', 'POST'])
def lounge():
    lang = get_current_language()
    csv_path = os.path.join(app.root_path, 'data', 'messages.csv')

    # 🖋️ 1. 寫入管道：當粉絲按下「發送魔法便籤」
    if request.method == 'POST':
        name = request.form.get('wizard_name', '').strip()
        msg = request.form.get('wizard_msg', '').strip()
        if name and msg:
            # (a) 老老實實寫入硬碟永久保存，確保斷電也不會弄丟資料
            with open(csv_path, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([name, msg])

            # (b) 💡 智慧合圍：一微秒內，直接把新留言硬核塞入全域記憶體大腦！
            # 這樣下一個使用者點進來，不需要讀取硬碟，就能「瞬間」看到最新留言！
            if "lounge_messages" not in GLOBAL_CACHE:
                GLOBAL_CACHE["lounge_messages"] = []
            GLOBAL_CACHE["lounge_messages"].insert(0, {"name": name, "message": msg})

        return redirect('/lounge')

    # 📜 2. 讀取管道：當粉絲進房參觀
    # 💡 核心優化：如果記憶體裡有，直接從全域大腦提貨，零硬碟讀寫延遲！
    if "lounge_messages" in GLOBAL_CACHE and GLOBAL_CACHE["lounge_messages"]:
        all_messages = GLOBAL_CACHE["lounge_messages"]
    else:
        # 降級防禦：萬一記憶體是空的，才去硬碟撈第一次，並反向灌回記憶體
        all_messages = []
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                next(reader, None)  # 跳過標頭
                for row in reader:
                    if len(row) == 2:
                        all_messages.append({"name": row[0], "message": row[1]})
        all_messages.reverse()  # 讓最新留言置頂
        GLOBAL_CACHE["lounge_messages"] = all_messages  # 灌錄記憶體保險箱

    # 💡 配送 messages 給前端，100% 嚴絲合縫對齊 lounge.html 的 {% for msg in messages %}
    return render_template('lounge.html',
                           messages=all_messages,
                           current_lang=lang)


@app.route('/solace', methods=['GET', 'POST'])
def solace():
    """ ⚡ 終極防禦版：黃昏溫室密室 (對應：solace) """
    lang = get_current_language()

    # 🔒 1. 智慧憑證提取中心：精準接住密碼並清除空白
    secret_key = request.form.get('secret_key', '').strip()
    if not secret_key:
        secret_key = request.form.get('password', '').strip()
    if not secret_key:
        secret_key = request.cookies.get('solace_token', '').strip()

    # 🛡️ 憑證對比防禦：直接核對字串！徹底粉碎死鎖，未授權者一律踢回大禮堂
    if secret_key != "1229sana&ho":
        return redirect('/castle')

    csv_path = os.path.join(app.root_path, 'data', 'private_messages.csv')

    # 🖋️ 2. 羽毛筆秘密留言寫入管道 (POST 且 action == write)
    if request.method == 'POST' and request.form.get('action') == 'write':
        sender = request.form.get('sender', '').strip()
        text = request.form.get('text', '').strip()
        if sender and text:
            # (a) 老老實實寫入硬碟 CSV 永久保存
            if not os.path.exists(csv_path):
                with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["sender", "text"])
            with open(csv_path, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([sender, text])

            # (b) 💡 快取雙向同步：一微秒內直接強行塞入記憶體陣列最頂端，實現「無感即時留言更新」！
            if "private_messages" not in GLOBAL_CACHE:
                GLOBAL_CACHE["private_messages"] = []
            GLOBAL_CACHE["private_messages"].insert(0, {"sender": sender, "text": text})

    # 📜 3. 讀取管道：共鳴石私密留言紀錄
    # 💡 核心優化：如果記憶體有，直接拿！零硬碟讀寫延遲！
    if "private_messages" in GLOBAL_CACHE and GLOBAL_CACHE["private_messages"]:
        private_messages = GLOBAL_CACHE["private_messages"]
    else:
        private_messages = []
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                next(reader, None)  # 跳過標頭
                for row in reader:
                    if len(row) == 2:
                        private_messages.append({"sender": row[0], "text": row[1]})
        private_messages.reverse()  # 最新留言置頂 prezent
        GLOBAL_CACHE["private_messages"] = private_messages  # 灌錄回保險箱

    # 📜 4. 💡 核心優化：神聖長信資料庫直接從 GLOBAL_CACHE 記憶體大腦提貨！
    letter_data = GLOBAL_CACHE.get("secret_letter", {})
    localized_letter = {}
    if letter_data:
        localized_letter = {
            "salutation": letter_data.get("salutation", {}).get(lang, ""),
            "body": letter_data.get("body", {}).get(lang, ""),
            "signature": letter_data.get("signature", {}).get(lang, "")
        }

    # 5. 建立網格響應，並發放長期通關 Cookie
    is_authenticated = (secret_key == "1229sana&ho")
    response = make_response(render_template('solace.html',
                                             letter=localized_letter,
                                             private_messages=private_messages,
                                             secret_key=secret_key,
                                             current_lang=lang))

    # 烙印通關令牌
    response.set_cookie('solace_token', secret_key, max_age=3600, path='/')
    return response


@app.route('/starlight')
def starlight():
    """ 1. 現實大廳：星光大道 (對應：大禮堂 castle) """
    lang = get_current_language()

    # 1. 導覽列三國語言字典
    nav_labels = {
        "zh": {"starlight": "✦ 星光大道", "dressing": "✧ VIP 化妝間", "studio": "✧ 頂級錄音室", "tour": "✧ 巡演中控台", "bubble": "✧ 粉絲氣泡牆", "night_drive": "✧ 午夜保母車"},
        "ja": {"starlight": "✦ 星光の道", "dressing": "✧ VIP 楽屋", "studio": "✧ プレミアムスタジオ", "tour": "✧ ツアーコントロール", "bubble": "✧ ファンBubble壁", "night_drive": "✧ 深夜の送迎車"},
        "ko": {"starlight": "✦ 스타라이트 로드", "dressing": "✧ VIP 대기실", "studio": "✧ 프리미엄 스튜디오", "tour": "✧ 투어 컨트롤 센터", "bubble": "✧ 팬 버블 월", "night_drive": "✧ 심야 밴"}
    }

    # 💡 核心優化：徹底告別硬碟讀取！直接從 GLOBAL_CACHE 記憶體大腦提貨！
    profile_data = GLOBAL_CACHE.get("sana_profile", {})
    full_data = GLOBAL_CACHE.get("timeline", [])

    # --- 💎 2. 100% 嚴絲合縫對齊 sana_profile.json 與 starlight.html 的拉頁變數期待 ---
    localized_profile = {}
    if profile_data:
        localized_profile = {
            "reg_title": profile_data.get("parchment_meta", {}).get("registry_title", {}).get(lang, ""),
            "name": profile_data.get("core_identity", {}).get("full_name", {}).get(lang, ""),
            "birth": profile_data.get("core_identity", {}).get("birthday", {}).get(lang, ""),
            "place": profile_data.get("core_identity", {}).get("birthplace", {}).get(lang, ""),
            "blood": profile_data.get("core_identity", {}).get("blood_status", {}).get(lang, ""),
            "mbti": profile_data.get("core_identity", {}).get("mbti_astral", {}).get(lang, ""),
            "names": profile_data.get("core_identity", {}).get("ancient_aliases", {}).get(lang, ""),
            "core": profile_data.get("core_identity", {}).get("wand_essence", {}).get(lang, "")
        }

    # --- 🎞️ 3. 100% 完美對齊時尚版編年史巨幕的卡片資料結構 ---
    localized_timeline = []
    for item in full_data:
        localized_timeline.append({
            "year": item["year"],
            "date": item["date"].get(lang, ""),
            "title": item["title"].get(lang, ""),
            "image": item["image"],
            "position": item.get("position", "50% 50%"),
            "fit_mode": item.get("fit_mode", "cover"),
            "event": item["event"].get(lang, ""),
            "achievement": item["achievement"].get(lang, "")
        })
    # -------------------------------------------------------------------------

    # 💡 配送所有高奢資產給前端，完美對齊 starlight.html 的靈魂！
    return render_template('starlight.html',
                           timeline=localized_timeline,
                           profile=localized_profile,
                           current_lang=lang,
                           nav=nav_labels[lang])


@app.route('/dressing')
def dressing():
    """ 2. 後台世界：VIP 化妝間 (對應：萬應室 room) """
    lang = get_current_language()

    # 💡 核心優化：注入導覽列三國語言晶片
    nav_labels = {
        "zh": {"starlight": "✦ 星光大道", "dressing": "✧ VIP 化妝間", "studio": "✧ 頂級錄音室", "tour": "✧ 巡演中控台", "bubble": "✧ 粉絲氣泡牆", "night_drive": "✧ 午夜保母車"},
        "ja": {"starlight": "✦ 星光の道", "dressing": "✧ VIP 楽屋", "studio": "✧ プレミアムスタジオ", "tour": "✧ ツアーコントロール", "bubble": "✧ ファンBubble壁", "night_drive": "✧ 深夜の送迎車"},
        "ko": {"starlight": "✦ 스타라이트 로드", "dressing": "✧ VIP 대기실", "studio": "✧ 프리미엄 스튜디오", "tour": "✧ 투어 컨트롤 센터", "bubble": "✧ 팬 버블 월", "night_drive": "✧ 심야 밴"}
    }

    # 💡 核心優化：告別硬碟讀取！直接從 GLOBAL_CACHE 記憶體中取出化妝間資料！
    full_data = GLOBAL_CACHE.get("room", [])

    # --- 💎 100% 嚴絲合縫對齊 room.json 結構與 dressing.html 的拉頁變數期待 ---
    localized_items = []
    for item in full_data:
        localized_items.append({
            "id": item["id"],
            "name": item["name"].get(lang, ""),
            "image": item["image"],
            "style": item.get("position", "50% 50%"),  # 配送不切臉 Grid 樣式
            "fact": item["fact"].get(lang, "")         # 配送對應語系後台秘聞
        })
    # -------------------------------------------------------------------------

    # 💡 配送 room_items 與 nav 給前端，100% 嚴絲合縫對齊 dressing.html 的期待
    return render_template('dressing.html',
                           room_items=localized_items,
                           current_lang=lang,
                           nav=nav_labels[lang])


@app.route('/studio')
def studio():
    """ 3. 頂級錄音室：黑膠唱片牆 (對應：符咒學 charms) """
    lang = get_current_language()

    # 💡 核心優化：注入導覽列三國語言晶片
    nav_labels = {
        "zh": {"starlight": "✦ 星光大道", "dressing": "✧ VIP 化妝間", "studio": "✧ 頂級錄音室", "tour": "✧ 巡演中控台", "bubble": "✧ 粉絲氣泡牆", "night_drive": "✧ 午夜保母車"},
        "ja": {"starlight": "✦ 星光の道", "dressing": "✧ VIP 楽屋", "studio": "✧ プレミアムスタジオ", "tour": "✧ ツアーコントロール", "bubble": "✧ ファンBubble壁", "night_drive": "✧ 深夜の送迎車"},
        "ko": {"starlight": "✦ 스타라이트 로드", "dressing": "✧ VIP 대기실", "studio": "✧ 프리미엄 스튜디오", "tour": "✧ 투어 컨트롤 센터", "bubble": "✧ 팬 버블 월", "night_drive": "✧ 심야 밴"}
    }

    # 💡 核心優化：徹底告別硬碟讀取！直接從 GLOBAL_CACHE 記憶體中取出黑膠唱片數據！
    full_data = GLOBAL_CACHE.get("music", [])

    # --- 💎 100% 嚴絲合縫對齊 music.json 結構與 studio.html 的變數期待 ---
    localized_music = []
    for item in full_data:
        localized_music.append({
            "id": item["id"],
            "year": item["year"].get(lang, ""),
            "album": item["album"].get(lang, ""),
            "title": item["title"],
            "cover": item["cover"],
            "position": item.get("position", "50% 50%"),
            "type": item["type"].get(lang, ""),
            "description": item["description"].get(lang, ""),
            "magic_effect": item["magic_effect"].get(lang, "") # 在世界 B 代表「作詞意境與音樂故事」
        })
    # -------------------------------------------------------------------------

    # 💡 配送 music_books 與 nav 給前端，100% 嚴絲合縫對齊 studio.html
    return render_template('studio.html',
                           music_books=localized_music,
                           current_lang=lang,
                           nav=nav_labels[lang])


@app.route('/tour')
def tour():
    """ 4. 全球巡演中控台：數位地球儀 (對應：儲思盆 media) """
    lang = get_current_language()

    # 💡 核心優化：注入導覽列三國語言晶片
    nav_labels = {
        "zh": {"starlight": "✦ 星光大道", "dressing": "✧ VIP 化妝間", "studio": "✧ 頂級錄音室", "tour": "✧ 巡演中控台", "bubble": "✧ 粉絲氣泡牆", "night_drive": "✧ 午夜保母車"},
        "ja": {"starlight": "✦ 星光の道", "dressing": "✧ VIP 楽屋", "studio": "✧ プレミアムスタジオ", "tour": "✧ ツアーコントロール", "bubble": "✧ ファンBubble壁", "night_drive": "✧ 深夜の送迎車"},
        "ko": {"starlight": "✦ 스타라이트 로드", "dressing": "✧ VIP 대기실", "studio": "✧ 프리미엄 스튜디오", "tour": "✧ 투어 컨트롤 센터", "bubble": "✧ 팬 버블 월", "night_drive": "✧ 심야 밴"}
    }

    # 💡 核心優化：告別硬碟讀取！直接從 GLOBAL_CACHE 記憶體大腦提貨！
    full_data = GLOBAL_CACHE.get("media", {})

    # 建立純淨前端網格，準備接受灌錄
    localized_media = {
        "videos": [],
        "concerts": [],
        "history_tours": {"world": [], "physical": [], "online": []}
    }

    if full_data:
        # 🎬 1. 虛擬聯網影片數據清洗
        for vid in full_data.get("videos", []):
            localized_media["videos"].append({
                "id": vid["id"],
                "title": vid.get("title", {}).get(lang, ""),
                "youtube_id": vid.get("youtube_id", ""),
                "description": vid.get("description", {}).get(lang, "")
            })

        # 🗺️ 2. 雷達地圖訊號節點座標分配
        for con in full_data.get("concerts", []):
            localized_media["concerts"].append({
                "id": con["id"],
                "name": con.get("name", {}).get(lang, ""),
                "coords": con.get("coords", "50% 50%"), # 百分比物理定位
                "detail": con.get("detail", {}).get(lang, "")
            })

        # 📜 3. 歷史世界巡演日程數據注入 (直接抓取 "zh"/"ja"/"ko" 欄位，100% 免疫死鎖)
        for cat in ["world", "physical", "online"]:
            tours_list = full_data.get("history_tours", {}).get(cat, [])
            for tour in tours_list:
                localized_media["history_tours"][cat].append({
                    "year": tour.get("year", ""),
                    "title": tour.get("title", ""),
                    "detail": tour.get(lang, ""),  # 完美對齊 JSON 語系
                    "image": tour.get("image", "")  # 完美配送現場高奢直擊照
                })

    # 💡 配送 media_data 與 nav 給前端，100% 嚴絲合縫對齊 tour.html 的結構
    return render_template('tour.html',
                           media_data=localized_media,
                           current_lang=lang,
                           nav=nav_labels[lang])


@app.route('/bubble', methods=['GET', 'POST'])
def bubble():
    """ 5. ONCE 粉絲留言牆：手機 Bubble 氣泡動態牆 (對應：交誼廳 lounge) """
    lang = get_current_language()

    # 💡 核心優化：導覽列與介面三國語言晶片
    nav_labels = {
        "zh": {"starlight": "✦ 星光大道", "dressing": "✧ VIP 化妝間", "studio": "✧ 頂級錄音室", "tour": "✧ 巡演中控台", "bubble": "✧ 粉絲氣泡牆", "night_drive": "✧ 午夜保母車"},
        "ja": {"starlight": "✦ 星光の道", "dressing": "✧ VIP 楽屋", "studio": "✧ プレミアムスタジオ", "tour": "✧ ツアーコントロール", "bubble": "✧ ファンBubble壁", "night_drive": "✧ 深夜の送迎車"},
        "ko": {"starlight": "✦ 스타라이트 로드", "dressing": "✧ VIP 대기실", "studio": "✧ 프리미엄 스튜디오", "tour": "✧ 투어 컨트롤 센터", "bubble": "✧ 팬 버블 월", "night_drive": "✧ 심야 밴"}
    }

    ui_labels = {
        "zh": {"title": "ONCE BUBBLE CHANNEL", "subtitle": "與 SANA 的白金專屬私密對話氣泡", "placeholder_name": "輸入妳的 ONCE 暱稱...", "placeholder_msg": "寫下對 Sana 的應援長文...", "btn": "發送 Bubble 訊息 ✉️"},
        "ja": {"title": "ONCE BUBBLE CHANNEL", "subtitle": "SANAとのプラチナ限定プライベートトーク", "placeholder_name": "ONCEのニック네임を入力...", "placeholder_msg": "サナへの応援メッセージをここに...", "btn": "Bubbleを送信する ✉️"},
        "ko": {"title": "ONCE BUBBLE CHANNEL", "subtitle": "SANA와의 플래티넘 전용 프라이빗 대화 버블", "placeholder_name": "ONCE 닉네임 입력...", "placeholder_msg": "사나를 향한 응원 메시지를 적어보세요...", "btn": "버블 메시지 전송 ✉️"}
    }

    csv_path = os.path.join(app.root_path, 'data', 'messages.csv') # 🔒 完美直連、與交誼廳共用同一個公開留言資料庫！

    # 🖋️ 1. 寫入管道：當 ONCE 按下「發送 Bubble 訊息」
    if request.method == 'POST':
        name = request.form.get('wizard_name', '').strip()
        msg = request.form.get('wizard_msg', '').strip()
        if name and msg:
            # (a) 老老實實寫入硬碟永久保存
            if not os.path.exists(csv_path):
                with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["name", "message"])
            with open(csv_path, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([name, msg])

            # (b) 💡 快取雙向同步：一微秒內直接強行塞入記憶體陣列最頂端（共用 lounge_messages 快取，兩界同步！）
            if "lounge_messages" not in GLOBAL_CACHE:
                GLOBAL_CACHE["lounge_messages"] = []
            GLOBAL_CACHE["lounge_messages"].insert(0, {"name": name, "message": msg})

        return redirect('/bubble')

    # 📜 2. 讀取管道：當粉絲進房參觀氣泡牆
    # 💡 核心優化：直接從全域大腦提貨，零硬碟讀寫延遲！
    if "lounge_messages" in GLOBAL_CACHE and GLOBAL_CACHE["lounge_messages"]:
        all_messages = GLOBAL_CACHE["lounge_messages"]
    else:
        all_messages = []
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                next(reader, None) # 跳過標頭
                for row in reader:
                    if len(row) == 2:
                        all_messages.append({"name": row[0], "message": row[1]})
        all_messages.reverse() # 最新留言置頂呈現
        GLOBAL_CACHE["lounge_messages"] = all_messages # 灌錄回保險箱

    # 💡 配送所有高奢資產，100% 嚴絲合縫對齊 bubble.html
    return render_template('bubble.html',
                           messages=all_messages,
                           current_lang=lang,
                           nav=nav_labels[lang],
                           ui=ui_labels[lang])


@app.route('/night_drive', methods=['GET', 'POST'])
def night_drive():
    """ 6. 終極密室：午夜保母車 / 私人手機未讀訊息 (對應：黃昏密室 solace) """
    lang = get_current_language()

    # 💡 核心優化：導覽列與解鎖介面三國語言晶片
    nav_labels = {
        "zh": {"starlight": "✦ 星光大道", "dressing": "✧ VIP 化妝間", "studio": "✧ 頂級錄音室", "tour": "✧ 巡演中控台", "bubble": "✧ 粉絲氣泡牆", "night_drive": "✧ 午夜保母車"},
        "ja": {"starlight": "✦ 星光の道", "dressing": "✧ VIP 楽屋", "studio": "✧ プレミアムスタジオ", "tour": "✧ ツアーコントロール", "bubble": "✧ ファンBubble壁", "night_drive": "✧ 深夜の送迎車"},
        "ko": {"starlight": "✦ 스타라이트 로드", "dressing": "✧ VIP 대기실", "studio": "✧ 프리미엄 스튜디오", "tour": "✧ 투어 컨트롤 센터", "bubble": "✧ 팬 버블 월", "night_drive": "✧ 심야 밴"}
    }

    ui_labels = {
        "zh": {"lock_title": "SANA'S PRIVATE PHONE", "lock_tip": "請輸入解鎖密碼以閱讀未讀訊息", "status": "今日行程已結束 • 靜音模式", "sender": "來自最深沉的守護信", "btn": "解鎖手機"},
        "ja": {"lock_title": "SANA'S PRIVATE PHONE", "lock_tip": "未読メッセージを読むにはパスワードを入力してください", "status": "本日のスケジュール終了 • サイレントモード", "sender": "最も深い守護からの手紙", "btn": "ロック解除"},
        "ko": {"lock_title": "SANA'S PRIVATE PHONE", "lock_tip": "읽지 않은 메시지를 읽으려면 비밀번호를 입력하세요", "status": "오늘 일정 종료 • 무음 모드", "sender": "가장 깊은 수호의 편지", "btn": "휴대폰 잠금해제"}
    }

    # 🔒 智慧憑證安全防禦（相容 POST 與 COOKIE）
    secret_key = request.form.get('secret_key', '').strip()
    if not secret_key:
        secret_key = request.form.get('password', '').strip()
    if not secret_key:
        secret_key = request.cookies.get('solace_token', '').strip()

    csv_path = os.path.join(app.root_path, 'data', 'private_messages.csv')

    # 🖋️ 1. 寫入管道：當粉絲在解鎖的手機裡傳送私人密訊
    if request.method == 'POST' and request.form.get('action') == 'write' and secret_key == "1229sana&ho":
        sender = request.form.get('sender', '').strip()
        text = request.form.get('text', '').strip()
        if sender and text:
            # (a) 寫入硬碟永久保存
            if not os.path.exists(csv_path):
                with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["sender", "text"])
            with open(csv_path, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([sender, text])

            # (b) 💡 快取雙向同步：強行塞入記憶體最頂端（共用 private_messages 快取，兩界同步！）
            if "private_messages" not in GLOBAL_CACHE:
                GLOBAL_CACHE["private_messages"] = []
            GLOBAL_CACHE["private_messages"].insert(0, {"sender": sender, "text": text})

    # 📜 2. 讀取管道：從記憶體保險箱索取私人對話紀錄，零硬碟讀寫延遲！
    if "private_messages" in GLOBAL_CACHE and GLOBAL_CACHE["private_messages"]:
        private_messages = GLOBAL_CACHE["private_messages"]
    else:
        private_messages = []
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) == 2:
                        private_messages.append({"sender": row[0], "text": row[1]})
        private_messages.reverse()
        GLOBAL_CACHE["private_messages"] = private_messages # 灌錄回保險箱

    # 📜 3. 💡 核心優化：神聖長信資料庫直接從 GLOBAL_CACHE 記憶體大腦提貨！
    letter_data = GLOBAL_CACHE.get("secret_letter", {})
    localized_letter = {}
    if letter_data:
        localized_letter = {
            "salutation": letter_data.get("salutation", {}).get(lang, ""),
            "body": letter_data.get("body", {}).get(lang, ""),
            "signature": letter_data.get("signature", {}).get(lang, "")
        }

    # 智慧驗證權限狀態位元
    is_authenticated = (secret_key == "1229sana&ho")

    # 💡 配送所有白金資產，100% 嚴絲合縫對齊 night_drive.html
    response = make_response(render_template('night_drive.html',
                                             letter=localized_letter,
                                             private_messages=private_messages,
                                             secret_key=secret_key,
                                             is_authenticated=is_authenticated,
                                             current_lang=lang,
                                             nav=nav_labels[lang],
                                             ui=ui_labels[lang]))

    if is_authenticated:
        response.set_cookie('solace_token', secret_key, max_age=3600, path='/')
    return response


@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    if lang_code not in ['zh', 'ja', 'ko']:
        lang_code = 'zh'
    referrer = request.referrer if request.referrer else '/'
    response = make_response(redirect(referrer))
    response.set_cookie('lang', lang_code, max_age=31536000, path='/')
    return response


@app.route('/fortress_reload_secret_json', methods=['GET'])
def fortress_reload():
    token = request.args.get('token')
    if token == "sana_power_2026":
        load_all_json_to_cache()
        return jsonify({"status": "success", "message": "全站記憶體快取無感刷新大成功！"}), 200
    return jsonify({"status": "denied", "message": "密鑰錯誤"}), 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)