import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from random import choice
from selenium.common.exceptions import StaleElementReferenceException
from tests.pack_018_Virtual_Sports.BaseVirtualsTest import BaseVirtualsTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, exists_filter, SiteServeRequests


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.virtual_sports
@pytest.mark.reg157_fix
@vtest
class Test_C16375059_Verify_highlighting_1st_2nd_3rd_ANY_selections_from_Tricast(BaseVirtualsTest):
    """
    TR_ID: C16375059
    NAME: Verify highlighting 1st, 2nd, 3rd, ANY selections from Tricast
    DESCRIPTION: This test case verifies functionality of adding and removing 1st, 2nd, 3rd and ANY selections from Tricast tab.
    PRECONDITIONS: 1. Tricast market is configured and shown for Virtual Sports such as: Horse Racing, Horse Racing Jumps, Greyhound, Motor Racing and Cycling. Note: Forecast tab should not be shown for such Virtual Sports as: VGN (Virtual Grand Nationals Races), Football, Tennis, Speedway, Boxing, Darts.
    PRECONDITIONS: 2. User is on Virtual Sports page/Tricast tab (this test case should be run for all sports displayed in the previous step where Tricast tab should be displayed).
    PRECONDITIONS: The rules of displaying Virtuals Forecast and Tricast tabs:
    PRECONDITIONS: 1. Tabs are not shown at all if event does not have ncastTypeCodes attribute. Only WinOrEw Market is displayed in this case (UI looks like on current production).
    PRECONDITIONS: 2. All tabs are shown if event has ncastTypeCodes attribute with set CF and CT.
    PRECONDITIONS: 3. Two tabs: Forecast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CF.
    PRECONDITIONS: 4. Two tabs: Tricast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CT.
    PRECONDITIONS: Also we check if market is WinOrEw: ['To Win', 'To-Win', 'Win/EachWay', 'Win or Each Way']
    """
    keep_browser_open = True

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
            raise SiteServeException('There are no available virtual event with Tricast tab')
        self.__class__.expected_sports = \
            self.cms_virtual_sport_tab_name_by_class_ids(class_ids=sports_class_ids_with_tricast_markets)
        self.site.open_sport(name=self.get_sport_title(category_id=self.ob_config.virtuals_config.category_id),
                             content_state='VirtualSports')
        self.__class__.horse_race = next(
            (sport.get("title") for sport in self.cms_config.get_parent_virtual_sports() if
             "/horse-racing" in sport.get('ctaButtonUrl')), None)

    def test_001_tap_1st_button_for_any_runner(self):
        """
        DESCRIPTION: Tap 1st button for any runner.
        EXPECTED: - Selected button is highlighted in green;
        EXPECTED: - 2nd, 3rd and ANY buttons for this runner become disabled;
        EXPECTED: - All other 1st buttons for all other runners become disabled;
        EXPECTED: - Add to Betslip button is still disabled.
        """
        # Virtual hub home page status from CMS
        virtual_hub_home_page = self.cms_config.get_system_configuration_structure().get('VirtualHubHomePage')
        if virtual_hub_home_page.get('enabled'):
            # Added New Virtual races hub page in 157.0.0 release
            hubs_section = next((section for section_name, section in
                                 self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                                 section_name.upper() != vec.virtuals.VIRTUAL_HUB_NEXT_EVENTS.upper()), None)
            section_sports = list(hubs_section.items_as_ordered_dict.values())[0]
            section_sports.click()

        virtual_sports = self.site.virtual_sports.sport_carousel.items_as_ordered_dict
        virtual_sport = next((virtual_sport for virtual_sport in virtual_sports.keys() if
                              virtual_sport.upper() == self.horse_race.upper()), None)
        if not virtual_sport:
            raise CmsClientException('"Horse racing" is not configure in CMS for virtual sport')
        virtual_sports.get(virtual_sport).click()

        sport_category_names_from_page = self.site.virtual_sports.sport_carousel.items_names
        self.assertTrue(sport_category_names_from_page, msg='Virtual sports are not present on UI')

        if self.horse_race in sport_category_names_from_page:
            if self.horse_race in self.expected_sports:
                virtual_sports_list = self.site.virtual_sports
                open_tab = virtual_sports_list.sport_carousel.open_tab(self.horse_race)
                self.assertTrue(open_tab, msg=f'Tab "{self.horse_race}" is not opened')
                self._logger.info(f'*** Forecast tab layout verification for virtual sport: "{self.horse_race}"')
                event_off_times_list = virtual_sports_list.tab_content.event_off_times_list
                self.assertTrue(event_off_times_list.is_displayed(),
                                msg=f'Event selector ribbon is not displayed for "{self.horse_race}"')

                event_off_time_tabs = event_off_times_list.items_as_ordered_dict.keys()
                event_off_time_tab = choice(list(event_off_time_tabs)[3:9])
                event_off_times_list.select_off_time(event_off_time_tab)

                self.__class__.tab_name = vec.racing.RACING_EDP_TRICAST_MARKET_TAB
                open_tab = virtual_sports_list.tab_content.event_markets_list.market_tabs_list.open_tab(self.tab_name)
                self.assertTrue(open_tab, msg=f'Tab "{self.tab_name}" is not opened')
                self.__class__.selections = wait_for_result(lambda: virtual_sports_list.tab_content.event_markets_list.items_as_ordered_dict, timeout=5,
                                                            name='Selection is not empty')
                self.assertTrue(self.selections, msg='No selections were found')
                outcome_name, outcome = list(self.selections.items())[0]
                self.assertTrue(outcome_name, msg='Runner names are not available')
                runner_buttons = self.get_runner_bet_buttons()
                runner_buttons[0].click()
                sleep(2)
                try:
                    self.assertFalse(runner_buttons[1].is_enabled(),
                                     msg=f'2nd button was not disabled for the runner "{outcome_name}"')
                    self.assertFalse(runner_buttons[2].is_enabled(),
                                     msg=f'3rd button was not disabled for the runner "{outcome_name}"')
                    self.assertFalse(runner_buttons[3].is_enabled(),
                                     msg=f'ANY button was not disabled for the runner "{outcome_name}"')
                    if self.tab_name != open_tab:
                        self.site.virtual_sports.tab_content.event_markets_list.market_tabs_list.open_tab(self.tab_name)
                    for i in range(1, len(self.selections)):
                        runner_buttons = self.get_runner_bet_buttons(index=i)
                        self.assertFalse(runner_buttons[0].is_enabled(),
                                         msg=f'1st button was not disabled for the runner: "{list(self.selections.keys())[i]}"')

                    self.assertFalse(virtual_sports_list.tab_content.event_markets_list.add_to_betslip_button.is_enabled(
                                     expected_result=False), msg='Add To Betslip button is enabled')
                except StaleElementReferenceException as e:
                    self._logger.debug(f'*** Virtual sport content refreshed: "{e}"')
                    self.site.virtual_sports.tab_content.event_markets_list.market_tabs_list.open_tab(self.tab_name)
        else:
            raise SiteServeException('Horse Racing category not found')

    def test_002_tap_2nd_button_for_any_other_runner(self):
        """
        DESCRIPTION: Tap 2nd button for any other runner.
        EXPECTED: - Selected button is highlighted in green. Previously selected button remains green and selected;
        EXPECTED: - 1st, 3rd and ANY button for this runner become disabled;
        EXPECTED: - All other 2nd buttons for all other runners become disabled;
        EXPECTED: - Other 3rd and ANY buttons remain enabled;
        EXPECTED: - Add to Betslip button is still disabled.
        """
        runner_buttons = self.get_runner_bet_buttons(index=1)
        runner_buttons[1].click()
        sleep(2)
        try:
            self.assertFalse(runner_buttons[0].is_enabled(),
                             msg=f'1st button was not disabled for the runner "{list(self.selections.keys())[1]}"')
            self.assertFalse(runner_buttons[2].is_enabled(),
                             msg=f'3rd button was not disabled for the runner "{list(self.selections.keys())[1]}"')
            self.assertFalse(runner_buttons[3].is_enabled(),
                             msg=f'ANY button was not disabled for the runner "{list(self.selections.keys())[1]}"')
            for i in range(2, len(self.selections)):
                runner_buttons = self.get_runner_bet_buttons(index=i)
                self.assertFalse(runner_buttons[1].is_enabled(),
                                 msg=f'2nd button was not disabled for the runner: "{list(self.selections.keys())[i]}"')
                self.assertTrue(runner_buttons[2].is_enabled(),
                                msg=f'3rd button was not enabled for the runner: "{list(self.selections.keys())[i]}"')
                self.assertTrue(runner_buttons[3].is_enabled(),
                                msg=f'ANY button was not enabled for the runner: "{list(self.selections.keys())[i]}"')
            self.assertFalse(
                self.site.virtual_sports.tab_content.event_markets_list.add_to_betslip_button.is_enabled(expected_result=False),
                msg='Add To Betslip button is enabled')
        except Exception as e:
            self._logger.debug(f'*** Virtual sport content refreshed: "{e}"')
            self.site.virtual_sports.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_TRICAST_MARKET_TAB)

    def test_003_tap_3rd_button_for_any_runner(self):
        """
        DESCRIPTION: Tap 3rd button for any runner.
        EXPECTED: - Selected button is highlighted in green. Previously selected button remains green and selected;
        EXPECTED: - 1st, 2nd and ANY button for this runner become disabled;
        EXPECTED: - All other 3rd buttons for all other runners become disabled;
        EXPECTED: - All ANY buttons remain enabled;
        EXPECTED: - Add to Betslip button becomes enabled.
        """
        runner_buttons = self.get_runner_bet_buttons(index=2)
        runner_buttons[2].click()
        sleep(2)
        try:
            self.assertFalse(runner_buttons[0].is_enabled(),
                             msg=f'1nd button was not disabled for the runner "{list(self.selections.keys())[2]}"')
            self.assertFalse(runner_buttons[1].is_enabled(),
                             msg=f'2nd button was not disabled for the runner "{list(self.selections.keys())[2]}"')
            self.assertFalse(runner_buttons[3].is_enabled(),
                             msg=f'ANY button was not disabled for the runner "{list(self.selections.keys())[2]}"')
            for i in range(3, len(self.selections)):
                runner_buttons = self.get_runner_bet_buttons(index=i)
                self.assertFalse(runner_buttons[2].is_enabled(),
                                 msg=f'3rd button was not disabled for the runner: "{list(self.selections.keys())[i]}"')
                self.assertTrue(runner_buttons[3].is_enabled(),
                                msg=f'ANY button was not enabled for the runner: "{list(self.selections.keys())[i]}"')
            self.assertTrue(
                self.site.virtual_sports.tab_content.event_markets_list.add_to_betslip_button.is_enabled(
                    expected_result=True),
                msg='Add To Betslip button is not enabled')
        except Exception as e:
            self._logger.debug(f'*** Virtual sport content refreshed: "{e}"')
            self.site.virtual_sports.tab_content.event_markets_list.market_tabs_list.open_tab(
                vec.racing.RACING_EDP_TRICAST_MARKET_TAB)

    def test_004_tap_any_button_for_any_runner(self):
        """
        DESCRIPTION: Tap ANY button for any runner.
        EXPECTED: - Selected button is highlighted in green;
        EXPECTED: - All 1st 2nd and 3rd buttons became disabled and unhighlighted;
        EXPECTED: - Other ANY buttons remain enabled;
        EXPECTED: - 'Add to Betslip' button becomes disabled.
        """
        for i in range(3, 6):
            self.site.virtual_sports.tab_content.event_markets_list.market_tabs_list.open_tab(self.tab_name)
            runner_buttons = self.get_runner_bet_buttons(index=i)
            runner_buttons[3].click()
            sleep(2)
            for j in range(len(self.selections)):
                self.site.virtual_sports.tab_content.event_markets_list.market_tabs_list.open_tab(self.tab_name)
                try:
                    runner_buttons = self.get_runner_bet_buttons(index=j)
                    self.assertFalse(runner_buttons[0].is_enabled(),
                                     msg=f'1st button was not disabled for the runner: "{list(self.selections.keys())[j]}"')
                    self.assertFalse(runner_buttons[1].is_enabled(),
                                     msg=f'2nd button was not disabled for the runner: "{list(self.selections.keys())[j]}"')
                    self.assertFalse(runner_buttons[2].is_enabled(),
                                     msg=f'3rd button was not disabled for the runner: "{list(self.selections.keys())[j]}"')
                    self.assertTrue(runner_buttons[3].is_enabled(),
                                    msg=f'ANY button was not enabled for the runner: "{list(self.selections.keys())[j]}"')
                    if i == 5:
                        self.assertTrue(
                            self.site.virtual_sports.tab_content.event_markets_list.add_to_betslip_button.is_enabled(
                                expected_result=True),
                            msg='Add To Betslip button is not enabled')
                    else:
                        self.assertFalse(
                            self.site.virtual_sports.tab_content.event_markets_list.add_to_betslip_button.is_enabled(
                                expected_result=False),
                            msg='Add To Betslip button is enabled')
                except Exception as e:
                    self._logger.debug(f'*** Virtual sport content refreshed: "{e}"')

    def test_005_tap_any_button_for_one_more_runner(self):
        """
        DESCRIPTION: Tap ANY button for one more runner.
        EXPECTED: - Selected button is highlighted in green;
        EXPECTED: - All 1st 2nd and 3rd buttons became disabled and unhighlighted;
        EXPECTED: - Other ANY buttons remain enabled;
        EXPECTED: - 'Add to Betslip' button remains disabled.
        """
        # Covered in test step 004

    def test_006_tap_any_button_for_one_more_runner(self):
        """
        DESCRIPTION: Tap ANY button for one more runner.
        EXPECTED: - Selected button and previously tapped button are highlighted in green;
        EXPECTED: - All 1st 2nd and 3rd buttons are still disabled and unhighlighted;
        EXPECTED: - Other ANY buttons remain enabled;
        EXPECTED: - 'Add to Betslip' button becomes enabled.
        """
        # Covered in test step 004
