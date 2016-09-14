import argparse
import os.path
import sys

MAX_KEY_LENGTH = 0
FILENAME = ""

def init_default_hash():
    '''
    returns the default hash
    '''
    hash = {'a':0,
            'b':0,
            'c':0,
            'd':0,
            'e':0,
            'f':0,
            'g':0,
            'h':0,
            'i':0,
            'j':0,
            'k':0,
            'l':0,
            'm':0,
            'n':0,
            'o':0,
            'p':0,
            'q':0,
            'r':0,
            's':0,
            't':0,
            'u':0,
            'v':0,
            'w':0,
            'x':0,
            'y':0,
            'z':0}
    return hash

def init_default_alphabet_freq():
    '''
    frequencies taken from https://en.wikipedia.org/wiki/Letter_frequency
    '''
    hash = {'a':8.167,
            'b':1.492,
            'c':2.782,
            'd':4.253,
            'e':12.702,
            'f':2.228,
            'g':2.015,
            'h':6.094,
            'i':6.966,
            'j':0.153,
            'k':0.772,
            'l':4.025,
            'm':2.406,
            'n':6.749,
            'o':7.507,
            'p':1.929,
            'q':0.095,
            'r':5.987,
            's':6.327,
            't':9.056,
            'u':2.758,
            'v':0.978,
            'w':2.360,
            'x':0.150,
            'y':1.974,
            'z':0.074}
    return hash
    
def get_cipher_input():
    '''
    returns the cipher text as a string
    '''
    f = open(FILENAME, 'r')
    input = f.read().rstrip()
    return input

def get_cipher_text_as_array(s):
    '''
    takes the input string and returns it as an array
    removes all spaces and non-alpha characters
    '''
    new_list = "".join( letter for letter in s if letter.isalpha())
    new_list = list(new_list)
    return new_list

def get_slice_freq(original_array, new_list):
    '''
    compares the two lists and works out the number of letters that match
    '''
    hit_counter = 0
    for i in range(len(new_list)):
        if original_array[i] == new_list[i]:
            hit_counter += 1
    return hit_counter

def get_nth_char_list(cipher_array, n, m):
    '''
    returns a list of every nth character starting at m
    '''
    return cipher_array[m::n]
    
def calc_letter_freq(input_arr):
    '''
    determines the freqency of each letter in the input array
    ignores non-alpha characters
    returns the result as a hash mapping the letter to the its freqency
    '''
    count_hash = init_default_hash()
    for i in range(len(input_arr)):
        char = input_arr[i]
        if char.isalpha():
            # increment hash
            count_hash[char.lower()] += 1
    
    list_size = len(input_arr)
    for key,value in count_hash.items():
        count_hash[key] = value/float(list_size)
    return count_hash
    
def perform_shift_analysis(nth_list, list_frequencies):
    '''
    takes the input list and compares the frequencies of the characters against the frequencies of the english alphabet
    shifts the input list by one 26 times to find the optimal shift
    returns the optimal shift value 
    '''
    max_value = 0.0
    shift_index = 0
    alphabet_frequencies = init_default_alphabet_freq()
    for i in range(26):
        current_total = 0.0
        for j in range(26):
            alpha_char = chr(j+97)
            test_char = chr(((j+i)%26)+97)
            current_total += list_frequencies[test_char] * float(alphabet_frequencies[alpha_char])
            
        if (current_total > max_value):
            max_value = current_total
            shift_index = i
    #print("The solution shift index is: " + str(shift_index) + ", value: " + str(max_value))
    return chr(shift_index + 97)
    
def freq_analysis(cipher_array, key_length):
    '''
    determines the key used via freq analysis
    returns a list containing the key
    '''
    key = []
    for i in range(key_length):
        nth_list = get_nth_char_list(cipher_array, key_length, i)
        list_frequencies = calc_letter_freq(nth_list)
        key.append(perform_shift_analysis(nth_list, list_frequencies))
    
    return key 

def determine_key_length(cipher_array):
    '''
    Using the Kasiski test determine the most likely key length
    returns the size of the key as an int
    '''
    #print(cipher_array)
    number_of_hits = []
    for i in range(1, MAX_KEY_LENGTH):
        new_list = cipher_array[i:]
        number_of_hits.append(get_slice_freq(cipher_array, new_list))
    
    return 1 + number_of_hits.index(max(number_of_hits))

def decrypt_cipher(input_arr, cipher_key):
    '''
    Decrypts the cipher based on the inputed key
    Prints to Stdout
    '''
    key_index = 0
    for i in range(len(input_arr)):
        char = input_arr[i]
        if char.isalpha():
            char_index = ((ord(char.lower())-97) - (ord(cipher_key[key_index])-97))%26
            #print(char_index)
            output_char = chr(97 + char_index)
            if char.islower():
                char = output_char
            else:
                char = output_char.upper()
            # Increment the key
            if key_index < len(cipher_key)-1:
                key_index += 1
            else:
                key_index = 0
        print(char, end="")
    
def main():
    # read the input
    cipher = get_cipher_input()
    cipher_array = get_cipher_text_as_array(cipher)
    # find the key length
    key_length = determine_key_length(cipher_array)
    print("The length of the key is: " + str(key_length))
    # perform frequency analysis
    key = freq_analysis(cipher_array, key_length)
    print("Found the key: ", end="")
    print(key)
    # output the results
    print("Decrypted plaintext:")
    decrypt_cipher(list(cipher), key)

def init_args():
    parser = argparse.ArgumentParser(description='Vigenere Cipher Cracking Tool', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("input_filename",
                        action="store",
                        help="The filename of the input")
    parser.add_argument("max_key_length",  
                        type=int, 
                        nargs="?", 
                        default=8, 
                        action="store",
                        help="specifies the maximum length of keys to search through")
    args = parser.parse_args()
    if args.max_key_length < 1:
        print("Your max key length is too small.")
        sys.exit()
    if not os.path.isfile(args.input_filename):
        print("Your file does not exist.")
        sys.exit()
    return args.input_filename, args.max_key_length
    
if __name__ == "__main__":
    FILENAME, MAX_KEY_LENGTH = init_args()
    main()
