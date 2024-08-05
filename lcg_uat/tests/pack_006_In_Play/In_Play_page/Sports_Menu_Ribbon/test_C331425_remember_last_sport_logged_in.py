
import pytest

import tests
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
@pytest.mark.login
@vtest
class Test_C331425_Verify_remember_last_Sport_functionality_on_In_Play_page_for_Logged_In_user(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C331425
    NAME: Verify remember last Sport functionality on In-Play page for Logged In user
    DESCRIPTION: This test case verifies remember last Sport functionality on In-Play page for Logged In user
    PRECONDITIONS: TI (events) config:
    PRECONDITIONS: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Category, where X.XX - the latest OpenBet release
    PRECONDITIONS: Load Oxygen application
    PRECONDITIONS: Log in
    """
    keep_browser_open = True
    sport_name = 'In-Play'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Football event
        PRECONDITIONS: Log in
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
        self.site.login()

    def test_001_go_to_in_play_page(self):
        """
        DESCRIPTION: Go to In-Play page
        EXPECTED: * 'In-Play' page is opened
        EXPECTED: * First <Sport> tab is opened by default
        """
        if self.device_type == 'desktop':
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertIn('IN-PLAY', sports.keys(), msg='IN-PLAY is not found in the header sport menu')
            sports.get('IN-PLAY').click()
            self.assertTrue(sports['IN-PLAY'].is_selected(), msg='IN-PLAY is not selected after clicking on it')
        else:
            self.site.open_sport(name=self.sport_name, timeout=10)
        self.assertTrue(self.site.inplay.inplay_sport_menu.items_as_ordered_dict,
                        msg='There is not any sport in In-Play tab')
        self.__class__.chosen_sport = list(self.site.inplay.inplay_sport_menu.items_as_ordered_dict.keys())[2]
        self.__class__.default_sport = list(self.site.inplay.inplay_sport_menu.items_as_ordered_dict.keys())[1]
        self.verify_active_sport_on_inplay_page(self.default_sport)

    def test_002_choose_any_sports_icon(self):
        """
        DESCRIPTION: Choose any Sports icon
        EXPECTED: * Selected Sports tab is underlined by red line
        EXPECTED: * The appropriate content is displayed for selected Sports
        """
        self.site.inplay.inplay_sport_menu.click_item(self.chosen_sport)
        self.verify_active_sport_on_inplay_page(self.chosen_sport)

    def test_003_navigate_across_application(self):
        """
        DESCRIPTION: Navigate across application
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])
        self.site.close_betslip()
        self.site.go_to_home_page()
        self.site.wait_content_state(state_name='Homepage')

    def test_004_back_to_in_play_page(self):
        """
        DESCRIPTION: Back to In-Play page
        EXPECTED: * 'In-Play' page is opened
        EXPECTED: * Tab from step 2 is selected and underlined by red line
        """
        if self.device_type == 'desktop':
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertIn('IN-PLAY', sports.keys(), msg='IN-PLAY is not found in the header sport menu')
            sports.get('IN-PLAY').click()
            self.assertTrue(sports['IN-PLAY'].is_selected(), msg='IN-PLAY is not selected after clicking on it')
        else:
            self.site.open_sport(name=self.sport_name, timeout=10)
        self.verify_active_sport_on_inplay_page(self.chosen_sport)

    def test_005_repeat_steps_1_4_when_there_are_no_in_play_events_for_saved_sport(self):
        """
        DESCRIPTION: Repeat steps 1-4 when there are no In-Play events for saved sport
        EXPECTED: * 'In-Play' Landing Page is opened
        EXPECTED: * First <Sport> tab is opened by default and underlined by red line
        """
        # We should skip this step because it requires to delete all live events from some sport
