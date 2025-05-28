def application(environ, start_response):
    from urllib.parse import parse_qs
    method = environ['REQUEST_METHOD']
    if method == 'GET':
        params = parse_qs(environ['QUERY_STRING'])
    elif method == 'POST':
        try:
            size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            size = 0
        body = environ['wsgi.input'].read(size).decode()
        params = parse_qs(body)
    else:
        params = {}

    response_body = "Received parameters:\n"
    for key, value in params.items():
        response_body += f"{key}: {value}\n"

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return [response_body.encode('utf-8')]
