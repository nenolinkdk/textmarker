from enum import Enum

class State(Enum): IDLE='IDLE'; FILES_READY='FILES_READY'; VALIDATING='VALIDATING'; READY='READY'; PROCESSING='PROCESSING'; COMPLETED='COMPLETED'; FAILED='FAILED'; CANCELLED='CANCELLED'

class Workflow:
    def __init__(self): self.state=State.IDLE
    def event(self,event):
        transitions={
            (State.IDLE,'files'):State.FILES_READY,(State.FILES_READY,'validate'):State.VALIDATING,
            (State.VALIDATING,'ok'):State.READY,(State.VALIDATING,'fail'):State.FAILED,
            (State.READY,'start'):State.PROCESSING,(State.PROCESSING,'progress'):State.PROCESSING,
            (State.PROCESSING,'complete'):State.COMPLETED,(State.PROCESSING,'fail'):State.FAILED,
            (State.PROCESSING,'cancel'):State.CANCELLED,
        }
        if event=='reset' and self.state in {State.COMPLETED,State.FAILED,State.CANCELLED}: self.state=State.IDLE; return self.state
        key=(self.state,event)
        if key not in transitions: raise ValueError(f"Ugyldig hændelse {event} i {self.state.value}")
        self.state=transitions[key]; return self.state
