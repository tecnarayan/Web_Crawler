import requests
from bs4 import BeautifulSoup
import lxml
import re
import warnings
import urllib.parse
import urllib.error
from requests.exceptions import RequestException
from urllib3.exceptions import LocationParseError
from urllib.parse import urlparse
from urllib3.exceptions import LocationParseError
import argparse
import os



# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Web Crawler')

# Add command-line arguments
parser.add_argument('-u', '--url', type=str, help='URL of the website to crawl')
parser.add_argument('-t', '--threshold', type=int, default = 10000 ,help='Threshold of recursiveness')
parser.add_argument('-o', '--output', type=str, help='Output file name')
parser.add_argument('-s', '--size' , type=int , default = 0 ,help='size output')
parser.add_argument('-c', '--current' , type=int , default = 0 ,help='size output')
parser.add_argument('-d', '--download' , type=str , default = 'tec' ,help='size output')



# Parse the command-line arguments
args = parser.parse_args()

# Access the values of the arguments
url = args.url
threshold = args.threshold
output_file = args.output
size_option = args.size
current = args.current
download = args.download

# Perform validation on the arguments
if not url:
    parser.error('URL is required.')
if threshold is None or threshold <= 0:
    parser.error('Threshold must be a positive integer.')


warnings.filterwarnings("ignore") # this is to ignore warnings that get printed too much and decrese the main readbility 

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

print("-------------------------------------")


#cleating lists to store data ( links )
universe_explored=[]
HTML = []
CSS =[]
JAVA_SCRIPT = []
IMAGE = [[],[],[],[],[]] # .jpg, .jpeg, .png, .gif, .svg 
DOCUMENT=[[],[],[],[]] # .pdf, .doc, .docx, .txt
DATA=[[],[],[]] # .csv, .json, .xml
VIDEO=[[],[],[],[]] # .mp4, .avi, .mov, .wmv
AUDIO=[[],[],[]] # .mp3, .wav, .ogg
EXTRA = [[],[],[],[],[]] # .php, .asp, .jsp, .scss, .less
MISCELLANEOUS =[]
INTERNAL = []
EXTERNAL = []
ccc = 0

def is_valid_url(url): # check validity of link
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except LocationParseError:
        return False

def check_link_availability(link): # check avalability of link
    global headers
    if is_valid_url(link):
        try:
            response = requests.get(link, headers=headers, verify=False)
            response.raise_for_status()
            return 1
        except LocationParseError:
            return 0
        except requests.exceptions.RequestException:
            return 0
    else:
        return 0

def get_size(link): ## to get size of correcponding link
    if size_option == 1:

        global headers
        try:
            response = requests.get(link, headers=headers, verify=False)
            response.raise_for_status()  # Raise an exception for unsuccessful HTTP status codes
            content_size = len(response.content)
            return content_size
        except requests.exceptions.RequestException as e:
            return 0

    else:
         return 0


