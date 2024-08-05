import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28529_First_Second_Half_Correct_Score_market_section_in_case_suspensions_occurrence(BaseBetSlipTest,
                                                                                                BaseSportTest):
    """
    TR_ID: C28529
    NAME: First/Second Half Correct Score market section in case suspensions occurrence
    DESCRIPTION: This test case verifies First Half Correct Score/ Second Half Correct Score /Correct Score markets sections behavior on suspensions occurrence
    DESCRIPTION: **Jira ticket:** BMA-3861
    PRECONDITIONS: To get information for an event use the following url
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Data should be available for Correct Score with H/D/A - Any other.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: In TI create football sport event
        EXPECTED: Event was created
        """
        other_event = self.ob_config.add_autotest_premier_league_football_event(
            markets=[('correct_score', {'cashout': True}),
                     ('first_half_correct_score', {'cashout': True}),
                     ('second_half_correct_score', {'cashout': True})])
        event = self.ob_config.add_autotest_premier_league_football_event(
            markets=[('correct_score', {'cashout': True})])
        event1 = self.ob_config.add_autotest_premier_league_football_event(
            markets=[('first_half_correct_score', {'cashout': True})])
        event2 = self.ob_config.add_autotest_premier_league_football_event(
            markets=[('second_half_correct_score', {'cashout': True})])
        self.__class__.eventID = event.event_id
        self.__class__.eventID1 = event1.event_id
        self.__class__.eventID2 = event2.event_id
        self.__class__.other_event_id = other_event.event_id
        event_list = [self.eventID, self.eventID1, self.eventID2, self.other_event_id]

        for event_id in event_list:
            self.ob_config.change_event_state(event_id=event_id, displayed=True, active=False)

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_tapfootball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '<Football>' icon on the Sports Menu Ribbon
        EXPECTED: *   <Football> Landing Page is opened
        EXPECTED: *   'Leagues & Competitions' sorting type is selected by default
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')

    def test_003_go_to_football_event_details_page_of_suspended_eventwith_attributeeventstatuscodes(self,
                                                                                                    event_id=None):
        """
        DESCRIPTION: Go to Football Event Details page of suspended event
        DESCRIPTION: (with attribute **eventStatusCode="S")**
        EXPECTED: *   Football Event Details page is opened
        EXPECTED: *   'Main Markets' collection is selected by default
        """
        if event_id is None:
            event = self.eventID
        else:
            event = event_id
        self.navigate_to_edp(event_id=event)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        if self.brand == 'bma':
            self.assertEqual(current_tab, self.expected_market_tabs.main,
                             msg=f'Main Markets is not active tab, active tab is "{current_tab}"')
            all_markets_tab = vec.siteserve.EXPECTED_MARKET_TABS.all_markets
            self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=all_markets_tab)
        else:
            self.assertEqual(current_tab, self.expected_market_tabs.all_markets,
                             msg=f'Main Markets is not active tab, active tab is "{current_tab}"')

    def test_004_verify_correct_score_marketof_suspended_event(self, market_name=None):
        """
        DESCRIPTION: Verify Correct Score market of suspended event
        EXPECTED: *   'Add to Betslip N/A' disabled button is shown
        EXPECTED: *   Selections and controls within are disabled and it's impossible to make a bet
        """
        if market_name is None:
            market_name = self.expected_market_sections.correct_score
        all_markets_tab = vec.siteserve.EXPECTED_MARKET_TABS.all_markets
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=all_markets_tab)
        self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict[market_name].expand()
        add_to_betslip_button = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict[
            market_name].add_to_betslip_button.name
        self.assertEqual(add_to_betslip_button, "N/A",
                         msg=f'Add to Betslip button is not disabled "{add_to_betslip_button}"')

    def test_005_go_to_other_football_event_details_page(self, event_id=None):
        """
        DESCRIPTION: Go to other Football Event Details Page
        EXPECTED: Event Details page is opened
        """
        if event_id is None:
            event_id = self.eventID
        self.navigate_to_edp(event_id=event_id)

    def test_006_verify_correct_score_section_in_case_of_market_suspension(self, market_name=None):
        """
        DESCRIPTION: Verify Correct Score section in case of market suspension
        EXPECTED: *   If Correct Score market** **are with attribute **marketStatusCode="S",  **Market is disabled and it's imposible to make a bet
        EXPECTED: *   'Add to Betslip N/A' disabled button is shown
        EXPECTED: *   Selections and controls within are disabled and it's impossible to make a bet
        """
        if market_name is None:
            market_name = self.expected_market_sections.correct_score
        self.test_004_verify_correct_score_marketof_suspended_event(market_name=market_name)

    def test_007_go_to_other_football_event_details_page(self):
        """
        DESCRIPTION: Go to other Football Event Details Page
        EXPECTED: Event Details page is opened
        """
        self.test_005_go_to_other_football_event_details_page(event_id=self.other_event_id)

    def test_008_verify_outcome_of_correct_score_market_section_with_attribute_outcomestatuscodes(self, market_name=None):
        """
        DESCRIPTION: Verify outcome of Correct Score market section with attribute **outcomeStatusCode="S" **
        EXPECTED: *   Selection is disabled with prices
        EXPECTED: *   The rest event's selections are enabled with prices
        """
        if market_name is None:
            market_name = self.expected_market_sections.correct_score
        self.test_004_verify_correct_score_marketof_suspended_event(market_name=market_name)

    def test_009_repeat_steps_3_8_for_first_half_correct_score_market_section(self):
        """
        DESCRIPTION: Repeat steps 3-8 for First Half Correct Score market section
        EXPECTED:
        """
        self.test_003_go_to_football_event_details_page_of_suspended_eventwith_attributeeventstatuscodes(event_id=self.eventID1)
        self.test_004_verify_correct_score_marketof_suspended_event(market_name=self.expected_market_sections.first_half_correct_score)
        self.test_005_go_to_other_football_event_details_page(event_id=self.other_event_id)
        self.test_006_verify_correct_score_section_in_case_of_market_suspension(market_name=self.expected_market_sections.first_half_correct_score)
        self.test_007_go_to_other_football_event_details_page()
        self.test_008_verify_outcome_of_correct_score_market_section_with_attribute_outcomestatuscodes(market_name=self.expected_market_sections.first_half_correct_score)

    def test_010_repeat_steps_3_8_for_second_half_correct_score_section(self):
        """
        DESCRIPTION: Repeat steps 3-8 for Second Half Correct Score section
        EXPECTED:
        """
        self.test_003_go_to_football_event_details_page_of_suspended_eventwith_attributeeventstatuscodes(
            event_id=self.eventID2)
        self.test_004_verify_correct_score_marketof_suspended_event(
            market_name=self.expected_market_sections.second_half_correct_score)
        self.test_005_go_to_other_football_event_details_page(event_id=self.other_event_id)
        self.test_006_verify_correct_score_section_in_case_of_market_suspension(
            market_name=self.expected_market_sections.second_half_correct_score)
        self.test_007_go_to_other_football_event_details_page()
        self.test_008_verify_outcome_of_correct_score_market_section_with_attribute_outcomestatuscodes(
            market_name=self.expected_market_sections.second_half_correct_score)
