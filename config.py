
class Config:
    def __init__(self):
        self.ds_prefix = "/media/ali/extradata/Pitt_ds/Pitt_Dataset/Pitt/"

        self.profiles_json_address = self.ds_prefix + 'profiles.json'
        self.profile_json_path = self.ds_prefix + 'profiles/'


class CognitionTasks:
    def __init__(self):
        self.cookie: int = 0
        self.fluency: int = 1
        self.recall: int = 2
        self.sentence: int = 3

        self.cookie_str: str = 'cookie'
        self.fluency_str: str = 'fluency'
        self.recall_str: str = 'recall'
        self.sentence_str: str = 'sentence'

    def str_to_id(self, key):
        obj = {
            "cookie":0,
            "fluency":1,
            "recall":2,
            "sentence":3,
        }
        return obj[key]

    def get_all(self):
        return [self.cookie, self.fluency, self.recall, self.sentence]
    def get_all_str(self):
        return [self.cookie_str, self.fluency_str, self.recall_str, self.sentence_str]



class CognitionType:
    def __init__(self):
        self.Control: int = 0
        self.Dementia: int = 1
        self.Control_str: str = 'Control'
        self.Dementia_str: str = 'Dementia'

    def str_to_id(self, key):
        obj = {
            "Control": 0,
            "Dementia": 1,
        }
        return obj[key]

    def get_all(self):
        return [self.Control, self.Dementia]
    def get_all_str(self):
        return [self.Control_str, self.Dementia_str]