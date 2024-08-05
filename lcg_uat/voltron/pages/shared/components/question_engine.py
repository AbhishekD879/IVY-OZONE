from collections import OrderedDict
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.utils.waiters import wait_for_result


class QuickLinksPage(ComponentBase):
    _back_button = 'xpath=.//*[@class="qe-btn-back-svg"] | //*[@class="btn-back" or @class="back-link"]'
    _prizes_page_text = 'xpath=.//*[@class="Prizes links-list"] | .//*[@class="links-list prizes"]'
    _faqs_page_text = 'xpath=.//*[@class="FAQs links-list"]'
    _terms_page_text = 'xpath=.//*[@class="TandCs links-list"]'

    @property
    def back_button(self):
        return self._find_element_by_selector(selector=self._back_button, timeout=5)

    def has_back_button(self, timeout=2, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._back_button, timeout=5) is not None,
            name=f'Back Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def prizes_page_text(self):
        return self._find_element_by_selector(selector=self._prizes_page_text, timeout=5)

    @property
    def faqs_page_text(self):
        return self._find_element_by_selector(selector=self._faqs_page_text, timeout=5)

    @property
    def terms_page_text(self):
        return self._find_element_by_selector(selector=self._terms_page_text, timeout=5)


class QuestionEngineQuicklinks(ComponentBase):
    _name = 'xpath=.//*[contains(@class, "qe-footer-list")]/span'
    _chevron = 'xpath=.//*[contains(@class, "arrow-icon next-arrow qe-footer")] | //*[@class = "qe-footer-list__svg"]'
    _quick_links_page = 'xpath=.//*[@class="qe-container"]'
    _exit_button = 'xpath=.//*[contains(@class,"back-link")]'

    @property
    def chevron(self):
        return self._find_element_by_selector(selector=self._chevron, timeout=5)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=5)

    @property
    def quick_links_page(self):
        return QuickLinksPage(selector=self._quick_links_page)

    @property
    def exit_button(self):
        return LinkBase(selector=self._exit_button, context=self._we)

    def has_exit_link(self, timeout=2, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._exit_button, timeout=0) is not None,
            name=f'exit link status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result


class QuestionEngineQuicklinksSection(ComponentBase):
    _item = 'xpath=.//*[contains(@class, "qe-footer-list-item")] | //*[contains(@class, "qe-footer-list__item")]'
    _list_item_type = QuestionEngineQuicklinks


class QuestionEngine(QuestionEngineQuicklinks):
    _title_logo = 'xpath=.//*[@class="logo"] | .//*[@class="logo-small"]'
    _quick_links_section = 'xpath=.//*[@class="qe-footer"]'
    _strap_line_text = 'xpath=.//*[@class="strap-line"]'
    _CTA_button = 'xpath=.//*[contains(@class, "main-btn")]'
    _previous_results_link = 'xpath=.//*[contains(@class, "qe-main-section-link")]'
    _footer_text = 'xpath=.//*[contains(@class, "bottom-text")]'
    _close_button = 'xpath=.//*[contains(@class, "qe-btn-close")]'
    _back_button = 'xpath=.//*[@data-crlat="btnBack"]'

    def has_title_logo(self, timeout=2, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._title_logo, timeout=0) is not None,
            name=f'Logo Presense status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def quicklinks_section(self):
        return QuestionEngineQuicklinksSection(selector=self._quick_links_section, context=self._we)

    @property
    def strap_line_text(self):
        return self._get_webelement_text(selector=self._strap_line_text, timeout=5)

    def has_cta_button(self, timeout=2, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._CTA_button, timeout=0) is not None,
            name=f'Previous Games Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def cta_button(self):
        return self._find_element_by_selector(selector=self._CTA_button, timeout=5)

    def has_previous_results_link(self, timeout=2, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._previous_results_link, timeout=0) is not None,
            name=f'Previous Games Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def previous_results_link(self):
        return self._find_element_by_selector(selector=self._previous_results_link, timeout=5)

    @property
    def footer_text(self):
        return self._get_webelement_text(selector=self._footer_text, timeout=5)

    def has_close_button(self, timeout=2, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._close_button, timeout=0) is not None,
            name=f'Close Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def close_button(self):
        return self._find_element_by_selector(selector=self._close_button, timeout=5)

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, timeout=5)


class AnswerOption(ComponentBase):
    _name = 'xpath=.//*[contains(@class, "questions-carousel-btn")]/text() | .//*[contains(@class, "questions-carousel__btn")]/text()'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=5)


