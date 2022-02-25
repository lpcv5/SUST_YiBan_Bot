#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import os
import yaml
from readcaptcha.categorys import *


def get_default(src, default):
    return src if src else default


class Config(object):
    def __init__(self, conf_path: str, graph_path: str = None, model_path: str = None):
        self.model_path = model_path
        self.conf_path = conf_path
        self.graph_path = graph_path
        self.sys_cf = self.read_conf
        self.default_model = self.sys_cf['System']['DefaultModel']
        self.split_flag = self.sys_cf['System']['SplitFlag']


    @property
    def read_conf(self):
        with open(self.conf_path, 'r', encoding="utf-8") as sys_fp:
            sys_stream = sys_fp.read()
            return yaml.load(sys_stream, Loader=yaml.SafeLoader)


class Model(object):

    def __init__(self, conf: Config, model_conf_path: str):
        self.conf = conf
        self.graph_path = conf.graph_path
        self.model_path = conf.model_path
        self.model_conf_path = model_conf_path
        self.model_conf_demo = 'model_demo.yaml'

    def category_extract(self, param):
        if isinstance(param, list):
            return param
        if isinstance(param, str):
            if param in SIMPLE_CATEGORY_MODEL.keys():
                return SIMPLE_CATEGORY_MODEL.get(param)
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
        self.model_scene_param: str = self.model_root.get('ModelScene')

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
        else:
            self.model_exists = True

    @staticmethod
    def get_var(src: dict, name: str, default=None):
        if not src or name not in src:
            return default
        return src.get(name)

    @property
    def size_string(self):
        return "{}x{}".format(self.image_width, self.image_height)
