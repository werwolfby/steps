import os
import yaml
import sys

def walkDict(dataDict, key, answer=None, sofar=None):
    if sofar is None:
        sofar = []
    if answer is None:
        answer = []
    for k,v in dataDict.items():
        if k == key:
            answer.append(sofar + [k])
        if isinstance(v, dict):
            walkDict(v, key, answer, sofar+[k])
    return answer


def getFromDict(dataDict, mapList):
    for k in mapList: 
        dataDict = dataDict[k]
    return dataDict


# Used to update values for specific keys
def setValueInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value
    return dataDict


def main():

    directory = os.getenv('CF_VOLUME_PATH')
    repository = os.getenv('CF_REPO_NAME')
    yaml_file = os.getenv('YAMLFILE')
    payload = os.getenv('PAYLOAD')
    yaml_path = os.path.join(directory, respository, yaml_file)

    # Open YAML file for editing
    try:
        with open(yaml_path) as f:
            dataDict = yaml.safe_load(f)
    except:
        print('File Not Found')
        print(yaml_path)
        sys.exit(1)

    # Update values
    key, value = payload.split('=')
    mapList = key.split('.')
    setValueInDict(dataDict, mapList, value)

    # Write YAML file
    with open(yaml_path, 'w') as f:
        yaml.dump(dataDict, f)

    # Setting indicator step completed successfully to skip compose step
    file_env_to_export_path = '/meta/env_vars_to_export'

    print("Set Environment Variable YAML_MODIFIED to true")
    with open(file_env_to_export_path, 'a') as file:
        file.write("YAML_MODIFIED=true")

if __name__ == "__main__":
    main()