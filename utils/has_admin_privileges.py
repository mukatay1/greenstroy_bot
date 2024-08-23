import os


def check_admin_privileges(user_id: str) -> str:
    ADMIN_ID = os.getenv('ADMIN_ID')
    is_admin = user_id in ADMIN_ID

    if not is_admin:
        return 'У вас нет прав для выполнения этого действия.'
    else:
        return ''

