import math
import re
from collections import Counter, defaultdict, deque, namedtuple
from copy import deepcopy
from dataclasses import dataclass
from functools import cache, lru_cache
from heapq import heappop, heappush
from itertools import permutations, product
from hashlib import md5
import random
import json
from types import SimpleNamespace

# import pyperclip as pc

# import networkx as nx
# from shapely import LinearRing, Polygon


data = open(0).read()
scanners = data.strip().split("\n\n")
