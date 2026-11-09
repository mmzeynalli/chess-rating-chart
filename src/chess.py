import json
from typing import TYPE_CHECKING

import asciichartpy as ac
import httpx

from env import EnvironmentManager as EM


class ChessManager:
    @classmethod
    def get_ratings_plot(cls):
        name, games = cls.get_data()

        return (
            f'{name} rating chart for the last {EM.LAST_N_GAMES} games:\n'
            + '\n```ascii\n'
            + ac.plot(games, {'height': EM.RATING_CHART_HEIGHT, 'format': '{:4.0f}'})
            + '\n```'
        )

    if TYPE_CHECKING:

        @classmethod
        def get_data(cls) -> tuple[str, list[int]]: ...


class ChessComManager(ChessManager):
    USERNAME = EM.CHESS_COM_USERNAME
    TIME_CLASS = EM.CHESS_COM_TIME_CLASS
    URL = f'https://api.chess.com/pub/player/{USERNAME}/games/archives'
    HEADERS = {'User-Agent': 'ChessRatingChart/1.0 miradil.zeynalli@gmail.com'}

    @classmethod
    def get_data(cls):
        if not cls.USERNAME:
            return

        archives = cls.get_archives()
        games = cls.get_filtered_games(archives)
        ratings = cls.get_ratings_from_games(games)

        return 'Chess.com', ratings

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


class LichessManager(ChessManager):
    USERNAME = EM.LICHESS_USERNAME
    TIME_CLASS = EM.LICHESS_TIME_CLASS
    URL = f'https://lichess.org/api/games/user/{USERNAME}?max={EM.LAST_N_GAMES}&pgn=false&moves=false&tags=false&pgnInJson=true&perfType={TIME_CLASS}'
    HEADERS = {
        'Accept': 'application/x-ndjson',
        'User-Agent': 'ChessRatingChart/1.0 (https://github.com/mmzeynalli/chess-rating-chart)',
    }
    if EM.LICHESS_TOKEN:
        HEADERS['Authorization'] = f'Bearer {EM.LICHESS_TOKEN}'

    @classmethod
    def get_data(cls):
        if not cls.USERNAME:
            return

        games = cls.get_filtered_games()
        ratings = cls.get_ratings_from_games(games)

        return 'Lichess', ratings

    @classmethod
    def get_filtered_games(cls) -> list:
        with httpx.Client(timeout=30) as client:
            response = client.get(url=cls.URL, headers=cls.HEADERS)

        if response.status_code != 200:
            raise RuntimeError(
                f'Lichess API returned HTTP {response.status_code} for {cls.URL}: '
                f'{response.text[:500]}'
            )

        games = []
        for line in response.content.splitlines():
            if not line.strip():
                continue
            data = json.loads(line)
            if 'players' not in data:
                print(f'Skipping unexpected Lichess response line: {str(data)[:200]}')
                continue
            games.append(data)

        return games

    @classmethod
    def get_ratings_from_games(cls, games: list) -> list:
        username = (cls.USERNAME or '').lower()
        ratings = []
        for game in games:
            for color in ('white', 'black'):
                player = game['players'].get(color, {})
                name = player.get('user', {}).get('name', '')
                if name.lower() == username and 'rating' in player:
                    ratings.append(player['rating'])
                    break
        return ratings
