from configparser import ConfigParser

def config(filename="project.ini", section='serpapi'):
    parser = ConfigParser()
    parser.read(filename)

    info = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            info[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file.')

    return info
