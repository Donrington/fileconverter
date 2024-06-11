from flask import Flask
from datetime import datetime,time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TEXT
db = SQLAlchemy()