class AnswerOptions(ComponentBase):
    _item = 'xpath=.//*[contains(@class, "questions-carousel-btn")] | .//*[contains(@class, "questions-carousel__btn")]'
    _list_item_type = AnswerOption

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({f'{items_we.index(item_we)}': list_item})
        return items_ordered_dict


class QuestionSlider(ComponentBase):
    _question_num_header = 'xpath=.//*[contains(@class,"questions-carousel-signposting")]'
    _question_header = 'xpath=.//*[contains(@class,"questions-carousel-title")] |' \
                       './/*[contains(@class,"questions-carousel__title")]'
    _question_description = 'xpath=.//*[contains(@class,"questions-carousel-text")] |' \
                            ' .//*[contains(@class,"-carousel__text")]'
    _answer_options = 'xpath=.//slide[@id="{}"]'

    @property
    def question_num_header(self):
        return self._get_webelement_text(selector=self._question_num_header, timeout=5)

    @property
    def question_header(self):
        return self._find_element_by_selector(selector=self._question_header, timeout=5)

    @property
    def question_description(self):
        return self._find_element_by_selector(selector=self._question_description, timeout=5)

    @property
    def answer_options(self):
        val = self._answer_options.format(int(self.question_num_header.split(' ')[1]) - 1)
        return AnswerOptions(selector=val, timeout=5)


class QuestionsContainer(ComponentBase):
    _item = 'xpath=.//*[@class="slide"]/div'
    _list_item_type = QuestionSlider

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({f'{items_we.index(item_we)}': list_item})
        return items_ordered_dict


class ProgressBar(ComponentBase):
    _bar = 'xpath=.//*[@class="qe-progress-bar__item qe-progress-status"] | .//*[@class="qe-progress-bar-item qe-progress-status"]'

    @property
    def bar(self):
        return self._find_element_by_selector(selector=self._bar)

    @property
    def bar_size(self):
        style = self.bar.get_attribute('style')
        width = int(style.split(": ")[1].split("%")[0])
        return width


class QuizHomePage(QuestionEngine):
    _header = 'xpath=.//*[contains(@class, "qe-header-inf")]'
    _tabs = 'xpath=.//*[contains(@class, "info-list-item")]'
    _no_game_text = 'xpath=.//*[@class="no-game-wrapper"]'
    _questions_container = 'xpath=.//*[contains(@class,"swiper-container")]'
    _progress_bar = 'xpath=.//*[@class="qe-progress-bar"]'
    _submit = 'xpath=//*[@class="btn btn-submit"]'
    _quiz_right_swipe_overlay = 'xpath=.//span[contains(@class,"qe-arrow is-right")]'
    _quiz_left_swipe_overlay = 'xpath=.//span[contains(@class,"qe-arrow is-left")]'
    _back_button = 'xpath=.//top-bar/a[@data-crlat="btnBack"]'
    _quiz_right_swipe_inactive = 'xpath=.//*[contains(@class,"slide-btn next inactive")]'

    @property
    def question_container(self):
        return QuestionsContainer(selector=self._questions_container, timeout=5)

    @property
    def progress_bar(self):
        return ProgressBar(selector=self._progress_bar)

    @property
    def header(self):
        return self._find_element_by_selector(selector=self._header, timeout=5)

    @property
    def quiz_right_swipe_overlay(self):
        return self._find_element_by_selector(selector=self._quiz_right_swipe_overlay, timeout=5)

    @property
    def quiz_left_swipe_overlay(self):
        return self._find_element_by_selector(selector=self._quiz_left_swipe_overlay, timeout=5)

    def has_no_game_text(self, timeout=2, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._no_game_text, timeout=0) is not None,
            name=f'Game status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def submit(self):
        return ButtonBase(selector=self._submit, context=self._we)

    @property
    def back_button(self):
        return self._find_element_by_selector(selector=self._back_button, timeout=5)

    def has_quiz_right_swipe_inactive(self, timeout=2, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._quiz_right_swipe_inactive, timeout=0) is not None,
            name=f'next link disabled to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result


class ResultsPage(ComponentBase):
    _name = 'xpath=.//*[@class="qe-summary-item-index"]'
    _question_name = 'xpath=.//*[@class="qe-summary-item-question"]'
    _answer_name = 'xpath=.//*[@class="qe-summary-item-answer"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=5)

    @property
    def question_name(self):
        return self._get_webelement_text(selector=self._question_name, timeout=5)

    @property
    def answer_name(self):
        return self._get_webelement_text(selector=self._answer_name, timeout=5)


