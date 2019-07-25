
import time
from datetime import timedelta, datetime
from timeloop import Timeloop


def send_message_per_hour(bot):
    tl = Timeloop()

    @tl.job(interval=timedelta(seconds=15))
    def send_message():
        pass
"Сейчас(вроде) всё время хранится в ютс0 тут надо получать chat_id, reminder_time, всех юзеров у которых" \
"бот статус = ОН, далее сравниваем совпадает ли текущее время с reminder_time если да то шлем сообшение и увеличиваем время на 1." \
"как то надо учесть шоб время ставилось на wake_up если выпита норма или уже поздно"

