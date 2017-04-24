## Я хочу, чтоб каждый пример был преобразован в 1 строку таблицы SCV.
## Строка (по клетке):
##    Левый контекст;
##    выделенные слова из левого контеста;
##    "ни шиша" - лучше бы, чтобы case-sensitive, но я не могу это умно сделать;
##    правый контекст без ссылки;
##    выделенные слова из правого контекста; 
##    источник - внутри квадратных скобок;
##    дата - внутри круглых скобок внутри квадратных;
## Если в строке нет сочетания "ни шиша", то вся строка превращается в первую клетку.


import csv
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
        n_case = re.search('(Н|н)и(?:\n|.)*?шиша', ex)
        if n_case:
            n_case = n_case.group(1)
        else:
            n_case = ''
        raw_n = re.search('(Н|н)и(?:\n|.)*?шиша', ex)
        if raw_n:
            ex = re.sub('(Н|н)и(?:\n|.)*?шиша', n_case+'и шиша', ex)
        else:
            lines_list = re.findall('RU\'>((?:.|\n)*?)<', ex)
            non_n_list = []
            for match in lines_list:
                examples.append(match)
            ## Тут надо написать чтобы он добавлял в примеры строки без ни шиша
        n = re.search('(?:Н|н)и шиша', ex)
        if n:
            n = n.group(0)
            raw_lcontext = re.split('(?:Н|н)и шиша', ex)[0].strip()
            raw_rcontext = re.split('(?:Н|н)и шиша', ex)[1].strip()
            raw_rcontext = re.sub('\[.*?\]','', raw_rcontext)
        else:
            raw_lcontext = ''
            raw_rcontext = ''
        lcontext = re.findall('RU\'>((?:.|\n)*?)<', raw_lcontext)
        if lcontext:
            match_list = []
            for match in lcontext:
                match_list.append(match)
            lcontext = ' '.join(match_list)
        else:
            lcontext = ''
        rcontext = re.findall('RU\'>((?:.|\n)*?)<', raw_rcontext)
        if rcontext:
            match_list = []
            for match in rcontext:
                match_list.append(match)
            rcontext = ' '.join(match_list)
##            if link:
##                re.sub(link.group(), '', rcontext) if error
####            Убрать ссылки из примера - []
            else:
                pass
        else:
            rcontext = ''
        lcontext_highlight = re.search('<i(?:.|\n)*?RU\'>((?:.|\n)*?)<(?:.|\n)*?<\/i>', raw_lcontext)
        if lcontext_highlight:
            lcontext_highlight = lcontext_highlight.group(1)
        else:
            lcontext_highlight = ''
        rcontext_highlight = re.search('<i(?:.|\n)*?RU\'>((?:.|\n)*?)<(?:.|\n)*?<\/i>', raw_rcontext)
        if rcontext_highlight:
            rcontext_highlight = rcontext_highlight.group(1)
        else:
            rcontext_highlight = ''
        examples.append([lcontext, lcontext_highlight, n, rcontext, rcontext_highlight, source, date])
##        сделать все элементы одноэлементными массивами, втч lcontext, rcontext, он почему-то печатает их в кавычках
    return examples


def main():
    
    examples = find_examples(open_text('html.txt'))
    with open('example_final_spreadsheet.csv', 'w', encoding='utf-8') as n:
        text = csv.writer(n, delimiter=',')
        header = ['lcontext', 'lcontext_highlight', 'n', 'rcontext', 'rcontext_highlight', 'source', 'date'] # это будет заголовок
        text.writerow(header)
        for row in examples:
            text.writerow(row)

if __name__ == '__main__':
    main()
