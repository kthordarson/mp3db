import hashlib


def get_hash(filename):
    """ calculate md5 and sh1 of given file
    :param filename: input filename to hash
    :return: hash value
    """
    BUF_SIZE = 10
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()

    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            # sha1.update(data)

    # print('h', end='', flush=True)
    return md5


def file_hash(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda: f.read(128 * 1024), b''):
            h.update(b)
    return h.hexdigest()
