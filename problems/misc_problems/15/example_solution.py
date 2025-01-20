from dataclasses import dataclass
from typing import Dict, List, Set, Tuple
import sys

@dataclass
class Participant:
    name: str
    id: int

@dataclass
class Event:
    name: str
    id: int

@dataclass
class Assignment:
    participant_id: int
    event_id: int
    start_time: int
    end_time: int

class EventManagementSystem:
    def __init__(self):
        self.participants: Dict[int, Participant] = {}
        self.events: Dict[int, Event] = {}
        self.assignments: List[Assignment] = []

    def add_participant(self, name: str, id: int) -> bool:
        if id in self.participants:
            return False
        self.participants[id] = Participant(name, id)
        return True

    def add_event(self, name: str, id: int) -> bool:
        if id in self.events:
            return False
        self.events[id] = Event(name, id)
        return True

    def assign_participant_to_event(self, participant_id: int, event_id: int, 
                                  start_time: int, end_time: int) -> bool:
        # Validate participant and event exist
        if (participant_id not in self.participants or 
            event_id not in self.events):
            return False

        # Validate timestamps
        if start_time >= end_time:
            return False

        self.assignments.append(Assignment(participant_id, event_id, 
                                        start_time, end_time))
        return True

    def get_all_events_for_participant(self, participant_id: int) -> str:
        if participant_id not in self.participants:
            return ""

        event_ids = set(
            assignment.event_id 
            for assignment in self.assignments 
            if assignment.participant_id == participant_id
        )
        
        return ",".join(str(id) for id in sorted(event_ids)) if event_ids else ""

    def get_all_participants_for_event(self, event_id: int, timestamp: int) -> str:
        if event_id not in self.events:
            return ""

        participant_ids = set(
            assignment.participant_id 
            for assignment in self.assignments 
            if (assignment.event_id == event_id and 
                assignment.start_time <= timestamp < assignment.end_time)
        )
        
        return ",".join(str(id) for id in sorted(participant_ids)) if participant_ids else ""

def main():
    system = EventManagementSystem()
    
    for line in sys.stdin:
        command = line.strip().split()
        
        if not command:
            continue
            
        if command[0] == "AddParticipant":
            result = system.add_participant(command[1], int(command[2]))
            print(str(result).lower())
            
        elif command[0] == "AddEvent":
            result = system.add_event(command[1], int(command[2]))
            print(str(result).lower())
            
        elif command[0] == "AssignParticipantToEvent":
            result = system.assign_participant_to_event(
                int(command[1]), int(command[2]), 
                int(command[3]), int(command[4])
            )
            print(str(result).lower())
            
        elif command[0] == "GetAllEventsForParticipant":
            result = system.get_all_events_for_participant(int(command[1]))
            print(result)
            
        elif command[0] == "GetAllParticipantsForEvent":
            result = system.get_all_participants_for_event(
                int(command[1]), int(command[2])
            )
            print(result)

if __name__ == "__main__":
    main()