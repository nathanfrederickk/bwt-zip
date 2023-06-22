import sys
import heapq

class SuffixArray:
    """
    Class to generate the suffix array of a string using the naive method.
    """
    def __init__(self, text: str) -> None:
        self.text = text
        self.suffix_array = []
        self.naive_suffix_array()

    def naive_suffix_array(self):
        """
        Naive suffix array construction using the built in sort function.

        Input
        :text:   A string
        """
        array = []

        # generate all suffixes of the string
        for i in range(len(self.text)):

            array.append((self.text[i:], i))

        # sort all the suffixes
        array.sort()

        # add one because the required format is 1-indexed.
        self.suffix_array = [x[1] + 1 for x in array]
    
    def get_suffix_array(self):
        """
        Method to return the suffix array
        """
        # return the suffix array
        return self.suffix_array
    
class BWT_Encoding:
    def __init__(self, text: str) -> None:
        """
        Class to generate the BWT string of a string.

        :Input:
        :text       : A string
        """
        self.text = text
        self.bwt_string = ""
        self.bwt()
    
    def bwt(self):
        """
        Method to generate the BWT string of a string.

        :Complexity: 
        :Time          : O(N), where N is the length of the string. This complexity is excluding the suffix array construction.
        :Aux Space     : O(N)
        """
        suffix_array = SuffixArray(self.text).get_suffix_array()
        
        for y in suffix_array:

            # to get the last character of the string to form the BWT string
            self.bwt_string += self.text[((y + len(self.text) - 2) % len(self.text))]

    def get_bwt_string(self):
        """
        Returns the BWT string
        """
        return self.bwt_string

class EliasEncoding:
    def __init__(self, value: int) -> None:
        """
        Class to generate the Elias encoding of a number.
        """
        self.value = value

        self.elias_string = ""

        self.elias_encoding()

    def elias_encoding(self):
        """
        Method to generate the Elias encoding of a number.

        :Complexity:
        :Time          : O(log(N)), where N is the value of the number.
        """
        length = self.value.bit_length()
        
        bit_array = []

        bit_array.append(bin(self.value)[2:])

        # O(log(N))
        # loops until the value is 1
        while self.value > 1:
            self.value = length - 1

            length = self.value.bit_length()

            # to generate a binary with the same length as the value and the first bit of the binary is 0
            mask = ~(1 << length - 1)

            # to turn the first bit of the self.value to 0 using the AND operation
            temp = mask & self.value

            # to append the binary to the array
            bit_array.append(bin(temp)[2:].zfill(length))
        
        # Required because the Elias encoding requires prepend
        for y in range(len(bit_array)-1, -1, -1):
            self.elias_string += bit_array[y]

    def get_elias_string(self):
        """
        Returns the Elias encoding of the number.
        """
        return self.elias_string


class HuffManEncoding:
    def __init__(self, characters: list, unique_characters: list) -> None:
        self.character = characters
        self.unique = unique_characters
        self.huffman_encoding()
        self.reverse_all()
    
    def append(self, index:int, value: str):
        """
        To append the bit that forms the Huffman encoding of a character.
        The index represents the character of chr(index + 36).
        """
        try:
            # try to append the bit to the index
            self.character[index] += value
        except:
            # if there is no character at the index, then create a new character
            self.character[index] = value

    def huffman_encoding(self):
        """
        Huffman encoding of a string.

        :Complexity: 
        :Time           :O(Nlog(N)), where N is the number of unique characters in the string.
        :Aux Space      :O(N)

        """

        # to create a min heap of the unique characters
        heapq.heapify(self.unique)

        # while the heap is not empty
        while len(self.unique) > 1:
            
            left = heapq.heappop(self.unique)
            right = heapq.heappop(self.unique)
            
            # every character in the left variable will have a 0 appended to it (actually it issupposed to be prepended but will be reversed later)
            for char in left[1]:
                self.append(ord(char) - 36, "0")

            # every character in the left variable will have a 0 appended to it (actually it is supposed to be prepended but will be reversed later)
            for char in right[1]:
                self.append(ord(char) - 36, "1")

            # push the new node to the heap
            heapq.heappush(self.unique, (left[0] + right[0],left[1] + right[1]))  

    def __getitem__(self, index: int):
        """
        To get the Huffman encoding of a character.
        The index represents the character of chr(index + 36).
        """
        return self.character[index]
    
    def __setitem__(self, index: int, value: str):
        """
        To set the Huffman encoding of a character.
        The index represents the character of chr(index + 36).
        """
        self.character[index] = value
    
    def get_unique_characters(self):
        """
        Returns the unique characters in the string.
        """
        return self.unique[0][1]
    
    def reverse_all(self):
        """
        Since Huffman Coding is supposed to be prepended, this method will reverse all the strings because
        initially the strings are appended to the list. So this method will reverse all the strings of the Huffman code formed."
        """

        # goes through the list of unique characters
        for i in self.get_unique_characters():
            index = ord(i) - 36

            # reverse the huffman code string
            self[index] = self.reverse_string(self[index])
    
    def reverse_string(self, string):
        """
        To reverse a string
        """
        new_string = ""

        # O(N), where N is the length of the string
        for i in range(len(string) -1, -1, -1):
            new_string += string[i]

        # returns the new reversed string
        return new_string
    
