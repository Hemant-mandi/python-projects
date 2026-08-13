try:

    n = int(input("enter number a: "))
    p = int(input("enter number b: "))

    ch = input("Enter operation: ")

    match ch:
        case '+': print(n+p)
        case '-': print(n-p)
        case '*': print(n*p)
        case '/': print(n/p)
        case default: print("wrong number")

except Exception as e:
    print("there occured some error")