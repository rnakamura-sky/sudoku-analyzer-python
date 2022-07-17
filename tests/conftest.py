# coding: utf-8
"""conftest"""

import sys
import os

# srcのモジュール等読み込めるように設定
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../src/"))