class Upsell(ComponentBase):
    _upsell_title = 'xpath=.//*[@class="qe-upsell-title"]'
    _upsell_caption = 'xpath=.//*[@class="qe-upsell-caption"]'
    _bet_button = 'xpath=.//*[contains(@class,"qe-upsell-cta")]'

    @property
    def upsell_title(self):
        return self._get_webelement_text(selector=self._upsell_title, timeout=5)

    @property
    def upsell_caption(self):
        return self._get_webelement_text(selector=self._upsell_caption, timeout=5)

    @property
    def bet_button(self):
        return ButtonBase(selector=self._bet_button, timeout=5)


class ResultsPageTabContent(ComponentBase):
    _upsell_content = 'xpath=.//*[contains(@class, "qe-upsell-container")]'
    _summary_title = 'xpath=.//*[@class="qe-summary-title"]'
    _item = 'xpath=.//*[@class="qe-summary-item"]'
    _list_item_type = ResultsPage

    @property
    def upsell(self):
        return Upsell(selector=self._upsell_content, timeout=5)

    @property
    def summary_title(self):
        return self._find_element_by_selector(selector=self._summary_title, timeout=5)

    def has_upsell_card(self, timeout=2, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._upsell_content, timeout=0) is not None,
            name=f'Upsell Card Content status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result


class QuizResultsPage(QuestionEngine):
    _switchers = 'xpath=.//*[@class="tabs-switcher-container"]'
    _switcher = 'xpath=.//*[contains(@class,"tab-item tab-item-")]'
    _no_results_text = 'xpath=.//*[@class="no-game-title"]'
    _latest_tab = 'xpath=.//*[contains(@class,"tab-item-latest")]'
    _previous_tab = 'xpath=.//*[contains(@class,"tab-item-previous")]'
    _tab_content = 'xpath=.//*[contains(@class, "tab-content tab-content")]'
    _submit_message = 'xpath=.//*[contains(@class, "notify-content")]'
    _results_summary = 'xpath=.//*[@class="game-summary-label"] | .//*[@class="game-summary__label"]'

    def has_results_summary(self, timeout=2, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._results_summary, timeout=0) is not None,
            name=f'Game status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def view_game_summary(self):
        return LinkBase(selector=self._results_summary, timeout=5)

    def has_no_game_text(self, timeout=2, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._no_results_text, timeout=0) is not None,
            name=f'Game status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def latest_tab(self):
        return LinkBase(selector=self._latest_tab, timeout=5)

    @property
    def previous_tab(self):
        return LinkBase(selector=self._previous_tab, timeout=5)

    @property
    def submit_message(self):
        return self._get_webelement_text(selector=self._submit_message, timeout=2)

    @property
    def tab_content(self):
        return ResultsPageTabContent(selector=self._tab_content, timeout=5)


class QuizPagePopup(ComponentBase):
    _submit_button = 'xpath=.//button[contains(@class,"btn btn-submit")]'
    _go_back_edit_button = 'xpath=//button[contains(@class,"btn btn-handle")]'
    _quiz_exit_popup = 'xpath=.//*[@class="modal-content"]'

    def has_submit_button(self, timeout=2, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._submit_button, timeout=0) is not None,
            name=f'Game status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def go_back_edit_button(self):
        return self._find_element_by_selector(selector=self._go_back_edit_button, timeout=5)

    @property
    def submit_button(self):
        return self._find_element_by_selector(selector=self._submit_button, timeout=5)

    def has_quiz_exit_popup(self, timeout=2, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._quiz_exit_popup, timeout=0) is not None,
            name=f'quiz popup displayed "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def exit_quiz_popup(self):
        return ExitQuizPagePopup(selector=self._quiz_exit_popup, timeout=5)


class ExitQuizPagePopup(ComponentBase):
    _exit_popup_header = 'xpath=.//div[@class="modal-content"]/div/span'
    _exit_popup_desc = 'xpath=.//div[@class="modal-body"]/div'
    _exit_popup_playing_btn = 'xpath=.//button[contains(@class, "btn-continue")]'
    _exit_popup_leave_btn = 'xpath=.//div[@class="modal-body"]//button[contains(@class, "btn-handle")]'

    @property
    def keep_playing_button(self):
        return self._find_element_by_selector(selector=self._exit_popup_playing_btn, timeout=5)

    @property
    def leave_button(self):
        return self._find_element_by_selector(selector=self._exit_popup_leave_btn, timeout=5)

    @property
    def exit_popup_desc(self):
        return self._get_webelement_text(selector=self._exit_popup_desc, context=self._we)
