def exchange_values_in_dict(some_dict, key, new_value):
    """
    Assigns value "new_value" to the key "key" from dict "some_dict", finds key which was associated with value
    "new_value" in dict "some_dict" and replaces its value with the previous value of key "key"
    :param some_dict:
    :param key:
    :param new_value:
    :return: dict with changed items
    """
    previous_value= some_dict[key]
    next_value = new_value
    for key1, new_value in some_dict.items():
        if some_dict[key1] == next_value:
            some_dict[key1] = previous_value
    some_dict[key] = next_value
    return some_dict

def leave_sure(string, sure_list:list):
    """
    Replaces all characters which are not in the list 'sure_list'
    :param string:
    :param sure_list:
    :return: new string
    """
    for i in range(len(string)):
        if string[i] not in sure_list:
            string = string[:i] +'-' + string[i+1:]
    return string

def exchange_letters(string: str, letter1, letter2):
    """
    Exchanges letters in string, such that all the letters 'letter1' become 'letter2",
    'letter2' become 'letter1'
    :param string:
    :param letter1:
    :param letter2:
    :return:
    """
    string = string.replace(letter1, '*')
    string = string.replace(letter2, letter1)
    string = string.replace('*', letter2)
    return string

def get_sym_freq_file(path):
    """

    :param path: path to the file
    :return: dict where each key is a symbol from file defined by path, value is a number of its occurrences in the file
    """
    file = open(path, "r")
    dict_fr = dict()
    for line in file:
        for char in line.strip():
            if char not in dict_fr:
                dict_fr[char] = 0
            dict_fr[char] = dict_fr[char] + 1
    file.close()
    return dict_fr

def get_freq_double(path):
    """

    :param path:
    :return: dict where each key is a symbol from file defined by path, value is a number of occurrences of its double
    in the file
    """
    file = open(path, "r")
    dict_fr = dict()
    string = ("".join([line.strip() for line in file.readlines()]))
    for i in range(len(string)-1):
        if string[i]==string[i+1]:
            if string[i] not in dict_fr:
                dict_fr[string[i]]=0
            dict_fr[string[i]]=dict_fr[string[i]]+1
    file.close()
    return dict_fr

def get_two_different_before(path, character):
    """

    :param path:
    :param character:
    :return: dict where each key is a tuple of two different symbols from file defined by path, value is a number of occurrences
    of this symbols before char specified by "character "
    """
    file = open(path, "r")
    dict_fr = dict()
    string = ("".join([line.strip() for line in file.readlines()]))
    for i in range(2, len(string)):
        if string[i]==character:
            if string[i-1] != string[i-2] != string[i]:
                if (string[i-2], string[i-1]) not in dict_fr:
                    dict_fr[(string[i-2], string[i-1])] = 0
                dict_fr[(string[i - 2], string[i - 1])] = dict_fr[(string[i - 2], string[i - 1])] + 1
    file.close()
    return sorted(dict_fr.items(),key=lambda v: v[1], reverse=True)



def map_to_language(language_frequency, freq_dict):
    """

    :param language_frequency: string of characters sorted by their frequency in language from the most to least
    popular
    :param freq_dict: dict where each key is a symbol from file defined by path, value is a number of its
    occurrences in encrypted text
    :return: dict with probable language mapping where key is a key from freq_dict, value is a character from the
    language_freuqency
    """
    dict_map = {}
    i = 0
    for item in sorted(freq_dict.items(), key=lambda v: v[1], reverse=True):
        dict_map[item[0]] = language_frequency[i]
        i = i + 1
    return dict_map

def decode(dict_map, path):
    """
    :param dict_map:
    :param path:
    :return: string decoded using the dict with probable language mapping
    """
    file = open(path, "r")
    answer = ""
    string = ("".join([line.strip() for line in file.readlines()]))
    file.seek(0)
    for line in file:
        for char in line.strip():
            if char not in dict_map:
                answer = answer + '-'
            else:
                answer = answer + dict_map[char]
    return answer

string_freuqency = "ETAOINSHRDLCUMWFGYPBVKJXQZ".lower()
print('Symbols frequency in the file:')
freq = get_sym_freq_file("encrypted.txt")
print(sorted(freq.items(), key=lambda v:v[1], reverse=True))
language_dict = map_to_language(string_freuqency, freq)
print("Mapped to english")
print(language_dict)

print("Most common double")
freq = get_freq_double("encrypted.txt")
print(sorted(freq.items(), key=lambda v: v[1], reverse=True))
e = sorted(freq.items(), key=lambda v: v[1], reverse=True)[0][0]
print(f"Most common pair before probable e : {e}")
print(get_two_different_before("encrypted.txt", '8'))

language_dict =exchange_values_in_dict(language_dict, ';', 't')
language_dict = exchange_values_in_dict(language_dict, '4', 'h')

#Guessing other values, by exchange values here
language_dict = exchange_values_in_dict(language_dict, '‡', 'o')
language_dict = exchange_values_in_dict(language_dict, '1', 'f')

decoded = decode(language_dict, "encrypted.txt")

decoded = exchange_letters(decoded, 'a', 'i')
decoded = exchange_letters(decoded, 'g', 'u')
decoded = exchange_letters(decoded, 'w', 'g')
decoded = exchange_letters(decoded, 'a', 's')
decoded = exchange_letters(decoded, 'y', 'l')

decoded = exchange_letters(decoded, 'c', 'l')
decoded = exchange_letters(decoded, 'c', 'v')
decoded = exchange_letters(decoded, 'w', 'b')
print("\n1)current result")
print("2)leave only the most probable characters\n")
print(f"1){decoded}")
# Leave only those characters we are sure in to make the process more comfortable

print(f"2){leave_sure(decoded, ['t', 'h', 'e', 'o', 'f', 'i', 'r', 'n', 'm', 'u', 's', 'a', 'd', 'g', 'y', 'l', 'b' , 'v', 'p', 'w'])}")
