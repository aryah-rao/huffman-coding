from collections import Counter
import heapq
import os

class Node:
    """
    Node class to represent each node in the Huffman tree.
    Attributes:
        key (str): The character represented by the node.
        freq (int): The frequency of the character.
        left (Node): Left child in the Huffman tree.
        right (Node): Right child in the Huffman tree.
    """
    def __init__(self, key, freq):
        self.key = key  # Store the character
        self.freq = freq  # Store the frequency of the character
        self.left = None  # Initialize left child
        self.right = None  # Initialize right child

    def __lt__(self, other):
        """
        Comparator for heapq to compare nodes based on frequency.
        """
        return self.freq < other.freq  # Compare nodes based on frequency
    
    def __eq__(self, other):
        """
        Comparator for heapq to check if frequencies are equal.
        """
        return self.freq == other.freq  # Check if frequencies are equal

class HuffmanCoding:
    """
    HuffmanCoding class to handle the Huffman coding algorithm.
    Attributes:
        path (str): Path to the input file.
        __min_heap (list): Min-heap to build the Huffman tree.
        __codes_hash_table (dict): Hash table to store characters and their corresponding Huffman codes.
        __reverse_codes_hash_table (dict): Hash table to store Huffman codes and their corresponding characters.
    """
    def __init__(self, path):
        self.path = path  # Store the path to the input file
        self.__min_heap = []  # Initialize the min-heap
        self.__codes_hash_table = {}  # Initialize the hash table for Huffman codes
        self.__reverse_codes_hash_table = {}  # Initialize the reverse hash table for decoding

    def __make_freq_dict(self, text):
        """
        Creates a frequency dictionary for the characters in the text.
        Args:
            text (str): The input text.
        Returns:
            dict: Frequency dictionary.
        """
        freq_dict = Counter(text)  # Create a frequency dictionary using Counter
        return freq_dict  # Return the frequency dictionary

    def __build_heap(self, freq_dict):
        """
        Builds a min-heap from the frequency dictionary.
        Args:
            freq_dict (dict): Frequency dictionary.
        """
        for key in freq_dict:  # Iterate through the frequency dictionary
            freq = freq_dict[key]  # Get the frequency of the character
            node = Node(key, freq)  # Create a new node
            heapq.heappush(self.__min_heap, node)  # Push the node to the min-heap

    def __build_tree(self):
        """
        Builds the Huffman tree using the min-heap.
        """
        while len(self.__min_heap) > 1:  # Loop until the heap has only one node left
            node_1 = heapq.heappop(self.__min_heap)  # Pop the smallest node
            node_2 = heapq.heappop(self.__min_heap)  # Pop the next smallest node
            freq_sum = node_1.freq + node_2.freq  # Sum the frequencies of the two nodes
            new_node = Node(None, freq_sum)  # Create a new internal node
            new_node.left = node_1  # Assign the first node as the left child
            new_node.right = node_2  # Assign the second node as the right child
            heapq.heappush(self.__min_heap, new_node)  # Push the new node back to the heap

    def __build_codes(self, node, bin_code=""):
        """
        Generates Huffman codes by traversing the Huffman tree.
        Args:
            node (Node): Current node in the Huffman tree.
            bin_code (str): Binary code for the current path in the tree.
        """
        if node is None:  # Base case for recursion
            return

        if node.key is not None:  # If it's a leaf node
            self.__codes_hash_table[node.key] = bin_code  # Store the code for the character
            self.__reverse_codes_hash_table[bin_code] = node.key  # Store the character for the code

        self.__build_codes(node.left, bin_code + "0")  # Recur for the left child with '0' added to the code
        self.__build_codes(node.right, bin_code + "1")  # Recur for the right child with '1' added to the code

    def __encode_text(self, text):
        """
        Encodes the input text using the generated Huffman codes.
        Args:
            text (str): The input text.
        Returns:
            str: Encoded binary string.
        """
        encoded_text = ""  # Initialize the encoded text string
        for char in text:  # Iterate through each character in the text
            encoded_text += self.__codes_hash_table[char]  # Append the Huffman code for the character

        # Padding to make the encoded text length a multiple of 8
        pad_amount = 8 - (len(encoded_text) % 8)  # Calculate the amount of padding needed
        for i in range(pad_amount):  # Add the padding bits
            encoded_text += '0'

        # Information about the amount of padding added
        pad_info = "{0:08b}".format(pad_amount)  # Convert the pad amount to an 8-bit binary string
        encoded_text = pad_info + encoded_text  # Add the padding info to the start of the encoded text

        return encoded_text  # Return the encoded text

    def __encoded_to_bin(self, encoded_text):
        """
        Converts the encoded text to a list of binary values.
        Args:
            encoded_text (str): The encoded binary string.
        Returns:
            list: List of binary values.
        """
        bin_array = []  # Initialize the binary array
        for i in range(0, len(encoded_text), 8):  # Iterate through the encoded text in chunks of 8 bits
            byte = encoded_text[i:i+8]  # Get the current 8-bit chunk
            bin_array.append(int(byte, 2))  # Convert the chunk to a binary number and add it to the array

        return bin_array  # Return the binary array

    def compress(self):
        """
        Compresses the input file using Huffman coding.
        Returns:
            str: Path to the compressed binary file.
        """
        # Get the output file path
        file_name = os.path.splitext(self.path)[0]  # Get the file name without extension
        output_path = file_name + "_compressed" + ".bin"  # Create the output file path with .bin extension

        # Open the input file with 'utf-8' encoding and the output file in binary mode
        with open(self.path, 'r+', encoding='utf-8') as file, open(output_path, 'wb') as output:
            text = file.read().rstrip()  # Read text from the input file and strip trailing whitespace

            freq_dict = self.__make_freq_dict(text)  # Create frequency dictionary

            self.__build_heap(freq_dict)  # Build min-heap from the frequency dictionary

            self.__build_tree()  # Build the Huffman tree from the min-heap

            self.__build_codes(heapq.heappop(self.__min_heap))  # Generate Huffman codes from the Huffman tree

            encoded_text = self.__encode_text(text)  # Encode the text using the generated Huffman codes

            bin_array = self.__encoded_to_bin(encoded_text)  # Convert the encoded text to binary format

            bin_bytes = bytes(bin_array)  # Convert the binary array to bytes
            output.write(bin_bytes)  # Write the binary data to the output file
            
            print("Compressed at ", output_path)  # Print the output file path
            return output_path  # Return the output file path

    def __remove_pad(self, bit_string):
        """
        Removes the padding from the encoded binary string.
        Args:
            bit_string (str): The encoded binary string with padding.
        Returns:
            str: The binary string without padding.
        """
        pad_info = int(bit_string[:8], 2)  # Extract the padding information
        bit_string = bit_string[8:-pad_info]  # Remove the padding from the binary string
        return bit_string  # Return the binary string without padding

    def __decode_text(self, compressed_text):
        """
        Decodes the encoded binary string back to the original text.
        Args:
            compressed_text (str): The encoded binary string without padding.
        Returns:
            str: The original text.
        """
        decoded_text = ""  # Initialize the decoded text string
        curr_bits = ""  # Initialize the current bits string

        for bit in compressed_text:  # Iterate through each bit in the compressed text
            curr_bits += bit  # Append the current bit to the current bits string
            if curr_bits in self.__reverse_codes_hash_table:  # Check if the current bits form a valid Huffman code
                decoded_text += self.__reverse_codes_hash_table[curr_bits]  # Append the corresponding character to the decoded text
                curr_bits = ""  # Reset the current bits string

        return decoded_text  # Return the decoded text

    def decompress(self, compressed_path):
        """
        Decompresses the input file using Huffman coding.
        Returns:
            str: Path to the decompressed text file.
        """
        # Get the output file path
        file_name = os.path.splitext(self.path)[0]  # Get the file name without extension
        output_path = file_name + "_decompressed" + ".txt"  # Create the output file path with .txt extension

        # Open the compressed file in binary mode and the output file with 'utf-8' encoding
        with open(compressed_path, 'rb') as file, open(output_path, 'w', encoding='utf-8') as output:
            bit_string = ""  # Initialize the bit string
            byte = file.read(1)  # Read the first byte from the file
            while byte:  # Loop until the end of the file
                byte_value = int.from_bytes(byte, byteorder='big')  # Convert the byte to an integer
                bits = bin(byte_value)[2:].rjust(8, '0')  # Convert the integer to an 8-bit binary string
                bit_string += bits  # Append the bits to the bit string
                byte = file.read(1)  # Read the next byte
            
            compressed_text = self.__remove_pad(bit_string)  # Remove the padding from the bit string

            decompressed_text = self.__decode_text(compressed_text)  # Decode the compressed text with reverse codes hash table

            output.write(decompressed_text)  # Write the decompressed text to the output file
            
            print("Decompressed at ", output_path)  # Print the output file path
            return output_path  # Return the output file path

# Specify the path to the input text file
path = "./text.txt"

# Create an instance of HuffmanCoding with the specified file path
h = HuffmanCoding(path)

# Call the compress method to compress the file
output_path_compressed = h.compress()

# Call the decompress method to decompress the compressed file
output_path_decompressed = h.decompress(output_path_compressed)
