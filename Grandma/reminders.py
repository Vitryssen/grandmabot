import sys
channelId = ""
path = "../../reminders.txt"
file = open(path, 'r')
reminderValues = [line.strip('\n') for line in file]