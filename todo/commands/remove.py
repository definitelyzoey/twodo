from __future__ import absolute_import

import os
import sys
import json

from todo.commands.toggle import ToggleCommand
from todo.utils.menu import show_options
from todo.utils.styles import Fore, Style


class RemoveCommand(ToggleCommand):
    def get_subtitle(self):
        """Returns the subtitle of the menu"""
        return 'Remove items'


    def menu_handle(self, todos, item_index): # Removes items threw the menu
        todos_removed = todos.copy()
        todos_removed.pop(item_index)
        return todos_removed


    def toggle_handle(self, todos, item):
        todos_removed = todos.copy()
        todos_removed.remove(item)
        return todos_removed
    
    def search_all_handle(self, todos, item): # Removes all todos
        return self.toggle_handle(todos, item)
    
    def search_done_handle(self, todos, item): # Removes all of the compleated todos
        todos_removed = todos.copy()
        
        if item['done'] == True:
            todos_removed.remove(item)
        
        return todos_removed


Remove = RemoveCommand()
