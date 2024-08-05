from voltron.pages.shared.components.base import ComponentBase
from collections import OrderedDict

from voltron.pages.shared.components.primitives.buttons import ButtonBase


class AnswerOptions(ComponentBase):
    _item = 'xpath=.//*[@class="answer-option"]'

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            name = item_we.get_attribute('innerText')
            items_ordered_dict.update({name: item_we})
        return items_ordered_dict


class FreeRideOverlay(ComponentBase):
    _welcome_message = 'xpath=.//*[@class="question"]'
    _first_question = 'xpath=.//*[@class="question" and @id="1"]'
    _second_question = 'xpath=.//*[@class="question" and @id="2"]'
    _third_question = 'xpath=.//*[@class="question" and @id="3"]'
    _answer_options = 'xpath=.//*[@class="stepCount"]//following-sibling::div[@class="optionContainer"]'
    _first_selected_answer = 'xpath=.//*[@class="answer" and @id="1"]'
    _second_selected_answer = 'xpath=.//*[@class="answer" and @id="4"]'
    _third_selected_answer = 'xpath=.//*[@class="answer" and @id="7"]'
    _chat_bot_response_one = 'xpath=.//*[@class="answer" and @id="1"] //following-sibling::div[@class="question"][1]'
    _chat_bot_response_two = 'xpath=.//*[@class="answer" and @id="4"] //following-sibling::div[@class="question"][1]'
    _chat_bot_response_three = 'xpath=.//*[@class="answer" and @id="7"] //following-sibling::div[@class="question"][1]'
    _close_icon = 'xpath=.//*[@class="closebtn"]'
    _results_container = 'xpath=.//*[@class="resultContainer"]'
    _summary = 'xpath=.//*[@class="summary"]'
    _jockey_logo = 'xpath=.//*[@class="resultImg"]/div[@class="silk-img"]'
    _CTA_Go_racing_button = 'xpath=.//*[@class="ctaContainer"]/button[@class="ctaBtn"]'

    @property
    def welcome_message(self):
        return self._get_webelement_text(self._welcome_message, timeout=5)

    @property
    def first_question(self):
        return self._get_webelement_text(self._first_question, timeout=5)

    @property
    def second_question(self):
        return self._get_webelement_text(self._second_question, timeout=5)

    @property
    def third_question(self):
        return self._get_webelement_text(self._third_question, timeout=5)

    @property
    def answers(self):
        return AnswerOptions(selector=self._answer_options, timeout=5)

    @property
    def first_selected_answer(self):
        return self._get_webelement_text(self._first_selected_answer, timeout=5)

    @property
    def second_selected_answer(self):
        return self._get_webelement_text(self._second_selected_answer, timeout=5)

    @property
    def third_selected_answer(self):
        return self._get_webelement_text(self._third_selected_answer, timeout=5)

    @property
    def chat_bot_response_one(self):
        return self._get_webelement_text(self._chat_bot_response_one, timeout=5)

    @property
    def chat_bot_response_two(self):
        return self._get_webelement_text(self._chat_bot_response_two, timeout=5)

    @property
    def chat_bot_response_three(self):
        return self._get_webelement_text(self._chat_bot_response_three, timeout=5)

    @property
    def close_icon(self):
        return self._find_element_by_selector(selector=self._close_icon, timeout=2)

    @property
    def results_container(self):
        return self._get_webelement_text(selector=self._results_container, timeout=5)

    @property
    def summary(self):
        return self._get_webelement_text(selector=self._summary, timeout=5)

    @property
    def jockey_logo(self):
        return self._find_element_by_selector(selector=self._jockey_logo, timeout=5)

    @property
    def CTA_button(self):
        return ButtonBase(selector=self._CTA_Go_racing_button, timeout=5)
