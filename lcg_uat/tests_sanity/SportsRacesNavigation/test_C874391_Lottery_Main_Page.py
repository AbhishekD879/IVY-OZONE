from datetime import datetime
from random import choice

import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.lotto
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.desktop
@pytest.mark.back_button
@pytest.mark.sanity
@vtest
class Test_C874391_Lottery_Main_Page(Common):
    """
    TR_ID: C874391
    NAME: Lottery Main Page
    DESCRIPTION: This Test Case verifies Lottery Main Page.
    DESCRIPTION: Note: 'More Market's expandible/collapsible section is not implemented functionality
    PRECONDITIONS: 1. Lotto icon should be preconfigured in Sports Menu Ribbon and/or A-Z Page via CMS
    PRECONDITIONS: 2. Launch Oxygen application
    """
    keep_browser_open = True
    number_name = None

    def format_name(self, lotto_name: str):
        """
        This method unifies lotto's name as it is displayed on UI
        :param lotto_name: lotto's name
        :return: formatted lotto's name
        """
        formatted_name = lotto_name.upper().replace(' LOTTO', '').replace(' LOTTERY', '').\
            replace(' BALL', '').replace(' 6', '').replace(' 7', '').replace(' TEST2019', '').replace(' DRAW', '')
        return formatted_name

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get data from SS for test
        """
        utc_time = datetime.strftime(datetime.utcnow(), self.ob_format_pattern)

        ss_req = SiteServeRequests(env=tests.settings.backend_env, brand=self.brand)

        lotto_filter = self.ss_query_builder.add_filter(simple_filter(LEVELS.LOTTERY, ATTRIBUTES.HAS_OPEN_DRAW))
        lotto_resp = ss_req.ss_lottery_to_draw(query_builder=lotto_filter)
        self.__class__.range_wheel_max_numbers = {self.format_name(lottery['lottery']['name']): lottery['lottery']['maxNumber'] for lottery in lotto_resp}

        oz_lotto = 'Australian Ozlotto Lottery'
        tats_lotto = 'Australian Tattslotto Lottery'
        irish_6 = 'Irish Lotto 6 ball'
        irish_7 = 'Irish Lotto 7 ball'

        # this is configured in bma project:
        # src/environments/configs/lotteriesConfig.ts for Coral
        # src/environments/configs/lotteriesLadbrokesConfig.ts for Ladbrokes
        if tests.settings.backend_env != 'prod':
            ids_to_exclude = ['7', '20', '26', '27'] if self.brand != 'ladbrokes' else ['']
        else:
            ids_to_exclude = ['7', '20', '26', '27'] if self.brand != 'ladbrokes' else ['1801', '1806']

        excluded = [x for x in lotto_resp if x['lottery']['id'] not in ids_to_exclude]
        all_range_wheel_max_numbers = {lottery['lottery']['name']: lottery['lottery']['maxNumber'] for lottery in excluded}
        all_ball_numbers = {lottery['lottery']['name']: lottery['lottery']['maxPicks'] for lottery in excluded}

        lotto_name_list = [x['lottery']['description'] for x in excluded]
        lotto_data_list = [x['lottery']['children'] for x in excluded]

        draw_list = []
        for item in lotto_data_list:
            draw = [x for x in item if x.get('draw') is not None]
            draw_list.append(draw)

        lotto_dict = dict(zip(lotto_name_list, draw_list))

        if tests.settings.backend_env == 'prod' and self.brand != 'ladbrokes':
            if oz_lotto in list(lotto_dict.keys()):
                lotto_dict[tats_lotto].extend(lotto_dict[oz_lotto])
                lotto_dict.pop(oz_lotto)
                all_range_wheel_max_numbers.pop(oz_lotto)
                all_ball_numbers.pop(oz_lotto)

        if tests.settings.backend_env != 'prod' and self.brand == 'ladbrokes':
            if irish_7 in list(lotto_dict.keys()):
                lotto_dict[irish_6].extend(lotto_dict[irish_7])
                lotto_dict.pop(irish_7)
                all_range_wheel_max_numbers.pop(irish_7)
                all_ball_numbers.pop(irish_7)

        self.__class__.range_wheel_max_numbers = {self.format_name(lottery): num for lottery, num in all_range_wheel_max_numbers.items()}
        self.__class__.ball_numbers = {self.format_name(lottery): num for lottery, num in all_ball_numbers.items()}
        shut_at_time = []
        for name in lotto_dict.keys():
            shut = [x['draw']['shutAtTime'] for x in lotto_dict[name] if x['draw']['shutAtTime'] >= utc_time]
            if shut:
                shut_at_time.append(min(shut))
        self.assertTrue(shut_at_time, msg='There are no shut time for lotteries')

        shut_at_time_local = [self.convert_time_to_local(
            date_time_str=x, ob_format_pattern=self.ob_format_pattern,
            ui_format_pattern=self.ob_format_pattern,
            future_datetime_format=self.ob_format_pattern,
            ss_data=True) for x in shut_at_time]

        lotto_ui_names = [self.format_name(x) for x in lotto_dict.keys()]

        name_time = dict(zip(lotto_ui_names, shut_at_time_local))
        sorted_name_time = dict(sorted(name_time.items(), key=lambda x: (x[1], x[0])))

        self.__class__.ss_lotto_names = list(sorted_name_time.keys())

    def test_001_tap_lotto_icon_from_sports_menu_ribbon_or_a_z_page_or_header_menu_for_desktop(self):
        """
        DESCRIPTION: Tap 'Lotto' icon (from Sports Menu Ribbon or A-Z page or Header menu for desktop)
        EXPECTED: 'Lotto' page is opened with following elements:
        EXPECTED: *   'Lotto' header
        EXPECTED: *   Back button
        EXPECTED: *   Banner section
        EXPECTED: *   Lottery Selector carousel
        EXPECTED: *   Lottery title
        EXPECTED: *   'Lucky' buttons
        EXPECTED: *   Number Selector module
        EXPECTED: *   The Bonus Ball toggle (if available)
        EXPECTED: *   'Options' expandible/collapsible section
        EXPECTED: *   'Place Bet' button is shown by default
        EXPECTED: **For Desktop:**
        EXPECTED: * Breadcrumbs are displayed below 'Lotto' header
        EXPECTED: * Breadcrumbs are displayed in the following format : 'Home' > 'Lotto'
        """
        self.site.open_sport(name='lotto', timeout=10)
        self.site.wait_content_state(state_name='LOTTO')

        tab_content = self.site.lotto.tab_content
        self.assertTrue(tab_content, msg='Lotto tab content didn\'t found')

        sport_title = self.site.lotto.header_line.page_title.sport_title

        expected_title = vec.lotto.LOTTO.title() if self.brand == 'ladbrokes' else vec.lotto.LOTTO.upper()
        self.assertEqual(expected_title, sport_title,
                         msg=f'Page title is not "{expected_title}", but "{sport_title}"')

        self.assertTrue(self.site.has_back_button,
                        msg='Back button isn\'t displayed on page header')

        # Banner Section disabled in Coral-prod. Depends on sitecore config and we cannot retrieve data from
        # site core to verify, please check manually.
        # self.assertTrue(self.site.lotto.banner_section.is_displayed(),
        #                 msg='Banner section isn\'t present on page header')
        self.assertTrue(self.site.lotto.lotto_carousel.is_displayed(),
                        msg='Lottery Selector Carousel isn\'t present on Lotto page')
        self.assertTrue(tab_content.info_panel.is_displayed(),
                        msg='Lottery title isn\'t present on Lotto page')
        self.assertTrue(tab_content.lucky_buttons.is_displayed(),
                        msg='Lucky buttons aren\'t present on Lotto page')
        self.assertTrue(tab_content.number_selectors.is_displayed(),
                        msg='Number Selectors Line is not present on Lotto')
        if tab_content.has_include_bonus_ball():
            self.assertTrue(tab_content.include_bonus_ball.is_displayed(),
                            msg='Include Bonus ball is not present on Lotto page')
        else:
            self._logger.warning('Include Bonus ball is not present on Lotto page')

        self.assertTrue(self.site.lotto.tab_content.options.is_displayed(),
                        msg='Options section isn\'t shown on Lotto page')
        self.assertTrue(self.site.lotto.tab_content.place_bet.is_displayed(),
                        msg='Place bet button isn\'t shown on Lotto page')

        if self.device_type == 'desktop':
            breadcrumbs = list(self.site.lotto.breadcrumbs.items_as_ordered_dict.keys())
            self.assertTrue(breadcrumbs, msg='No breadcrumbs found')
            expected_breadcrumbs = ['Home', 'lotto']
            self.assertEqual(breadcrumbs, expected_breadcrumbs,
                             msg=f'Breadcrumbs "{breadcrumbs}" are not the same as expected "{expected_breadcrumbs}"')

    def test_002_verify_lottery_selector_carousel(self):
        """
        DESCRIPTION: Verify Lottery Selector Carousel
        EXPECTED: Each Lottery in the Carousel has it's own icon and title
        """
        lotto_list = self.site.lotto.lotto_carousel.items_as_ordered_dict
        self.assertTrue(lotto_list, msg='No Lottery Selector Carousel items found')

        # Verify each Lottery icon and title
        for lotto_name, lotto in lotto_list.items():
            self.assertTrue(lotto.icon.is_displayed(), msg=f'"{lotto_name}" Icon is not present on Lotto page')
            self.assertTrue(lotto.title.is_displayed(), msg=f'"{lotto_name}" Title is not present on Lotto page')

    def test_003_verify_lottery_name(self):
        """
        DESCRIPTION: Verify Lottery name
        EXPECTED: Lottery name corresponds to "**description**" attribute on the lottery level
        """
        self.__class__.lotto_carousel = self.site.lotto.lotto_carousel.items_as_ordered_dict
        self.assertTrue(self.lotto_carousel, msg='No Lottery Selector Carousel items found')

        actual_list = [x.upper() for x in self.lotto_carousel.keys()]
        self.assertListEqual(self.ss_lotto_names, actual_list,
                             msg=f'\nLists are not equal! \nActual list: {actual_list} \nExpected list: {self.ss_lotto_names}')

    def test_004_tap_any_lottery_icon(self):
        """
        DESCRIPTION: Tap any Lottery icon
        EXPECTED: *   Each Lottery has a title in between the lottery selector and Numbers Selector Module
        EXPECTED: *   The title shows the name of the Lottery and time left for the next draw
        """
        random_lotto = choice(list(self.lotto_carousel.values()))
        random_lotto.click()
        self.__class__.selected_lottery = self.site.lotto.tab_content.info_panel.lottery_name
        self.assertTrue(self.selected_lottery, msg='The title didn\'t show the name of the Lottery')

        time = self.site.lotto.tab_content.info_panel.bet_until_time
        self.assertTrue(time, msg='The title didn\'t show the time of the Lottery')

    def test_005_verify_default_state_of_numbers_selector_module(self):
        """
        DESCRIPTION: Verify default state of Numbers Selector Module
        EXPECTED: *   Numbers Selector Module is placed under Lottery Title
        EXPECTED: *   Numbers Selector Module consists of **5** wheels which hold the numbers
        EXPECTED: *   **"-" **is displayed in each of the Wheels by default (although further user selection is saved in local storage)
        EXPECTED: *   The range of the Numbers available in each Wheel is 1 to the Max number of the Lottery e.g. 49 (The max number depends on the Lottery selected)
        """
        self.__class__.list_numbers = self.site.lotto.tab_content.number_selectors.items_as_ordered_dict
        wheel_numbers = self.ball_numbers.get(self.selected_lottery)
        self.assertTrue(wheel_numbers,
                        msg=f'"{self.selected_lottery}" lottery did not found in ss response "{self.ball_numbers.keys()}"')
        self.assertEqual(len(self.list_numbers), int(wheel_numbers),
                         msg=f'Amount of number selector items -  is not equal to "{int(wheel_numbers)}"')
        for _, number in self.list_numbers.items():
            self.assertEqual(number.name, "-", msg='Default number selectors values are not equal to "-"')

        list(self.list_numbers.values())[0].click()

        choose_lucky_num_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW,
                                                            timeout=10)
        self.assertTrue(choose_lucky_num_dialog, msg='"Choose Your Lucky Numbers" dialog is not shown')
        available_selections = choose_lucky_num_dialog.items_as_ordered_dict
        self.assertTrue(available_selections, msg=f'There is no lotto buttons')
        expected_range = self.range_wheel_max_numbers.get(self.selected_lottery)
        self.assertTrue(expected_range,
                        msg=f'"{self.selected_lottery}" lottery did not found in ss response "{self.range_wheel_max_numbers.keys()}"')
        self.assertEqual(len(available_selections), int(expected_range),
                         msg=f'The min range of the Numbers available is "{len(available_selections)}", but expected "{int(expected_range)}"')

        choose_lucky_num_dialog.close_dialog()

    def test_006_set_up_5_different_numbers_within_wheels(self):
        """
        DESCRIPTION: Set up 5 different numbers within Wheels
        EXPECTED: Numbers are set up correctly
        """
        selected_numb = []
        for wheel in self.list_numbers.values():
            wheel.click()
            choose_lucky_num_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW,
                                                                timeout=10)
            self.assertTrue(choose_lucky_num_dialog, msg='"Choose Your Lucky Numbers" dialog is not shown')
            available_selections = choose_lucky_num_dialog.items_as_ordered_dict
            self.assertTrue(available_selections, msg=f'There is no lotto buttons')
            for numb in selected_numb:
                available_selections.pop(str(numb))
            number_to_select = choice(list(available_selections.values()))
            self.number_name = number_to_select.name
            selected_numb.append(int(self.number_name))

            number_to_select.click()
            self.assertTrue(number_to_select.is_selected(), msg=f'"{self.number_name}" is not highlighted')
            choose_lucky_num_dialog.done_button.scroll_to()
            choose_lucky_num_dialog.done_button.click()
            choose_lucky_num_dialog.wait_dialog_closed()

        number_selectors = self.site.lotto.tab_content.number_selectors.items_as_ordered_dict.values()
        self.assertTrue(number_selectors, msg='Lotto number selectors are not present')
        ui_selected_numb = [int(i.name) if i.name.isdigit() else i.name for i in number_selectors]
        self.assertListEqual(sorted(selected_numb), ui_selected_numb,
                             msg=f'Expected Number values: {sorted(selected_numb)} '
                             f'are not equal to those that were set: {ui_selected_numb}')
