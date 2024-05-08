import math

import numpy as np
import pandas as pd
from config import Config, CognitionType,CognitionTasks
from tqdm import tqdm
import os
import json


class DataHelper:
    def __init__(self):
        pass

    def read_profiles(self, query=None):
        for file in tqdm(os.listdir(Config().profile_json_path)):
            if file.endswith('.npy'):
                chat_profile = np.load(Config().profile_json_path+file, allow_pickle=True).item()
                pass



