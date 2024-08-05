import voltron.environments.constants as vec
import pytest
import tests
from tenacity import retry, retry_if_exception_type, stop_after_attempt
from random import choice
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from tests.pack_018_Virtual_Sports.BaseVirtualsTest import BaseVirtualsTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter, SiteServeRequests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.virtual_sports
@pytest.mark.horseracing
@pytest.mark.tricast
@pytest.mark.open_bets
@pytest.mark.slow
@pytest.mark.timeout(1300)
@pytest.mark.login
@pytest.mark.reg157_fix
@vtest
class Test_C16375057_Verify_Tricast_tab_content_on_Virtual_Sports_EDPs(BaseVirtualsTest):
    """
    TR_ID: C16375057
    NAME: Verify Tricast tab content on Virtual Sports EDPs
    DESCRIPTION: This test case verifies the content of the Tricast tab on Virtual Sports page for different sports.
    PRECONDITIONS: Tricast market is configured and shown for Virtual Sports such as: Horse Racing, Horse Racing Jumps, Greyhound, Motor Racing and Cycling.
    PRECONDITIONS: Note: Tricast tab should not be shown for such Virtual Sports as: VGN (Virtual Grand Nationals Races), Football, Tennis, Speedway, Boxing, Darts.
    PRECONDITIONS: The rules of displaying Virtuals Forecast and Tricast tabs:
    PRECONDITIONS: 1. Tabs are not shown at all if event does not have ncastTypeCodes attribute. Only WinOrEw Market is displayed in this case (UI looks like on current production).
    PRECONDITIONS: 2. All tabs are shown if event has ncastTypeCodes attribute with set CF and CT.
    PRECONDITIONS: 3. Two tabs: Forecast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CF.
    PRECONDITIONS: 4. Two tabs: Tricast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CT.
    PRECONDITIONS: Also we check if market is WinOrEw: ['To Win', 'To-Win', 'Win/EachWay', 'Win or Each Way']
    """
    keep_browser_open = True
    runner_buttons = []
    next_events = vec.virtuals.VIRTUAL_HUB_NEXT_EVENTS

    @retry(stop=stop_after_attempt(4),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException, NoSuchElementException, ValueError)), reraise=True)
    def verify_tricast_layout(self, virtual_sport):
        if virtual_sport in self.expected_sports:
            virtual_sports_list = self.site.virtual_sports
            open_tab = virtual_sports_list.sport_carousel.open_tab(virtual_sport)
            self.assertTrue(open_tab, msg=f'Tab "{virtual_sport}" is not opened')
            self._logger.info(f'*** Forecast tab layout verification for virtual sport: "{virtual_sport}"')
            event_off_times_list = virtual_sports_list.tab_content.event_off_times_list
            self.assertTrue(event_off_times_list.is_displayed(),
                            msg=f'Event selector ribbon is not displayed for "{virtual_sport}"')

            event_off_time_tabs = event_off_times_list.items_as_ordered_dict.keys()
            event_off_time_tab = choice(list(event_off_time_tabs)[3:9])
            event_off_times_list.select_off_time(event_off_time_tab)

            tab_name = vec.racing.RACING_EDP_TRICAST_MARKET_TAB
            open_tab = virtual_sports_list.tab_content.event_markets_list.market_tabs_list.open_tab(tab_name)
            self.assertTrue(open_tab, msg=f'Tab "{tab_name}" is not opened')
            selections = wait_for_result(
                lambda: virtual_sports_list.tab_content.event_markets_list.items_as_ordered_dict, timeout=5,
                name='Selection is not empty')
            self.assertTrue(selections, msg='No selections were found')
            outcome_name, outcome = list(selections.items())[0]
            runners_names = list(selections.keys())
            self.assertTrue(runners_names, msg='Runner names are not available')
            self.assertFalse(outcome.is_non_runner, msg='Non runner is displayed')
            self.assertFalse(vec.racing.UNNAMED_FAVORITE in runners_names,
                             msg=f'"{vec.racing.UNNAMED_FAVORITE}" selection is shown on the Forecast tab')


            runner_buttons = self.get_runner_bet_buttons()
            runner_buttons[0].click()
            self.assertFalse(outcome.has_silks, msg=f'Silk icon is displayed for outcome: "{outcome_name}"')
            runner_buttons = self.get_runner_bet_buttons()
            self.assertTrue(runner_buttons[0].is_selected(),
                            msg=f'1st Button is not selected for "{self.outcome_name}"')
            self.assertFalse(runner_buttons[1].is_enabled(expected_result=False),
                             msg=f'2nd Button is enabled for "{self.outcome_name}"')
            self.assertFalse(runner_buttons[2].is_enabled(expected_result=False),
                             msg=f'3rd Button is enabled for "{self.outcome_name}"')
            self.assertFalse(runner_buttons[3].is_enabled(expected_result=False),
                             msg=f'Any Button is enabled for "{self.outcome_name}"')
            self.assertFalse(virtual_sports_list.tab_content.event_markets_list.add_to_betslip_button.is_enabled(
                expected_result=False),
                             msg='Add To Betslip button is enabled')

            actual_runners_order = [outcome.runner_number for outcome in selections.values()]
            expected_runners_order = sorted(actual_runners_order, key=lambda x: int(x))
            self.assertEqual(actual_runners_order, expected_runners_order,
                             msg=f'Runners are not ordered by runner number. Actual order: "{actual_runners_order}"'
                                 f'Expected: "{expected_runners_order}"')

            # All horses in the Tricast tab
            outcome_list = list(selections.items())[1:]

            index = 1
            for outcome_name, outcome in outcome_list:
                runner_buttons = outcome.items_as_ordered_dict
                self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{outcome_name}"')
                self.assertFalse(outcome.has_silks, msg=f'Silk icon is displayed for outcome: "{outcome_name}"')
                runner_bet_button_names = list(runner_buttons.keys())
                self.assertEqual(runner_bet_button_names, vec.racing.RACING_EDP_TRICAST_RACING_BUTTONS,
                                 msg=f'Actual racing button names "{runner_bet_button_names}" '
                                     f'does not match expected "{vec.racing.RACING_EDP_TRICAST_RACING_BUTTONS}"')
                self.assertFalse(outcome.is_non_runner, msg='Non runner is displayed')
                runner_buttons = self.get_runner_bet_buttons(index=index)
                self.assertFalse(runner_buttons[0].is_selected(expected_result=False),
                                 msg=f'1st Button is selected')
                index = index + 1

            # Tap one of the same runner button again.
            runner_buttons = self.get_runner_bet_buttons()
            runner_buttons[0].click()
            runner_buttons = self.get_runner_bet_buttons()
            self.assertFalse(runner_buttons[0].is_selected(expected_result=False),
                             msg=f'1st Button is selected for "{self.outcome_name}"')
            self.assertTrue(runner_buttons[1].is_enabled(), msg=f'2nd Button is disabled for "{self.outcome_name}"')
            self.assertTrue(runner_buttons[2].is_enabled(), msg=f'3rd Button is disabled for "{self.outcome_name}"')
            self.assertTrue(runner_buttons[3].is_enabled(), msg=f'Any Button is disabled for "{self.outcome_name}"')
            for outcome_name, outcome in outcome_list:
                runner_buttons = self.get_runner_bet_buttons()
                self.assertTrue(runner_buttons[0].is_enabled(),
                                msg=f'1st Button is disabled for "{outcome_name}"')
                self.assertTrue(runner_buttons[1].is_enabled(), msg=f'2nd Button is disabled for "{outcome_name}"')
                self.assertTrue(runner_buttons[2].is_enabled(), msg=f'3rd Button is disabled for "{outcome_name}"')
                self.assertTrue(runner_buttons[3].is_enabled(), msg=f'Any Button is disabled for "{outcome_name}"')


    def test_000_preconditions(self):
        """
        DESCRIPTION: Get list of active virtual sport categories
        DESCRIPTION: Login into the app
        EXPECTED: User successfully log into the app
        """
        virtuals_cms_class_ids = self.cms_virtual_sports_class_ids()
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.virtuals_config.category_id)
        sports_list = ss_req.ss_class(query_builder=self.ss_query_builder.
                                      add_filter(simple_filter(LEVELS.CLASS,
                                                               ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                                               str(self.ob_config.virtuals_config.category_id))))
        if not sports_list:
            raise SiteServeException('There are no active virtual sports')
        event = None
        sports_class_ids_with_tricast_markets = []
        for sport_class in sports_list:
            class_id = sport_class['class']['id']
            additional_filter = exists_filter(
                LEVELS.EVENT, simple_filter(LEVELS.MARKET,
                                            ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'CT')), exists_filter(
                LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE))
            events = self.get_active_event_for_class(class_id=class_id, additional_filters=additional_filter,
                                                     raise_exceptions=False)
            if not events:
                continue
            event = choice(events)
            ss_class_id = event['event']['classId']
            if ss_class_id in virtuals_cms_class_ids:
                sports_class_ids_with_tricast_markets.append(ss_class_id)
            else:
                continue
        if not event:
            raise SiteServeException('There are no available virtual event with Forecast tab')
        self.__class__.expected_sports = \
            self.cms_virtual_sport_tab_name_by_class_ids(class_ids=sports_class_ids_with_tricast_markets)
        self.site.login()

    def test_001_navigate_to_virtual_sport_page_and_tap_on_some_sport__where_tricast_tab_should_be_displayed(self):
        """
        DESCRIPTION: Navigate to Virtual Sport page and tap on some sport from preconditions where Tricast tab should be displayed.
        DESCRIPTION: Note: this test cases should be run for all Virtual Sports where Tricast tab should be displayed.
        EXPECTED: Separate Tricast tab is displayed after Win or Each Way (and Forecast tab if available) market tab.
        """
        self.site.open_sport(name=self.get_sport_title(category_id=self.ob_config.virtuals_config.category_id),
                             content_state='VirtualSports')

    def test_002_select_tricast_and_verify_its_layout(self):
        """
        DESCRIPTION: Select Tricast and verify its layout.
        EXPECTED: 1.List of selections is displayed with:
        EXPECTED: runner number
        EXPECTED: runner name
        EXPECTED: no silks
        EXPECTED: no race form info
        EXPECTED: Unnamed favourites and Non runners are NOT displayed
        EXPECTED: Runners are ordered by runner number
        EXPECTED: 2.Four grey tappable buttons displayed at the right side of each runner:
        EXPECTED: 1st
        EXPECTED: 2nd
        EXPECTED: 3rd
        EXPECTED: ANY
        EXPECTED: 3.Green 'Add To Betslip' button displayed at the bottom of the list, disabled by default.
        virtual sports hub is configured to a new page and from virtual sports hub we navigate to virtual sports page.
        """
        virtual_hub_home_page = self.cms_config.get_system_configuration_structure().get('VirtualHubHomePage')
        if virtual_hub_home_page.get('enabled'):
            virtual_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.upper() != self.next_events.upper()), None)
            list(virtual_section.items_as_ordered_dict.values())[0].click()

        sport_category_names_from_page = self.site.virtual_sports.sport_carousel.items_names
        self.assertTrue(sport_category_names_from_page, msg='Virtual sports are not present on UI')

        for virtual_sport in sport_category_names_from_page:
            self.verify_tricast_layout(virtual_sport=virtual_sport)

    def test_003_tap_any_1st_2nd_3rd_or_any_button(self):
        """
        DESCRIPTION: Tap any 1st, 2nd, 3rd or ANY button.
        EXPECTED: 1. Tapped button is displayed as selected and highlighted in green.
        EXPECTED: 2. All other such buttons are disabled (e.g. - after tapping on 1st button, all other 1st buttons should be disabled for all horses).
        EXPECTED: 3. All other buttons for the same horse is disabled (e.g. - after tapping on 1st button, 2nd, 3rd and ANY button should be disabled for the same horse).
        """
        pass
        # This step is covered in scope of test step 2

    def test_004_tap_the_same_button_again(self):
        """
        DESCRIPTION: Tap the same button again.
        EXPECTED: 1. Tapped button is deselected and not highlighted in green.
        EXPECTED: 2. All other buttons should be enabled again.
        """
        pass
        # This step is covered in scope of test step 2
