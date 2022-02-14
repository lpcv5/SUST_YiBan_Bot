#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import os
import sys
import uuid
import json
import yaml
import hashlib
import logging
import logging.handlers
from category import *
from constants import SystemConfig, ModelField, ModelScene

MODEL_SCENE_MAP = {
    'Classification': ModelScene.Classification
}

MODEL_FIELD_MAP = {
    'Image': ModelField.Image,
    'Text': ModelField.Text
}

BLACKLIST_PATH = "blacklist.json"
WHITELIST_PATH = "whitelist.json"


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_version():
    version_file_path = resource_path("VERSION")

    if not os.path.exists(version_file_path):
        return "NULL"

    with open(version_file_path, "r", encoding="utf8") as f:
        return "".join(f.readlines()).strip()


def get_default(src, default):
    return src if src else default


def get_dict_fill(src: dict, default: dict):
    if not src:
        return default
    new_dict = default
    new_dict.update(src)
    return new_dict


def blacklist() -> list:
    if not os.path.exists(BLACKLIST_PATH):
        return []
    try:
        with open(BLACKLIST_PATH, "r", encoding="utf8") as f_blacklist:
            result = json.loads("".join(f_blacklist.readlines()))
            return result
    except Exception as e:
        print(e)
        return []


def whitelist() -> list:
    if not os.path.exists(WHITELIST_PATH):
        return ["127.0.0.1", "localhost"]
    try:
        with open(WHITELIST_PATH, "r", encoding="utf8") as f_whitelist:
            result = json.loads("".join(f_whitelist.readlines()))
            return result
    except Exception as e:
        print(e)
        return ["127.0.0.1", "localhost"]


def set_blacklist(ip):
    try:
        old_blacklist = blacklist()
        old_blacklist.append(ip)
        with open(BLACKLIST_PATH, "w+", encoding="utf8") as f_blacklist:
            f_blacklist.write(json.dumps(old_blacklist, ensure_ascii=False, indent=2))
    except Exception as e:
        print(e)


