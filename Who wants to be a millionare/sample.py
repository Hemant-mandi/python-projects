lists = [
    ["what do you call a puppy?","kutte ka bachha","awlelelelele","kuchu puchu","phis phis phis",3],
    ["kya chabbis mein duniya khatam hui?","ha hui na","meri duniya chor gayi","meri duniya mere paas hai","tum tu dum dum thisyaooooo",4]
        ]

points = 0;

for list in lists :
    print(list[0])
    print(f"1) {list[1]}")
    print(f"2) {list[2]}")
    print(f"3) {list[3]}")
    print(f"4) {list[4]}")

    ans = int(input("Enter the correct option: "))
    if(ans == list[5]):
        print("Yayyy you guessed it right!!!")
        points += 1
    else: 
        print("Betterluck next time!")
        break

print(f"your final score is: {points}")