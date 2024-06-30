#<---  Pwned parser | Database parser by Adapters  --->
#<---               python 3.x                     --->
#<---   Only for educationnal / good purposes      --->

import json
import os
from colorama import Fore, init

# json writer
def write_json(json_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=1)

# Data formater -> convert data to json
def format_data(line, remove, id, line_counter, id_name):
    try:
        json_return = 'null'
        line_cleaned = line
        for bin in remove: #clean line
            line_cleaned = line_cleaned.replace(bin[0], bin[1])
        line_cutted = line_cleaned.split(':')
        
        if len(line_cutted) == 2:
            if ' ' not in line_cutted[0] and '@' in line_cutted[0] and ';' not in line_cutted[0]: #email:password
                if '|' in line_cutted[1]:
                    resplitted = line_cutted[1].split('|')
                    json_return = ({"id": id_name + '-' + str(id),"Email": line_cutted[0], "Password": resplitted[0], "Other": ''.join(resplitted).replace(resplitted[0], '')})
                else:
                    json_return = ({"id": id_name + '-' + str(id),"Email": line_cutted[0], "Password": line_cutted[1]})
                
            elif ' ' not in line_cutted[0] and ';' not in line_cutted[0]: #username:password
                if '|' in line_cutted[1]:
                    resplitted = line_cutted[1].split('|')
                    json_return = ({"id": id_name + '-' + str(id), "Username": line_cutted[0], "Password": resplitted[0], "Other": ''.join(resplitted).replace(resplitted[0], '')})
                else:
                    json_return = ({"id": id_name + '-' + str(id), "Username": line_cutted[0], "Password": line_cutted[1]})
            
            elif ";" in line_cutted[0]: #source;username/email:password
                resplitted = line_cutted[0].split(';')
                if '@' in resplitted[1]: #source;email:password
                    json_return = ({"id": id_name + '-' + str(id), "Source": resplitted[0].replace("link/", ""), "Email": resplitted[1], "Password": line_cutted[1]})
                else: #source;username:password
                    json_return = ({"id": id_name + '-' + str(id), "Source": resplitted[0].replace('link/', ''), "Username": resplitted[1], "Password": line_cutted[1]})

            else: #source username/email:password
                resplitted = line_cutted[0].split(' ')
                if '@' in resplitted[1]: #source email:password
                    json_return = ({"id": id_name + '-' + str(id), "Source": resplitted[0].replace("link/", ""), "Email": resplitted[1], "Password": line_cutted[1]})
                else:  #source username:password
                    json_return = ({"id": id_name + '-' + str(id), "Source": resplitted[0].replace('link/', ''), "Username": resplitted[1], "Password": line_cutted[1]})
        
        elif len(line_cutted) == 3:
            if 'link/' in line_cutted[2]: 
                if '@' in line_cutted[1]: #email:password:source
                    json_return = ({"id": id_name + '-' + str(id), "Source": line_cutted[2].replace("link/", ''), "Email": line_cutted[0], "Password": line_cutted[1]})
                else: #email:username:source
                    json_return = ({"id": id_name + '-' + str(id), "Source": line_cutted[2].replace("link/", ""), "Username": line_cutted[0], "Password": line_cutted[1]})
                
            elif 'link/' in line_cutted[0]:
                if '@' in line_cutted[1]: #source:email:password
                    json_return = ({"id": id_name + '-' + str(id), "Source": line_cutted[0].replace("link/", ""), "Email": line_cutted[1], "Password": line_cutted[2]})
                else:  #source:username:password
                    json_return = ({"id": id_name + '-' + str(id), "Source": line_cutted[0].replace("link/", ""), "Username": line_cutted[1], "Password": line_cutted[2]})
            
            elif 'license' in line_cutted[0]:
                resplitted = ((line_cleaned.replace('(', '')).replace(')', '')).replace("'", "").split(', ')     
                json_return = ({"id": id_name + '-' + str(id), "Username": resplitted[7], "Ip": resplitted[6].replace('ip:', '') ,"Fivem-license": resplitted[1].replace('license:', ''), "Steam-id": resplitted[2].replace('steam:', '')})
            else:
                json_return = 'null'
        
        elif len(line_cutted) < 2:
            resplitted = line_cutted[0].split(',')
            if resplitted[1] == '':  #Username,,suspectthing,ip,suspecthing
                json_return = ({"id": id_name + '-' + str(id), "Username": resplitted[0], "Ip": resplitted[3]})
            else: #Username,email,suspectthing,ip,suspecthing
                json_return = ({"id": id_name + '-' + str(id), "Username": resplitted[0], "Email": resplitted[1], "Ip": resplitted[3]})
        
        # if unknown schema
        elif len(line_cutted) > 3:
            if 'license' in line_cutted[0]:
                resplitted = ((line_cleaned.replace('(', '')).replace(')', '')).replace("'", "").split(', ')   
                json_return = ({"id": id_name + '-' + str(id), "Username": resplitted[7], "Ip": resplitted[6].replace('ip:', '') ,"Fivem-license": resplitted[1].replace('license:', ''), "Steam-id": resplitted[2].replace('steam:', ''), "Discord-id": resplitted[5].replace('discord:', ''), "Xbl-id": resplitted[4].replace('xbl:', ''), "Live-id": resplitted[3].replace('live:', '')})
        else:
            json_return = 'null'

    except Exception as e:
        print(e)
        print(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTRED_EX}!{Fore.LIGHTWHITE_EX}] Element: ' + str(line_counter) + ' Passed !')
        json_return = 'null'
    finally:
        return json_return

