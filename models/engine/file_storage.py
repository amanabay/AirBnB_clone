#!/usr/bin/python3
'''Defines the FileStorage class.'''

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place


class FileStorage:
    '''Definition of class FileStorage that handles serialization of instances
       to JSON file and deserialization of JSON files to instances
    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    '''

    __file_path = "file.json"
    __objects = {}

    def all(self):
        '''Return the dictionary __objects.'''
        return FileStorage.__objects

    def new(self, obj):
        '''Sets a new instance in the '__objects' dictionary using
           <obj class name>.id as the key

        Attributes:
            obj (object): object to be set in the __objects dictionary
        '''
        ocname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ocname, obj.id)] = obj

    def save(self):
        '''Serialize __objects to the JSON file __file_path.'''
        odict = FileStorage.__objects
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        try:
            with open(FileStorage.__file_path, "w") as f:
                json.dump(objdict, f)
        except Exception as e:
            print('Error while writting to file: ', e)

    def reload(self):
        '''Deserialize the JSON file __file_path to __objects, if it exists.'''
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
