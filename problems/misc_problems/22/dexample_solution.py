import sys
import shlex

def average_rating(ratings):
    if not ratings:
        return None  # No reviews
    return sum(ratings) / len(ratings)

def get_series_rating(series_data):
    episodes = series_data["episodes"]
    if not episodes:
        # No episodes means "false"
        return "false"
    # Average rating of all episodes:
    # If an episode has no reviews, it counts as 0
    total = 0.0
    count = 0
    for ep_name, ep_data in episodes.items():
        if ep_data["reviews"]:
            ep_avg = sum(ep_data["reviews"]) / len(ep_data["reviews"])
        else:
            ep_avg = 0
        total += ep_avg
        count += 1
    if count == 0:
        return "false"
    return str(total / count)

def get_episode_rating(series_data, episode_name):
    episodes = series_data["episodes"]
    if episode_name not in episodes:
        return "false"
    reviews = episodes[episode_name]["reviews"]
    if not reviews:
        return "false"
    return str(sum(reviews) / len(reviews))

def get_series_by_rating(series_db):
    # Returns comma-separated series names, sorted by descending average rating
    # If tie in rating, alphabetical
    if not series_db:
        return ""
    series_ratings = []
    for s_name, s_data in series_db.items():
        # Compute series rating (0 if no episodes)
        eps = s_data["episodes"]
        if not eps:
            # No episodes => rating 0
            rating = 0.0
        else:
            # Average of episodes (0 for episodes w/o reviews)
            total = 0.0
            count = 0
            for epd in eps.values():
                if epd["reviews"]:
                    avg_ep = sum(epd["reviews"]) / len(epd["reviews"])
                else:
                    avg_ep = 0
                total += avg_ep
                count += 1
            if count == 0:
                rating = 0.0
            else:
                rating = total / count
        series_ratings.append((rating, s_name))
    # Sort by rating desc, name asc if tie
    series_ratings.sort(key=lambda x: (-x[0], x[1]))
    return ",".join([x[1] for x in series_ratings])

def get_episodes_by_rating(series_data):
    episodes = series_data["episodes"]
    if not episodes:
        return ""
    ep_list = []
    for ep_name, ep_data in episodes.items():
        if ep_data["reviews"]:
            ep_rating = sum(ep_data["reviews"]) / len(ep_data["reviews"])
        else:
            ep_rating = 0
        ep_list.append((ep_rating, ep_data["number"], ep_name))
    # Sort by rating desc, if tie by episode number asc
    ep_list.sort(key=lambda x: (-x[0], x[1]))
    return ",".join([x[2] for x in ep_list])

def get_series_by_actor(series_db, actor):
    # All series that contain the actor
    result = []
    for s_name, s_data in series_db.items():
        if actor in s_data["actors"]:
            result.append(s_name)
    result.sort()  # alphabetical
    return ",".join(result)

def main():
    series_db = {}

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        # Parse with shlex to handle quotes properly
        args = shlex.split(line)
        if not args:
            continue

        cmd = args[0]

        if cmd == "AddSeries":
            # Format: AddSeries series_name actor1 actor2 ...
            # Returns "true" if added, "false" if already exists
            series_name = args[1]
            actors = args[2:]
            if series_name in series_db:
                print("false")
            else:
                series_db[series_name] = {
                    "actors": actors,
                    "episodes": {}
                }
                print("true")

        elif cmd == "AddEpisode":
            # Format: AddEpisode series_name episode_name episode_number
            series_name = args[1]
            episode_name = args[2]
            try:
                episode_number = int(args[3])
            except ValueError:
                print("false")
                continue
            if series_name not in series_db:
                print("false")
            else:
                if episode_name in series_db[series_name]["episodes"]:
                    # episode already exists
                    print("false")
                else:
                    series_db[series_name]["episodes"][episode_name] = {
                        "number": episode_number,
                        "reviews": []
                    }
                    print("true")

        elif cmd == "AddReview":
            # Format: AddReview series_name episode_name rating
            series_name = args[1]
            episode_name = args[2]
            try:
                rating = int(args[3])
            except ValueError:
                print("false")
                continue
            if rating < 1 or rating > 5:
                print("false")
                continue
            if series_name not in series_db:
                print("false")
            else:
                if episode_name not in series_db[series_name]["episodes"]:
                    print("false")
                else:
                    series_db[series_name]["episodes"][episode_name]["reviews"].append(rating)
                    print("true")

        elif cmd == "GetSeriesRating":
            # Format: GetSeriesRating series_name
            series_name = args[1]
            if series_name not in series_db:
                print("false")
            else:
                print(get_series_rating(series_db[series_name]))

        elif cmd == "GetEpisodeRating":
            # Format: GetEpisodeRating series_name episode_name
            series_name = args[1]
            episode_name = args[2]
            if series_name not in series_db:
                print("false")
            else:
                print(get_episode_rating(series_db[series_name], episode_name))

        elif cmd == "GetSeriesByRating":
            # no additional args
            print(get_series_by_rating(series_db))

        elif cmd == "GetEpisodesByRating":
            # Format: GetEpisodesByRating series_name
            series_name = args[1]
            if series_name not in series_db:
                print("")
            else:
                print(get_episodes_by_rating(series_db[series_name]))

        elif cmd == "GetSeriesByActor":
            # Format: GetSeriesByActor actor_name
            actor_name = args[1]
            print(get_series_by_actor(series_db, actor_name))

        else:
            # Unknown command
            print("false")

if __name__ == "__main__":
    main()
