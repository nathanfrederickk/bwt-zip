import sys

class Node:
    def __init__(self, payload: str = None) -> None:
        """
        Node class for the Ukkonen's algorithm. Each node will have a start and end pointer.
        """

        self.payload = payload
        self.child_nodes = [None, None]

    def __getitem__(self, __index: int):
        """
        Returns the child node at the given index
        """
        return self.child_nodes[__index]
    
    def __setitem__(self, __index: int, value):
        """
        Sets the child node at the given index
        """
        self.child_nodes[__index] = value


class HuffmanDecoding:
    def __init__(self, unique_chars) -> None:
        """
        Node class for the Ukkonen's algorithm. Each node will have a start and end pointer.
        """

        self.root = Node()
        self.unique_chars = unique_chars
        
        self.generate_huffman_tree()

    def generate_huffman_tree(self):
        """
        Generates the huffman tree from the unique characters decoded from the header
        """
        
        for char in range(len(self.unique_chars)):
            
            # create the path for the character
            # all starts from the root node
            current_node = self.root

            # iterate through the bits of the string
            for bit in range(len(self.unique_chars[char][1])):

                # if the bit is 0, go to the left child node
                if self.unique_chars[char][1][bit] == "0":

                    # node does not exist, create a new node
                    if current_node[0] == None:
                        current_node[0] = Node()
                    current_node = current_node[0]

                else: # if bit is 1, go to the right child node
                    if current_node[1] == None:
                        current_node[1] = Node()
                    current_node = current_node[1]

            # set the payload of the node to the character
            current_node.payload = self.unique_chars[char][0]
    
    def decode(self, bit_string: str, start_index: int):
        """
        Decodes the bit string using the huffman tree. If the bit is 0, go left and
        if the bit is 1, go right. If the node has a payload, return the payload. Returns None othwerise.

        :Input:
        :bit_string:    The bit string to be decoded
        :start_index:   The index to start decoding from in the bitstring
        """

        # to keep track where the index is
        index_counter = 0

        # syart from the root node
        current_node = self.root

        # goes through each bit
        for bit in bit_string[start_index:]:
            
            index_counter += 1

            # if bit == 0 go left, else go right
            if bit == "0":
                current_node = current_node[0]
            else:
                current_node = current_node[1]

            # if there is a payload, return the payload and the ending index.
            if current_node.payload != None:
                return current_node.payload, index_counter + start_index
        
        # no payload found, return None
        return None, None

class EliasDecoding:
    def __init__(self, bit_string: str, start_index) -> None:
        """
        Decodes the elias code from the bit string. The start index is the index to start decoding from.
        """
        self.bit_string = bit_string
        self.start_index = start_index
        self.end_pointer = 0
        self.decoded = 0
        self.decode()

    
    def decode(self):
        """
        Decodes the elias code from the bit string. The start index is the index to start decoding from.
        """
        
        # the start of the bit string elias code
        i = self.start_index

        # where the current part of the bit string elias code is trying to decode ends
        self.end_pointer = i + 1

        # used to increment the i
        value = 1

        # iterate through the bit string
        while i < len(self.bit_string):
            
            # if bit starts with 0 then it is the length of the elias code
            # this sections finds out the next section that needs to be decoded
            if self.bit_string[i] == "0":
                temp = value
                value = int("1" + self.bit_string[i + 1: self.end_pointer], 2) + 1
                
                # increment i 
                i += temp
                self.end_pointer = value + i

            # the bit starts with one, this means that the elias code has been found
            else:

                # decode the elias code
                self.decoded = int("1" + self.bit_string[i + 1: self.end_pointer], 2)

                # finish the loop since the elias code has been found
                break
    
    def get_decode(self):
        """
        Returns the decoded elias code and the end pointer(where the pointer ends after decoding elias code)
        """
        return self.decoded, self.end_pointer
    
