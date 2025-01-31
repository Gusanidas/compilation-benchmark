from typing import List, Dict, Set, Tuple
from statistics import mean
from collections import defaultdict

class Episode:
    def __init__(self, name: str, number: int, actors: List[str]):
        self.name = name
        self.number = number
        self.actors = set(actors)
        self.ratings: List[int] = []

    def add_rating(self, rating: int) -> bool:
        if 1 <= rating <= 5:
            self.ratings.append(rating)
            return True
        return False

    def get_average_rating(self) -> float:
        return mean(self.ratings) if self.ratings else 0

    def remove_actor(self, actor: str) -> bool:
        if actor in self.actors:
            self.actors.remove(actor)
            return True
        return False

class Series:
    def __init__(self, name: str):
        self.name = name
        self.episodes: Dict[str, Episode] = {}

    def add_episode(self, name: str, number: int, actors: List[str]) -> bool:
        if name in self.episodes:
            return False
        self.episodes[name] = Episode(name, number, actors)
        return True

    def get_average_rating(self) -> float:
        if not self.episodes:
            return 0
        return mean(episode.get_average_rating() for episode in self.episodes.values())

    def get_actors(self) -> Set[str]:
        actors = set()
        for episode in self.episodes.values():
            actors.update(episode.actors)
        return actors

class TVSeriesDatabase:
    def __init__(self):
        self.series: Dict[str, Series] = {}
        self.actor_to_series: Dict[str, Set[str]] = defaultdict(set)

    def add_series(self, series_name: str) -> bool:
        if series_name in self.series:
            return False
        self.series[series_name] = Series(series_name)
        return True

    def add_episode(self, series_name: str, episode_name: str, 
                   episode_number: int, actors: List[str]) -> bool:
        if series_name not in self.series:
            return False
        
        # Update actor_to_series mapping
        if self.series[series_name].add_episode(episode_name, episode_number, actors):
            for actor in actors:
                self.actor_to_series[actor].add(series_name)
            return True
        return False

    def add_review(self, series_name: str, episode_name: str, rating: int) -> bool:
        if (series_name not in self.series or 
            episode_name not in self.series[series_name].episodes):
            return False
        return self.series[series_name].episodes[episode_name].add_rating(rating)

    def get_series_rating(self, series_name: str) -> str:
        if series_name not in self.series:
            return "false"
        rating = self.series[series_name].get_average_rating()
        return str(rating) if rating > 0 else "false"

    def get_episode_rating(self, series_name: str, episode_name: str) -> str:
        if (series_name not in self.series or 
            episode_name not in self.series[series_name].episodes):
            return "false"
        rating = self.series[series_name].episodes[episode_name].get_average_rating()
        return str(rating) if rating > 0 else "false"

    def get_series_by_rating(self) -> str:
        if not self.series:
            return ""
        sorted_series = sorted(
            self.series.values(),
            key=lambda x: (-x.get_average_rating(), x.name)
        )
        r =  ",".join(series.name for series in sorted_series)
        return r

    def get_episodes_by_rating(self, series_name: str) -> str:
        if series_name not in self.series or not self.series[series_name].episodes:
            return ""
        episodes = self.series[series_name].episodes
        sorted_episodes = sorted(
            episodes.values(),
            key=lambda x: (-x.get_average_rating(), x.number)
        )
        return ",".join(episode.name for episode in sorted_episodes)

    def get_series_by_actor(self, actor_name: str) -> str:
        return ",".join(sorted(self.actor_to_series.get(actor_name, set())))

    def get_actors_by_series(self, series_name: str) -> str:
        if series_name not in self.series:
            return ""
        return ",".join(sorted(self.series[series_name].get_actors()))

    def remove_actor_from_episode(self, series_name: str, episode_name: str, 
                                actor_name: str) -> bool:
        if (series_name not in self.series or 
            episode_name not in self.series[series_name].episodes):
            return False
        
        episode = self.series[series_name].episodes[episode_name]
        if episode.remove_actor(actor_name):
            # Remove series from actor's list if they're no longer in any episodes
            if actor_name not in self.series[series_name].get_actors():
                self.actor_to_series[actor_name].remove(series_name)
                if not self.actor_to_series[actor_name]:
                    del self.actor_to_series[actor_name]
            return True
        return False

def parse_command(line: str) -> Tuple[str, List[str]]:
    """Parse a command line into command and arguments."""
    parts = []
    current = []
    in_quotes = False
    
    for char in line:
        if char == '"':
            if in_quotes:
                parts.append(''.join(current))
                current = []
            in_quotes = not in_quotes
        elif in_quotes:
            current.append(char)
        elif char.isspace():
            if current:
                parts.append(''.join(current))
                current = []
        else:
            current.append(char)
    
    if current:
        parts.append(''.join(current))
    
    if not parts:
        return "", []
        
    return parts[0], parts[1:]

def main():
    db = TVSeriesDatabase()
    while True:
        try:
            line = input().strip()
            command, args = parse_command(line)

            if command == "AddSeries":
                if len(args) != 1:  # Check correct number of arguments
                    print("false")
                    continue
                print(str(db.add_series(args[0])).lower())
                
            elif command == "AddEpisode":
                if len(args) < 4:  # Need at least series, episode, number, and one actor
                    print("false")
                    continue
                series_name, episode_name = args[0], args[1]
                try:
                    episode_number = int(args[2])
                    actors = args[3:]
                    print(str(db.add_episode(series_name, episode_name, episode_number, actors)).lower())
                except ValueError as e:
                    print("false")
                    
            elif command == "AddReview":
                if len(args) != 3:  # Need series, episode, and rating
                    print("false")
                    continue
                try:
                    rating = int(args[2])
                    print(str(db.add_review(args[0], args[1], rating)).lower())
                except ValueError:
                    print("false")
                    
            elif command == "GetSeriesRating":
                if len(args) != 1:
                    print("false")
                    continue
                print(db.get_series_rating(args[0]))
                
            elif command == "GetEpisodeRating":
                if len(args) != 2:
                    print("false")
                    continue
                print(db.get_episode_rating(args[0], args[1]))
                
            elif command == "GetSeriesByRating":
                if args:  # Should have no arguments
                    print("false")
                    continue
                print(db.get_series_by_rating())
                
            elif command == "GetEpisodesByRating":
                if len(args) != 1:
                    print("false")
                    continue
                print(db.get_episodes_by_rating(args[0]))
                
            elif command == "GetSeriesByActor":
                if len(args) != 1:
                    print("false")
                    continue
                print(db.get_series_by_actor(args[0]))
                
            elif command == "GetActorsBySeries":
                if len(args) != 1:
                    print("false")
                    continue
                print(db.get_actors_by_series(args[0]))
                
            elif command == "RemoveActorFromEpisode":
                if len(args) != 3:
                    print("false")
                    continue
                print(str(db.remove_actor_from_episode(args[0], args[1], args[2])).lower())
            
            else:
                print("false")

        except EOFError:
            break
        except Exception as e:
            print("false")

if __name__ == "__main__":
    main()