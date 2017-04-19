def open_text(fname):
    phrases = []
    with open (fname, 'r', encoding = 'utf-8') as f:
        text = f.read()
    return text

def count_examples(text, identifier):
    return text.count(identifier)

def main():
    print(count_examples(open_text('text.txt'), '['))

if __name__ == '__main__':
    main()