class Compress:
    def __init__(self, text: str, filename: str) -> None:
        """
        The actual class to do the compressing from string to a binary file using BWT, Elias and Huffman Encoding.
        """
        # add the terminal '$' to the string
        self.text = text + '$'

        # file to write the binary file
        self.file = WriteBinaryFile(filename)

        # to store the huffman encoding string for each char
        self.huffman_encoding = None

        # to store the unique characters in the string
        self.unique = []

        # to store the number of occurences of each character in the string
        self.characters = [0] * 91

        # to store the string to be written to the binary file
        self.to_write = ""
        self.header()
        self.message()
        self.write()


    def header(self):
        """
        To generate the header of the binary file as per assignment instructions.

        Complexity:
        :Time          :O(N log N), where N is the length of the string. This is caused by
                        the use of both Elias and Huffman Encoding.
        """

        # counting the number of occurences of each character in text
        for char in self.text:
            self.characters[ord(char) - 36] += 1

        # to store the unique characters in the string
        for i in range(len(self.characters)):
            if self.characters[i] > 0:
                
                # stores it as a tuple of (number of occurences, character)
                self.unique.append((self.characters[i], chr(i + 36)))
        
        # elias encoding of the string length
        self.to_write +=  EliasEncoding(len(self.text)).get_elias_string()
        
        # elias encoding of the number of unique characters
        self.to_write +=  EliasEncoding(len(self.unique)).get_elias_string()

        # huffman encoding of the string
        self.huffman_encoding = HuffManEncoding(self.characters, self.unique)

        # to generate the next part of the header
        for char in self.huffman_encoding.get_unique_characters():
            index = ord(char) - 36

            # binary ascii encoding of the character with 7 bits as per instruction
            ascii = bin(ord(char))[2:].zfill(7)
            # concatenate to bitstring
            self.to_write += ascii

            # huffman code of each unique char
            huffman_code = self.huffman_encoding[index]

            # elias encoding of the length of the huffman code
            elias_length = EliasEncoding(len(huffman_code)).get_elias_string()
            # concatenate to bitstring
            self.to_write += elias_length

            # append the huffman code
            self.to_write += huffman_code

        return self.to_write
    
    def message(self):
        """
        To generate the message part of the binary file as per assignment instructions.
        """

        # encoding the actual message
        bwt_string = BWT_Encoding(self.text).get_bwt_string()

        # to keep track the number of repeated characters in a row
        counter = 1

        # goes through the string
        for char in range(len(bwt_string) - 1):

            # if the next character is the same as the current character
            if bwt_string[char] == bwt_string[char + 1]:

                # increment the counter and go to the next char
                counter += 1

            # if the next character is not the same as the current character
            else:
                index = ord(bwt_string[char]) - 36
                
                # find the huffman code of the character
                huffman_code = self.huffman_encoding[index]

                # generate the elias encoding of the counter or number of occurences of the character
                elias = EliasEncoding(counter).get_elias_string()

                # concatenate the huffman code and elias encoding to the bitstring
                self.to_write += huffman_code + elias

                # reset the counter
                counter = 1

        # for the last character
        # same steps as above (in the loop)
        index = ord(bwt_string[-1]) - 36

        huffman_code = self.huffman_encoding[index]

        elias = EliasEncoding(counter).get_elias_string()
        
        self.to_write += huffman_code + elias

    def write(self):
        """
        To write the self.to_write to the binary file
        """

        # to write the bitstring to the binary file
        while len(self.to_write) >= 8 :

            # so that we could write the bits in bytes ir multiples of 8
            byte = self.to_write[:8]

            # the rest of the string
            self.to_write = self.to_write[8:]

            # convert the bit string to a number
            number = int(byte, 2)  

            # convert the number to a byte              
            mybyte = number.to_bytes(1, byteorder='big')
            
            # write to bin file
            self.file.write(mybyte)
        
        # if there is a remainder
        if len(self.to_write) > 0:

            # add 0s to the end of the string to make it a multiple of 8
            self.to_write += "0" * (8 - len(self.to_write))

            # convert to a number
            number = int(self.to_write, 2)

            # convert to a byte
            mybyte = number.to_bytes(1, byteorder='big')
            
            # write to bin file
            self.file.write(mybyte)

         # close the file
        self.file.close()

class WriteBinaryFile:
 
    def __init__(self, file_name: str) -> None:
        """
        Class to write a binary file
        """
        self.file_name = file_name
        self.file = open(self.file_name, 'wb')

    def write(self, data: str) -> None:
        """
        Writes the data to the file
        """
        self.file.write(data)

    def close(self) -> None:
        """
        Closes the file
        """
        self.file.close()

def read_file(file_path: str) -> str:
    """
     To read the text inside a text file.

    Input:
        :file_path      : a string which is a filename of the 
                          text file that will be opened.

    Citation: This method is taken from my assignment 1 FIT 3155
    """

    string_text = ""

    file = open(file_path)

    for line in file:
        string_text += line.strip()

    file.close()
    
    return string_text

if __name__ == '__main__':

    _, filename1= sys.argv

    text = read_file(filename1)

    Compress(text, "bwtencoded.bin")
