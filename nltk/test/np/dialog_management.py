import json
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import numpy as np
import re
from sklearn.externals import joblib
from unicodedata import normalize

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
    def __init__(self, num_intents):
        self.__states = {}
        self.__current_state = ''
        self.__num_intents = num_intents
        self.__intent = 0
    
    @property
    def current_state(self):
        return self.__current_state   

    @current_state.setter
    def current_state(self, value):
        self.__current_state = value

    @property
    def intent(self):
        return self.__intent

    @intent.setter
    def intent(self, value):
        self.__intent = value
        
    def add_state(self, identifier, vectorizer, model):
        if identifier not in self.__states:            
            self.__states[identifier] = State(vectorizer, model)
        else:
            raise StateMachineError('Este estado ya esta definido')
            
    def add_transitions(self, state, transitions):
        if state in self.__states:
            undefined_states = set(transitions.values()) - set(self.__states.keys())
            if not undefined_states:
                undefined_labels = set(transitions.keys()) - set(self.__states[state].model.classes_)
                if not undefined_labels:
                    self.__states[state].transitions = transitions
                else:
                    raise StateMachineError('Las etiquetas {0} no estan definidas en el modelo del estado {1}'
                                    .format(undefined_labels, state))
            else:
                raise StateMachineError('Los estados {0} no estan definidos'.format(undefined_states))     
        else:
            raise StateMachineError('El estado {0} no esta definido'.format(state))
            
    def add_initial_state(self, identifier):
        if identifier in self.__states:
            if not self.__current_state:
                self.__current_state = identifier
            else:
                raise StateMachineError('Ya se definio un estado inicial')
        else:
            raise StateMachineError('Este estado no esta definido')
            
    def __clear_message(self, text):
        irrelevant_words = [word for word in stopwords.words('spanish') if word not in ['si', 'no']]
        irrelevant_words.extend(['sandra', 'carlos', 'luz', 'buitrago', 'luisa', 'castiblanco',
                                 'andres','jimenez', 'diana', 'cortes', 'nataly', 'aguirre', 'leidy', 'diaz', 'joana', 
                                 'zapata', 'karen', 'moreno', 'hiliany', 'adied', 'fracica', 'velasquez', 
                                 'chavez', 'torres', 'yeny', 'fernanda', 'rincon', 'didier', 'david', 'mendoza', 'gomez',
                                 'yhanira', 'vivas', 'adriana', 'barbosa', 'yang', 'pachon', 'maria', 'guzman', 'mario',
                                 'alejandro', 'francy', 'carolina'])
        irrelevant_words.extend(['senor', 'senora', 'senorita', 'hola', 'buenos', 'buen', 'buenas', 'buena', 'dias', 'dia', 
                                 'tardes', 'tarde', 'favor'])
        irrelevant_words.extend(['saber', 'hacer', 'haciendo', 'hacerlo', 'necesito', 'quiero', 'quisiera', 'puedo', 'podria',
                                 'amable', 'aqui', 'alli', 'alla', 'indicar', 'indicas', 'indica', 'consultar', 'consulta',
                                 'consultas', 'solicito', 'solicita'])
        exception_words = ['formulario', 'continuidad']

        stemmer = SnowballStemmer('spanish')
        words = tokenize.word_tokenize(str(text))
        norm_words = [normalize('NFKD', word.lower()).encode('ascii', 'ignore').decode('utf-8') 
                      for word in words]
        clean_words = [stemmer.stem(word) if word not in exception_words else word
                       for word in norm_words if word.isalpha() and word not in irrelevant_words
                       and re.search('[aeiou]', word) and re.search('[bcdfghjklmnpqrstvwxyz]', word)]
        return ' '.join(clean_words)
            
    def transition(self, message):
        if self.__states:
            if self.__current_state:
                clean_message = self.__clear_message(message)
                features = self.__states[self.__current_state].vectorizer.transform([clean_message])
                predict = self.__states[self.__current_state].model.predict(features)[0]
                current_state_proba = self.__states[self.__current_state].model.predict_proba(features).max()
                transitions = self.__states[self.__current_state].transitions
                if self.__current_state == transitions[predict]:
                    if self.__intent >= self.__num_intents:
                        self.__intent = 0
                        self.__current_state = 's1'
                        return ('agente', -1, -1)
                    else:
                        self.__intent += 1
                else:
                    self.__intent = 0
                self.__current_state = transitions[predict]
                features = self.__states[self.__current_state].vectorizer.transform([clean_message])
                next_state_proba = self.__states[self.__current_state].model.predict_proba(features).max()
                return (predict, np.around(current_state_proba * 100, 0), np.around(next_state_proba * 100, 0))
            else:
                raise StateMachineError('El estado inicial no se ha definido')
        else:
            raise StateMachineError('Aun no hay estados definidos')
    
    def load_params(self, filepath):        
        with open(filepath, 'r') as jsonfile:
            params = json.load(jsonfile)
            self.__current_state = params['current_state']
            self.__intent = params['intent']
            
    def save_params(self, filepath):
        with open(filepath, 'w') as jsonfile:
            params = {'current_state': self.__current_state, 'intent': self.__intent}
            json.dump(params, jsonfile)

