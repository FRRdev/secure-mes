

def get_path_upload_avatar(instance, file):
    """Building a file path,format: (media)/avatar/user_id/photo.jpg
    """
    return f'avatar/user_{instance.id}/{file}'
