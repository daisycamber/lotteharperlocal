import sys
to_upload = 1
if len(sys.argv) > 1: to_upload = int(sys.argv[2])
print('Uploading {} videos to YouTube.'.format(to_upload))
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotteh.settings')
import django
django.setup()
from django.conf import settings
from live.models import VideoRecording, VideoCamera
from live.models import get_file_path
import pytz, os, traceback
from django.conf import settings
from recordings.youtube import upload_youtube
from better_profanity import profanity
count = 0
for recording in VideoRecording.objects.filter(processed=True, uploaded=False).order_by('-last_frame'):
    cameras = VideoCamera.objects.filter(name=recording.camera, user=recording.user).order_by('-last_frame')
    print(recording)
#    print(cameras)
    camera = cameras.first()
    from live.duration import get_duration
    if camera.upload and get_duration(recording.file.path) > settings.LIVE_INTERVAL/1000 * 1.5:
        try:
            if not (recording.file and os.path.exists(recording.file.path)):
                print('Getting file from bucket for upload')
                full_path = os.path.join(settings.BASE_DIR, 'media/', get_file_path(None, 'rec.mp4'))
                with recording.file_processed.storage.open(str(recording.file_processed.name), mode='rb') as bucket_file:
                    with open(full_path, "wb") as video_file:
                        video_file.write(bucket_file.read())
                    video_file.close()
                bucket_file.close()
                recording.file = full_path
                recording.save()
        except: print(traceback.format_exc())
        try:
            import requests
            files = None
            with open(recording.file.path, 'rb') as file:
                files = {'file': file}
                payload = {'id_file': 'rec.mp4'}
                resp = requests.post('https://lotteh.com/upload/?k={}'.format(settings.UPLOAD_KEY), files=files, data=payload)
                print(resp)
                print(resp.text)
                print(resp.status_code)
                if resp.status_code == 200:
                    recording.uploaded = True
        except:
            recording.uploaded = False
            print(traceback.format_exc())
        recording.save()
        count+=1
    if count >= to_upload: break
