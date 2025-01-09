import cv2   

def touch_bit(byte, v, sig_bit=0):
    '''Return byte changed so that the bit specifed by sig_bit
    is set to the value specified by v.
    Restricted to use with 8 bit numbers.'''
    if(v):
        return byte | (0 + (2**sig_bit)) # masks used because cool
    else:
        return byte & (255 ^ (2**sig_bit)) 

def feel_bit(byte, sig_bit):
    '''Return value of bit specified by sig_bit in byte.
    Not actually restricted to only 8 bit numbers.'''
    if(byte & (2**sig_bit)):
        return 1
    else:
        return 0

def encode(image, source):
    '''encode source bytes into image using lsb. image is expected to be a
    cv2 representation of a 24png. Length of content in bytes is encoded
    ahead of content. Returns modified image array.'''
    len_bytes = str(len(source)).encode()
    len_array = []
    for by in len_bytes:
        len_array.append(int(by))

    # add byte representation of length, and stop symbol, to content
    source = bytearray(len_array + [13,]) + source 

    source_bit = 0
    for i in range(len(image)):
        for j in range(len(image[i])):
            for k in range(3): # Each of 3 color channels. upgrade for transparency option?
                bit = feel_bit(source[source_bit // 8], source_bit % 8)
                image[i, j, k] = touch_bit(image[i, j, k], bit)
                source_bit += 1
                if (source_bit // 8 >= len(source)):
                    break
            if (source_bit // 8 >= len(source)):
                break
        if (source_bit // 8 >= len(source)):
            break
    if (source_bit // 8 < len(source)):
        print("Warning: not enough space in image for content")
    return image

def decode(image):
    '''decode source bytes from image. image is expected to be a
    cv2 representation of a 24png. Length of content in bytes must be decoded
    ahead of content. Returns byte array.'''
    result = [0,]
    source_bit = 0
    total_bytes = -1
    for i in range(len(image)):
        for j in range(len(image[i])):
            for k in range(3):
                bit = feel_bit(image[i, j, k], 0)
                result[source_bit // 8] = touch_bit(result[source_bit // 8], bit, source_bit % 8)
                source_bit += 1
                # when we first finish reading stop symbol for length, save length and reset read bytes
                if (total_bytes < 0 and result[(source_bit // 8) - 1] == 13):
                    len_array = result[:((source_bit // 8) - 1)]
                    len_str = bytes(bytearray(len_array)).decode('utf-8')
                    #print("Content Length: " + len_str + " bytes")
                    total_bytes = int(len_str)
                    result = [0,]
                    source_bit = 0
                elif ((source_bit // 8) != ((source_bit - 1) // 8)):
                    result.append(0)
                if (total_bytes > 0 and source_bit // 8 >= total_bytes):
                    break
            if (total_bytes > 0 and source_bit // 8 >= total_bytes):
                break
        if (total_bytes > 0 and source_bit // 8 >= total_bytes):
            break
    result.pop()
    return result

