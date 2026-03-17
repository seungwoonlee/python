cities = ['Seoul', 'Suwon', 'Gumi']
f = open('city.txt', 'w')
f.write('\n'.join(cities))
f.close()

li = []
f = open('city.txt', 'r')
li = f.read().split()
f.close()
print(li)