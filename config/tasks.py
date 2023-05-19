from celery import shared_task
import ffmpeg

@shared_task
def convert_to_hls(rtsp_link, out_path):
    try:
        stream = ffmpeg.input(rtsp_link)
        stream = ffmpeg.output(stream, out_path, format='hls', start_number=0, hls_time=2, hls_list_size=10)
        ffmpeg.run(stream)
    except ffmpeg._run.Error as e:
        raise Exception(str(e))