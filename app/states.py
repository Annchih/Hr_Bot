from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class HrWait(StatesGroup):
    InputState=State()
    