import string

def calculate_bigram_frequencies(file_path, word_dict):
    index = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        bigram_dict = {}
        for line in file:
            if index == 1000000:
                print("Mile stone")
                index = 0
            index+=1
            # Remove punctuation and convert to lowercase
            cleaned_line = line.translate(str.maketrans("", "", string.punctuation)).lower().split(" ")

            # Split the line into words
            bigrams = [(cleaned_line[i], cleaned_line[i+1]) for i in range(len(cleaned_line)-1)]

            # Update word frequencies in the dictionary
            for bigram in bigrams:
                if bigram[0] in word_dict and bigram[1] in word_dict:
                    sen = bigram[0] + " " + bigram[1]
                    if(bigram_dict.get(sen) is not None):
                        bigram_dict[sen]+=1
                    else:
                        bigram_dict[sen] = 1
    
    write_word_frequencies_to_file(bigram_dict)


def write_word_frequencies_to_file(bigram_dict):
    bigram_list = sorted(bigram_dict.items(), key=lambda x: x[1], reverse=True)
    with open('./vietnamese_bigram_frequency.txt', 'a', encoding='utf-8') as file:
        for bigram, frequency in bigram_list:
            file.write(f"{bigram} {frequency}\n")

def load_dictionary():
    word_dict = set()

    with open('./index.dic', 'r', encoding='utf-8') as dic_file:
        for line in dic_file:
            # Remove leading and trailing whitespaces, and convert to lowercase
            dictionary_word = line.strip().lower()
            
            # Add the lowercase word to the set
            word_dict.add(dictionary_word)

    return word_dict

if __name__ == "__main__":
    file_path = "./corpus-full.txt"
    word_dict = load_dictionary()

    # Calculate word frequencies
    calculate_bigram_frequencies(file_path, word_dict)

    
