class EventManagementSystem:
    def __init__(self):
        self.participants = {}  # id -> name
        self.events = {}        # id -> name
        self.participant_events = {}  # participant_id -> set of event_ids
        self.event_participants = {}  # event_id -> set of participant_ids

    def add_participant(self, name, participant_id):
        """Add a new participant to the system."""
        if participant_id in self.participants:
            return "false"
        self.participants[participant_id] = name
        self.participant_events[participant_id] = set()
        return "true"

    def add_event(self, name, event_id):
        """Add a new event to the system."""
        if event_id in self.events:
            return "false"
        self.events[event_id] = name
        self.event_participants[event_id] = set()
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

def main():
    system = EventManagementSystem()
    
    while True:
        try:
            command = input().strip()
            if not command:
                break
                
            parts = command.split()
            
            if parts[0] == "AddParticipant":
                print(system.add_participant(parts[1], int(parts[2])))
            elif parts[0] == "AddEvent":
                print(system.add_event(parts[1], int(parts[2])))
            elif parts[0] == "AssignParticipantToEvent":
                print(system.assign_participant_to_event(int(parts[1]), int(parts[2])))
            elif parts[0] == "GetAllEventsForParticipant":
                print(system.get_all_events_for_participant(int(parts[1])))
            elif parts[0] == "GetAllParticipantsForEvent":
                print(system.get_all_participants_for_event(int(parts[1])))
            else:
                print("false")
                
        except EOFError:
            break
        except (IndexError, ValueError):
            print("false")

if __name__ == "__main__":
    main()