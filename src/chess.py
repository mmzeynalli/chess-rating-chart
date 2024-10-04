import json

import asciichartpy as ac
import httpx
from env import EnvironmentManager as EM


class ChessComManager:
    USERNAME = EM.CHESS_COM_USERNAME
    TIME_CLASS = EM.CHESS_COM_TIME_CLASS
    URL = f'https://api.chess.com/pub/player/{USERNAME}/games/archives'
    HEADERS = {'User-Agent': 'ChessRatingChart/1.0 miradil.zeynalli@gmail.com'}

    @classmethod
    def get_ratings_plot(cls):
        if not cls.USERNAME:
            return

        archives = cls.get_archives()
        games = cls.get_filtered_games(archives)
        ratings = cls.get_ratings_from_games(games)

        return f'Chess.com rating chart for the last {EM.LAST_N_GAMES} games:\n\n' + ac.plot(
            ratings, {'height': EM.RATING_CHART_HEIGHT}
        )

    @classmethod
    def get_archives(cls):
        with httpx.Client(timeout=10) as client:
            archives_dict = client.get(url=cls.URL, headers=cls.HEADERS).json()

        monthly_archives = archives_dict.get('archives', [])
        return monthly_archives[::-1]

    @classmethod
    def get_filtered_games(cls, archive_urls: list[str]) -> list:
        games: list[dict] = []

        with httpx.Client(timeout=10) as client:
            for archive in archive_urls:
                if len(games) >= EM.LAST_N_GAMES:
                    break

                games_dict = (
                    client.get(
                        url=archive,
                        headers=cls.HEADERS,
                    )
                ).json()

                monthly_games = games_dict.get('games', [])

                games.extend(
                    list(
                        filter(
                            lambda game: game['time_class'] == cls.TIME_CLASS
                            and game['rules'] == EM.CHESS_TYPE,
                            monthly_games,
                        )
                    )
                )

        return games[: EM.LAST_N_GAMES][::-1]

    @classmethod
    def get_ratings_from_games(cls, games: list) -> list:
        return [
            game['white']['rating']
            if game['white']['username'] == cls.USERNAME
            else game['black']['rating']
            for game in games
        ][::-1]


class LichessManager:
    USERNAME = EM.LICHESS_USERNAME
    TIME_CLASS = EM.LICHESS_TIME_CLASS
    URL = f'https://lichess.org/api/games/user/{USERNAME}?max={EM.LAST_N_GAMES}&png=false&moves=false&tags=false&pgnInJson=true&perfType={TIME_CLASS},{EM.CHESS_TYPE}'
    HEADERS = {'Accept': 'application/x-ndjson'}

    @classmethod
    def get_ratings_plot(cls):
        if not cls.USERNAME:
            return

        games = cls.get_filtered_games()
        ratings = cls.get_ratings_from_games(games)

        return f'Lichess rating chart for the last {EM.LAST_N_GAMES} games:\n\n' + ac.plot(
            ratings, {'height': EM.RATING_CHART_HEIGHT}
        )

    @classmethod
    def get_filtered_games(cls) -> list:
        with httpx.Client(timeout=10) as client:
            ndjson_data = (client.get(url=cls.URL, headers=cls.HEADERS)).content

        return [json.loads(line) for line in ndjson_data.splitlines()]

    @classmethod
    def get_ratings_from_games(cls, games: list) -> list:
        return [
            game['players']['white']['rating']
            if game['players']['white']['user']['name'] == cls.USERNAME
            else game['players']['black']['rating']
            for game in games
        ]
