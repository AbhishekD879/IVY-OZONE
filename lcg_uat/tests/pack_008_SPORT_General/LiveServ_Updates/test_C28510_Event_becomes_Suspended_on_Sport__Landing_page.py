import pytest

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.slow
@vtest
class Test_C28510_Event_Becomes_Suspended_on_Today_Tab_of_Sport_Landing_Page(BaseSportTest):
    """
    TR_ID: C28510
    NAME: Event/Market/Selection becomes Suspended/Active on Today tab of <Sport> Landing page
    DESCRIPTION: This test case verifies suspension/un-suspension of Event on Today tab of <Sport> Landing page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        event_params = self.ob_config.add_football_event_to_autotest_league2()
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_league2.market_name.replace('|', '').replace(' ', '_').lower()

        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.event_name}"')

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

        self.__class__.marketID = self.ob_config.market_ids[self.eventID][market_short_name]

        self.__class__.selection_name = event_params.team1
        self.__class__.selection_id = event_params.selection_ids[event_params.team1]

    def test_001_open_matches_tab_of_sport_landing_page(self):
        """
        DESCRIPTION: Open 'Matches' tab of <Sport> Landing page
        EXPECTED: 'Matches' tab  is selected
        """
        self.navigate_to_page('sport/football')
        self.site.wait_content_state(state_name='Football')

        current_tab_name = self.site.football.tabs_menu.current
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.football_config.category_id)
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Current active tab: "{current_tab_name}", instead of "{expected_tab_name}"')

    def test_002_suspend_the_event(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **eventStatusCode="S"**
        DESCRIPTION: and at the same time have <Sport> Landing page opened to watch for updates
        """
        self.__class__.section = self.get_section(section_name=self.section_name)
        self.section.expand()

        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: Price/Odds buttons of this event are displayed immediately as greyed out
        EXPECTED: and become disabled on <Sport> Landing page but still displaying the prices
        """
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=self.section_name,
                                        level='event',
                                        expected_result=False)

    def test_004_make_event_active_again(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **eventStatusCode="A" **
        DESCRIPTION: and at the same time have <Sport> Landing page opened to watch for updates
        EXPECTED: All Price/Odds buttons of this event are no more disabled, they become active immediately
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)

        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=self.section_name,
                                        level='event')

    def test_005_verify_event_suspension_in_collapsed_section(self):
        """
        DESCRIPTION: Verify event suspension in collapsed section
        EXPECTED: If section is collapsed and event was suspended,
        EXPECTED: then after expanding the section Price/Odds buttons of this event are shown as greyed out and disabled
        """
        self.__class__.section = self.get_section(section_name=self.section_name)
        self.section.collapse()

        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=self.section_name,
                                        level='event',
                                        expected_result=False)

        self.__class__.section = self.get_section(section_name=self.section_name)
        self.section.collapse()

        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=self.section_name,
                                        level='event')

    def test_006_repeat_steps_2_5_for_market_level(self):
        """
        DESCRIPTION: Repeat steps 2-5 for Suspension on Market level: marketStatusCode="S", marketStatusCode="A"
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=False)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=self.section_name,
                                        level='market',
                                        expected_result=False)

        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=self.section_name,
                                        level='market')

        self.__class__.section = self.get_section(section_name=self.section_name)
        self.section.collapse()
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=False)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=self.section_name,
                                        level='market',
                                        expected_result=False)

        self.__class__.section = self.get_section(section_name=self.section_name)
        self.section.collapse()
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=self.section_name,
                                        level='market')

    def test_007_repeat_steps_2_5_for_outcome_level(self):
        """
        DESCRIPTION: Repeat steps 2-5 for Suspension on Market level: outcomeStatusCode="S", outcomeStatusCode="A"
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=False)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=self.section_name,
                                        level='selection',
                                        expected_result=False)

        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=True)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=self.section_name,
                                        level='selection')

        self.__class__.section = self.get_section(section_name=self.section_name)
        self.section.collapse()
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=False)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=self.section_name,
                                        level='selection',
                                        expected_result=False)

        self.__class__.section = self.get_section(section_name=self.section_name)
        self.section.collapse()
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=True)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=self.section_name,
                                        level='selection')
