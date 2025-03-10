# for i in range(61):
#     if (i + 23) % 15 == 0:
#         print(i)


y = []
x = [1, 2, 2, 3, 4, 5, 5, 6, 7, 8, 8, 9]
for i in range(len(x)):
    if i < len(x) - 1:
        if x[i] == x[i + 1]:
            continue
        if x[i] % 1 == 0:
            y.append(x[i]) 
print(y)       