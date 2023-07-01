
   
import os
from pathlib import Path
import logging


class DirectoryCreator:
    def create(self, filedir, filename):
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")


class EmptyFileCreator:
    def create(self, filepath):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")


class FileExistenceChecker:
    def file_not_existed(self, filepath):
        return not os.path.exists(filepath)

    def file_empty(self, filepath):
        return os.path.getsize(filepath) == 0


class FileManager:
    def __init__(self, directory_creator,file_creator, file_checker):
        self.file_creator = file_creator
        self.file_checker = file_checker
        self.directory_creator=directory_creator

    def create_files(self, file_paths):
        for filepath in file_paths:
            filepath = Path(filepath)
            filedir, filename = os.path.split(filepath)

            if filedir != "":
                self.directory_creator.create(filedir,filename)

            if self.file_checker.file_not_existed(filepath) or self.file_checker.file_empty(filepath):
                self.file_creator.create(filepath)
            else:
                logging.info(f"{filename} already exists")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')
    project_name = "RiceClassifier"

    list_of_files = [
        ".github/workflows/.gitkeep",
        f"src/{project_name}/__init__.py",
        f"src/{project_name}/components/__init__.py",
        f"src/{project_name}/utils/__init__.py",
        f"src/{project_name}/config/__init__.py",
        f"src/{project_name}/config/configuration.py",
        f"src/{project_name}/pipeline/__init__.py",
        f"src/{project_name}/entity/__init__.py",
        f"src/{project_name}/constants/__init__.py",
        f"tests/test_{project_name}/__init__.py",
        f"tests/test_{project_name}/test_components/__init__.py",
        f"tests/test_{project_name}/test_config/__init__.py",
        f"tests/test_{project_name}/test_config/test_configuration.py",
        f"tests/test_{project_name}/test_entity/__init__.py",
        f"tests/test_{project_name}/test_pipeline/__init__.py",
        f"tests/test_{project_name}/test_utils/__init__.py",
        f"tests/test_{project_name}/test_constants/__init__.py",
        "config/config.yaml",
        "dvc.yaml",
        "params.yaml",
        "requirements.txt",
        "setup.py",
        "research/trials.ipynb",
        "templates/index.html",
        "README.md",
    ]

    directory_creator = DirectoryCreator()
    empty_file_creator = EmptyFileCreator()
    file_checker = FileExistenceChecker()
    file_manager = FileManager(directory_creator,empty_file_creator, file_checker,)
    file_manager.create_files(list_of_files)
