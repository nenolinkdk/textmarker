import pytest
from textmarker.application.fsm import State, Workflow

def test_workflow_happy_path():
    w=Workflow()
    for e in ('files','validate','ok','start','progress','complete'): w.event(e)
    assert w.state is State.COMPLETED

def test_workflow_rejects_illegal_event():
    with pytest.raises(ValueError): Workflow().event('start')

def test_cancel_is_normal_terminal_state():
    w=Workflow(); w.state=State.PROCESSING; assert w.event('cancel') is State.CANCELLED; assert w.event('reset') is State.IDLE
