

diccio = {'x':9, 'y':4, 'u':1}

diccio = list(sorted(diccio.items(), key=lambda item: item[1], reverse= True))

print(diccio.pop()[0])