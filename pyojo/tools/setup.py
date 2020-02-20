def gen_data_files(*dirs):
    results = []
    for src_dir in dirs:
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file[0] == '.':
                    files.remove(file)
            results.append((root, list(map(lambda f: root + "/" + f, files))))
    return results
