import psutil
import requests
import argparse

parser = argparse.ArgumentParser(description="Скрипт для мониторинга ресурсов сервера и отправки отчетов в Telegram.")
parser.add_argument("-nick", type=str, required=True, 
                    help="Никнейм или название вашего сервера (отображается в заголовке)")
parser.add_argument("-api_key", type=str, required=True, 
                    help="API токен вашего Telegram бота")
parser.add_argument("-chat_id", type=str, required=True, 
                    help="ID чата, в который нужно отправить сообщение")
parser.add_argument("-thread_id", type=str, required=False, 
                    help="ID ветки (thread) в супергруппах Telegram (необязательно)")

args = parser.parse_args()
args = parser.parse_args()

cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory()
disks = ''
for part in psutil.disk_partitions():
    try:
        if part.opts == 'ro,readonly,cdrom':
            continue
        usage = psutil.disk_usage(part.mountpoint)
        disks += f'Диск: {part.device[:1]} - {usage.percent}%\n'
    except Exception:
        continue


message =   (f"<u><b>Сервер: {args.nick}</b></u>\n\n"+
             "<b>Загрузка процессора:</b> "+
             f'{cpu} %\n'+
             "<b>Использование RAM:</b> "+
             f'{ram.percent} %\n'+
             "<b>Информация о дисках:</b>\n"+
             disks)
url = f"https://api.telegram.org/bot{args.api_key}/sendMessage"
data = {
    'chat_id': args.chat_id,
    'text': message,
    'parse_mode': 'HTML',
}

if args.thread_id is not None:
    data['message_thread_id'] = args.thread_id

try:
    response = requests.post(url, data=data)
    response.raise_for_status() 
    print(f"Статус отправки: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Ошибка при отправке: {e}")
print(response.status_code)