from gladier import GladierBaseTool, generate_flow_definition


def decrypt(**data):

    import os
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash
    import base64

    password = bytes(data['decrypt_key'], 'utf-8')
    ckdf = ConcatKDFHash(algorithm=hashes.SHA256(), length=32,
                         otherinfo=None, )
    key = base64.urlsafe_b64encode(ckdf.derive(password))
    fernet = Fernet(key)

    infile = data['decrypt_input']
    if '~' in infile:
        infile = os.path.expanduser(infile)

    outfile = data.get('decrypt_output', infile[:len(infile)-4])
    print(outfile)
    if '~' in outfile:
        outfile = os.path.expanduser(outfile)

    with open(infile, 'rb') as file:
        encrypted = file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(outfile, 'wb') as out:
        out.write(decrypted)
    return outfile


@generate_flow_definition
class Decrypt(GladierBaseTool):
    """
    Decrypt tool takes in an encrypted file and a password to perform
    decryption on the file.
    The decryption only works on files that have been encrypted by the
    Gladier Encrypt tool.
    It has not been found to be compatible with 3rd party
    encryption/decryption tools.

    :param decrypt_input: Path to the file which needs to be decrypted.
    :param decrypt_key: Symmetric key or "password" which will be used
    to decrypt the encrypted file. Must be the same key that was used
    during encryption.
    :param decrypt_output: (optional) The full path to the decrypted file.
    If not provided, the decrypted file will have the same name as the input
    file, with the last 4 characters truncated(assuming it was a .aes file).
    :param funcx_endpoint_compute: By default, uses the ``compute`` funcx
    endpoint.
    :returns output_path: Location of the decrypted file.
    """

    funcx_functions = [decrypt]
    required_input = [
        'decrypt_input',
        'decrypt_key',
        'funcx_endpoint_compute'
    ]