class Config(object):
    def __init__(self, conf_path: str, graph_path: str = None, model_path: str = None):
        self.model_path = model_path
        self.conf_path = conf_path
        self.graph_path = graph_path
        self.sys_cf = self.read_conf
        self.access_key = None
        self.secret_key = None
        self.default_model = self.sys_cf['System']['DefaultModel']
        self.default_port = self.sys_cf['System'].get('DefaultPort')
        if not self.default_port:
            self.default_port = 19952
        self.split_flag = self.sys_cf['System']['SplitFlag']
        self.split_flag = self.split_flag if isinstance(self.split_flag, bytes) else SystemConfig.split_flag
        self.route_map = get_default(self.sys_cf.get('RouteMap'), SystemConfig.default_route)
        self.log_path = "logs"
        self.request_def_map = get_default(self.sys_cf.get('RequestDef'), SystemConfig.default_config['RequestDef'])
        self.response_def_map = get_default(self.sys_cf.get('ResponseDef'), SystemConfig.default_config['ResponseDef'])
        self.save_path = self.sys_cf['System'].get("SavePath")
        self.request_count_interval = get_default(
            src=self.sys_cf['System'].get("RequestCountInterval"),
            default=60 * 60 * 24
        )
        self.g_request_count_interval = get_default(
            src=self.sys_cf['System'].get("GlobalRequestCountInterval"),
            default=60 * 60 * 24
        )
        self.request_limit = get_default(self.sys_cf['System'].get("RequestLimit"), -1)
        self.global_request_limit = get_default(self.sys_cf['System'].get("GlobalRequestLimit"), -1)
        self.exceeded_msg = get_default(
            src=self.sys_cf['System'].get("ExceededMessage"),
            default=SystemConfig.default_config['System'].get('ExceededMessage')
        )
        self.illegal_time_msg = get_default(
            src=self.sys_cf['System'].get("IllegalTimeMessage"),
            default=SystemConfig.default_config['System'].get('IllegalTimeMessage')
        )

        self.request_size_limit: dict = get_default(
            src=self.sys_cf['System'].get('RequestSizeLimit'),
            default={}
        )
        self.blacklist_trigger_times = get_default(self.sys_cf['System'].get("BlacklistTriggerTimes"), -1)

        self.use_whitelist: dict = get_default(
            src=self.sys_cf['System'].get('Whitelist'),
            default=False
        )

        self.error_message = get_dict_fill(
            self.sys_cf['System'].get('ErrorMessage'), SystemConfig.default_config['System']['ErrorMessage']
        )
        self.logger_tag = get_default(self.sys_cf['System'].get('LoggerTag'), "coriander")
        self.without_logger = self.sys_cf['System'].get('WithoutLogger')
        self.without_logger = self.without_logger if self.without_logger is not None else False
        self.logger = logging.getLogger(self.logger_tag)
        self.use_default_authorization = False
        self.authorization = None
        self.init_logger()
        self.assignment()

    def init_logger(self):
        self.logger.setLevel(logging.INFO)

        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
        if not os.path.exists(self.graph_path):
            os.makedirs(self.graph_path)

        self.logger.propagate = False

        if not self.without_logger:
            if not os.path.exists(self.log_path):
                os.makedirs(self.log_path)
            file_handler = logging.handlers.TimedRotatingFileHandler(
                '{}/{}.log'.format(self.log_path, "captcha_platform"),
                when="MIDNIGHT",
                interval=1,
                backupCount=180,
                encoding='utf-8'
            )
            stream_handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def assignment(self):
        # ---AUTHORIZATION START---
        mac_address = hex(uuid.getnode())[2:]
        self.use_default_authorization = False
        self.authorization = self.sys_cf.get('Security')
        if not self.authorization or not self.authorization.get('AccessKey') or not self.authorization.get('SecretKey'):
            self.use_default_authorization = True
            model_name_md5 = hashlib.md5(
                "{}".format(self.default_model).encode('utf8')).hexdigest()
            self.authorization = {
                'AccessKey': model_name_md5[0: 16],
                'SecretKey': hashlib.md5("{}{}".format(model_name_md5, mac_address).encode('utf8')).hexdigest()
            }
        self.access_key = self.authorization['AccessKey']
        self.secret_key = self.authorization['SecretKey']
        # ---AUTHORIZATION END---

    @property
    def read_conf(self):
        if not os.path.exists(self.conf_path):
            with open(self.conf_path, 'w', encoding="utf-8") as sys_fp:
                sys_fp.write(yaml.safe_dump(SystemConfig.default_config))
                return SystemConfig.default_config
        with open(self.conf_path, 'r', encoding="utf-8") as sys_fp:
            sys_stream = sys_fp.read()
            return yaml.load(sys_stream, Loader=yaml.SafeLoader)


class Model(object):

    def __init__(self, conf: Config, model_conf_path: str):
        self.conf = conf
        self.logger = self.conf.logger
        self.graph_path = conf.graph_path
        self.model_path = conf.model_path
        self.model_conf_path = model_conf_path
        self.model_conf_demo = 'model_demo.yaml'
        self.verify()

    def verify(self):
        if not os.path.exists(self.model_conf_path):
            raise Exception(
                'Configuration File "{}" No Found. '
                'If it is used for the first time, please copy one from {} as {}'.format(
                    self.model_conf_path,
                    self.model_conf_demo,
                    self.model_path
                )
            )

        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
            raise Exception(
                'For the first time, please put the trained model in the model directory.'
            )

    def category_extract(self, param):
        if isinstance(param, list):
            return param
        if isinstance(param, str):
            if param in SIMPLE_CATEGORY_MODEL.keys():
                return SIMPLE_CATEGORY_MODEL.get(param)
            self.logger.error(
                "Category set configuration error, customized category set should be list type"
            )
            return None

    @property
    def model_conf(self) -> dict:
        with open(self.model_conf_path, 'r', encoding="utf-8") as sys_fp:
            sys_stream = sys_fp.read()
            return yaml.load(sys_stream, Loader=yaml.SafeLoader)


