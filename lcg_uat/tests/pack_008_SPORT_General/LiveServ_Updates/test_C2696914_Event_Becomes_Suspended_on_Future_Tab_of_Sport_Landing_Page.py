import pytest

import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.slow
@pytest.mark.timeout(800)
@vtest
class Test_C2696914_Event_Becomes_Suspended_on_Future_tab_of_Sport_Landing_Page(BaseSportTest):
    """
    TR_ID: C2696914
    VOL_ID: C9697784
    NAME: Event/Market/Selection becomes Suspended/Active on Future tab of <Sport> Landing page
    DESCRIPTION: This test case verifies suspension/un-suspension of Event on Future tab of <Sport> Landing page
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        event_params = self.ob_config.add_football_event_to_autotest_league2(
            start_time=self.get_date_time_formatted_string(days=7))

        self.__class__.eventID = event_params.event_id
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_league2.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.marketID = self.ob_config.market_ids[self.eventID][market_short_name]

        self.__class__.selection_name = event_params.team1
        self.__class__.selection_id = event_params.selection_ids[event_params.team1]

    def test_001_open_future_tab_of_sport_landing_page(self):
        """
        DESCRIPTION: Open Future tab of <Sport> Landing page
        EXPECTED: Future tab is selected
        """
        self.navigate_to_page('sport/football')
        self.site.wait_content_state(state_name='Football')
        self.site.sports_page.date_tab.future.click()
        self.assertEqual(self.site.sports_page.date_tab.current_date_tab, vec.sb.SPORT_DAY_TABS.future,
                         msg=f'Current active date tab: "{self.site.sports_page.date_tab.current_date_tab}", '
                             f'expected: "{vec.sb.SPORT_DAY_TABS.future}"')

    def test_002_suspend_the_event(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **eventStatusCode="S"**
        DESCRIPTION: and at the same time have <Sport> Landing page opened to watch for updates
        """
        self.__class__.section = self.get_section(section_name=tests.settings.football_autotest_league2)
        self.section.expand()

        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: Price/Odds buttons of this event are displayed immediately as greyed out and become disabled on <Sport> Landing page but still displaying the prices
        """
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=tests.settings.football_autotest_league2,
                                        level='event',
                                        expected_result=False)

    def test_004_make_event_active_again(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **eventStatusCode="A" **
        DESCRIPTION: and at the same time have <Sport> Landing page opened to watch for updates
        EXPECTED: All Price/Odds buttons of this event are no more disabled, they become active immediately
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=tests.settings.football_autotest_league2,
                                        level='event')

    def test_005_verify_event_suspension_in_collapsed_section(self):
        """
        DESCRIPTION: Verify event suspension in collapsed section
        EXPECTED: If section is collapsed and event was suspended, then after expanding the section Price/Odds buttons of this event are shown as greyed out and disabled
        """
        self.__class__.section = self.get_section(section_name=tests.settings.football_autotest_league2)
        self.section.collapse()
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=tests.settings.football_autotest_league2,
                                        level='event',
                                        expected_result=False)

        self.__class__.section = self.get_section(section_name=tests.settings.football_autotest_league2)
        self.section.collapse()
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=tests.settings.football_autotest_league2,
                                        level='event')

    def test_006_repeat_steps_2_5_for_market_level(self):
        """
        DESCRIPTION: Repeat steps 2-5 for Suspension on Market level: marketStatusCode="S", marketStatusCode="A"
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=False)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=tests.settings.football_autotest_league2,
                                        level='market',
                                        expected_result=False)

        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=tests.settings.football_autotest_league2,
                                        level='market')

        self.__class__.section = self.get_section(section_name=tests.settings.football_autotest_league2)
        self.section.collapse()
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=False)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=tests.settings.football_autotest_league2,
                                        level='market',
                                        expected_result=False)

        self.__class__.section = self.get_section(section_name=tests.settings.football_autotest_league2)
        self.section.collapse()
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=tests.settings.football_autotest_league2,
                                        level='market')

    def test_007_repeat_steps_2_5_for_outcome_level(self):
        """
        DESCRIPTION: Repeat steps 2-5 for Suspension on Market level: outcomeStatusCode="S", outcomeStatusCode="A"
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=False)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=tests.settings.football_autotest_league2,
                                        level='selection',
                                        expected_result=False)

        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=True)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=tests.settings.football_autotest_league2,
                                        level='selection')

        self.__class__.section = self.get_section(section_name=tests.settings.football_autotest_league2)
        self.section.collapse()
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=False)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=tests.settings.football_autotest_league2,
                                        expected_result=False,
                                        level='selection')

        self.__class__.section = self.get_section(section_name=tests.settings.football_autotest_league2)
        self.section.collapse()
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=True)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=tests.settings.football_autotest_league2,
                                        level='selection')
