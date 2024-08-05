
class UnexpectedStatusCode(Exception):
    def __init__(self, environment, backend, status_code, content):
        message = '{0} {1} respond with unexpected status code {2}. Content is:\n{3}' \
            .format(environment, backend, status_code, content)
        super(UnexpectedStatusCode, self).__init__(message)


class UnexpectedContent(Exception):
    def __init__(self, environment, backend, data):
        message = '{0} {1} respond with unexpected content:\n{2}' \
            .format(environment, backend, data)
        super(UnexpectedContent, self).__init__(message)

class UnexpectedRedirection(Exception):
    def __init__(self, environment, backend, status_code, data):
        message = '{0} {1} respond with status code "{2}" unexpected redirection:\n{3}' \
            .format(environment, backend, status_code, data)
        super(UnexpectedRedirection, self).__init__(message)