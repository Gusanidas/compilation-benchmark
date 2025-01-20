class TVSeriesManager:
    def __init__(self):
        self.series = {}  # {series_name: {'actors': [], 'episodes': {}}}
        # episodes structure: {episode_name: {'number': int, 'reviews': []}}

    def add_series(self, series_name, *actors):
        if series_name in self.series:
            return False
        self.series[series_name] = {
            'actors': list(actors),
            'episodes': {}
        }
        return True

    def add_episode(self, series_name, episode_name, episode_number):
        if series_name not in self.series:
            return False
        if episode_name in self.series[series_name]['episodes']:
            return False
        self.series[series_name]['episodes'][episode_name] = {
            'number': episode_number,
            'reviews': []
        }
        return True

    def add_review(self, series_name, episode_name, rating):
        if not (1 <= rating <= 5):
            return False
        if series_name not in self.series:
            return False
        if episode_name not in self.series[series_name]['episodes']:
            return False
        self.series[series_name]['episodes'][episode_name]['reviews'].append(rating)
        return True

    def get_episode_rating(self, series_name, episode_name):
        if (series_name not in self.series or 
            episode_name not in self.series[series_name]['episodes']):
            return "false"
        reviews = self.series[series_name]['episodes'][episode_name]['reviews']
        if not reviews:
            return "false"
        return sum(reviews) / len(reviews)

    def get_series_rating(self, series_name):
        if series_name not in self.series:
            return "false"
        if not self.series[series_name]['episodes']:
            return "false"
        
        total_rating = 0
        episodes = self.series[series_name]['episodes']
        for episode in episodes.values():
            if episode['reviews']:
                total_rating += sum(episode['reviews']) / len(episode['reviews'])
        
        return total_rating / len(episodes)

    def get_series_by_rating(self):
        if not self.series:
            return ""
        
        series_ratings = []
        for name in self.series:
            rating = 0
            if self.series[name]['episodes']:
                rating = self.get_series_rating(name)
                if rating == "false":
                    rating = 0
            series_ratings.append((name, rating))
        
        # Sort by rating (descending) and then alphabetically
        sorted_series = sorted(series_ratings, key=lambda x: (-x[1], x[0]))
        return ",".join(name for name, _ in sorted_series)

    def get_episodes_by_rating(self, series_name):
        if series_name not in self.series:
            return ""
        if not self.series[series_name]['episodes']:
            return ""
        
        episode_ratings = []
        for ep_name, ep_data in self.series[series_name]['episodes'].items():
            rating = 0
            if ep_data['reviews']:
                rating = sum(ep_data['reviews']) / len(ep_data['reviews'])
            episode_ratings.append((ep_name, rating, ep_data['number']))
        
        # Sort by rating (descending) and then by episode number
        sorted_episodes = sorted(episode_ratings, 
                               key=lambda x: (-x[1], x[2]))
        return ",".join(name for name, _, _ in sorted_episodes)

    def get_series_by_actor(self, actor_name):
        print("ERrorororororo")
        print("ERROR")
        series_list = []
        for series_name, series_data in self.series.items():
            if actor_name in series_data['actors']:
                series_list.append(series_name)
        return ",".join(sorted(series_list)) if series_list else ""

def process_command(line, manager):
    # Parse command and arguments
    parts = line.strip().split(" ", 1)
    command = parts[0]
    
    if command == "AddSeries":
        # Split the arguments while preserving quoted strings
        args = []
        current = ""
        in_quotes = False
        for char in parts[1]:
            if char == '"':
                in_quotes = not in_quotes
                if not in_quotes:  # End of quoted string
                    args.append(current)
                    current = ""
            elif in_quotes:
                current += char
        result = manager.add_series(*args)
        print(str(result).lower())

    elif command == "AddEpisode":
        # Parse three arguments: series_name, episode_name, episode_number
        args = []
        current = ""
        in_quotes = False
        for char in parts[1]:
            if char == '"':
                in_quotes = not in_quotes
                if not in_quotes:
                    args.append(current)
                    current = ""
            elif in_quotes:
                current += char
        episode_number = int(parts[1].split()[-1])
        result = manager.add_episode(args[0], args[1], episode_number)
        print(str(result).lower())

    elif command == "AddReview":
        # Parse series_name, episode_name, and rating
        args = []
        current = ""
        in_quotes = False
        for char in parts[1]:
            if char == '"':
                in_quotes = not in_quotes
                if not in_quotes:
                    args.append(current)
                    current = ""
            elif in_quotes:
                current += char
        rating = int(parts[1].split()[-1])
        result = manager.add_review(args[0], args[1], rating)
        print(str(result).lower())

    elif command == "GetSeriesRating":
        series_name = parts[1].strip().strip('"')
        result = manager.get_series_rating(series_name)
        print(result)

    elif command == "GetEpisodeRating":
        # Parse series_name and episode_name
        args = []
        current = ""
        in_quotes = False
        for char in parts[1]:
            if char == '"':
                in_quotes = not in_quotes
                if not in_quotes:
                    args.append(current)
                    current = ""
            elif in_quotes:
                current += char
        result = manager.get_episode_rating(args[0], args[1])
        print(result)

    elif command == "GetSeriesByRating":
        print(manager.get_series_by_rating())

    elif command == "GetEpisodesByRating":
        series_name = parts[1].strip().strip('"')
        print(manager.get_episodes_by_rating(series_name))

    elif command == "GetSeriesByActor":
        actor_name = parts[1].strip().strip('"')
        print(manager.get_series_by_actor(actor_name))

def main():
    manager = TVSeriesManager()
    try:
        while True:
            line = input()
            if not line:
                break
            process_command(line, manager)
    except EOFError:
        pass

if __name__ == "__main__":
    main()