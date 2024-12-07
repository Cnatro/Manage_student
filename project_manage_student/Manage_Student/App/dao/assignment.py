

def save_action():
    print('Thêm dữ liệu')
    return ''


def delete_action():
    print('xóa dữ liệu')
    return ''


ACTION_ASSIGNMENT ={
    'save':save_action,
    'delete':delete_action
}

def handle_action(action_name):
    handle = ACTION_ASSIGNMENT.get(action_name)
    return handle()
# ======================================================================