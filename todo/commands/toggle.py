from __future__ import absolute_import

import os
import sys
import json

from todo.commands.base import Command
from todo.utils.menu import show_options
from todo.utils.styles import Fore, Style


class ToggleCommand(Command):
    def get_subtitle(self): # change to base.py?
        """Returns the subtitle of the menu"""
        return 'Toggle items'

    def toggle_item(self, item): # Toggles the item
        item_toggled = item.copy()
        status = item['done']
        item_toggled['done'] = not status
        return item_toggled

    def menu_handle(self, todos, item_index): # Searches toggled items threw the menu
        todos_toggled = todos.copy()
        item_to_toggle = todos[item_index]
        todos_toggled[item_index] = self.toggle_item(item_to_toggle)
        return todos_toggled


    def search_handle(self, todos, item): # Searches toggled items threw the terminal
        todos_toggled = todos.copy()
        item_index = todos_toggled.index(item)
        item_to_toggle = todos_toggled[item_index]
        todos_toggled[item_index] = self.toggle_item(item_to_toggle)
        return todos_toggled

    def open_list(self, data, name):
        if len(data['todos']) == 0:
            raise KeyError
        try:
            return show_options(
                name,
                self.get_subtitle(),
                data['todos'],
                self.menu_handle
            )
        except KeyboardInterrupt:
            self.cancel_command()

    def update_todos(self, data):
        new_data = data.copy()
        items_titles = self.get_titles_input()
        options_all = ['-a', '-all']
        options_done = ['-d', '-done']
        todos = new_data['todos']

        if items_titles[0].lower() in options_all:
            for item in todos:
                todos = self.search_handle(todos)
        elif items_titles[0].lower() in options_done: # Maybe add confirmation?
            for item in todos:
                try: # Basically error handing for anything other than todo remove -d as it breaks the code.
                    todos = self.search_done_handle(todos, item)
                except AttributeError:
                    print(
                        '{warning}No command found.{reset}'
                        .format(
                            warning=Fore.WARNING,
                            reset=Style.RESET_ALL,
                        )
                    )

                    sys.exit()
        else:
            for title in items_titles:
                try:
                    title = int(title)
                    items_matching = [ item for item in todos if todos.index(item) == title ]
            
                    if items_matching:
                        for item_found in items_matching:
                            todos = self.search_handle(todos, item_found)
                    
                    # If there are no items matching the index, we print the index to the user.
                    items_not_found = []
                    for item in todos:
                        if todos.index(item) != title:
                            if str(title) in items_not_found:
                                break
                            else:
                                items_not_found.append(str(title))
                    
                    if items_not_found:
                       print(
                            '{info}Unknown {items_print}: {items}{reset}'
                            .format(
                                info=Fore.INFO,
                                reset=Style.RESET_ALL,
                                items_print=('indexs' if len(items_not_found) > 1 else 'index'),
                                items=', '.join(items_not_found),
                            )
                        )
                except ValueError:
                    items_matching = [ item for item in todos if item['title'] == title ]
                    if items_matching:
                        for item_found in items_matching:
                            todos = self.search_handle(todos, item_found)

                    # If there are no items matching the title, we print the title to the user.
                    items_not_found = []
                    for item in todos:
                        if item['title'] != title:
                            if str(title) in items_not_found:
                                break
                            else:
                                items_not_found.append(str(title))

                    if items_not_found:
                       print(
                            '{info}Unknown {items_print}: {items}{reset}'
                            .format(
                                info=Fore.INFO,
                                reset=Style.RESET_ALL,
                                items_print=('items' if len(items_not_found) > 1 else 'item'),
                                items=', '.join(items_not_found),
                            )
                        )

        self.sort_dict(todos)
        return todos


    def run(self):
        try:
            with open(self.PROJECT_FILE, 'r') as project_file:
                data = json.load(project_file)
        except FileNotFoundError:
            self.project_not_found()
        except KeyError:
            print(
                '{fail}An error has occured while toggling the todos.{reset}'
                .format(
                    fail=Fore.FAIL,
                    reset=Style.RESET_ALL,
                )
            )
            sys.exit(1)

        try: name = data['name']
        except: name = self.UNTITLED_NAME

        try:
            if self.get_command_attributes():
                new_todos = self.update_todos(data)
            else:
                new_todos = self.open_list(data, name)
        except KeyError:
            print(
                '{warning}No items in the project.{reset}'
                .format(
                    warning=Fore.WARNING,
                    reset=Style.RESET_ALL,
                )
            )
            sys.exit()

        new_data = {
            'name': name,
            'todos': new_todos
        }

        self.update_project(new_data)


Toggle = ToggleCommand()
