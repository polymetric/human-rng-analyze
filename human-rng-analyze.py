import json
import arrow
from statistics import *
import re
import matplotlib.pyplot as plot

class Exemption:
    start: int
    end: int
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __str__(self):
        return f"start={self.start}, end={self.end}"

class ExemptException(Exception):
    range: Exemption
    m_id: int




f = open('dump2.json').read()
messages = json.loads(f)

re_numfilter = re.compile('^[0-9]$')
re_exemptfilter = re.compile('exempt ([0-9]*)\.\.([0-9]*)')

# get all the exemptions
exemptions = []
for m_id in messages:
    message = messages[m_id]
    match = re_exemptfilter.match(message['content'])
    if match == None:
        continue
    if len(match.groups()) != 2:
        continue
    exemptions.append(Exemption(start=match.group(1), end=match.group(2)))

# 1st stage filter
# this stage isolates the actual numbers from
# the rest of the messages
messages_filtered = dict()
for m_id in messages:
    # loop through all our exemption ranges
    # if the message is exempted then we'll skip to the next message
    try:
        for e in exemptions:
            if m_id >= e.start and m_id <= e.end:
                raise ExemptException(e, m_id)
    except ExemptException:
        continue
    m = messages[m_id]
    if re_numfilter.match(m['content']) == None:
        continue
    messages_filtered[m_id] = m
messages = messages_filtered

# 2nd stage filter
# this stage only passes messages from certain users
messages_filtered = dict()
for m_id in messages:
    m = messages[m_id]
    # TODO filter checks
    messages_filtered[m_id] = m
messages = messages_filtered

total = 0
nums = []
f = open('nums', 'w')

for m_id in messages:
    m = messages[m_id]
#    print(m_id, m)
    total += 1
    nums.append(int(m['content']))
    f.write(f"{int(m['content'])}\n")

mean = mean(nums)
median = median(nums)
mode = mode(nums)

print(f"total: {total} mean: {mean} median: {median} mode: {mode}")

plot.hist(nums)
plot.show()




