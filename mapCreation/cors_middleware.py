class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_origins = ['http://127.0.0.1:8000']

    def __call__(self, request):
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    def process_response(self, request, response):
        if request.method == 'OPTIONS':
            response['Access-Control-Allow-Origin'] = ', '.join(self.allowed_origins)
            response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
        elif request.headers.get('Origin') in self.allowed_origins:
            response['Access-Control-Allow-Origin'] = request.headers.get('Origin')
            response['Access-Control-Allow-Credentials'] = 'true'
        return response