## this function is for downloading images
def download_files(links, folder_name = "images_by_crawler"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for link_list in links:
        for link in link_list:
            file_name = os.path.join(folder_name, link.split("/")[-1])
            response = requests.get(link)
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")


def explore(link , num):
    
    if num == 0:
        return
    num -=1

    # naming lists
    global universe_explored
    global HTML
    global CSS
    global JAVA_SCRIPT
    global IMAGE
    global DOCUMENT
    global DATA
    global VIDEO
    global AUDIO
    global EXTRA
    global MISCELLANEOUS
    global headers
    global url
    global ccc
    
    ccc += 1
    if ccc == 5:
        if current == 1:
            print("current links stored = {}".format(len(universe_explored)))
        ccc = 0

    if link in universe_explored:
        return
    
    # Regular Expression foe extension matches
    universe_explored.append(link)
    if re.match(r".*\.html.*", link): ## NOTE : re = regular expression
        HTML.append(link)
    elif re.match(r".*\.css.*", link):
        CSS.append(link)
    elif re.match(r".*\.jsp.*", link):
        EXTRA[2].append(link)
    elif re.match(r".*\.js.*", link):
        JAVA_SCRIPT.append(link)
    elif re.match(r".*\.jpg.*", link):
        IMAGE[0].append(link)
    elif re.match(r".*\.jpeg.*", link):
        IMAGE[1].append(link)
    elif re.match(r".*\.png.*", link):
        IMAGE[2].append(link)
    elif re.match(r".*\.gif.*", link):
        IMAGE[3].append(link)
    elif re.match(r".*\.svg.*", link):
        IMAGE[4].append(link)
    elif re.match(r".*\.pdf.*", link):
        DOCUMENT[0].append(link)
    elif re.match(r".*\.docx.*", link):
        DOCUMENT[2].append(link)
    elif re.match(r".*\.doc.*", link):
        DOCUMENT[1].append(link)
    elif re.match(r".*\.txt.*", link):
        DOCUMENT[3].append(link)
    elif re.match(r".*\.csv.*", link):
        DATA[0].append(link)
    elif re.match(r".*\.json.*", link):
        DATA[1].append(link)
    elif re.match(r".*\.xml.*", link):
        DATA[2].append(link)
    elif re.match(r".*\.mp4.*", link):
        VIDEO[0].append(link)
    elif re.match(r".*\.avi.*", link):
        VIDEO[1].append(link)
    elif re.match(r".*\.mov.*", link):
        VIDEO[2].append(link)
    elif re.match(r".*\.wmv.*", link):
        VIDEO[3].append(link)
    elif re.match(r".*\.mp3.*", link):
        AUDIO[0].append(link)
    elif re.match(r".*\.wav.*", link):
        AUDIO[1].append(link)
    elif re.match(r".*\.ogg.*", link):
        AUDIO[2].append(link)
    elif re.match(r".*\.php.*", link):
        EXTRA[0].append(link)
    elif re.match(r".*\.asp.*", link):
        EXTRA[1].append(link)
    elif re.match(r".*\.scss.*", link):
        EXTRA[3].append(link)
    elif re.match(r".*\.less.*", link):
        EXTRA[4].append(link)
    else:
        MISCELLANEOUS.append(link)

    if url not in link:
        EXTERNAL.append(link)
        return
    
    else:
        INTERNAL.append(link)

    if check_link_availability(link):
        # Send a GET request to the link
        f = requests.get(link, headers=headers, verify=False)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(f.content, 'lxml')

        # Find all <a> tags with href attribute
        href_tags = soup.find_all(href=True)
    
        # Find all tags with src attribute
        src_tags = soup.find_all(src=True)

        # List to store the modified URLs
    
        final=[]

        for tag in href_tags:
          href_value = tag['href']
          if not href_value.startswith("http"):
            if not href_value.startswith("/"):
              href_value=url+"/"+href_value #
            elif href_value.startswith('#'):
              continue
            elif href_value.startswith("//"):
              href_value="http:"+href_value
            else:
              href_value=url+href_value #
          final.append(href_value)

        for tag in src_tags:
          src_value=tag['src']
          if not src_value.startswith("http"):
            if not src_value.startswith("/"):
              src_value=url+"/"+src_value#
            elif src_value.startswith('#'):
              continue
            elif src_value.startswith('//'):
              src_value="http:"+src_value
            else:
              src_value=url+src_value #
          final.append(src_value)
    
        
        for i in final:
            i = urllib.parse.unquote(i) 
            explore(i,num)  ## this is form of recursion 
       


explore(url , threshold+1)

if download == "image":  ## function calling daownload image
    download_files(IMAGE)

if output_file:  ## this to to write stuff in output file 
    with open(output_file, 'w') as f:

        f.write("\n\n -------------------- \n\n")

        f.write("INTERNAL"+"\n")
        f.write("  COUNT = {}".format(len(INTERNAL))+"\n")
        for i in INTERNAL:
            f.write("{} bytes :  {}".format(get_size(i),i)+"\n")

        f.write("\n\nEXTERNAL"+"\n")
        f.write("  COUNT = {}".format(len(EXTERNAL))+"\n")
        for i in EXTERNAL:
            f.write("{} bytes :  {}".format(get_size(i),i)+"\n")

        f.write("\n\nHTML"+"\n")

        f.write("  .html: {}".format(len(HTML))+"\n")
        for i in HTML:
            f.write("    {}".format(i)+"\n")

        f.write("\nCSS"+"\n")
        f.write("  .css: {}".format(len(CSS))+"\n")
        for i in CSS:
            f.write("    {}".format(i)+"\n")

        f.write("\nJAVA_SCPIPT"+"\n")
        f.write("  .js: {}".format(len(JAVA_SCRIPT))+"\n")
        for i in JAVA_SCRIPT:
            f.write("    {}".format(i)+"\n")

        f.write("\nIMAGE"+"\n")
        f.write("  .jpg: {}".format(len(IMAGE[0]))+"\n")
        for i in IMAGE[0]:
            f.write("    {}".format(i)+"\n")

        f.write("  .jpeg: {}".format(len(IMAGE[1]))+"\n")
        for i in IMAGE[1]:
            f.write("    {}".format(i)+"\n")

        f.write("  .png: {}".format(len(IMAGE[2]))+"\n")
        for i in IMAGE[2]:
            f.write("    {}".format(i)+"\n")

        f.write("  .gif: {}".format(len(IMAGE[3]))+"\n")
        for i in IMAGE[3]:
            f.write("    {}".format(i)+"\n")

        f.write("  .svg: {}".format(len(IMAGE[4]))+"\n")
        for i in IMAGE[4]:
            f.write("    {}".format(i)+"\n")

        f.write("\nDOCUMENT"+"\n")
        f.write("  .pdf: {}".format(len(DOCUMENT[0]))+"\n")
        for i in DOCUMENT[0]:
            f.write("    {}".format(i)+"\n")

        f.write("  .doc: {}".format(len(DOCUMENT[1]))+"\n")
        for i in DOCUMENT[1]:
            f.write("    {}".format(i)+"\n")

        f.write("  .docx: {}".format(len(DOCUMENT[2]))+"\n")
        for i in DOCUMENT[2]:
            f.write("    {}".format(i)+"\n")

        f.write("  .txt: {}".format(len(DOCUMENT[3]))+"\n")
        for i in DOCUMENT[3]:
            f.write("    {}".format(i)+"\n")

        f.write("\nDATA")
        f.write("  .csv: {}".format(len(DATA[0]))+"\n")
        for i in DATA[0]:
            f.write("    {}".format(i)+"\n")

        f.write("  .json: {}".format(len(DATA[1]))+"\n")
        for i in DATA[1]:
            f.write("    {}".format(i)+"\n")

        f.write("  .xml: {}".format(len(DATA[2]))+"\n")
        for i in DATA[2]:
            f.write("    {}".format(i)+"\n")

        f.write("\nVIDEO")
        f.write("  .mp4: {}".format(len(VIDEO[0]))+"\n")
        for i in VIDEO[0]:
            f.write("    {}".format(i)+"\n")

        f.write("  .avi: {}".format(len(VIDEO[1]))+"\n")
        for i in VIDEO[1]:
            f.write("    {}".format(i)+"\n")

        f.write("  .mov: {}".format(len(VIDEO[2]))+"\n")
        for i in VIDEO[2]:
            f.write("    {}".format(i)+"\n")

        f.write("  .wmv: {}".format(len(VIDEO[3]))+"\n")
        for i in VIDEO[3]:
            f.write("    {}".format(i)+"\n")
        f.write("\nAUDIO"+"\n")
        f.write("  .mp3: {}".format(len(AUDIO[0]))+"\n")
        for i in AUDIO[0]:
            f.write("    {}".format(i)+"\n")

        f.write("  .wav: {}".format(len(AUDIO[1]))+"\n")
        for i in AUDIO[1]:
            f.write("    {}".format(i)+"\n")

        f.write("  .ogg: {}".format(len(AUDIO[2]))+"\n")
        for i in AUDIO[2]:
            f.write("    {}".format(i)+"\n")

        f.write("\nEXTRA"+"\n")
        f.write("  .php: {}".format(len(EXTRA[0]))+"\n")
        for i in EXTRA[0]:
            f.write("    {}".format(i)+"\n")

        f.write("  .asp: {}".format(len(EXTRA[1]))+"\n")
        for i in EXTRA[1]:
            f.write("    {}".format(i)+"\n")

        f.write("  .jsp: {}".format(len(EXTRA[2]))+"\n")
        for i in EXTRA[2]:
            f.write("    {}".format(i)+"\n")

        f.write("  .scss: {}".format(len(EXTRA[3]))+"\n")
        for i in EXTRA[3]:
            f.write("    {}".format(i)+"\n")

        f.write("  .less: {}".format(len(EXTRA[4]))+"\n")
        for i in EXTRA[4]:
            f.write("    {}".format(i)+"\n")

        f.write("\nMISCELLANOUS"+"\n")
        f.write(" count = {}".format(len(MISCELLANEOUS))+"\n")
        for i in MISCELLANEOUS:
            f.write("    {}".format(i)+"\n")

        f.write("\n TOTAL LINK = {}".format(len(universe_explored))+"\n")

        f.close()


else:    ## this is to be printed on screen
    for zz in range(1):
        print("\n\n -------------------- \n\n")

        print("INTERNAL")
        print("  COUNT = {}".format(len(INTERNAL)))
        for i in INTERNAL:
            print("{} bytes :  {}".format(get_size(i),i))

        print("\n\nEXTERNAL")
        print("  COUNT = {}".format(len(EXTERNAL)))
        for i in EXTERNAL:
            print("{} bytes :  {}".format(get_size(i),i))

        print("\n\nHTML")

        print("  .html: {}".format(len(HTML)))
        for i in HTML:
            print("    {}".format(i))

        print("\nCSS")
        print("  .css: {}".format(len(CSS)))
        for i in CSS:
            print("    {}".format(i))

        print("\nJAVA_SCPIPT")
        print("  .js: {}".format(len(JAVA_SCRIPT)))
        for i in JAVA_SCRIPT:
            print("    {}".format(i))

        print("\nIMAGE")
        print("  .jpg: {}".format(len(IMAGE[0])))
        for i in IMAGE[0]:
            print("    {}".format(i))

        print("  .jpeg: {}".format(len(IMAGE[1])))
        for i in IMAGE[1]:
            print("    {}".format(i))

        print("  .png: {}".format(len(IMAGE[2])))
        for i in IMAGE[2]:
            print("    {}".format(i))

        print("  .gif: {}".format(len(IMAGE[3])))
        for i in IMAGE[3]:
            print("    {}".format(i))

        print("  .svg: {}".format(len(IMAGE[4])))
        for i in IMAGE[4]:
            print("    {}".format(i))

        print("\nDOCUMENT")
        print("  .pdf: {}".format(len(DOCUMENT[0])))
        for i in DOCUMENT[0]:
            print("    {}".format(i))

        print("  .doc: {}".format(len(DOCUMENT[1])))
        for i in DOCUMENT[1]:
            print("    {}".format(i))

        print("  .docx: {}".format(len(DOCUMENT[2])))
        for i in DOCUMENT[2]:
            print("    {}".format(i))

        print("  .txt: {}".format(len(DOCUMENT[3])))
        for i in DOCUMENT[3]:
            print("    {}".format(i))

        print("\nDATA")
        print("  .csv: {}".format(len(DATA[0])))
        for i in DATA[0]:
            print("    {}".format(i))

        print("  .json: {}".format(len(DATA[1])))
        for i in DATA[1]:
            print("    {}".format(i))

        print("  .xml: {}".format(len(DATA[2])))
        for i in DATA[2]:
            print("    {}".format(i))

        print("\nVIDEO")
        print("  .mp4: {}".format(len(VIDEO[0])))
        for i in VIDEO[0]:
            print("    {}".format(i))

        print("  .avi: {}".format(len(VIDEO[1])))
        for i in VIDEO[1]:
            print("    {}".format(i))

        print("  .mov: {}".format(len(VIDEO[2])))
        for i in VIDEO[2]:
            print("    {}".format(i))

        print("  .wmv: {}".format(len(VIDEO[3])))
        for i in VIDEO[3]:
            print("    {}".format(i))
        print("\nAUDIO")
        print("  .mp3: {}".format(len(AUDIO[0])))
        for i in AUDIO[0]:
            print("    {}".format(i))

        print("  .wav: {}".format(len(AUDIO[1])))
        for i in AUDIO[1]:
            print("    {}".format(i))

        print("  .ogg: {}".format(len(AUDIO[2])))
        for i in AUDIO[2]:
            print("    {}".format(i))

        print("\nEXTRA")
        print("  .php: {}".format(len(EXTRA[0])))
        for i in EXTRA[0]:
            print("    {}".format(i))

        print("  .asp: {}".format(len(EXTRA[1])))
        for i in EXTRA[1]:
            print("    {}".format(i))

        print("  .jsp: {}".format(len(EXTRA[2])))
        for i in EXTRA[2]:
            print("    {}".format(i))

        print("  .scss: {}".format(len(EXTRA[3])))
        for i in EXTRA[3]:
            print("    {}".format(i))

        print("  .less: {}".format(len(EXTRA[4])))
        for i in EXTRA[4]:
            print("    {}".format(i))

        print("\nMISCELLANOUS")
        print(" count = {}".format(len(MISCELLANEOUS)))
        for i in MISCELLANEOUS:
            print("    {}".format(i))

        print("\n TOTAL LINK = {}".format(len(universe_explored)))


warnings.filterwarnings("default")
print("\nreturn 0")  ## this is finally printed to represent that its an end of execution now 