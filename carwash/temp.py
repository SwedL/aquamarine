# fields = [['time_' + str(k) + ('0', '')[i] + str(i*30) for i in range(0, 2)] for k in range(10, 21)]
fields = [('time_' + str(k) + '00', 'time_' + str(k) + '30') for k in range(10, 21, 5)]

print(fields, sep=' ')
