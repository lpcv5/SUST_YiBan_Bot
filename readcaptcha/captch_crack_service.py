#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>

from readcaptcha.interface import Interface
from readcaptcha.utils import ImageUtils

model_path = "readcaptcha/model"


def predict(interface: Interface, image_batch, split_char):
    return interface.predict_batch(image_batch, split_char)


def read(basecode, system_config, interface_manager):
    bytes_batch = ImageUtils.get_bytes_batch(ImageUtils(system_config), basecode)

    image_sample = bytes_batch[0]
    image_size = ImageUtils.size_of_image(image_sample)
    size_string = "{}x{}".format(image_size[0], image_size[1])

    interface: Interface = interface_manager.get_by_size(size_string)

    image_batch = ImageUtils.get_image_batch(
        interface.model_conf,
        bytes_batch,
        param_key=None,
        extract_rgb=None
    )

    predict_result = predict(interface, image_batch, '')
    print('验证码识别结果为:{}'.format(predict_result))
    return predict_result
