# -*- coding: utf-8 -*-

import yaml


class YamlParser(object):
    def __init__(self, path):
        self.__config_dict = self.__load_yaml_file(path)
        self._concepts = None

    def __load_yaml_file(self, file_path):
        with open(file_path, 'r') as f:
            return yaml.load(f)

    @property
    def concepts(self):
        if self._concepts is None:
            self._concepts = '\n'.join(
                ['concept:(%s) [%s]' % (k, ' '.join(self.qichat_hack(v))) for k, v in self.__config_dict['concepts'].items()])
            self._concepts += '\n'
        return self._concepts

    def generate_rules(self, event_name):
        res = ""
        for k in self.__config_dict['concepts'].keys():
            res += 'u: ({*} ~%(con)s {*}) $%(eve)s=%(con)s \n' % ({'con': k, 'eve': event_name})
        return res

    @property
    def applications(self):
        return self.__config_dict['applications']

    @property
    def precanned_text(self):
        return self.__config_dict['precanned_text']

    def qichat_hack(self, l):
        for e in l:
            if ' ' in e:
                yield '"' + e + '"'
            else:
                yield e
