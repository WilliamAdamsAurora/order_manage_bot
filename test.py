import logging
from time import sleep

from core import Core
from core.database import Database
from core.elements.templates import Templates
from core.locator import Locator
from core.log import Log
from core.order import Order
from core.user import User
from icecream import ic
from string import Template
import os
from datetime import datetime
from loguru import logger

x = User(1087968824)


print(x.position)
