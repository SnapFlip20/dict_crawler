#-*- coding:utf-8 -*-

# English Dictionary Crawler --------- by SnapFlip20
# crawling from https://www.wordsapi.com
# 2023/11/25 last updated



import requests

def crawler(api, word):
    # API from WordsAPI
    url = f'https://wordsapiv1.p.rapidapi.com/words/{word}'
    headers = {
        'X-RapidAPI-Key': api,
        'X-RapidAPI-Host': 'wordsapiv1.p.rapidapi.com'
    }
    response = requests.get(url, headers=headers)

    # request acceped
    if response.status_code == 200:
        jdata = response.json()
        if 'results' in jdata:
            results = jdata['results'][0]
            lst = {
                'word': word,
                'pos': results.get('partOfSpeech', ''),
                'synonyms': results.get('synonyms', []),
                'examples': results.get('examples', [])
            }
            return lst
    # request failed(search error)
    else:
        print(f'"{word}" was not founded. . .')
        return False



if __name__ == "__main__":
    api_key = ""
    fout = open('output.txt', 'w')
    pos_type = ['NOUN', 'VERB', 'ADJ', 'ADV', 'PREPOS']
    
    while True:
        search_word = input("input word[exit key: 0]: ")
        if search_word == '0':
            break
        word_info = crawler(api_key, search_word)

        if word_info:
            # parsing data
            word = word_info['word']
            pos = word_info['pos'].replace('adjective', 'ADJ').replace('adverb', 'ADV').replace('preposition', 'PREPOS').upper()
            if pos not in pos_type:
                continue
            synonyms = word_info['synonyms']
            for i in range(len(synonyms)):
                synonyms[i] = '"' + synonyms[i] + '"'
            synonyms = ', '.join(synonyms)
            example = ', '.join(word_info['examples'])
            
            if len(example) > 0:
                print(f' word:     {word}')
                print(f' pos:      {pos}')
                print(f' synonyms: {synonyms}')
                print(f' examples: {example}')

                fout.write('Voca(')
                fout.write(f'"{word}", {pos}, ')
                fout.write('{ ')
                for i in synonyms:
                    fout.write(i)
                fout.write(' }, {')
                fout.write(f' "{example}" ')
                fout.write('}),\n')
        else:
            print('request failed . . .')

    fout.close()
