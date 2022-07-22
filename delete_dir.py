import os
import shutil


def delete_document_dir() -> bool:
    """Удаление папки documents со всем её содержимым"""
    if os.path.exists('documents'):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'documents')
        shutil.rmtree(path)
        return True
    return False
