from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # We are writing this becoz we want to change the default response format of our API
        # We want to wrap our response data in a custom format like this:
        # {
        #   "status": "success",
        #   "data": {
        #     "id": 1,
        #     "email": "
        response = ''
        if 'Errordetail' in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps(data)
            
        return response
        