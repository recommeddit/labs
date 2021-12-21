from configparser import ConfigParser

def config(filename="project.ini", section='serpapi'):
    """
    Ascertain the API key and other confidential data from a particular section
    in a local file.
    Input:
        filename : type(str); name of the file where the confidential data is kept
        section : type(str); name of the section in file filename where data needs
                  to be pulled from

    Output:
        str : information stored in `filename` with section name `section`

    Raises:
        ValueError : if the section is not found in the filename (see bottom of
                     file for sample .ini file)
    """
    parser = ConfigParser()
    parser.read(filename)

    # store the information from the parser
    info = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            info[param[0]] = param[1]
    else:
        raise ValueError(f'Section {section} not found in the `{filename}` file.')

    return info

# sample ini file contents below:
"""
[servicename1]
apikey=KEY1

[servicename2]
apikey=KEY2
"""
