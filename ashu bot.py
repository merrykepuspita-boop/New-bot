# =========================================================
# ADVANCED TELEGRAM PHONE LOOKUP BOT
# Educational Purpose Only
# Long Polling | No python-telegram-bot Library
# Modules Used: requests, json, time
# =========================================================

import requests
import json
import time

# =========================================================
# CONFIGURATION
# =========================================================

BOT_TOKEN = "8386449019:AAFL_FFxb4qXP9sGkBUkkfhv44ljW52iSMI"
API_URL = "https://paid-num-info-xkez.vercel.app/api/proxy.js?type=info&value="
ADMIN_ID = 7035366626

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Dummy HTTPS Server
DUMMY_HTTPS_SERVER = "https://secure.example.com"

# =========================================================
# DATABASES
# =========================================================

users = {}
user_states = {}
redeem_codes = {}

# =========================================================
# TELEGRAM API FUNCTIONS
# =========================================================

def send_message(chat_id, text, reply_markup=None):

    url = BASE_URL + "/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)

    try:
        requests.post(url, data=data)
    except:
        pass


def get_updates(offset):

    url = BASE_URL + "/getUpdates"

    params = {
        "timeout": 30,
        "offset": offset
    }

    try:
        response = requests.get(url, params=params)
        return response.json()

    except:
        return {"result": []}

# =========================================================
# KEYBOARDS
# =========================================================

def main_keyboard():

    keyboard = {
        "keyboard": [
            [{"text": "📱 Phone Lookup"}],
            [{"text": "💳 My Credits"}],
            [{"text": "🎟 Redeem Code"}],
            [{"text": "ℹ️ Help"}]
        ],
        "resize_keyboard": True
    }

    return keyboard


def admin_keyboard():

    keyboard = {
        "keyboard": [
            [{"text": "🎟 Create Redeem"}],
            [{"text": "📊 Bot Stats"}],
            [{"text": "⬅️ Back"}]
        ],
        "resize_keyboard": True
    }

    return keyboard

# =========================================================
# USER SYSTEM
# =========================================================

def create_user(user_id):

    if user_id not in users:

        users[user_id] = {
            "credits": 5
        }


def get_credits(user_id):

    create_user(user_id)

    return users[user_id]["credits"]


def add_credits(user_id, amount):

    create_user(user_id)

    users[user_id]["credits"] += amount


def remove_credit(user_id):

    create_user(user_id)

    if users[user_id]["credits"] > 0:

        users[user_id]["credits"] -= 1
        return True

    return False

# =========================================================
# PHONE LOOKUP
# =========================================================

def phone_lookup(number):

    try:

        url = API_URL + str(number)

        response = requests.get(url, timeout=15)

        try:
            data = response.json()
            return json.dumps(data, indent=4)

        except:
            return response.text

    except Exception as e:

        return f"API ERROR: {str(e)}"

# =========================================================
# STYLISH MESSAGES
# =========================================================

WELCOME_TEXT = """
<b>
╔══════════════════════╗
⚡ 𝐀𝐃𝐕𝐀𝐍𝐂𝐄𝐃 𝐎𝐒𝐈𝐍𝐓 ⚡
╚══════════════════════╝
</b>

<b>🔍 Advanced Mobile Lookup System</b>

✨ 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬:
• 𝐈𝐧𝐬𝐭𝐚𝐧𝐭 𝐏𝐡𝐨𝐧𝐞 𝐋𝐨𝐨𝐤𝐮𝐩
• 𝐂𝐫𝐞𝐝𝐢𝐭 𝐒𝐲𝐬𝐭𝐞𝐦
• 𝐑𝐞𝐝𝐞𝐞𝐦 𝐂𝐨𝐝𝐞𝐬
• 𝐀𝐝𝐦𝐢𝐧 𝐏𝐚𝐧𝐞𝐥
• 𝐒𝐭𝐲𝐥𝐢𝐬𝐡 𝐈𝐧𝐭𝐞𝐫𝐟𝐚𝐜𝐞

🎁 Free Credits: <b>5</b>

⚠️ 𝑵𝒆𝒆𝒅 𝑴𝒐𝒓𝒆 𝑪𝒓𝒆𝒅𝒊𝒕𝒔?
𝑪𝒐𝒏𝒕𝒂𝒄𝒕 𝑨𝒅𝒎𝒊𝒏.
@fe7xy

👇 Choose An Option Below
"""

