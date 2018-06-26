import json
import os
import re

import numpy as np
import sqlite3
from sklearn.externals import joblib


class StateMachineError(Exception):
    pass

class ChatbotError(Exception):
    pass

# http://www.quesucede.com/page/show/id/python-3-tree-implementation
# Brett Kromkamp (brett@perfectlearn.com)
# You Programming (http://www.youprogramming.com)
# May 03, 2014

class State:
    def __init__(self, vectorizer, model):
        self.__vectorizer = vectorizer
        self.__model = model
        self.__transitions = {}

    @property
    def vectorizer(self):
        return self.__vectorizer

    @property
    def model(self):
        return self.__model

    @property
    def transitions(self):
        return self.__transitions

    @transitions.setter
    def transitions(self, transitions):
        self.__transitions.update(transitions)

class StateMachine:
    def __init__(self, max_attempts):
        assert max_attempts >= 0, 'max_attempts deberia ser mayor o igual que 0'

        self.__states = {}
        self.__topics = {}

        self.__max_attempts = max_attempts
        self.__current_state = ''
        self.__last_transition = {}
        self.__topic = 'none'
        self.__attempt = 0

    @property
    def current_state(self):
        return self.__current_state

    @property
    def last_transition(self):
        return self.__last_transition

    @property
    def topic(self):
        return self.__topic

    @property
    def attempt(self):
        return self.__attempt

    @current_state.setter
    def current_state(self, value):
        self.__current_state = value

    @last_transition.setter
    def last_transition(self, value):
        self.__last_transition = value

    @topic.setter
    def topic(self, value):
        self.__topic = value

    @attempt.setter
    def attempt(self, value):
        self.__attempt = value

    def add_state(self, identifier, vectorizer, model):
        if identifier in self.__states:            
            raise StateMachineError('Este estado ya esta definido')
        if not any([name in str(model.__class__)
                    for name in ['LogisticRegression', 'GaussianNB', 'DistanceClassifier', 'RuleBasedClassifier']]):
            raise StateMachineError('El modelo de la clase {0} no esta soportado'
                                    .format(str(model.__class__)))
        
        self.__states[identifier] = State(vectorizer, model)

    def add_transitions(self, label, starting_state, ending_state, is_forced=False, proba_thresh=0):
        if starting_state not in self.__states:
            raise StateMachineError('El estado {0} no esta definido'.format(starting_state))
        if ending_state not in self.__states:
            raise StateMachineError('El estado {0} no esta definido'.format(ending_state))
        if label not in self.__states[starting_state].model.classes_:
            raise StateMachineError('La etiqueta {0} no esta definida en el modelo del estado {1}'
                                    .format(label, starting_state))
        if is_forced and (proba_thresh > 100 or proba_thresh < 0):
            raise StateMachineError('La probabilidad debe ser un valor entre 0 y 100')

        self.__states[starting_state].transitions[label] = {'next_state': ending_state, 
                                                            'is_forced': is_forced, 
                                                            'proba_thresh': proba_thresh}

    def add_initial_state(self, state):
        if state not in self.__states:
            raise StateMachineError('Este estado no esta definido')
        if self.__current_state != '':
            raise StateMachineError('Ya se definio un estado inicial')
        
        self.__current_state = state        

    def add_topics(self, normal, none=[]):
        self.__topics['normal'] = normal
        self.__topics['none'] = none

    def __get_model_results(self, state, message):
        if any([name in str(state.model.__class__)
                for name in ['LogisticRegression', 'GaussianNB']]):
            features = state.vectorizer.transform([message])
            prediction = state.model.predict(features)[0]
            proba = state.model.predict_proba(features).max()
        elif 'DistanceClassifier' in str(state.model.__class__):
            features = state.vectorizer.transform([message])
            prediction = state.model.get_label(features)[0]
            proba = state.model.get_similarity(features).max()
        elif 'RuleBasedClassifier' in str(state.model.__class__):
            prediction = state.model.get_label([message])[0]
            proba = state.model.get_similarity([message]).max()
        return (prediction, np.around(proba * 100, 0))

    def make_transition(self, message):
        if self.__states == '':
            raise StateMachineError('Aun no hay estados definidos')
        if self.__current_state == '':
            raise StateMachineError('El estado inicial no se ha definido')
        
        record = {}
        while True:
            prediction, current_state_proba = self.__get_model_results(self.__states[self.__current_state], message)
            record[(self.__current_state, prediction)] = current_state_proba
            if prediction not in self.__states[self.__current_state].transitions:
                raise StateMachineError('La transicion {0} del estado {1} no fue implementada'
                                        .format(prediction, self.__current_state))

            transition_attributes = self.__states[self.__current_state].transitions[prediction]
            if self.__current_state == transition_attributes['next_state']:
                if self.__attempt >= self.__max_attempts:
                    self.__attempt = 0
                    self.__current_state = 's1'
                    self.__topic = 'none'
                    prediction = 'agente'
                else:
                    self.__attempt += 1
            else:
                self.__attempt = 0

            if self.__current_state in self.__topics['none']:
                self.__topic = 'none'
            elif self.__current_state in self.__topics['normal']:
                self.__topic = prediction

            self.__last_transition['prediction'] = prediction
            self.__last_transition['state'] = self.__current_state

            if prediction == 'agente':
                break

            self.__current_state = transition_attributes['next_state']
            _, next_state_proba = self.__get_model_results(self.__states[self.__current_state], message)
            record[(self.__current_state, 'unknown')] = next_state_proba
            if not transition_attributes['is_forced'] or next_state_proba <= transition_attributes['proba_thresh']:
                break

        return record

