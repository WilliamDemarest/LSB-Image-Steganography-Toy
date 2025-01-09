import cv2
import argparse
import lsb

def encode_from_path(image_path, content_path):
    image = cv2.imread(image_path)
    if (len(image) < 2):
        raise Exception("Could not read image_path")
        return []

    content_file = open(content_path, "rb")
    content = content_file.read()
    content_file.close()

    content_path_list = []
    for c in content_path:
        content_path_list.append(ord(c))
    content = bytearray(content_path_list + [13,]) + content
    
    result = lsb.encode(image, content)
    return result

def decode_from_path(image_path):
    image = cv2.imread(image_path)
    if (len(image) < 2):
        raise Exception("Could not read image_path")
        return []
    result = lsb.decode(image)

    result_path = ""
    for i in range(len(result)):
        if (result[i] == 13):
            del result[:i+1]
            break
        result_path = result_path + chr(result[i])
    return result_path, result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--encode", action="store_true", 
        help='Specifies that a file is being encoded.')
    parser.add_argument("-d", "--decode", action="store_true",
        help='Specifies that a file is being decoded.')
    parser.add_argument("-i", "--image",
        help="Path of file that the content will be, or is, hidden in."
        +" Must be a .png, transparent .png not supported.")
    parser.add_argument("-c", "--content",
        help="Path of file that will be hidden in image. Not used in decoding."
        +" Path of content will also be encoded.")
    parser.add_argument("-o", "--output",
        help="Name to be given to output file. Optional when decoding: "
        +"if not specified the origonal name of the encoded file will be used.")

    args = parser.parse_args()

    method = None
    image_path = args.image
    content_path = args.content
    out_path = args.output

    if (args.encode and args.decode):
        raise Exception("Multiple mode args used")
    elif (args.encode):
        method = 'e'
    elif (args.decode):
        method = 'd'


    if (method == None):
        method = input("Are you encoding(e) or decoding(d)? ")

    if (method == 'e'):
        if (image_path == None):
            image_path = input("Enter image file path: ")
        if (content_path == None):
            content_path = input("Enter content file path: ")
        if (out_path == None):
            out_path = input("Enter image output path: ")
        result = encode_from_path(image_path, content_path)

        if (len(result)):
            cv2.imwrite(out_path, result)
        else:
            raise Exception("failed to encode") 

    elif (method == 'd'):
        if (image_path == None):
            image_path = input("Enter image file path: ")
        #out_path = input("Enter output content path: ")
        result_path, result = decode_from_path(image_path)

        print("Content Length: " + str(len(result)) + " bytes")
        if (len(result)):
            if (out_path == None):
                out_path = result_path
            
            outfile = open(out_path, "wb")
            outfile.write(bytes(bytearray(result)))
            outfile.close()
        else:
            raise Exception("failed to decode")
    

if (__name__ == "__main__"):
    main()
