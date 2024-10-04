from os import environ, getenv


class EnvironmentManager:
    _TRUTHY = ['true', '1', 't', 'y', 'yes']

    GH_TOKEN = environ['INPUT_GH_TOKEN']

    CHESS_COM_USERNAME = getenv('INPUT_CHESS_COM_USERNAME')
    CHESS_COM_TIME_CLASS = getenv('INPUT_CHESS_COM_TIME_CLASS', 'blitz')
    LICHESS_USERNAME = getenv('INPUT_LICHESS_USERNAME')
    LICHESS_TIME_CLASS = getenv('INPUT_LICHESS_TIME_CLASS', 'blitz')

    CHESS_TYPE = getenv('INPUT_CHESS_TYPE', 'chess')
    LAST_N_GAMES = int(getenv('INPUT_LAST_N_GAMES', 100))
    RATING_CHART_HEIGHT = int(getenv('INPUT_RATING_CHART_HEIGHT', 20))

    PUSH_BRANCH_NAME = getenv('INPUT_PUSH_BRANCH_NAME', '')

    COMMIT_BY_ME = getenv('INPUT_COMMIT_BY_ME', 'False').lower() in _TRUTHY
    COMMIT_MESSAGE = getenv('INPUT_COMMIT_MESSAGE', 'Updated the chess rating graph')

    DEBUG_LOGGING = getenv('INPUT_DEBUG_LOGGING', 'False').lower() in _TRUTHY
    DEBUG_RUN = getenv('DEBUG_RUN', 'False').lower() in _TRUTHY
