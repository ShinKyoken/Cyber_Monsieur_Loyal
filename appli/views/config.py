from appli.app import app
from appli.models import *
from flask import render_template, redirect, url_for, request, send_file, make_response
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, validators, PasswordField
from hashlib import sha256
from io import BytesIO
import io
import os
import base64
import os
