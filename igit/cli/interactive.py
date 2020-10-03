import os

os_type = os.name

if os_type == 'nt':
    from PyInquirer import prompt
    type_mapping = {}
else:
    from inquirer import prompt, List, Checkbox, Confirm
    type_mapping = {
        'list': List,
        'checkbox': Checkbox,
        'confirm': Confirm
    }


__all__ = [
    'branch_selector',
    'file_selector',
    'files_checkboxes',
    'verify_prompt'
]


def interact(opt):
    def decorator(f):
        def wrapper(*args, **kwargs):
            rv = f(*args, **kwargs)
            return rv[opt] if rv not in [None, {}] else None
        return wrapper
    return decorator


def get_questions(name, message, inq_type, choices=None):
    question = {
        'message': message,
        'name': name,
        'choices': choices
    }

    if os_type == 'nt':
        question.update({'type': inq_type})
        if inq_type == 'confirm':
            question.update({'default': False})
        elif inq_type == 'checkbox':
            question['choices'] = [{'name': choice} for choice in choices]
        return [
            question
        ]
    else:
        return [
            type_mapping[inq_type](**question)
        ]


@interact('response')
def verify_prompt(message):
    questions = get_questions('response', message, 'confirm')
    return prompt(questions)


@interact('file')
def file_selector(files):
    questions = get_questions('file', 'Choose file', 'list', choices=files)
    return prompt(questions)


@interact('branch')
def branch_selector(branches):
    questions = get_questions('branch', 'Choose branch from local', 'list', choices=branches)
    return prompt(questions)


@interact('files')
def files_checkboxes(files, method):
    questions = get_questions('files', f'Choose files to {method} [space key]', 'checkbox', choices=files)
    return prompt(questions)


if __name__ == '__main__':
    res = verify_prompt('testing verify')
    print(res)

    res = file_selector(['file1', 'file2'])
    print(res)

    res = files_checkboxes(['file1', 'file2'])
    print(res)
