import string

def calculate_word_frequencies(file_path, word_dict):
    index = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if index == 1000000:
                print("Mile stone")
                index = 0
            index+=1
            # Remove punctuation and convert to lowercase
            cleaned_line = line.translate(str.maketrans("", "", string.punctuation)).lower()

            # Split the line into words
            words = cleaned_line.split()

            # Update word frequencies in the dictionary
            for word in words:
                if word_dict.get(word) is not None:
                    word_dict[word]+=1
    
    write_word_frequencies_to_file(word_dict)


def write_word_frequencies_to_file(word_dict):
    word_freq = [(k, v) for k, v in dict.items()]
    word_freq.sort(key=lambda x: x[1], reverse=True)
    with open('./vietnamese_word_frequency.txt', 'a', encoding='utf-8') as file:
        for word, frequency in word_freq:
            file.write(f"{word} {frequency}\n")

def load_dictionary():
    word_dict = {}

    with open('./index.dic', 'r', encoding='utf-8') as dic_file:
        for line in dic_file:
            # Remove leading and trailing whitespaces, and convert to lowercase
            dictionary_word = line.strip().lower()
            
            # Add the lowercase word to the set
            word_dict[dictionary_word] = 0

    return word_dict

if __name__ == "__main__":
    file_path = "./corpus-full.txt"
    word_dict = load_dictionary()

    # Calculate word frequencies
    calculate_word_frequencies(file_path, word_dict)

    input_file_path = "./vietnamese_word_frequency.txt"
    output_file_path = "./vietnamese_word_frequency.txt"

    # sort_word_frequencies(input_file_path, output_file_path)
    
