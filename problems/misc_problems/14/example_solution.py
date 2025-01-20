class Participant:
    def __init__(self, name, id, height):
        self.name = name
        self.id = id
        self.height = height

class Event:
    def __init__(self, name, id, price):
        self.name = name
        self.id = id
        self.price = price

class EventManagementSystem:
    def __init__(self):
        self.participants = {}  # id -> Participant
        self.events = {}        # id -> Event
        self.participant_events = {}  # participant_id -> set of event_ids
        self.event_participants = {}  # event_id -> set of participant_ids

    def add_participant(self, name, participant_id, height):
        """Add a new participant to the system."""
        if participant_id in self.participants:
            return "false"
        self.participants[participant_id] = Participant(name, participant_id, height)
        self.participant_events[participant_id] = set()
        return "true"

    def remove_participant(self, participant_id):
        """Remove a participant from the system."""
        if participant_id not in self.participants:
            return "false"
        
        # Remove participant from all their events
        for event_id in self.participant_events[participant_id]:
            self.event_participants[event_id].remove(participant_id)
            
        # Clean up participant data
        del self.participants[participant_id]
        del self.participant_events[participant_id]
        return "true"

    def add_event(self, name, event_id, price):
        """Add a new event to the system."""
        if event_id in self.events:
            return "false"
        self.events[event_id] = Event(name, event_id, price)
        self.event_participants[event_id] = set()
        return "true"

    def remove_event(self, event_id):
        """Remove an event from the system."""
        if event_id not in self.events:
            return "false"
        
        # Remove event from all participants' lists
        for participant_id in self.event_participants[event_id]:
            self.participant_events[participant_id].remove(event_id)
            
        # Clean up event data
        del self.events[event_id]
        del self.event_participants[event_id]
        return "true"

    def assign_participant_to_event(self, participant_id, event_id):
        """Assign a participant to an event."""
        if participant_id not in self.participants or event_id not in self.events:
            return "false"
        
        self.participant_events[participant_id].add(event_id)
        self.event_participants[event_id].add(participant_id)
        return "true"

    def get_all_events_for_participant(self, participant_id):
        """Get all events for a participant."""
        if participant_id not in self.participants:
            return ""
        events = sorted(self.participant_events[participant_id])
        return ",".join(str(event_id) for event_id in events)

    def get_all_participants_for_event(self, event_id):
        """Get all participants for an event."""
        if event_id not in self.events:
            return ""
        participants = sorted(self.event_participants[event_id])
        return ",".join(str(participant_id) for participant_id in participants)

    def find_cheapest_event_for_participant(self, participant_id):
        """Find the cheapest event attended by a participant."""
        if participant_id not in self.participants:
            return "none"
        
        events = self.participant_events[participant_id]
        if not events:
            return "none"
            
        cheapest_event = min(
            events,
            key=lambda event_id: self.events[event_id].price
        )
        return str(cheapest_event)

    def find_average_height_for_event(self, event_id):
        """Find the average height of participants for an event."""
        if event_id not in self.events:
            return "0"
            
        participants = self.event_participants[event_id]
        if not participants:
            return "0"
            
        heights = [self.participants[p_id].height for p_id in participants]
        avg_height = round(sum(heights) / len(heights))
        return str(avg_height)

def main():
    system = EventManagementSystem()
    
    while True:
        try:
            command = input().strip()
            if not command:
                break
                
            parts = command.split()
            
            if parts[0] == "AddParticipant":
                print(system.add_participant(parts[1], int(parts[2]), float(parts[3])))
            elif parts[0] == "RemoveParticipant":
                print(system.remove_participant(int(parts[1])))
            elif parts[0] == "AddEvent":
                print(system.add_event(parts[1], int(parts[2]), float(parts[3])))
            elif parts[0] == "RemoveEvent":
                print(system.remove_event(int(parts[1])))
            elif parts[0] == "AssignParticipantToEvent":
                print(system.assign_participant_to_event(int(parts[1]), int(parts[2])))
            elif parts[0] == "GetAllEventsForParticipant":
                print(system.get_all_events_for_participant(int(parts[1])))
            elif parts[0] == "GetAllParticipantsForEvent":
                print(system.get_all_participants_for_event(int(parts[1])))
            elif parts[0] == "FindCheapestEventForParticipant":
                print(system.find_cheapest_event_for_participant(int(parts[1])))
            elif parts[0] == "FindAverageHeightForEvent":
                print(system.find_average_height_for_event(int(parts[1])))
            else:
                print("false")
                
        except EOFError:
            break
        except (IndexError, ValueError):
            print("false")

if __name__ == "__main__":
    main()