import re
        
def open_text(fname):
    phrases = []
    with open (fname, 'r', encoding = 'utf-8') as f:
        text = f.read()
    return text

def find_examples(text):
    raw_examples = re.findall('<p (?:.|\n)*?\'>.*?<.*?\/p>', text)
    examples = []
    for ex in raw_examples:
        link = re.search('\[(.+?)\((.+?)\)\]', ex)
        if link:
            source = re.search('\[(.+?)\((.+?)\)\]', ex).group(1).strip()
            date = re.search('\[(.+?)\((.+?)\)\]', ex).group(2).strip()
        else:
            source = ''
            date = ''
        n = re.search('(?:Н|н)и шиша', ex).group(0)
        if n:
            lcontext = re.split('(?:Н|н)и шиша', ex)[0].strip()
            rcontext = re.split('(?:Н|н)и шиша', ex)[1].strip()
        else:
            lcontext = ''
            rcontext = ''
        examples.append([lcontext, n, rcontext, source, date])
        print()
    return examples

def main():
    print(find_examples(open_text('test.txt'))[0])

if __name__ == '__main__':
    main()
