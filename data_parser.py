import math

import numpy as np
import pandas as pd
from config import Config, CognitionType,CognitionTasks
from tqdm import tqdm
import os
import json
import pylangacq

class DataParser:
    def __init__(self):
        self.error_list = []
        self.error_list_address = Config().ds_prefix  + 'Error_list_no_INV.txt'

    def create_subject_profile(self):
        paths =self._create_folders_paths()
        subjects = self._get_subjects(paths)

        for subj_id in tqdm(subjects.keys()):
            folders = subjects[subj_id]
            chat_profile = None
            for address in folders:
                chat_profile =self._parse_chat_file_participants_info(subject_id =subj_id, chat_address=address,
                                                                      chat_profile=chat_profile)
            for address in folders:
                self._parse_chat_file(chat_address=address,chat_profile=chat_profile)
                pass
            '''save'''
            np.save(Config().profile_json_path + subj_id, chat_profile)
        with open(self.error_list_address, 'w') as file:
            # Iterate over the list and write each element to the file
            for er in self.error_list:
                file.write("%s\n" % er)
            file.close()



    def _get_subjects(self, paths):
        subject_ids = {}

        for p_item in paths:
            folder = p_item['folder']
            for file in tqdm(os.listdir(folder)):
                if file.endswith('.cha'):
                    sid = file
                    address = folder + file
                    if sid in subject_ids:
                        subject_ids[sid].append(address)
                    else:
                        subject_ids[sid] = [address]
        return subject_ids


    def _parse_chat_file_participants_info(self, subject_id, chat_address, chat_profile=None):
        if chat_profile is None:
            chat_profile = self.create_chat_profile()
        chat_address = '/media/ali/extradata/Pitt_ds/Pitt_Dataset/Pitt/Control/cookie/158-2.cha'
        reader = pylangacq.read_chat(chat_address)
        utterances = reader.utterances()

        participant_info = None
        investigator_info = None

        try:
            participant_info = reader.headers()[0]['Participants']['PAR']
        except Exception as e:
            print('ERROR = > ')
            print(chat_address + ' :  ' +  str(e))
            self.error_list.append(chat_address)
            print('---------------------------------')

        try:
            investigator_info = reader.headers()[0]['Participants']['INV']
        except Exception as e:
            # print('ERROR = > ')
            # print(chat_address + ' :  ' +  str(e))
            self.error_list.append(chat_address)
            # print('---------------------------------')



        if chat_profile is None:
            chat_profile = self.create_chat_profile()

        chat_profile['subject_id'] = subject_id
        try:
            if participant_info is not  None:
                chat_profile['participant_info']['age'] = participant_info['age']
                chat_profile['participant_info']['sex'] = participant_info['sex']
                chat_profile['participant_info']['education'] = participant_info['education']
                chat_profile['participant_info']['group'] = participant_info['group']
        except Exception as e:
            print(chat_address + str(e))

        try:
            if investigator_info is not None:
                chat_profile['investigator_info']['age'] = investigator_info['age']
                chat_profile['investigator_info']['sex'] = investigator_info['sex']
                chat_profile['investigator_info']['education'] = investigator_info['education']
                chat_profile['investigator_info']['group'] = investigator_info['group']
        except Exception as e:
            print(chat_address + str(e))

        return chat_profile

    def _parse_chat_file(self, chat_address, chat_profile):
        cog_type_str = chat_address.split('/')[-3]
        cog_task_str = chat_address.split('/')[-2]

        cog_type = CognitionType().str_to_id(cog_type_str)
        cog_task = CognitionTasks().str_to_id(cog_task_str)

        if 'transcripts' not in chat_profile.keys():
            chat_profile['transcripts'] = {}

        chat_profile['transcripts'][cog_task_str] = {}

        reader = pylangacq.read_chat(chat_address)
        utterances = reader.utterances()

        for i ,utterance in enumerate(utterances):
            ut_obj = self._parse_utterance(utterance)
            chat_profile['transcripts'][cog_task_str][i] = ut_obj

        return chat_profile


    def _parse_utterance(self, utterance):
        participant = utterance.participant

        if utterance.time_marks is not None:
            t_fr = utterance.time_marks[0]
            t_to = utterance.time_marks[1]
        else:
            t_fr= None
            t_to = None

        tokens = utterance.tokens
        sentence = self._get_sentence_from_token(utterance.tokens)
        tiers = utterance.tiers
        return {
            'participant':participant,
            't_fr':t_fr,
            't_to':t_to,
            'tokens':tokens,
            'sentence':sentence,
            'tiers':tiers,
        }

    def _get_sentence_from_token(self, tokens):
        sentence = ''
        for token in tokens:
            sentence += token.word + ' '
        return sentence

    def _create_folders_paths(self):
        cong_types = CognitionType().get_all()
        cong_types_str = CognitionType().get_all_str()

        cong_tasks = CognitionTasks().get_all()
        cong_tasks_str = CognitionTasks().get_all_str()

        paths = []
        for i in range(len(cong_types)):
            for j in range(len(cong_tasks)):
                item = {
                    'cog_type': cong_types[i],
                    'cog_task': cong_tasks[j],
                    'folder': Config().ds_prefix + cong_types_str[i] + '/' + cong_tasks_str[j] + '/'
                }
                paths.append(item)
        return paths

    def create_chat_profile(self):
        return {
            'subject_id':None,
            'participant_info' : {
                'age': None,
                'sex': None,
                'education': None,
                'group': None,
            },
            'investigator_info': {
                'age': None,
                'sex': None,
                'education': None,
                'group': None,
            },

        }