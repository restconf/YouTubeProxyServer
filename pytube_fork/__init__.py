# -*- coding: utf-8 -*-
# flake8: noqa: F401
# noreorder
"""
Pytube: a very serious Python library for downloading YouTube Videos.
"""
__title__ = "pytube_fork3"
__author__ = "Nick Ficano, Harold Martin"
__license__ = "MIT License"
__copyright__ = "Copyright 2019 Nick Ficano"

from pytube_fork.version import __version__
from pytube_fork.streams import Stream
from pytube_fork.captions import Caption
from pytube_fork.query import CaptionQuery
from pytube_fork.query import StreamQuery
from pytube_fork.__main__ import YouTube
from pytube_fork.contrib.playlist import Playlist
