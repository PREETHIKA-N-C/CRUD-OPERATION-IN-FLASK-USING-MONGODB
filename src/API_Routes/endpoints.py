from flask import request, render_template


def api_routes(endpoints):
    @endpoints.route('/Hello World', methods=['GET'])
    def hello():
        res = 'Hello World!!'
        return res

    return endpoints
