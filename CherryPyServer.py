import cherrypy, DatabaseConnector
from jinja2 import Environment, PackageLoader, select_autoescape


class HelloWorld(object):
    def __init__(self, tsc):
        super().__init__()
        self.dbc = DatabaseConnector.DatabaseConnector()
        self.env = Environment(loader=PackageLoader("templates"), autoescape=select_autoescape(['html', 'xml']))
        self.tsc = tsc

    def get_characters(self, list):
        characters = []
        for character in self.dbc.get_list_characters(list):
            characters.append(character[1])
        return characters

    @cherrypy.expose
    def index(self):
        lists = {}
        for list in self.dbc.get_lists():
            lists[list[1].title()] = self.get_characters(list[1])
            #lists.append(list[1])
        list_states = {}
        for list in self.dbc.get_lists():
            list_states[list[1].title()] = self.dbc.is_list_notifications(list[1])
        return self.env.get_template("index.html").render(lists=lists, list_states=list_states)
        return ','.join(lists)

    @cherrypy.expose
    def removecharacter(self, list, character):
        self.dbc.remove_character_from_list(character, list)
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def addcharacter(self, list_name, character_name):
        self.dbc.add_character_to_list(character_name, list_name.lower())
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def masspoke(self, message):
        self.tsc.masspoke(message)
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def notifications(self, list, state):
        self.dbc.set_list_notifications(list.lower(), 1 if state == "True" else 0)
        print("Setting %s to %s" % (list, str(1 if state == "True" else 0)))
        raise cherrypy.HTTPRedirect('/')