# Data parser & writer
def parse_data(base_file, output_name, remove, id, line_counter, max_lines):
    json_content = []
    output_files = []
    
    with open(base_file, 'r', encoding='utf-8') as file:
        try:
            for line in file:
                if line.strip():  # Check if line is not empty
                    json_return = format_data(line, remove, id, line_counter, os.path.basename(base_file))
                    if json_return != 'null':
                        json_content.append(json_return)
                        print(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTMAGENTA_EX}+{Fore.LIGHTWHITE_EX}] {line_counter} - {json_return} pushed !')
                        # Counters
                        line_counter += 1
                        id += 1
                else: 
                    pass
        except: pass
    # Check length of json_content
    if len(json_content) > max_lines:
        part_number = len(json_content) / max_lines
        if len(json_content) % max_lines != 0:
            part_number += 1
        for i in range(int(part_number)):
            start_index = i * max_lines
            end_index = min(start_index + max_lines, len(json_content))
            current_json = json_content[start_index:end_index]
            write_json(current_json, f'{output_name}/{os.path.basename(base_file)}_{i+1}.json')
            output_files.append(f'{output_name}/{os.path.basename(base_file)}_{i+1}.json')
    else:
        write_json(json_content, f'{output_name}/{os.path.basename(base_file)}.json')
        output_files.append(f'{output_name}/{os.path.basename(base_file)}.json')

    return id, output_files

# Data pusher
def data_poster(output_name, core_name):
    #push folder
    try:
        command = f"""java -Durl=http://localhost:8983/solr/{core_name}/update/json -Dtype=application/json -jar post.jar {output_name}/*.json"""
        os.system(command)
        print(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTMAGENTA_EX}+{Fore.LIGHTWHITE_EX}] {output_name} pushed !')
    except Exception as e:
        print(e + 'error')

# Main function
def main():
    # Locked parameters
    remove = [('http://', 'link/'), ('https://', 'link/'), ("android://", "link/android/")]
    line_counter = 0
    init()

    print((Fore.LIGHTRED_EX + """ ██████╗ ██╗    ██╗███╗   ██╗███████╗██████╗ 
 ██╔══██╗██║    ██║████╗  ██║██╔════╝██╔══██╗
 ██████╔╝██║ █╗ ██║██╔██╗ ██║█████╗  ██║  ██║
 ██╔═══╝ ██║███╗██║██║╚██╗██║██╔══╝  ██║  ██║
 ██║     ╚███╔███╔╝██║ ╚████║███████╗██████╔╝
 ╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝╚═════╝""" + Fore.LIGHTRED_EX + """ by Adapters""" + Fore.LIGHTWHITE_EX).replace('█', Fore.LIGHTWHITE_EX + '█' + Fore.LIGHTRED_EX))
    

    base_folder = input(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTGREEN_EX}+{Fore.LIGHTWHITE_EX}] Enter here the folder path: ') #retrieve base folder path
    core_name = 'searcher'
    output_name = input(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTGREEN_EX}+{Fore.LIGHTWHITE_EX}] Enter the path of the output folder: ')
    start_id = int(input(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTGREEN_EX}+{Fore.LIGHTWHITE_EX}] Enter here your start id (id>0): '))
    
    line_counter = 0
    max_lines = 35000
    id = start_id

    os.makedirs(os.path.join(os.getcwd(), output_name))
    for root, folders, files in os.walk(base_folder):
        for file in files:
            base_file = os.path.join(root, file)
            try:
                id, output_files = parse_data(base_file, output_name, remove, id, line_counter, max_lines)
            except Exception as e: 
                print(e)

    data_poster(output_name, core_name) #post all parsed data
    input(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTGREEN_EX}+{Fore.LIGHTWHITE_EX}] Finished !\n *Final id: {id}')

if __name__ == "__main__":
    os.system('title Pwned parser')
    main()
