import re

def extract_words(text):
    text = text.lower()
    # Split the text into individual words
    words = text.split()
    return words


def main():
    word_set= set()
    index = 0
    allowed_characters = re.compile(r'^[a-zA-Z]+$')
    # Read the input text file
    with open('../dataset/corpus-full.txt', 'r', encoding='utf-8') as text_file:
        for line in text_file:
            print("Reading index: " +str(index))
            index+=1
            # Extract words from the text
            words = extract_words(line)
            for word in words:
                if word not in word_set and allowed_characters.match(word):
                    word_set.add(word)

    # Write words to the .dic file
    with open('./vocab.dic', 'w', encoding='utf-8') as dic_file:
        for word in word_set:
            dic_file.write(f"{word}\n")

    print("Words written to vocab.dic")


if __name__ == "__main__":
    main()