class BWT_Decoding:
    def __init__(self, bwt_text: str) -> None:
        """
        Decodes the bwt text.
        """
        self.bwt_text = bwt_text
        self.text = ""

        # to keep track of the rank in the first column of the bwt decoding
        self.rank = [None] * 91

        # to keep track of the order in the last column of the bwt decoding
        self.order = [0] * len(self.bwt_text)

        # to keep track of the decoded text
        self.answer = [None] * (len(self.bwt_text) - 1)

        self.rank_order()

        self.decode()

    def rank_order(self):
        """
        Generates the rank and order for the bwt decoding
        """
        
        # get the first column
        # N log N
        first_column = sorted(self.bwt_text)
        
        # to keep track of the number of occurences of each character
        order_checker = [0] * 91

        # iterate through the first column
        for char in range(len(first_column)):

            # if the rank of the character is None, set the rank to the index of the character
            # rank means the first occurence of that character in the first column (saved as index)
            if self.rank[ord(first_column[char]) - 36] == None:
                self.rank[ord(first_column[char]) - 36] = char

            # for the order
            index = ord(self.bwt_text[char]) - 36
            order_checker[index] += 1

            # set the order of the character to the number of occurences of that character
            self.order[char] = order_checker[index]

    def decode(self):
        """
        Decodes the actual bwt text
        """

        # to keep track of the index of the bwt text
        counter = 0
        
        # index starts at the end of the bwt text because of prepend
        for i in range(len(self.answer) - 1, -1, -1):
            
            # '$' marks the end of the string
            if self.bwt_text[counter] == '$':
                break
            
            # set the answer to the character at the index
            self.answer[i] = self.bwt_text[counter]

            # get the next index using the formula
            counter = self.formula(counter)

        # join the list altogether
        self.text = ''.join(self.answer)
        
    def formula(self, counter):
        """
        The formula to get the next index or character of the bwt text
        """

        
        char = self.bwt_text[counter]

        rank = self.rank[ord(char) - 36]

        order = self.order[counter]

        # use this formula to get the next index in the bwt text
        return rank + order - 1
    
    def get_text(self):
        return self.text

class Decompress:
    def __init__(self, filename: str) -> None:
        """
        Decompress the message encoded in the binary file.  
        """

        # binary file that will be read
        self.bit_string = ReadBinaryFile(filename).get_bit_string()
        self.text_length = 0

        # umber of unique characters in the text
        self.no_unique = 0

        # the current pointer in the bit string
        self.end_index = 0
        self.unique_chars = []
        self.huffman_tree = []
        self.bwt_text = ""
        self.text = ""
        self.run()
        self.write()

    def decode_header(self):
        """
        Decodes the header of the compressed file.
        """
        # decode the length of the text using elias decoding
        self.text_length, self.end_index = EliasDecoding(self.bit_string, 0).get_decode()

        # decode the number of unique characters using elias decoding
        self.no_unique, self.end_index = EliasDecoding(self.bit_string, self.end_index).get_decode()

        # decode the unique characters
        for _ in range(self.no_unique):

            # finds out about the char from the 7 bit ascii
            char = chr(int(self.bit_string[self.end_index: self.end_index + 7], 2))

            self.end_index += 7

            # decode the elias code of the legth of each huffman code length
            elias_code, self.end_index = EliasDecoding(self.bit_string, self.end_index).get_decode()

            # decode the huffman code
            huffman_code = self.bit_string[self.end_index: self.end_index + elias_code]

            self.end_index += elias_code

            # append the character and the huffman code to the list
            self.unique_chars.append((char, huffman_code))

    def generate_huffman_tree(self):
        self.huffman_tree = HuffmanDecoding(self.unique_chars)

    def decode_data(self):
        """
        Decode the actual data
        """
        while self.end_index < len(self.bit_string):

            # decode the character using the huffman tree
            char, self.end_index = self.huffman_tree.decode(self.bit_string, self.end_index)

            if char == None:
                break
            
            # decode thw number of times the character appears
            counter, self.end_index = EliasDecoding(self.bit_string, self.end_index).get_decode()
            
            # add it to the bwt text
            self.bwt_text += char * counter 

    def decode_bwt(self):
        """ 
        Decode the bwt text
        """
        # decode the bwt text gotten from the huffman and elias decoding
        self.text = BWT_Decoding(self.bwt_text).get_text()

    def run(self):
        """
        Method to run the whole decompression process
        """
        self.decode_header()
        self.generate_huffman_tree()
        self.decode_data()
        self.decode_bwt()

    def write(self):
        """
        Write the result to the recovered.txt file
        """
        print_result(self.text)

class ReadBinaryFile:
    def __init__(self, filename: str) -> None:
        """
        Read the binary file and convert it to a bit string
        """
        self.filename = filename
        self.bit_string = ""
        self.read()

    def read(self):
        with open(self.filename, "rb") as f:

            # read the file as a byte so that the leading zeros are not lost
            # turns the byte into a string of 8 bits
            self.bit_string = ''.join(format(byte, '08b') for byte in f.read())
    
            f.close()

    def get_bit_string(self):
        return self.bit_string
    
def print_result(result):
    """
    To print in the desireable format according
    to the assignment specification to the output_q1.txt file.

    Input:
        :result         : a nested list containing integers 
                        of index when the pattern matches in
                        the text.

    Citation: Taken from my Assignment 1 FIT 3155
    """
    with open('recovered.txt', 'w') as f:  

        f.write(result)

        f.close()
    
if __name__ == '__main__':

    _, filename1= sys.argv

    text = Decompress(filename1)
