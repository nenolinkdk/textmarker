import pytest
from textmarker.prompt_builder.fsm import PromptBuilderFSM, PromptState
from textmarker.prompt_builder.store import PromptStore

def complete(fsm):
    fsm.transition('task_selected','terminology_consistency'); fsm.transition('languages_selected',('en','da')); fsm.transition('domain_selected','legal'); fsm.transition('criteria_saved','preserve terminology'); fsm.transition('output_selected','structured review')

def test_fsm_valid_flow_back_reset_and_guards():
    fsm=PromptBuilderFSM(); assert fsm.transition('languages_selected',('en','da'))==PromptState.SELECT_TASK and fsm.error
    complete(fsm); assert fsm.state==PromptState.PREVIEW and 'Do not invent' in fsm.data.prompt_text
    assert fsm.transition('back')==PromptState.SELECT_OUTPUT; assert fsm.transition('reset')==PromptState.SELECT_TASK

def test_fsm_edit_save_and_unicode():
    fsm=PromptBuilderFSM(); complete(fsm); assert fsm.edit_prompt('Åbn kun kildeteksten.'); assert fsm.transition('save')==PromptState.SAVED; assert fsm.data.prompt_text.startswith('Åbn')

def test_prompt_store_crud_search_duplicate_export(tmp_path):
    store=PromptStore(tmp_path/'prompts.json'); item=store.create('Review','translation_risk','Confidential'); assert store.get(item.prompt_id)==item; copy=store.duplicate(item.prompt_id); assert len(store.list('review'))==2; out=store.export_text(copy.prompt_id,tmp_path/'prompt.txt'); assert out.read_text()=='Confidential'; store.delete(item.prompt_id); assert len(store.list())==1
