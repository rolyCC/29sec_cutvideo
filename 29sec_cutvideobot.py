from pyrogram import Client, filters
from pyrogram.types import Message
import os
import subprocess
import math

# Crea un cliente Pyrogram
api_id = 
api_hash = 
bot_token = 
app = Client('my_bot', api_id, api_hash, bot_token=bot_token)

# Definimos la función que se ejecuta cuando recibimos el comando /start
@app.on_message(filters.command("start"))
def start(client, message):
    # Enviamos un mensaje con lo que hace el bot
    message.reply_text("Hola! Soy un bot que puede dividir tus vídeos en segmentos de 29 segundos.")

# Definimos la función que se ejecuta cuando recibimos un vídeo
@app.on_message(filters.video)
def process_video(client, message):
    # Enviamos un mensaje de "procesando"
    message.reply_text("Procesando...")
    
    # Descargamos el vídeo y lo renombramos
    video_path = message.download()
    os.rename(video_path, "Video.mp4")

    # Obtenemos la duración del vídeo en segundos
    duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', 'Video.mp4']))
    
    # Definimos el tiempo de duración de los segmentos
    segment_duration = 29
    
    # Calculamos cuántos segmentos necesitamos
    num_segments = math.ceil(duration / segment_duration)

    # Dividimos el vídeo en segmentos
    for i in range(num_segments):
        # Calculamos los tiempos de inicio y fin del segmento
        start_time = i * segment_duration
        end_time = min(start_time + segment_duration, duration)
        
        # Creamos el nombre del archivo del segmento
        segment_path = f"Video_{i+1}.mp4"

        # Extraemos el segmento usando ffmpeg
        subprocess.call(['ffmpeg', '-y', '-i', 'Video.mp4', '-ss', str(start_time), '-t', str(end_time - start_time), '-c:v', 'copy', '-c:a', 'aac', segment_path])

        
        # Enviamos el segmento al usuario
        client.send_video(message.chat.id, segment_path)
        
        # Borramos el archivo del segmento
        os.remove(segment_path)

    # Borramos el archivo del vídeo original
    os.remove("Video.mp4")

# Iniciamos el cliente de Pyrogram
app.run()
