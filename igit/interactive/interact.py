import os


os_type = os.name
if os_type == 'nt':
    from PyInquirer import prompt
else:
    from inquirer import prompt, List, Checkbox, Confirm


class Interact:

    def __init__(self, os_name=os.name) -> None:
        self.os_type = os_name

    def prompt(self, message):
        inquiry = Inquiry('prompt', message, 'confirm', os_name=os_type).inquiry
        return self.response(prompt(inquiry), 'prompt')

    def select(self, message, choices):
        inquiry = Inquiry('select', message, 'list', choices=choices, os_name=os_type).inquiry
        return self.response(prompt(inquiry), 'select')

    def choose(self, message, choices):
        inquiry = Inquiry('choose', message, 'checkbox', choices=choices, os_name=os_type).inquiry
        return self.response(prompt(inquiry), 'choose')

    @staticmethod
    def response(res, opt):
        return res[opt] if res not in [None, {}] else None


class Inquiry:

    def __init__(self, name, message, inq_type, choices=None, os_name=os.name) -> None:

        inquiry = {
            'name': name,
            'message': message,
            'choices': choices
        }

        if os_name == 'nt':
            inquiry.update({'type': inq_type})
            if inq_type == 'confirm':
                inquiry.update({'default': False})
            elif inq_type == 'checkbox':
                inquiry['choices'] = [{'name': choice} for choice in choices]
            self.inquiry = [inquiry]
        else:
            inquiry_types = {
                'list': List,
                'checkbox': Checkbox,
                'confirm': Confirm
            }
            self.inquiry = [inquiry_types[inq_type](**inquiry)]


if __name__ == '__main__':
    print(Interact('nt').prompt('yes or no'))
    print(Interact('nt').select('please choose', ['option 1', 'option 2']))
    print(Interact('nt').choose('please choose', ['option 1', 'option 2']))
