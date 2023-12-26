# init file > ensure directory is current working directory
from directory import FilePath

path = FilePath()
path.change_working_directory(__file__)
