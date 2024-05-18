# Huffman Coding Compression and Decompression

## Introduction to Huffman Coding
Huffman coding is a popular algorithm used for lossless data compression. The primary goal is to reduce the size of data without losing any information by encoding frequently occurring characters with shorter codes and less frequent characters with longer codes. This technique is widely used in applications like file compression, image compression (e.g., JPEG), and many more.

## Importance of Compression and Decompression
In today's digital world, efficient data storage and transmission are critical. Compression helps reduce the amount of storage space required and speeds up data transmission over networks. Decompression restores the original data from the compressed form, ensuring that no information is lost. These processes are crucial for improving the performance and efficiency of various systems and applications.

## Huffman Coding Algorithm
The Huffman coding process involves several key steps:
1. **Frequency Analysis**: Count the frequency of each character in the input text.
2. **Building the Huffman Tree**: Construct a binary tree where each leaf node represents a character and its frequency.
3. **Generating Codes**: Traverse the tree to generate unique binary codes for each character.
4. **Encoding**: Replace each character in the input text with its corresponding Huffman code.
5. **Decoding**: Reverse the encoding process to retrieve the original text from the encoded binary string.

## Project Overview

This project implements the Huffman coding algorithm using various data structures in Python. Below, we describe the classes, methods, and their functionalities used in the implementation.

### `Node` Class
Represents each node in the Huffman tree.
- **Attributes**:
  - `key`: The character represented by the node.
  - `freq`: The frequency of the character.
  - `left`: Left child in the Huffman tree.
  - `right`: Right child in the Huffman tree.
- **Methods**:
  - `__init__`: Initializes the node with a character and its frequency.
  - `__lt__`: Comparator for heapq to compare nodes based on frequency.
  - `__eq__`: Comparator for heapq to check if frequencies are equal.

### `HuffmanCoding` Class
Handles the Huffman coding algorithm.
- **Attributes**:
  - `path`: Path to the input file.
  - `__min_heap`: Min-heap to build the Huffman tree.
  - `__codes_hash_table`: Hash table to store characters and their corresponding Huffman codes.
  - `__reverse_codes_hash_table`: Hash table to store Huffman codes and their corresponding characters.
- **Methods**:
  - `__init__`: Initializes the HuffmanCoding instance with the file path.
  - `__make_freq_dict`: Creates a frequency dictionary for the characters in the text.
  - `__build_heap`: Builds a min-heap from the frequency dictionary.
  - `__build_tree`: Builds the Huffman tree using the min-heap.
  - `__build_codes`: Generates Huffman codes by traversing the Huffman tree.
  - `__encode_text`: Encodes the input text using the generated Huffman codes.
  - `__encoded_to_bin`: Converts the encoded text to a list of binary values.
  - `compress`: Compresses the input file using Huffman coding and outputs a binary file.
  - `__remove_pad`: Removes the padding from the encoded binary string.
  - `__decode_text`: Decodes the encoded binary string back to the original text.
  - `decompress`: Decompresses the input file using Huffman coding and outputs the original text file.

### Methodology
1. **Frequency Dictionary**:
   - Read the input text and count the frequency of each character using `__make_freq_dict`.
2. **Min-Heap**:
   - Build a min-heap from the frequency dictionary using `__build_heap`.
3. **Huffman Tree**:
   - Construct the Huffman tree by repeatedly merging the two smallest nodes using `__build_tree`.
4. **Generate Codes**:
   - Traverse the tree to generate Huffman codes for each character using `__build_codes`.
5. **Encoding**:
   - Encode the text using the generated Huffman codes with `__encode_text`.
6. **Convert to Binary**:
   - Convert the encoded text to binary format using `__encoded_to_bin`.
7. **Compression**:
   - Compress the input file and write the binary data to a compressed file using `compress`.
8. **Decompression**:
   - Read the compressed binary file, remove padding, decode the binary string, and write the original text to a decompressed file using `decompress`.

### Use Case
- **Compression**: Reduces the size of large text files, making storage and transmission more efficient.
- **Decompression**: Restores the original text from the compressed file, ensuring no loss of information.

### Example Usage
```python
# Specify the path to the input text file
path = "./text.txt"

# Create an instance of HuffmanCoding with the specified file path
h = HuffmanCoding(path)

# Call the compress method to compress the file
output_path_compressed = h.compress()

# Call the decompress method to decompress the compressed file
output_path_decompressed = h.decompress(output_path_compressed)
```

# Time Complexity Analysis

## Huffman Coding Algorithm
The time complexity of the Huffman coding algorithm can be analyzed based on its key operations.

### Frequency Analysis
- **Time Complexity**: O(n)
  - Counting the frequency of each character in the input text requires iterating through the entire text once.

### Building the Huffman Tree
- **Time Complexity**: O(n log n)
  - Building the initial min-heap from the frequency dictionary takes O(n) time.
  - Merging nodes in the heap to construct the Huffman tree takes O(n log n) time, where n is the number of unique characters.

### Generating Codes
- **Time Complexity**: O(n log n)
  - Traversing the Huffman tree to generate unique codes for each character takes O(n log n) time, where n is the number of unique characters.

### Encoding
- **Time Complexity**: O(n)
  - Encoding the input text using the generated Huffman codes requires iterating through the text once, where n is the length of the text.

### Decoding
- **Time Complexity**: O(m)
  - Decoding the encoded binary string back to the original text takes O(m) time, where m is the length of the encoded binary string.

### Overall Time Complexity
- The dominant operations are building the Huffman tree and generating codes, each taking O(n log n) time.
- Thus, the overall time complexity of the Huffman coding algorithm is O(n log n), where n is the size of the input text.

## Compression and Decompression
The time complexity of compression and decompression processes depends on the size of the input text and the efficiency of the Huffman coding algorithm.
- **Compression**: O(n log n)
- **Decompression**: O(m)
  - Decompression typically involves decoding the encoded binary string, which has a linear time complexity.

### Note
- The time complexity analysis assumes that the lengths of Huffman codes are not significantly longer than the original characters. In worst-case scenarios, where the Huffman tree is highly unbalanced, the time complexity might vary.
- However, in practice, the Huffman algorithm tends to produce reasonably balanced trees, leading to efficient compression and decompression operations.

