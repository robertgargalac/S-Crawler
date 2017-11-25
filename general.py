import os

def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory', directory)
        os.makedirs(directory)

#Create queue and crawled files

def create_data_files(project_name, home_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, home_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')

# Create new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

# Add data onto an existing file

def append_to_file(path,data):
    with open(path, 'a') as file :
        file.write(data + '\n')

# Delete content

def delete_file_content(path):
    with open(path, 'w'):
        pass

# Read a file and covert each line to set items

def file_to_set(filename):
    results = set()
    with open(filename, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

# Transforms set into file
def set_to_file(links, file):
    delete_file_content(file)
    for link in sorted(links):
        append_to_file(file, link)
