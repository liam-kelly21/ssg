from textnode import *

def main():
    newnode = TextNode("This is some anchor text",TextType.LINK,"https://www.boot.dev")
    print(newnode)

if __name__ == "__main__":
    main()