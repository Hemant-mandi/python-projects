import qrcode

url = input("enter the url: ")

filename = input("Enter the filename: ")

if not filename.endswith(".png"):
    filename + ".png"

img = qrcode.make(url)
img.save(filename)