HELP_TEXT = """
<b>📚 HELP MENU</b>

📱 Phone Lookup
→ Search mobile information

💳 My Credits
→ Check your credits

🎟 Redeem Code
→ Redeem premium credits

⚠️ Rules:
• Send only 10 digit numbers
• One lookup = 1 credit

👑 Educational Purpose Only
"""

# =========================================================
# BOT LOOP
# =========================================================

offset = 0

print("BOT IS RUNNING...")

while True:

    updates = get_updates(offset)

    if "result" in updates:

        for update in updates["result"]:

            offset = update["update_id"] + 1

            try:

                if "message" not in update:
                    continue

                message = update["message"]

                chat_id = message["chat"]["id"]
                user_id = message["from"]["id"]
                text = message.get("text", "").strip()

                create_user(user_id)

                # =================================================
                # START COMMAND
                # =================================================

                if text == "/start":

                    user_states.pop(user_id, None)

                    send_message(
                        chat_id,
                        WELCOME_TEXT,
                        reply_markup=main_keyboard()
                    )

                # =================================================
                # HELP
                # =================================================

                elif text == "ℹ️ Help":

                    send_message(
                        chat_id,
                        HELP_TEXT,
                        reply_markup=main_keyboard()
                    )

                # =================================================
                # MY CREDITS
                # =================================================

                elif text == "💳 My Credits":

                    credits = get_credits(user_id)

                    msg = f"""
<b>💳 CREDIT INFORMATION</b>

👤 User ID:
<code>{user_id}</code>

⭐ Credits:
<b>{credits}</b>

⚠️ 𝑵𝒆𝒆𝒅 𝑴𝒐𝒓𝒆 𝑪𝒓𝒆𝒅𝒊𝒕𝒔?
𝑪𝒐𝒏𝒕𝒂𝒄𝒕 𝑨𝒅𝒎𝒊𝒏.
@fe7xy
"""

                    send_message(
                        chat_id,
                        msg,
                        reply_markup=main_keyboard()
                    )

                # =================================================
                # PHONE LOOKUP BUTTON
                # =================================================

                elif text == "📱 Phone Lookup":

                    if get_credits(user_id) <= 0:

                        send_message(
                            chat_id,
                            """
<b>❌ NO CREDITS LEFT</b>

⚠️ 𝐊𝐲𝐚 𝐫𝐞 𝐛𝐚𝐛𝐮 𝐜𝐫𝐞𝐝𝐢𝐭 𝐤𝐡𝐚𝐭𝐚𝐦 𝐡𝐨 𝐠𝐲𝐚 𝐤𝐲𝐚!
𝐝𝐦 𝐚𝐣𝐚𝐨 😘

📞 𝐂ⱺ𐓣𝗍α𝖼𝗍 𝐀ᑯꭑ𝗂𐓣.
@fe7xy
""",
                            reply_markup=main_keyboard()
                        )

                    else:

                        user_states[user_id] = "waiting_number"

                        send_message(
                            chat_id,
                            "📞 Send 10 digit mobile number:",
                            reply_markup=main_keyboard()
                        )

                # =================================================
                # REDEEM CODE BUTTON
                # =================================================

                elif text == "🎟 Redeem Code":

                    user_states[user_id] = "redeem_mode"

                    send_message(
                        chat_id,
                        """
<b>🎟 REDEEM SYSTEM</b>

Send your redeem code now:
""",
                        reply_markup=main_keyboard()
                    )

                # =================================================
                # ADMIN PANEL
                # =================================================

                elif text == "/admin":

                    if user_id == ADMIN_ID:

                        send_message(
                            chat_id,
                            """
<b>👑 ADMIN PANEL</b>

𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐀𝐃𝐌𝐈𝐍 𝐒𝐀𝐇𝐀𝐁.
""",
                            reply_markup=admin_keyboard()
                        )

                    else:

                        send_message(
                            chat_id,
                            "<b>❌ Access Denied</b>"
                        )

                # =================================================
                # BOT STATS
                # =================================================

                elif text == "📊 Bot Stats" and user_id == ADMIN_ID:

                    total_users = len(users)
                    total_codes = len(redeem_codes)

                    stats = f"""
<b>📊 BOT STATISTICS</b>

👥 Total Users:
<b>{total_users}</b>

🎟 Active Redeem Codes:
<b>{total_codes}</b>

🌐 HTTPS Server:
<code>{DUMMY_HTTPS_SERVER}</code>

⚡ Status:
<b>ONLINE</b>
"""

                    send_message(
                        chat_id,
                        stats,
                        reply_markup=admin_keyboard()
                    )

                # =================================================
                # CREATE REDEEM
                # =================================================

                elif text == "🎟 Create Redeem" and user_id == ADMIN_ID:

                    user_states[user_id] = "create_redeem"

                    send_message(
                        chat_id,
                        """
<b>🎟 CREATE REDEEM CODE</b>

Send details in this format:

<code>CODE CREDITS USERS</code>

Example:
<code>VIP50 50 10</code>

Meaning:
• Code = VIP50
• Credits = 50
• Max Users = 10
""",
                        reply_markup=admin_keyboard()
                    )

                # =================================================
                # ADMIN CREATE REDEEM PROCESS
                # =================================================

                elif user_states.get(user_id) == "create_redeem":

                    if user_id != ADMIN_ID:
                        continue

                    parts = text.split()

                    if len(parts) != 3:

                        send_message(
                            chat_id,
                            """
<b>❌ INVALID FORMAT</b>

Example:
<code>VIP50 50 10</code>
"""
                        )

                    else:

                        try:

                            code = parts[0]
                            credits = int(parts[1])
                            users_limit = int(parts[2])

                            redeem_codes[code] = {
                                "credits": credits,
                                "users_left": users_limit
                            }

                            del user_states[user_id]

                            send_message(
                                chat_id,
                                f"""
<b>✅ REDEEM CODE CREATED</b>

🎟 Code:
<code>{code}</code>

⭐ Credits:
<b>{credits}</b>

👥 Max Users:
<b>{users_limit}</b>
""",
                                reply_markup=admin_keyboard()
                            )

                        except:

                            send_message(
                                chat_id,
                                "<b>❌ Invalid Numbers</b>"
                            )

                # =================================================
                # REDEEM PROCESS
                # =================================================

                elif user_states.get(user_id) == "redeem_mode":

                    code = text.strip()

                    if code in redeem_codes:

                        info = redeem_codes[code]

                        if info["users_left"] <= 0:

                            send_message(
                                chat_id,
                                """
<b>❌ CODE EXPIRED</b>

No users remaining.
""",
                                reply_markup=main_keyboard()
                            )

                        else:

                            add_credits(user_id, info["credits"])

                            info["users_left"] -= 1

                            if info["users_left"] <= 0:
                                del redeem_codes[code]

                            del user_states[user_id]

                            send_message(
                                chat_id,
                                f"""
<b>✅ REDEEM SUCCESSFUL</b>

⭐ Credits Added:
<b>{info['credits']}</b>

💳 Total Credits:
<b>{get_credits(user_id)}</b>
""",
                                reply_markup=main_keyboard()
                            )

                    else:

                        send_message(
                            chat_id,
                            """
<b>❌ INVALID REDEEM CODE</b>
""",
                            reply_markup=main_keyboard()
                        )

                # =================================================
                # NUMBER LOOKUP PROCESS
                # =================================================

                elif user_states.get(user_id) == "waiting_number":

                    if text.isdigit() and len(text) == 10:

                        if not remove_credit(user_id):

                            send_message(
                                chat_id,
                                """
<b>❌ NO CREDITS LEFT</b>
""",
                                reply_markup=main_keyboard()
                            )

                            continue

                        send_message(
                            chat_id,
                            """
<b>🔍 Searching Database...</b>
"""
                        )

                        result = phone_lookup(text)

                        final_message = f"""
<b>📱 PHONE LOOKUP RESULT</b>

<pre>{result}</pre>

⭐ Remaining Credits:
<b>{get_credits(user_id)}</b>
"""

                        send_message(
                            chat_id,
                            final_message,
                            reply_markup=main_keyboard()
                        )

                        del user_states[user_id]

                    else:

                        send_message(
                            chat_id,
                            """
<b>❌ INVALID NUMBER</b>

⚠️ Please send a valid 10 digit mobile number.
""",
                            reply_markup=main_keyboard()
                        )

                # =================================================
                # BACK BUTTON
                # =================================================

                elif text == "⬅️ Back":

                    user_states.pop(user_id, None)

                    send_message(
                        chat_id,
                        """
<b>🏠 Main Menu</b>
""",
                        reply_markup=main_keyboard()
                    )

                # =================================================
                # UNKNOWN COMMAND
                # =================================================

                else:

                    send_message(
                        chat_id,
                        """
<b>❌ UNKNOWN COMMAND</b>

Please use the keyboard buttons below.
""",
                        reply_markup=main_keyboard()
                    )

            except Exception as e:

                print("ERROR:", e)

    time.sleep(1)