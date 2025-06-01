from chartwriter import ChartWriter
from note import notedata as nd
import random

path_dict = {'64':0, '192':1, '320':2, '321':2, '448':3, '449':3}
chart = ChartWriter('testify')

chart.create_chart(178, 194000, 1322)
with open('rawchart', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split(',')
        path = path_dict[parts[0]]
        start = round((int(parts[2]) - 1322)/(60000/178) * 4)
        if parts[3] == '128':
            suffix = parts[5].split(':')
            end = round((int(suffix[0]) - 1322)/(60000/178) * 4)
            chart.add_note(nd.NoteType.HOLD, start, path, end)
        else:
            chart.add_note(nd.NoteType.TAP, start, path)
chart.save()

