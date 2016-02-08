# -*- coding: utf-8 -*-
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from members.extensions import login_manager
from members.public.forms import LoginForm
from members.user.forms import RegisterForm
from members.user.models import User
from members.utils import flash_errors

blueprint = Blueprint('members', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))
