from aiogram.fsm.state import State, StatesGroup

class HrWait(StatesGroup):
    InputState=State()

class AddStates(StatesGroup):
    add = State()
    wait_answer = State()
    
class EditStates(StatesGroup):
    old_question = State()
    new_question = State()
    waiting_answer = State()

class DeleteStates(StatesGroup):
    delete = State()