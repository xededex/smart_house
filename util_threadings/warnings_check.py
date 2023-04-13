import time
from config_data.config import Config, load_config
from database.sqlite_api import DB_API
import asyncio

config : Config = load_config()
db = DB_API()

input_queue  = None
output_queue = None
bot          = None



def init_(bot_, in_, out_):
    global bot, input_queue, output_queue
    input_queue  = in_
    output_queue = out_
    bot          = bot_
    


class Alert_Messages:
    all_msg = {
        "temp"  : "Кажется, вы горите",
        "water" : "Кажется, вы тонете",
        "co2"   : "Кажется, вы задыхаетесь от co2",
        "gas"   : "Кажется, вы задыхаетесь, но не от co2"
    }
    
    @staticmethod 
    def get_alert_msg(alert, user_name) -> str:
        _, type_, val, from_, time  = alert.split(', ')
        
        
        
        return f"Уважаемый, {user_name}, {Alert_Messages.all_msg[type_]}, Значение : {val}"
        


async def broadcast(msg: str):
    subscribed_user = db.show_all_users()
    for user in subscribed_user:
        await bot.send_message(user["user_id"], Alert_Messages.get_alert_msg(msg, user["user_name"]))




DIFF = 3


counter = {
    "co2"   : 0,
    "water" : 0,
    "temp"  : 0,
    "gas"   : 0,
}
def is_alert(type):
    global counter
    print(counter)
    if counter[type] >= DIFF:
        counter[type] = 0
        return True
    else:
        counter[type] += 1
        return False
    

async def check_warnings() -> None:
        # await asyncio.sleep(10)
        
    print("check_warnings")
    # print(bot)
    if not output_queue.empty():
        msg = output_queue.get()
        print(msg)
        _, type_, val, from_, time  = msg.split(', ')
        # db.add_history(type = type_, from_= from_, time = time)
        print("broadcast")
        # if is_alert(type_):        
        await broadcast(msg)


# loop = asyncio.get_event_loop()
# asyncio.ensure_future(check_warnings())
# loop.run_forever()

# async def some_callback(args):
#     await some_function()

# def between_callback(args):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)


#     loop.run_until_complete(some_callback(args))
#     loop.close()

# _thread = threading.Thread(target=between_callback, args=("some text"))
# _thread.start()


        

