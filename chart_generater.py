from utils.chartwriter import ChartWriter
from note import notedata as nd
import random
import os
import shutil
from mutagen.mp3 import MP3


path_dict = {'63':0, '64':0, '65':0, \
             '191':1, '192':1, '193':1,\
             '319':2, '320':2, '321':2,\
             '447':3, '448':3, '449':3}

def generate_chart_div(name:str):
    dir_path = os.path.join('save', 'trackfile', name)
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

def generate_cover(src_path: str, dest_dir: str):
    """
    生成谱面封面
    :param src_path: 源图片路径
    :param dest_path: 目标路径
    """
    dest_name = 'cover.png'
    dest_path = os.path.join(dest_dir, dest_name)
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source cover image {src_path} does not exist.")
    shutil.copy(src_path, dest_path)

def generate_music(src_path: str, dest_dir: str):
    """
    生成谱面音乐文件
    :param src_path: 源音乐路径
    :param dest_dir: 目标目录
    """
    dest_name = 'music.mp3'
    dest_path = os.path.join(dest_dir, dest_name)
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source music file {src_path} does not exist.")
    shutil.copy(src_path, dest_path)
    audio = MP3(dest_path)
    duration_ms = int(audio.info.length * 1000)
    return duration_ms

def generate_chart(src_path: str, dest_dir: str, name: str, duration: int, bpm: int):
    chart = ChartWriter(name)
    # 默认值
    title = 'Unknown'
    artist = 'Unknown'
    chart_maker = 'Unknown'

    in_metadata = False
    in_hitobjects = False
    hitobject_lines = []

    with open(src_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 检查section
            if line.startswith('[Metadata]'):
                in_metadata = True
                in_hitobjects = False
                continue
            elif line.startswith('[HitObjects]'):
                in_metadata = False
                in_hitobjects = True
                continue
            elif line.startswith('['):
                in_metadata = False
                in_hitobjects = False
                continue

            # 读取Metadata
            if in_metadata:
                if line.startswith('Title:'):
                    title = line.split(':', 1)[1].strip()
                elif line.startswith('Artist:'):
                    artist = line.split(':', 1)[1].strip()
                elif line.startswith('Creator:'):
                    chart_maker = line.split(':', 1)[1].strip()
            # 收集HitObjects
            if in_hitobjects:
                hitobject_lines.append(line)

    chart.create_chart(bpm, duration, 0)
    for line in hitobject_lines:
        parts = line.split(',')
        if len(parts) < 5:
            continue
        path = path_dict.get(parts[0], 0)
        start_time = int(parts[2])
        if parts[3] == '128':
            suffix = parts[5].split(':')
            end_time = int(suffix[0])
            chart.add_note_by_time(nd.NoteType.HOLD, start_time, path, end_time - start_time)
        else:
            chart.add_note_by_time(nd.NoteType.TAP, start_time, path)
    # 将元数据传递给ChartWriter
    chart.track_file.title = title
    chart.track_file.artist = artist
    chart.track_file.chart_maker = chart_maker
    chart.save()

