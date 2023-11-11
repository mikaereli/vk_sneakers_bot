import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

vk_session = vk_api.VkApi(token = "TOKEN")
session_api = vk_session.get_api()
global yuan, choose
yuan = 13.85

def send_message(sender, message, keyboard=None):
    post = {'user_id': sender, 'message': message, 'random_id': 0}

    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
 
    vk_session.method('messages.send', post)

def calculate(sender, price, command):

    price_rub = yuan * int(price)
    if command == "Обувь":
        if price_rub < 5000:
            price_rub += 1500
        elif 5000 <= price_rub < 20000:
            price_rub += 2000
        elif 20000 <= price_rub < 70000:
            price_rub += 2500
        else:
            price_rub += 0
            send_message(sender, """Доставку будем обговаривать индивидуально. 
                         Итоговая цена без доставки: """, keyboard=None)
    
    elif command == "Одежда": 
        if price_rub < 5000:
            price_rub += 800
        elif 5000 <= price_rub < 20000:
            price_rub += 1200
        elif 20000 <= price_rub < 70000:
            price_rub += 1600
        else:
            price_rub += 0
            send_message(sender, """Доставку будем обговаривать индивидуально. 
                         Итоговая цена без доставки: """, keyboard=None)
    else:
        if price_rub < 20000:
            price_rub += 2500
        elif 20000 <= price_rub < 70000:
            price_rub += 4000
        else:
            price_rub += 0
            send_message(sender, """Доставку будем обговаривать индивидуально. 
                         Итоговая цена без доставки: """, keyboard=None)

    vk_session.method('messages.send', {'user_id': sender, 'message': str(int(price_rub)), 'random_id': 0})

for event in VkLongPoll(vk_session).listen():     
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        recieved_message = event.text
        sender = event.user_id
        
        if recieved_message.lower() == "начать":            
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button("Сделать заказ", VkKeyboardColor.POSITIVE)
            keyboard.add_button("Отследить заказ", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("Рассчитать стоимость", VkKeyboardColor.SECONDARY)
            keyboard.add_button("Текущий курс юаня", VkKeyboardColor.SECONDARY)
            keyboard.add_line()
            keyboard.add_button("Обратиться в поодержку", VkKeyboardColor.NEGATIVE)

            send_message(sender, """Привет привет! Это бот TrendBin. 
Выбери команду:
""", keyboard)
            
        elif recieved_message == "Сделать заказ":
            send_message(sender, "https://vk.com/aleksvova")
        
        elif recieved_message == "Отследить заказ":
            pass
        
        elif recieved_message == "Рассчитать стоимость":
            keyboard_calcul = VkKeyboard(one_time=True)
            keyboard_calcul.add_button("Одежда", VkKeyboardColor.PRIMARY)
            keyboard_calcul.add_line()
            keyboard_calcul.add_button("Обувь", VkKeyboardColor.PRIMARY)
            keyboard_calcul.add_line()
            keyboard_calcul.add_button("Техника", VkKeyboardColor.PRIMARY)
            send_message(sender, "Выберите категорию", keyboard=keyboard_calcul)
        
        elif recieved_message == "Одежда" or recieved_message == "Обувь" or recieved_message == "Техника":
            choose = recieved_message
            send_message(sender, "Введите стоимость в юанях")

        elif recieved_message == "Текущий курс юаня":
            send_message(sender, f"Текущий курс юаня на данный момент: {yuan}")
        
        elif recieved_message == "Обратиться в поодержку":
            keyboard_help = VkKeyboard(one_time=True)
            keyboard_help.add_button("Начать", VkKeyboardColor.PRIMARY)
            send_message(sender, "Ожидайте. Через некоторое время вам ответят.", keyboard_help)

        elif int(recieved_message):
            calculate(sender, recieved_message, choose)
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button("Сделать заказ", VkKeyboardColor.POSITIVE)
            keyboard.add_button("Отследить заказ", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("Рассчитать стоимость", VkKeyboardColor.SECONDARY)
            keyboard.add_button("Текущий курс юаня", VkKeyboardColor.SECONDARY)
            keyboard.add_line()
            keyboard.add_button("Обратиться в поодержку", VkKeyboardColor.NEGATIVE)
            send_message(sender, """<-- Итоговая стоимость с учетом доставки. 
                         Чтобы посмотреть стоимость доставки перейдите по ссылке: https://vk.com/@trendbin-ras -->""", keyboard)
            

