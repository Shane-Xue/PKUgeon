from chartwriter import ChartWriter
from note import notedata as nd
import random

chart = ChartWriter('test')
chart.create_chart(120, 60000, 0)
for i in range(0, 480, 8):
    chart.add_note(nd.NoteType.TAP, i, random.randint(0, 3))
    # chart.add_note(nd.NoteType.HOLD, i + 4, random.randint(0, 3), i + 8)
chart.save()

