#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import io
import re
import cv2
import base64
import numpy as np
from PIL import Image as PIL_Image
from readcaptcha.pretreatment import preprocessing, preprocessing_by_func
from readcaptcha.config import ModelConfig, Config
from readcaptcha.middleware.impl.gif_frames import concat_frames, blend_frame
from readcaptcha.middleware.impl.rgb_filter import rgb_filter


class PathUtils(object):
    @staticmethod
    def get_file_name(path: str):
        if '/' in path:
            return path.split('/')[-1]
        elif '\\' in path:
            return path.split('\\')[-1]
        else:
            return path


class ImageUtils(object):

    def __init__(self, conf: Config):
        self.conf = conf

    def get_bytes_batch(self, base64_or_bytes):
        b64_filter_s = lambda s: re.sub("data:image/.+?base64,", "", s, 1) if ',' in s else s
        b64_filter_b = lambda s: re.sub(b"data:image/.+?base64,", b"", s, 1) if b',' in s else s
        if isinstance(base64_or_bytes, bytes):
            if self.conf.split_flag in base64_or_bytes:
                bytes_batch = base64_or_bytes.split(self.conf.split_flag)
            else:
                bytes_batch = [base64_or_bytes]
        elif isinstance(base64_or_bytes, list):
            bytes_batch = [base64.b64decode(b64_filter_s(i).encode('utf-8')) for i in base64_or_bytes if
                           isinstance(i, str)]
            if not bytes_batch:
                bytes_batch = [base64.b64decode(b64_filter_b(i)) for i in base64_or_bytes if isinstance(i, bytes)]
        else:
            base64_or_bytes = b64_filter_s(base64_or_bytes)
            bytes_batch = base64.b64decode(base64_or_bytes.encode('utf-8')).split(self.conf.split_flag)
        return bytes_batch

    @staticmethod
    def get_image_batch(model: ModelConfig, bytes_batch, param_key=None, extract_rgb: list = None):
        # Note that there are two return objects here.
        # 1.image_batch, 2.response

        def load_image(image_bytes: bytes):
            data_stream = io.BytesIO(image_bytes)
            pil_image = PIL_Image.open(data_stream)

            gif_handle = model.pre_concat_frames != -1 or model.pre_blend_frames != -1

            if pil_image.mode == 'P' and not gif_handle:
                pil_image = pil_image.convert('RGB')

            rgb = pil_image.split()
            size = pil_image.size

            if (len(rgb) > 3 and model.pre_replace_transparent) and not gif_handle:
                background = PIL_Image.new('RGB', pil_image.size, (255, 255, 255))
                try:
                    background.paste(pil_image, (0, 0, size[0], size[1]), pil_image)
                    pil_image = background
                except:
                    pil_image = pil_image.convert('RGB')

            if len(pil_image.split()) > 3 and model.image_channel == 3:
                pil_image = pil_image.convert('RGB')

            if model.pre_concat_frames != -1:
                im = concat_frames(pil_image, model.pre_concat_frames)
            elif model.pre_blend_frames != -1:
                im = blend_frame(pil_image, model.pre_blend_frames)
            else:
                im = np.asarray(pil_image)

            if extract_rgb:
                im = rgb_filter(im, extract_rgb)

            im = preprocessing_by_func(
                exec_map=model.exec_map,
                key=param_key,
                src_arr=im
            )

            if model.image_channel == 1 and len(im.shape) == 3:
                im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

            im = preprocessing(
                image=im,
                binaryzation=model.pre_binaryzation,
            )

            if model.pre_horizontal_stitching:
                up_slice = im[0: int(size[1] / 2), 0: size[0]]
                down_slice = im[int(size[1] / 2): size[1], 0: size[0]]
                im = np.concatenate((up_slice, down_slice), axis=1)

            image = im.astype(np.float32)
            if model.resize[0] == -1:
                ratio = model.resize[1] / size[1]
                resize_width = int(ratio * size[0])
                image = cv2.resize(image, (resize_width, model.resize[1]))
            else:
                image = cv2.resize(image, (model.resize[0], model.resize[1]))
            image = image.swapaxes(0, 1)
            return (image[:, :, np.newaxis] if model.image_channel == 1 else image[:, :]) / 255.

        try:
            image_batch = [load_image(i) for i in bytes_batch]
            return image_batch
        except OSError:
            return None
        except ValueError as _e:
            print(_e)
            return None

    @staticmethod
    def size_of_image(image_bytes: bytes):
        _null_size = tuple((-1, -1))
        try:
            data_stream = io.BytesIO(image_bytes)
            size = PIL_Image.open(data_stream).size
            return size
        except OSError:
            return _null_size
        except ValueError:
            return _null_size

    @staticmethod
    def test_image(h):
        """JPEG"""
        if h[:3] == b"\xff\xd8\xff":
            return 'jpeg'
        """PNG"""
        if h[:8] == b"\211PNG\r\n\032\n":
            return 'png'
        """GIF ('87 and '89 variants)"""
        if h[:6] in (b'GIF87a', b'GIF89a'):
            return 'gif'
        """TIFF (can be in Motorola or Intel byte order)"""
        if h[:2] in (b'MM', b'II'):
            return 'tiff'
        if h[:2] == b'BM':
            return 'bmp'
        """SGI image library"""
        if h[:2] == b'\001\332':
            return 'rgb'
        """PBM (portable bitmap)"""
        if len(h) >= 3 and \
                h[0] == b'P' and h[1] in b'14' and h[2] in b' \t\n\r':
            return 'pbm'
        """PGM (portable graymap)"""
        if len(h) >= 3 and \
                h[0] == b'P' and h[1] in b'25' and h[2] in b' \t\n\r':
            return 'pgm'
        """PPM (portable pixmap)"""
        if len(h) >= 3 and h[0] == b'P' and h[1] in b'36' and h[2] in b' \t\n\r':
            return 'ppm'
        """Sun raster file"""
        if h[:4] == b'\x59\xA6\x6A\x95':
            return 'rast'
        """X bitmap (X10 or X11)"""
        s = b'#define '
        if h[:len(s)] == s:
            return 'xbm'
        return None
