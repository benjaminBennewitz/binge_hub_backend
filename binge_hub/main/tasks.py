import subprocess


"""
    triggers a cmd input to convert a video into 480p
"""
def convert_480p(source, target):
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd)

"""
    triggers a cmd input to convert a video into 720p
"""
def convert_720p(source, target):
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd)

"""
    triggers a cmd input to convert a video into 1080p
"""
def convert_1080p(source, target):
    cmd = 'ffmpeg -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd)