
def in_gitignore(gitignore_path, item):
    gitignore = []
    with open(gitignore_path, 'r') as ignore_file:
        for line in ignore_file.readlines():
            gitignore.append(line.strip())
    return item in gitignore


def add_gitignore(gitignore_path, item):
    with open(gitignore_path, 'a') as ignore_file:
        ignore_file.write('\n')
        ignore_file.write(item)
