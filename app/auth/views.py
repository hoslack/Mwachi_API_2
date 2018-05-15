from flask.views import MethodView
from flask import jsonify
from . import auth_blueprint


class SignUpView(MethodView):

    def __init__(self):
        super().__init__()

    def get(self):
        """This method handles the registration route"""
        return jsonify({'message': 'Hello world'})


#  Define the views/resources
signup_view = SignUpView.as_view('signup_view')


# add a url to be used to reach the view
auth_blueprint.add_url_rule('/auth', view_func=signup_view, methods=['GET'])
