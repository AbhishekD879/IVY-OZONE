import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@pytest.mark.desktop
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-49471')
@vtest
class Test_C331554_Verify_remember_last_Sport_functionality_on_In_Play_page_for_Logged_Out_user(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C331554
    NAME: Verify remember last Sport functionality on In-Play page for Logged Out user
    DESCRIPTION: This test case verifies remember last Sport functionality on In-Play page for Logged Out user
    DESCRIPTION: To be run on mobile, tablet and desktop.
    PRECONDITIONS: 1. User should be logged out
    """
    keep_browser_open = True
    sport_name = 'In-Play'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Football event
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.selection_ids = self.get_active_event_selections_for_category(
                category_id=self.ob_config.football_config.category_id)
            self.__class__.team1 = list(self.selection_ids.keys())[0]
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
                event_params.team1, event_params.team2, event_params.selection_ids
        self._logger.info(f'*** Found Football event with selection ids "{self.selection_ids}"')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED:
        """
        self.site.wait_content_state('Homepage')

    def test_002_go_to_in_play_page(self):
        """
        DESCRIPTION: Go to In-Play page
        EXPECTED: * 'In-Play' Landing Page is opened
        EXPECTED: * First <Sport> tab is opened by default
        EXPECTED: * Two sections are visible: 'Live Now' and 'Upcoming'
        """
        self.navigate_to_page(name='in-play')
        self.site.wait_content_state('IN-PLAY')

        live_now_section = vec.inplay.LIVE_NOW_SWITCHER if not self.brand == 'ladbrokes' else vec.inplay.LIVE_NOW_EVENTS_SECTION

        self.assertTrue(self.site.inplay.inplay_sport_menu.items_as_ordered_dict,
                        msg='There is not any sport in In-Play tab')
        self.__class__.chosen_sport = list(self.get_inplay_sport_menu_items().keys())[-1]
        self.__class__.default_sport = list(self.get_inplay_sport_menu_items().keys())[1]
        self.verify_active_sport_on_inplay_page(self.default_sport)
        if self.device_type == 'mobile':
            self.assertTrue(all(item in self.site.inplay.tab_content.items_names for item in [live_now_section,
                                                                                              vec.inplay.UPCOMING_EVENTS_SECTION]),
                            msg="'Live Now' and 'Upcoming' filters should be visible")
        else:
            expected_sorting_types_buttons = [vec.inplay.LIVE_NOW_SWITCHER.upper(),
                                              vec.inplay.UPCOMING_SWITCHER]
            expected_active_btn = vec.inplay.LIVE_NOW_SWITCHER.upper()
            self.verify_sorting_type_buttons(expected_sorting_types_buttons=expected_sorting_types_buttons,
                                             expected_active_btn=expected_active_btn)

    def test_003_choose_any_sports_icon(self):
        """
        DESCRIPTION: Choose any Sports icon
        EXPECTED: * Selected Sports tab is underlined by red line
        EXPECTED: * The appropriate content is displayed for selected Sports
        """
        self.site.inplay.inplay_sport_menu.click_item(item_name=self.chosen_sport)
        inplay_page = self.site.wait_content_state(state_name='In-Play', timeout=1,
                                                   raise_exceptions=False)  # added due to BMA-49471 for correct exception
        self.assertTrue(inplay_page, msg=f'User navigated away from "In-Play" page after clicking "{self.chosen_sport}"')
        self.verify_active_sport_on_inplay_page(self.chosen_sport)

    def test_004_navigate_across_application(self):
        """
        DESCRIPTION: Navigate across application
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.team1]))
        self.site.close_betslip()
        self.site.go_to_home_page()

    def test_005_back_to_in_play_page(self):
        """
        DESCRIPTION: Back to In-Play page
        EXPECTED: * 'In-Play' Landing Page is opened
        EXPECTED: * First <Sport> tab is opened by default and underlined by red line
        EXPECTED: * Two sections are visible: 'Live Now' and 'Upcoming'
        """
        self.test_002_go_to_in_play_page()
