import os
import fnmatch


class FileOpt:
    """
    FileOpt is a class with multiple file related operation functions:
    find_files_by_wildcard
    find_latest_file
    ==============================
    Parameter:
    p
        default path that FileOpt works at
    """

    def __init__(self, p):
        self.dir = p

    """
    Note: find_latest_file didn't use glob.glob 
    because glob doesn't return error alert when user don't have permission to a directory
    This can cause unnecessary confusion when debugging
    """

    """
    Function:
        find_files_by_wildcard
    Parameters: 
    -----------
    folder
        the path that files are stored. 
        if folder has no value then it will look for the default path p defined in __init__
    prefix
        prefix of the filename to search. can be null
    suffix 
        suffix of the filename to search. can be null
    
    Returns:
    --------
    matched_files ::  list
        a list of filenames in 'file' that has the 'prefix' and 'suffix'
    """

    def find_files_by_wildcard(self, folder='', prefix='', suffix=''):
        check_path = folder if folder != '' else self.dir
        file_list = os.listdir(check_path)
        matched_files = []
        for i in file_list:
            if fnmatch.fnmatch(i, prefix + '*' + suffix):
                matched_files.append(i)
        return matched_files

    """
    Function:
        find_latest_file
    Parameters: 
    -----------
    folder
        the path that files are stored. 
        if folder has no value then it will look for the default path p defined in __init__
    prefix :: str
        prefix of the filename to search. can be null
    suffix :: str
        suffix of the filename to search. can be null
    filename_only :: boolean
        if true then only return the file name else return the full path of the file

    Returns:
    --------
    latest_file ::  str
        latest created file in 'file' that has the 'prefix' and 'suffix'
    """

    def find_latest_file(self, folder='', prefix='', suffix='', filename_only=False):
        file_list = self.find_files_by_wildcard(folder=folder, prefix=prefix, suffix=suffix)
        a = [self.dir + '/' + i for i in file_list]
        latest_file = max(a, key=lambda x: os.path.getctime(x))
        return os.path.basename(latest_file) if filename_only else latest_file


# test = FileOpt('/Users/gaowei_1/Downloads')
# print(test.dir)
# print(test.find_files_by_wildcard())
# print(test.find_latest_file(filename_only=False))
