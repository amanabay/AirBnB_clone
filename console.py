#!/usr/bin/python3
'''The entry point of the command interpreter.'''

import re
import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.review import Review
from models.amenity import Amenity


class HBNBCommand(cmd.Cmd):
    '''HBNBCommand implements the Cmd class.
        It is a command  interpreter for the AirBnB project.

    Attributes:
            prompt (str): The command prompt.
    '''
    prompt = '(hbnb) '

    def default(self, line):
        '''Catch commands if nothing else matches then.'''
        self._precmd(line)

    def _precmd(self, line):
        '''Intercepts commands to test for class.syntax()'''
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                    1) or "") + " " + (match_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return command

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

    def do_show(self, line):
        ''' Prints the string representation of an instance based
            on the class name and id.
            Usage: show <ClassName> <id>
        '''
        cmds = parsCmd(line)
        models.storage.reload()
        objects = models.storage.all()

        try:
            print(objects[cmds[0] + "." + cmds[1]])
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, line):
        ''' Deletes an instance based on the class name and id.
            Change is saved.
            Usage: destroy <ClassName> <id>
        '''
        cmds = parsCmd(line)
        models.storage.reload()
        obj = models.storage.all()

        try:
            del obj[cmds[0] + "." + cmds[1]]
        except KeyError:
            print("** no instance found **")
            return

        models.storage.save()

    def do_all(self, line):
        ''' Display string representations of all instances of a given class.
            If no class is specified, displays all instantiated objects.
            Usage: all <ClassName> or all
        '''
        obj_list = []
        models.storage.reload()
        objs = models.storage.all()

        if line:
            try:
                eval(line)
            except NameError:
                print("** class doesn't exist **")
        else:
            line.strip()

        for key, val in objs.items():
            if line and isinstance(val, eval(line)):
                val = str(val)
                obj_list.append(val)
            elif not line:
                val = str(val)
                obj_list.append(val)

        print(obj_list)

    def do_update(self, line):
        '''
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.

        Usage:  update <class> <id> <attribute_name> <attribute_value> or
                <class>.update(<id>, <attribute_name>, <attribute_value>) or
                <class>.update(<id>, <dictionary>)
        '''
        dq1 = line.find('"')
        if dq1 != -1:
            dq2 = line[dq1+1:].find('"')
            if dq2 != -1:
                dq2 = dq1 + dq2 + 1

        cmds = parsCmd(line)

        models.storage.reload()
        objs = models.storage.all()

        try:
            value = objs[cmds[0] + "." + cmds[1]]
        except KeyError:
            print("** no instance found **")
            return
        if len(cmds) == 2:
            print("** attribute name missing **")
            return
        elif len(cmds) == 3:
            print("** value missing **")
            return

        try:
            if dq1 != -1:
                if dq2 != -1:
                    cmds[3] = line[dq1+1:dq2]
            attr_type = type(getattr(value, cmds[2]))
            cmds[3] = attr_type(cmds[3])

        except AttributeError:
            pass

        setattr(value, cmds[2], cmds[3])
        models.storage.save()


def parsCmd(command):
    splited_cmds = command.split()

    if len(splited_cmds) == 0:
        print("** class name missing **")
        return

    try:
        eval(splited_cmds[0])
    except NameError:
        print("** class doesn't exist **")
        return

    if len(splited_cmds) == 1:
        print("** instance id missing **")
        return
    else:
        return (splited_cmds)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
