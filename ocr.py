import pytesseract
import os
import sys

async def read_image(img_path, lang='eng'):

    '''performs ocr on a single image...
        img_path: str, path to the image file
        lang: str, lang to be used while conversion

        return
        :text: str, converted text from image
    '''
    try:
        return pytesseract.image_to_string(img_path, lang=lang)
    except:
        return '[ERROR] unable to process file: {0}'.format(img_path)

async def read_images_from_dir(dir_path, lang='eng', write_to_file=False):


        # '''
        # performs ocr on all images present in a directory
        # :dir_path: str, path to the directory of the images
        # :lang: str, language to be used while conversion
        #
        # :return:
        # :converted_text: dict, mapping of filename to converted text for each image
        # '''
    converted_text = {}
    for file_ in os.listdir(dir_path):
        if (file_.endswith(('png','jpeg','jpg'))):
            text = await read_image(os.path.join(dir_path,file_), lang=lang)
            converted_text[os.path.join(dir_path,file_)] = text

    if (write_to_file):
        for file_path, text in converted_text.items():
            _write_to_file(text,os.path.splitext(file_path)[0]+".txt")
    return converted_text


def _write_to_file(text, file_path):

    '''
    helper method to write text to a file
    :param text:
    :param file_path:
    :return:
    '''
    print("[INFO] writing text to file: {0}".format(file_path))
    with open(file_path,'w') as fp:
        fp.write(text)


if __name__ == '__main__':
    if(len(sys.argv)==1):
        print('python3 ocr.py <path>')
        print('provide the path to an image or the path to a directory containing images')
        exit(1)
    if os.path.isdir(sys.argv[1]):
        converted_text_map = read_images_from_dir(sys.argv[1], write_to_file=True)
    elif os.path.exists(sys.argv[1]):
        print(read_image(sys.argv[1]))
    else:
        print("unable to process this file. please check if it exists and is reachable.")
