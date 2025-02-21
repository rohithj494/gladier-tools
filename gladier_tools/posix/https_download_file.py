from gladier import GladierBaseTool


def https_download_file(**data):
    """Download a file from HTTPS server"""
    import os
    import requests

    ##minimal data inputs payload
    server_url = data.get('server_url', '')
    file_name = data.get('file_name', '')
    file_path = data.get('file_path', '')
    headers = data.get('headers', '')
    ##extra data inputs payload
    ##
    ##

    if server_url==None:
        raise(NameError('No `server URL` specified'))
    
    if file_name==None:
        raise(NameError('No `file_name` specified'))

    file_url = os.path.join(server_url,file_name)

    if not os.path.exists(file_path):
        os.mkdir(file_path)

    full_name = os.path.join(file_path,file_name)
    
    if not os.path.isfile(full_name):
        r = requests.get(file_url, headers=headers)
        if not r.status_code==200:  
            raise r.raise_for_status()
        open(full_name , 'wb').write(r.content)

    return full_name


class HttpsDownloadFile(GladierBaseTool):

    flow_definition = {
        'Comment': 'Downloads one file through https',
        'StartAt': 'httpDownloadFile',
        'States': {
            'httpDownloadFile': {
                'ActionUrl': 'https://api.funcx.org/automate',
                'Comment': None,
                'ExceptionOnActionFailure': True,
                'Parameters': {
                    'tasks': [
                        {
                            'endpoint.$': '$.input.funcx_endpoint_non_compute',
                            'function.$': '$.input.https_download_file_funcx_id',
                            'payload.$': '$.input'
                        }
                    ]
                },
                'ResultPath': '$.httpDownloadFile',
                'Type': 'Action',
                'WaitTime': 300,
                'End': True,
            },
        }
    }

    funcx_functions = [https_download_file]
    flow_input = {
        'headers':'',
        }
    required_input = [
        'server_url',
        'file_name',
        'file_path',
        'headers',
        'funcx_endpoint_non_compute'
        ]