class Chatbot:
    def __init__(self, config_section):
        self.__config_section = config_section
        self.__session_id = ''
              
        states = ['s1', 's2', 's3', 's4', 's5']   
        models = joblib.load(config_section['path'] + config_section['trained_package'])

        dialog_tree = StateMachine(0)

        for state, model in zip(states, models):
            vectorizer, classifier = model
            dialog_tree.add_state(state, vectorizer, classifier)

        dialog_tree.add_transitions('s1', {'saludo': 's2', 'otro': 's2'})
        dialog_tree.add_transitions('s2', {'fusion': 's4', 'inscripcion': 's3', 'otro': 's2'})
        dialog_tree.add_transitions('s3', {'primera vez': 's4', 'continuidad': 's4', 'perdida': 's4', 'otro': 's3'})
        dialog_tree.add_transitions('s4', {'costo': 's5', 'procedimiento': 's5'})
        dialog_tree.add_transitions('s5', {'positivo': 's2', 'negativo': 's2'})

        dialog_tree.add_initial_state('s1')
        self.__dialog_tree = dialog_tree
        self.__topic = 'none'

    def get_answer(self, input_message):
        with open(self.__config_section['path'] + self.__config_section['templates_file'], 'r') as jsonfile:
            templates = json.load(jsonfile)

        proba = []        
        if input_message != '':
            flow = True
            while flow:
                previous_state = self.__dialog_tree.current_state
                label, current_state_proba, next_state_proba = self.__dialog_tree.transition(input_message)
                if previous_state == 's1' and label == 'otro':
                    previous_state = self.__dialog_tree.current_state
                    label, current_state_proba, next_state_proba = self.__dialog_tree.transition(input_message)
                if previous_state == 's5' and label == 'positivo':
                    previous_state = self.__dialog_tree.current_state
                    label, current_state_proba, next_state_proba = self.__dialog_tree.transition(input_message)
                current_state = self.__dialog_tree.current_state
                proba.append((current_state_proba, next_state_proba))

                if (previous_state == 's2' or previous_state == 's3'):
                    self.__topic = label
                
                flow = ((previous_state == 's2' and current_state == 's3' and next_state_proba > 40) or 
                        (previous_state == 's2' and current_state == 's4' and next_state_proba > 70) or
                        (previous_state == 's3' and current_state == 's4' and next_state_proba > 70))

            output = [(item['message'], item['length']) for item in templates 
                      if item['state'] == previous_state and item['label'] == label
                      and item['topic'] == self.__topic]
            # print(previous_state, label, self.__topic)
            if output:
                message, length = output[0]
                transfer = label == 'agente'
            else:
                raise ChatbotError('No hay ninguna plantilla definida para el estado, etiqueta o tema que se esta intentando buscar')
            
            with open(self.__config_section['path'] + self.__config_section['sessions_file'], 'r') as jsonfile:
                sessions_id = json.load(jsonfile)
            sessions_id[self.__session_id] = (self.__dialog_tree.current_state, self.__dialog_tree.intent, self.__topic)
            with open(self.__config_section['path'] + self.__config_section['sessions_file'], 'w') as jsonfile:
                json.dump(sessions_id, jsonfile)
        else:
            proba.append((-1, -1))
            message, length = ('not answer', [2])
            transfer = False
        
        return (proba, message, length, transfer)

    def session(self, session_id, is_session_active):
        self.__session_id = session_id

        with open(self.__config_section['path'] + self.__config_section['sessions_file'], 'r') as jsonfile:
            sessions_id = json.load(jsonfile)

        if is_session_active:
            if session_id in sessions_id:
                self.__dialog_tree.current_state, self.__dialog_tree.intent, self.__topic = sessions_id[session_id]
        else: 
            sessions_id.pop(session_id)
            with open(self.__config_section['path'] + self.__config_section['sessions_file'], 'w') as jsonfile:
                json.dump(sessions_id, jsonfile)
