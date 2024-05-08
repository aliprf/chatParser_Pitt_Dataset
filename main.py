from config import Config, CognitionType,CognitionTasks
from data_parser import DataParser
from data_helper import DataHelper

if __name__ == '__main__':

    dp = DataParser()
    dp.create_subject_profile()

    dh = DataHelper()
    dh.read_profiles()