import time
import requests as r
import telebot
import sqlite3
import random
from telebot import types
from mconfig import token, admins
#ВСЯКИЕ ВАЖНЫЕ ПЕРЕМЕННЫЕ (НАВЕРНОЕ)
bot = telebot.TeleBot(token)
user_add_db_balance = """INSERT INTO users
                              (id, balance)
                              VALUES (?, 10000);"""


#ВСЯКИЕ ВАЖНЫЕ ПЕРЕМЕННЫЕ (НАВЕРНОЕ)

#MESSAGE DEF
@bot.message_handler(content_types='text')
def message_reply(message):
    userid = [message.chat.id]
    name = [message.chat.first_name]
    if "/start" in message.text:

        bot.send_message(message.chat.id, "команды:\n"
                                          "/menu - меню\n"
                                          "/betr + сумма - ставка на красное\n"
                                          "/betb + сумма - ставка на черное\n"
                                          "/betg + ставка - ставка на зеленое\n"
                                          "/top - топ баланса\n"
                                          "/ras + текст - рассылка всем\n"
                                          "Если баланс равен 0, обращайтесь к @exort21\n")
        try:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS users(
                   id INTEGER
                   balance INTEGER
                   name TEXT
               )""")
            print('включена!')
            #-------------------------------------------------------------------
            #добавление юзера в бд
            cur.execute(f"SELECT id FROM users WHERE id = '{userid}'")
            if cur.fetchone() == None:
                cur.execute(user_add_db_balance, userid)
                conn.commit()
                cur.execute(f"UPDATE users SET name = ? WHERE id = {message.chat.id}", name)
                conn.commit()
                bot.send_message(message.chat.id, "Вы были добавлены в бд!")
                print(f"новый юзер добавлен! {message.chat.id}")
                bot.send_message(6089704303, f"новый юзер добавлен в бд {message.chat.id}")
            else:
                bot.send_message(message.chat.id, "Вы уже в бд!")
            #--------------------------------------------------------------------
        except sqlite3.Error as error:
            bot.send_message(message.chat.id, "Что-то пошло не так!")
            print("Ошибка при работе с юзерами SQLite", error)
            conn.close()
    if message.text == "/menu":

        try:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute(f"SELECT balance FROM users WHERE id = ?", userid)
            balance = cur.fetchone()[0]
            menu = f"добро пожаловать!\nВаш айди: {userid[0]}\nВаш баланс: {balance}\nЕсли баланс равен 0, обращайтесь к @exort21\n"
            bot.send_message(message.chat.id, menu)
        except sqlite3.Error as error:
            print("Ошибка при работе с доставанием баланса SQLite", error)
            bot.send_message(message.chat.id, "Что-то пошло не так!")
            conn.close()

    if "/betr" in message.text:
        bet = int(message.text.split(" ")[1])
        print(bet)
        try:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute(f"SELECT balance FROM users WHERE id = ?", userid)
            balance = cur.fetchone()[0]


            bot.send_message(message.chat.id, f"ставка {bet} на красное")
            time.sleep(1)
            bot.send_message(message.chat.id, "крутим.")
            time.sleep(1)
            bot.send_message(message.chat.id, "крутим..")
            time.sleep(1)
            bot.send_message(message.chat.id, "крутим...")
            time.sleep(1)


            result = random.randint(0,40)

            if balance > 0 and bet <= balance:
                if result in range(15, 35):
                    bot.send_message(message.chat.id, "Выпало черное!")
                elif result == 40:
                    bot.send_message(message.chat.id, "Выпало зеленое!")
                elif result in range(1, 15):
                    bot.send_message(message.chat.id, "Выпало красное!")
                else:
                    bot.send_message(message.chat.id, "Выпало нихуя")
                if result in range(1, 15):
                    try:
                        balance += bet * 2
                        temp = [balance, message.chat.id]
                        cur.execute("UPDATE users SET balance = ? WHERE id = ?", temp)
                        conn.commit()

                        bot.send_message(message.chat.id, f'Ты выиграл {bet*2}!')
                    except sqlite3.Error as error:
                        print("Ошибка при работе с изменением баланса 1 SQLite", error)

                else:
                    try:
                        balance = int(balance) - int(bet)
                        temp = [balance, message.chat.id]
                        cur.execute("UPDATE users SET balance = ? WHERE id = ?", temp)
                        bot.send_message(message.chat.id, f'Ты проиграл {bet}!')
                        conn.commit()
                    except sqlite3.Error as error:
                        print("Ошибка при работе с изменением баланса 2 SQLite", error)


            else:
                bot.send_message(message.chat.id, 'Ты саня! (нет денег)')

        except sqlite3.Error as error:
            print("Ошибка при работе с изменением баланса 3 SQLite", error)

    if "/betb" in message.text:
        bet = int(message.text.split(" ")[1])
        print(bet)
        try:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute(f"SELECT balance FROM users WHERE id = ?", userid)
            balance = cur.fetchone()[0]


            bot.send_message(message.chat.id, f"ставка {bet} на черное")
            time.sleep(1)
            bot.send_message(message.chat.id, "крутим.")
            time.sleep(1)
            bot.send_message(message.chat.id, "крутим..")
            time.sleep(1)
            bot.send_message(message.chat.id, "крутим...")
            time.sleep(1)


            result = random.randint(0,40)
            if balance > 0 and bet <= balance:
                if result in range(15, 35):
                    bot.send_message(message.chat.id, "Выпало черное!")
                elif result == 40:
                    bot.send_message(message.chat.id, "Выпало зеленое!")
                elif result in range(1, 15):
                    bot.send_message(message.chat.id, "Выпало красное!")
                else:
                    bot.send_message(message.chat.id, "Выпало нихуя")
                if result in range(15, 35):
                    try:
                        balance += bet * 1.5
                        temp = [balance, message.chat.id]
                        cur.execute("UPDATE users SET balance = ? WHERE id = ?", temp)
                        conn.commit()

                        bot.send_message(message.chat.id, f'Ты выиграл {bet*1.5}!')
                    except sqlite3.Error as error:
                        print("Ошибка при работе с изменением баланса 1 SQLite", error)

                else:
                    try:
                        balance = int(balance) - int(bet)
                        temp = [balance, message.chat.id]
                        cur.execute("UPDATE users SET balance = ? WHERE id = ?", temp)
                        bot.send_message(message.chat.id, f'Ты проиграл {bet}!')
                        conn.commit()
                    except sqlite3.Error as error:
                        print("Ошибка при работе с изменением баланса 2 SQLite", error)
            else:
                bot.send_message(message.chat.id, 'Ты саня! (нет денег)')
        except sqlite3.Error as error:
            print("Ошибка при работе с изменением баланса 3 SQLite", error)

    if "/betg" in message.text:
        bet = int(message.text.split(" ")[1])
        print(bet)
        try:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute(f"SELECT balance FROM users WHERE id = ?", userid)
            balance = cur.fetchone()[0]
            bot.send_message(message.chat.id, f"ставка {bet} на зеленое")
            time.sleep(1)
            bot.send_message(message.chat.id, "крутим.")
            time.sleep(1)
            bot.send_message(message.chat.id, "крутим..")
            time.sleep(1)
            bot.send_message(message.chat.id, "крутим...")
            time.sleep(1)
            result = random.randint(0,40)
            if balance > 0 and bet <= balance:
                if result in range(15, 35):
                    bot.send_message(message.chat.id, "Выпало черное!")
                elif result == 40:
                    bot.send_message(message.chat.id, "Выпало зеленое!")
                elif result in range(1, 15):
                    bot.send_message(message.chat.id, "Выпало красное!")
                else:
                    bot.send_message(message.chat.id, "Выпало нихуя")
                if result == 40:
                    try:
                        balance += bet * 15
                        temp = [balance, message.chat.id]
                        cur.execute("UPDATE users SET balance = ? WHERE id = ?", temp)
                        conn.commit()
                        bot.send_message(message.chat.id, f'Ты выиграл {bet * 15}!')
                    except sqlite3.Error as error:
                        print("Ошибка при работе с изменением баланса 1 SQLite", error)

                else:
                    try:
                        balance = int(balance) - int(bet)
                        temp = [balance, message.chat.id]
                        cur.execute("UPDATE users SET balance = ? WHERE id = ?", temp)
                        bot.send_message(message.chat.id, f'Ты проиграл {bet}!')
                        conn.commit()
                    except sqlite3.Error as error:
                        print("Ошибка при работе с изменением баланса 2 SQLite", error)


            else:
                bot.send_message(message.chat.id, 'Ты саня! (нет денег)')
        except sqlite3.Error as error:
            print("Ошибка при работе с изменением баланса 3 SQLite", error)
    if message.text == '/top':

        try:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM users")

            db_top = cur.fetchall()
            for el in db_top:
                text_top = "Имя: "+str(el[2]) +" Баланс: "+str(el[1])+"\n"
                bot.send_message(message.chat.id, text_top)

        except sqlite3.Error as error:
            print("Ошибка при работе с топом SQLite", error)

    if "/ras" in message.text:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM users")
        id_list = cur.fetchall()
        msg = message.text.split(" ")
        msg.remove("/ras")
        text = ""
        for i in msg:
            text += i + " "
        for el in id_list:
             bot.send_message(el[0], text)

    if message.text == "/menu" or message.text == "/start" or message.text == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("⚫️Cтавка на черное⚫️")
        item2 = types.KeyboardButton("🔴Ставка на красное🔴")
        item3 = types.KeyboardButton("🟢Ставка на зелёное🟢")
        item5 = types.KeyboardButton("🎰Слоты🎰")
        item6 = types.KeyboardButton("🌕Монетка🌕")
        markup.add(item1, item2, item3, item5, item6)
        bot.send_message(message.chat.id, 'Варианты игры:', reply_markup=markup)
    if message.text == "⚫️Cтавка на черное⚫️":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1_1 = types.KeyboardButton("/betb 500")
        item1_2 = types.KeyboardButton("/betb 1000")
        item1_3 = types.KeyboardButton("/betb 1500")
        item4 = types.KeyboardButton("Назад")
        markup.add(item1_1, item1_2, item1_3, item4)
        bot.send_message(message.chat.id, 'Выберите сумму ставки (либо через команду укажите свою)', reply_markup=markup)
    if message.text == "🔴Ставка на красное🔴":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item2_1 = types.KeyboardButton("/betr 500")
        item2_2 = types.KeyboardButton("/betr 1000")
        item2_3 = types.KeyboardButton("/betr 1500")
        item4 = types.KeyboardButton("Назад")
        markup.add(item2_1, item2_2, item2_3, item4)
        bot.send_message(message.chat.id, 'Выберите сумму ставки (либо через команду укажите свою)', reply_markup=markup)
    if message.text == "🟢Ставка на зелёное🟢":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item3_1 = types.KeyboardButton("/betg 500")
        item3_2 = types.KeyboardButton("/betg 1000")
        item3_3 = types.KeyboardButton("/betg 1500")
        item4 = types.KeyboardButton("Назад")
        markup.add(item3_1, item3_2, item3_3, item4)
        bot.send_message(message.chat.id, 'Выберите сумму ставки (либо через команду укажите свою)', reply_markup=markup)
    if message.text == "🎰Слоты🎰":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item4_1 = types.KeyboardButton("/roll 100")
        item4_2 = types.KeyboardButton("/roll 250")
        item4_3 = types.KeyboardButton("/roll 500")
        item4 = types.KeyboardButton("Назад")
        markup.add(item4_1, item4_2, item4_3, item4)
        bot.send_message(message.chat.id, 'Выберите сумму ставки (либо через команду укажите свою)', reply_markup=markup)
    if message.text == "🌕Монетка🌕":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item5_1 = types.KeyboardButton("Орёл")
        item5_2 = types.KeyboardButton("Решка")
        item4 = types.KeyboardButton("Назад")
        markup.add(item5_1, item5_2, item4)
        bot.send_message(message.chat.id, 'Выберите сумму ставки (либо через команду укажите свою)', reply_markup=markup)
    if message.text == "Орёл":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item6_1 = types.KeyboardButton("/orel 1000")
        item6_2 = types.KeyboardButton("/orel 2000")
        item6_3 = types.KeyboardButton("/orel 5000")
        item4 = types.KeyboardButton("Назад")
        markup.add(item6_1, item6_2, item6_3, item4)
        bot.send_message(message.chat.id, 'Выберите сумму ставки (либо через команду укажите свою)',reply_markup=markup)
    if message.text == "Решка":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item7_1 = types.KeyboardButton("/reshka 1000")
        item7_2 = types.KeyboardButton("/reshka 2000")
        item7_3 = types.KeyboardButton("/reshka 5000")
        item4 = types.KeyboardButton("Назад")
        markup.add(item7_1, item7_2, item7_3, item4)
        bot.send_message(message.chat.id, 'Выберите сумму ставки (либо через команду укажите свою)',reply_markup=markup)


    if "/roll" in message.text:
        try:
            bet = int(message.text.split(" ")[1])
            result = random.randint(100, 777)
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute(f"SELECT balance FROM users WHERE id = ?", userid)
            balance = cur.fetchone()[0]
        except Exception as er:
            print(er)
        if balance > 0 and bet <= balance:
            try:
                bot.send_message(message.chat.id, f"ставка {bet}")
                if result == 111 or result == 222 or result == 333 or result == 444 or result == 555 or result == 666:
                    try:
                        balance += bet * 75
                        bot.send_message(message.chat.id, f"Вам выпало {result}!\n Вы выиграли {bet*75}\nОстаток: {balance}")

                        temp = [balance, message.chat.id]
                        cur.execute("UPDATE users SET balance = ? WHERE id = ?", temp)
                        conn.commit()
                        bot.send_message(message.chat.id, f'Ты выиграл {bet * 75}!')
                    except Exception as er:
                        bot.send_message(message.chat.id, 'Что-то пошло не так!')
                        print(er)
                elif result == 777:
                    try:
                        balance += bet * 150
                        temp = [balance, message.chat.id]
                        cur.execute("UPDATE users SET balance = ? WHERE id = ?", temp)
                        conn.commit()
                        bot.send_message(message.chat.id, f"Джекпот! выпало 777\n Вы выиграли {bet * 150}\nОстаток: {balance}")
                    except Exception as er:
                        print(er)
                        bot.send_message(message.chat.id, 'Что-то пошло не так!')
                else:
                    try:
                        balance = int(balance) - int(bet)
                        temp = [balance, message.chat.id]
                        cur.execute("UPDATE users SET balance = ? WHERE id = ?", temp)
                        conn.commit()
                        bot.send_message(message.chat.id, f'Выпало {result}\nТы проиграл {bet}\nОстаток: {balance}!')

                    except Exception as er:
                        print(er)
                        bot.send_message(message.chat.id, 'Что-то пошло не так!')
            except Exception as er:
                print(er)
                bot.send_message(message.chat.id, 'Что-то пошло не так!')
        else:
            bot.send_message(message.chat.id, "НЕТ ДЕНЕГ(((")
    if "/change" in message.text and message.chat.id in admins:
        try:
            splitting = message.text.split(" ")
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            temp = [splitting[1], splitting[2]]
            cur.execute(f"UPDATE users SET balance = ? WHERE id = ?", temp)
            conn.commit()
            bot.send_message(message.chat.id, f"Вы успешно сменили баланс юзеру {temp[1]} на {temp[0]}")
        except Exception as er:
            print(er)
            bot.send_message(message.chat.id, 'Что-то пошло не так!')

    if "/reshka" in message.text:
        try:
            bet = int(message.text.split(" ")[1])
            result = random.randint(1,2)
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute(f"SELECT balance FROM users WHERE id = ?", userid)
            balance = cur.fetchone()[0]
        except Exception as er:
            print(er)
        if balance > 0 and bet <= balance:
            try:
                bot.send_message(message.chat.id, f"ставка {bet}")
                if result == 1:
                    try:
                        bot.send_message(message.chat.id, f"Вам выпала решка!\n Вы выиграли {bet*2}\nОстаток: {balance + bet*2}")
                        balance += bet * 2
                        temp = [balance, message.chat.id]
                        cur.execute("UPDATE users SET balance = ? WHERE id = ?", temp)
                        conn.commit()
                    except Exception as er:
                        bot.send_message(message.chat.id, 'Что-то пошло не так!')
                        print(er)
                else:
                    try:
                        balance = int(balance) - int(bet)
                        temp = [balance, message.chat.id]
                        cur.execute("UPDATE users SET balance = ? WHERE id = ?", temp)
                        bot.send_message(message.chat.id, f'Выпал Орёл\nТы проиграл {bet}\nОстаток: {balance}!')
                        conn.commit()
                    except Exception as er:
                        print(er)
                        bot.send_message(message.chat.id, 'Что-то пошло не так!')
            except Exception as er:
                print(er)
                bot.send_message(message.chat.id, 'Что-то пошло не так!')
        else:
            bot.send_message(message.chat.id, "НЕТ ДЕНЕГ")
    if "/orel" in message.text:
        try:
            bet = int(message.text.split(" ")[1])
            result = random.randint(1,2)
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute(f"SELECT balance FROM users WHERE id = ?", userid)
            balance = cur.fetchone()[0]
        except Exception as er:
            print(er)
        if balance > 0 and bet <= balance:
            try:
                bot.send_message(message.chat.id, f"ставка {bet}")
                if result == 1:
                    try:
                        bot.send_message(message.chat.id, f"Вам выпал орёл!\n Вы выиграли {bet*2}\nОстаток: {balance + bet*2}")
                        balance += bet * 2
                        temp = [balance, message.chat.id]
                        cur.execute("UPDATE users SET balance = ? WHERE id = ?", temp)
                        conn.commit()
                    except Exception as er:
                        bot.send_message(message.chat.id, 'Что-то пошло не так!')
                        print(er)
                else:
                    try:
                        balance = int(balance) - int(bet)
                        temp = [balance, message.chat.id]
                        cur.execute("UPDATE users SET balance = ? WHERE id = ?", temp)
                        bot.send_message(message.chat.id, f'Выпала решка\nТы проиграл {bet}\nОстаток: {balance}!')
                        conn.commit()
                    except Exception as er:
                        print(er)
                        bot.send_message(message.chat.id, 'Что-то пошло не так!')
            except Exception as er:
                print(er)
                bot.send_message(message.chat.id, 'Что-то пошло не так!')
        else:
            bot.send_message(message.chat.id, "НЕТ ДЕНЕГ")







#MESSAGE DEF
while True:
    try:
        bot.polling()
    except Exception as er:
        print(er)