class Chatbot:
    def __init__(self, path, config_section, connection):
        self.__path = path
        self.__config_section = config_section
        self.__connection = connection
        self.__session_id = ''
        self.__is_session_active = True
        
        models = joblib.load(self.__path + config_section['trained_package'])
        with open(self.__path + config_section['state_machine_config'], 'r') as file:
            state_machine_config = json.load(file)

        dialog_tree = StateMachine(state_machine_config['max_attempts'])

        for item in state_machine_config['models']:
            model = [model for model in models if model['id'] == item['id']][0]
            dialog_tree.add_state(item['state'], model['vectorizer'], model['classifier'])

        dialog_tree.add_initial_state(state_machine_config['initial_state'])

        for transition in state_machine_config['transitions']:
            if transition['is_forced']:
                dialog_tree.add_transitions(transition['label'], transition['starting_state'], transition['ending_state'], 
                                            transition['is_forced'], transition['proba_thresh'])
            else:
                dialog_tree.add_transitions(transition['label'], transition['starting_state'], transition['ending_state'], 
                                            transition['is_forced'])

        dialog_tree.add_topics(state_machine_config['topics']['normal'], 
                               state_machine_config['topics']['none'])

        self.__dialog_tree = dialog_tree

    def session(self, session_id, is_session_active):
        self.__session_id = session_id
        self.__is_session_active = is_session_active

        cursor = self.__connection.cursor()

        if is_session_active:
            cursor.execute("""SELECT state, attempt, topic FROM sessions WHERE sessionID = ?""", (session_id,))
            data = cursor.fetchone()
            if data != None:
                self.__dialog_tree.current_state, self.__dialog_tree.attempt, self.__dialog_tree.topic = data
            else:
                cursor.execute("""INSERT INTO sessions VALUES (?, ?, ?, ?)""", 
                               (session_id, self.__dialog_tree.current_state, 
                                self.__dialog_tree.attempt, self.__dialog_tree.topic,))
                self.__connection.commit()
        else:
            cursor.execute("""DELETE FROM sessions WHERE sessionID = ?""", (session_id,))
            self.__connection.commit()

    def get_answer(self, input_message):
        with open(self.__path + self.__config_section['templates_file'], 'r') as file:
            templates = json.load(file)

        with open(self.__path + self.__config_section['state_machine_config'], 'r') as file:
            state_machine_config = json.load(file)

        debug = ''
        if input_message != '' and self.__is_session_active:
            record = self.__dialog_tree.make_transition(input_message)
            previous_state = self.__dialog_tree.last_transition['state']
            label = self.__dialog_tree.last_transition['prediction']
            topic = self.__dialog_tree.topic

            debug = str({'previous_state': previous_state, 'prediction': label, 'topic': topic, 'record': record})

            if label == 'agente':
                template_id = 'agente'
            else:
                template_id = next((item['id'] for item in state_machine_config['templates'] 
                                    if item['state'] == previous_state and item['label'] == label 
                                    and item['topic'] == topic), 'none')
            if template_id == 'none':
                raise ChatbotError('No hay ningun id de plantilla definido para el estado {0}, etiqueta {1} ' 
                                   'y tema {2}'.format(previous_state, label, topic))

            output = next(((item['message'], item['length']) 
                            for item in templates if item['id'] == template_id), 'none')

            if output != 'none':
                message, length = output
                transfer = label == 'agente'
            else:
                raise ChatbotError('No hay ninguna plantilla definida para el id {0}'.format(template_id))

            cursor = self.__connection.cursor()
            
            cursor.execute("""UPDATE OR IGNORE sessions SET state = ?, attempt = ?, topic = ? WHERE sessionID = ?""", 
                           (self.__dialog_tree.current_state, self.__dialog_tree.attempt, 
                            self.__dialog_tree.topic, self.__session_id,))
            self.__connection.commit()
        else:
            message, length = ('not answer', [2])
            transfer = False

        return (debug, message, length, transfer)
