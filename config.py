"""
@Author: Hizaoui Mohamed Abdelkader
@Email-1: hizaoui.ma@gmail.com
"""
import os
import sys
import yaml


def get_config():
    """
    parse yaml configuration file
    :return: dict
    """
    try:
        config_file_path = sys.argv[2]
    except IndexError:
        config_file_path = "config.yml"
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as yml_error:
                print(yml_error)
    else:
        print("%s does not exist" % config_file_path)
        print("ERROR:\nUSAGE: python strap.py \"keyword1, keyword2, keyword3, keyword4\" [path/to/config.yml]")
        exit(0)

conf = get_config()