class ModelConfig(Model):
    model_exists: bool = False

    def __init__(self, conf: Config, model_conf_path: str):
        super().__init__(conf=conf, model_conf_path=model_conf_path)

        self.conf = conf

        """MODEL"""
        self.model_root: dict = self.model_conf['Model']
        self.model_name: str = self.model_root.get('ModelName')
        self.model_version: float = self.model_root.get('Version')
        self.model_version = self.model_version if self.model_version else 1.0
        self.model_field_param: str = self.model_root.get('ModelField')
        self.model_field: ModelField = ModelConfig.param_convert(
            source=self.model_field_param,
            param_map=MODEL_FIELD_MAP,
            text="Current model field ({model_field}) is not supported".format(model_field=self.model_field_param),
            code=50002
        )

        self.model_scene_param: str = self.model_root.get('ModelScene')

        self.model_scene: ModelScene = ModelConfig.param_convert(
            source=self.model_scene_param,
            param_map=MODEL_SCENE_MAP,
            text="Current model scene ({model_scene}) is not supported".format(model_scene=self.model_scene_param),
            code=50001
        )

        """SYSTEM"""
        self.checkpoint_tag = 'checkpoint'
        self.system_root: dict = self.model_conf['System']
        self.memory_usage: float = self.system_root.get('MemoryUsage')

        """FIELD PARAM - IMAGE"""
        self.field_root: dict = self.model_conf['FieldParam']
        self.category_param = self.field_root.get('Category')
        self.category_value = self.category_extract(self.category_param)
        if self.category_value is None:
            raise Exception(
                "The category set type does not exist, there is no category set named {}".format(self.category_param),
            )
        self.category: list = SPACE_TOKEN + self.category_value
        self.category_num: int = len(self.category)
        self.image_channel: int = self.field_root.get('ImageChannel')
        self.image_width: int = self.field_root.get('ImageWidth')
        self.image_height: int = self.field_root.get('ImageHeight')
        self.max_label_num: int = self.field_root.get('MaxLabelNum')
        self.min_label_num: int = self.get_var(self.field_root, 'MinLabelNum', self.max_label_num)
        self.resize: list = self.field_root.get('Resize')
        self.output_split = self.field_root.get('OutputSplit')
        self.output_split = self.output_split if self.output_split else ""
        self.corp_params = self.field_root.get('CorpParams')
        self.output_coord = self.field_root.get('OutputCoord')
        self.batch_model = self.field_root.get('BatchModel')
        self.external_model = self.field_root.get('ExternalModelForCorp')
        self.category_split = self.field_root.get('CategorySplit')

        """PRETREATMENT"""
        self.pretreatment_root = self.model_conf.get('Pretreatment')
        self.pre_binaryzation = self.get_var(self.pretreatment_root, 'Binaryzation', -1)
        self.pre_replace_transparent = self.get_var(self.pretreatment_root, 'ReplaceTransparent', True)
        self.pre_horizontal_stitching = self.get_var(self.pretreatment_root, 'HorizontalStitching', False)
        self.pre_concat_frames = self.get_var(self.pretreatment_root, 'ConcatFrames', -1)
        self.pre_blend_frames = self.get_var(self.pretreatment_root, 'BlendFrames', -1)
        self.pre_freq_frames = self.get_var(self.pretreatment_root, 'FreqFrames', -1)
        self.exec_map = self.get_var(self.pretreatment_root, 'ExecuteMap', None)

        """COMPILE_MODEL"""
        self.compile_model_path = os.path.join(self.graph_path, '{}.pb'.format(self.model_name))
        if not os.path.exists(self.compile_model_path):
            if not os.path.exists(self.graph_path):
                os.makedirs(self.graph_path)
            self.logger.error(
                '{} not found, please put the trained model in the graph directory.'.format(self.compile_model_path)
            )
        else:
            self.model_exists = True

    @staticmethod
    def param_convert(source, param_map: dict, text, code, default=None):
        if source is None:
            return default
        if source not in param_map.keys():
            raise Exception(text)
        return param_map[source]

    def size_match(self, size_str):
        return size_str == self.size_string

    @staticmethod
    def get_var(src: dict, name: str, default=None):
        if not src or name not in src:
            return default
        return src.get(name)

    @property
    def size_string(self):
        return "{}x{}".format(self.image_width, self.image_height)
