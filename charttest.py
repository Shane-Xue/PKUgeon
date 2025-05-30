from chartwriter import ChartWriter
from note import notedata as nd
import random

path_dict = {'51':0, '153':1, '256':2, '358':3}
chart = ChartWriter('test')

chart.create_chart(150, 66000)
with open('rawchart', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split(',')
        path = path_dict[parts[0]]
        start = int(parts[2])//100
        if parts[3] == '1':
            chart.add_note(nd.NoteType.TAP, start, path)
        elif parts[3] == '128':
            suffix = parts[5].split(':')
            end = int(suffix[0])//100
            chart.add_note(nd.NoteType.HOLD, start, path, end)
chart.save()

