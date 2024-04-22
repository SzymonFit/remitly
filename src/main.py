import json

def verifyAWS(data: dict) -> bool:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

            statement = data['PolicyDocument']['Statement']
            for stmt in statement:
                if type(stmt['Resource']) == str and '*' in stmt['Resource'] and len(stmt['Resource']) == 1:
                    return True
                
                elif type(stmt['Resource']) == list and '*' in stmt['Resource']:
                    for resource in stmt['Resource']:
                        if '*' in resource and len(resource) == 1:
                            return True
            return False

    except FileNotFoundError:
        raise FileNotFoundError('File not found')
    
    except Exception as e:
        raise Exception(e)
    
if __name__ == '__main__':
    file_path = './test/test_cases/default.json'

    output = verifyAWS(file_path)
    if output:
        print('Valid AWS policy')
    else:
        print('Invalid AWS policy')