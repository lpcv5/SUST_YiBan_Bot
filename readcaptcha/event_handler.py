#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import os
import time
from watchdog.events import *
from readcaptcha.config import ModelConfig, Config
from readcaptcha.graph_session import GraphSession
from readcaptcha.interface import InterfaceManager, Interface
from readcaptcha.utils import PathUtils


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, conf: Config, model_conf_path: str, interface_manager: InterfaceManager):
        FileSystemEventHandler.__init__(self)
        self.conf = conf
        self.name_map = {}
        self.model_conf_path = model_conf_path
        self.interface_manager = interface_manager
        self.init()

    def init(self):
        model_list = os.listdir(self.model_conf_path)
        model_list = [os.path.join(self.model_conf_path, i) for i in model_list if i.endswith("yaml")]
        for model in model_list:
            self._add(model, is_first=True)

    def _add(self, src_path, is_first=False, count=0):
        try:
            model_path = str(src_path)
            if model_path.endswith("yaml"):
                model_conf = ModelConfig(self.conf, model_path)
                inner_name = model_conf.model_name
                inner_size = model_conf.size_string
                inner_key = PathUtils.get_file_name(model_path)
                for k, v in self.name_map.items():
                    if inner_size in v:
                        break

                inner_value = model_conf.model_name
                graph_session = GraphSession(model_conf)
                if graph_session.loaded:
                    interface = Interface(graph_session)
                    if inner_name == self.conf.default_model:
                        self.interface_manager.set_default(interface)
                    else:
                        self.interface_manager.add(interface)
                    self.name_map[inner_key] = inner_value
                    if src_path in self.interface_manager.invalid_group:
                        self.interface_manager.invalid_group.pop(src_path)
                else:
                    self.interface_manager.report(src_path)
                    if count < 12 and not is_first:
                        time.sleep(5)
                        return self._add(src_path, is_first=is_first, count=count + 1)

        except Exception as e:
            self.interface_manager.report(src_path)
