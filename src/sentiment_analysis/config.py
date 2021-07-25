config = {
    'language': 'english',
}

if config['language'] == 'english':
    config['lang_code'] = 'eng'
elif config['language'] == 'italian':
    raise Exception("Language still not supported")
else:
    raise Exception("Unrecognized language value")
