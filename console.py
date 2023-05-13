#!/usr/bin/python3
'''The entry point of the command interpreter.'''

import cmd
import models
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    '''HBNBCommand implements the Cmd class.
        It is a command  interpreter for the AirBnB project.

    Attributes:
            prompt (str): The command prompt.
    '''
    prompt = '(hbnb) '

    def do_quit(self):
        '''Quit command to exit the program.'''
        return True

    def do_EOF(self):
        '''EOF signal to exit the program.'''
        return True

    def emptyline(self):
        '''Do nothing when receiving an empty line.'''
        pass

    def do_create(self, line):
        '''Creates a new instance of BaseModel, saves it to the JSON file
            prints the id.
            Usage: create <ClassName>
        '''
        cmds = line.split()

        if len(cmds) == 0:
            print("** class name missing **")
            return

        try:
            eval(cmds[0])
        except NameError:
            print("** class doesn't exist **")
            return

        newModel = eval(cmds[0])()
        print(newModel.id)
        newModel.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()