from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import audio as mp_audio
from mediapipe.tasks.python.components import containers as mp_containers
import sounddevice as sd
from datetime import datetime, timedelta
from notifier import send_notification

THRESHOLD = 0.1
SAMPLE_RATE = 16000
SECONDS = 1
cry_count = 0
silence_count = 0
CRY_COUNT_THERESHOLD = 5
SILENCE_RESET_THERSHOLD = 10
alerted = False
last_notification_time = datetime.min
HEARTBEAT_INTERVAL = timedelta(seconds = 5)


options = mp_audio.AudioClassifierOptions(
    base_options=mp_python.BaseOptions(model_asset_path="yamnet.tflite"),
    max_results=10,
  )
classifier = mp_audio.AudioClassifier.create_from_options(options)
print("模型加载成功.")
print("监护中...")
log_file = open("cry_log.csv","a",encoding="utf-8")
try:
  while True:
      is_crying = False
      cry_score = 0
      top_category = ""
      top_score = 0
      audio_data = sd.rec(SAMPLE_RATE * SECONDS,samplerate = SAMPLE_RATE,channels = 1)
      sd.wait()
      volume = abs(audio_data).max()
      print(volume,cry_count)
      #检查音量是否超过阈值
      if volume > THRESHOLD:
        print("检测到声音")
        clip = mp_containers.AudioData.create_from_array(audio_data, SAMPLE_RATE)
        result = classifier.classify(clip)
        top = result[0].classifications[0].categories[0]
        top_category = top.category_name
        top_score = top.score
        for category in result[0].classifications[0].categories:
          if category.category_name == "Baby cry, infant cry" and category.score > 0.2:
            is_crying = True
          if category.category_name == "Baby cry, infant cry":
            cry_score = category.score
      #更新哭或者安静的秒数
      if is_crying:
        cry_count += 1
        silence_count = 0
        if cry_count >= CRY_COUNT_THERESHOLD and not alerted:
          print("宝宝正在哭")
          send_notification(f'datetime:{datetime.now()}, 宝宝正在哭')
          alerted = True
      else:
        silence_count += 1
        if silence_count >= SILENCE_RESET_THERSHOLD:
          cry_count = 0
          alerted = False
        if datetime.now() - last_notification_time > HEARTBEAT_INTERVAL:
          last_notification_time = datetime.now()
          send_notification(f'datetime: {datetime.now()}, 监护器心跳: 宝宝监控运行中')
      log_file.write(f'{datetime.now()},{volume},{is_crying},{cry_score},"{top_category}",{top_score}\n')
      log_file.flush()
except KeyboardInterrupt:
  print("监护停止")
