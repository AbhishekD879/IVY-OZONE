import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.greyhounds
@pytest.mark.event_details
@vtest
class Test_C10350052_Verify_Show_More_link(BaseGreyhound):
    """
    TR_ID: C10350052
    NAME: Verify 'Show More' link
    DESCRIPTION: This test case verifies ability to see 'Show More' link for each dog
    PRECONDITIONS: update: After BMA-40744 implementation we'll use RDH feature toggle:
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: we'll receive needed data from DF api:
    PRECONDITIONS: Racing Data Hub link:
    PRECONDITIONS: Coral DEV : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: Ladbrokes DEV : https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: URI : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: {categoryKey} : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: {eventKey} : OB Event id
    PRECONDITIONS: -------
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User is at Greyhound Race Card (Event Details page)
    PRECONDITIONS: - 'Comment' information for slection(s) is present in response from DF API https://raceinfo-api.ladbrokes.com/race_info/ladbrokesdog/[eventID]
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get Greyhound Race Event
        """
        event_info = self.get_event_details(datafabric_data=True)
        event_id = event_info.event_id
        self.navigate_to_edp(event_id=event_id, sport_name='greyhound-racing')
        self.site.wait_content_state(state_name='GreyHoundEventDetails')

        markets_tabs = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list
        if markets_tabs.current != vec.racing.RACING_EDP_MARKET_TABS.win_or_ew:
            markets_tabs.open_tab(vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
            self.site.wait_content_state_changed(timeout=5)

        markets = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        self.__class__.market = list(markets.values())[0]
        self.__class__.outcomes = self.market.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='Market does not have any items')

    def test_001_verify_that_show_more_link_is_displayed_for_selections(self):
        """
        DESCRIPTION: Verify that 'SHOW MORE' link is displayed for selection(s)
        EXPECTED: 'SHOW MORE' link with down chevron arrow is displayed after 'Form' information for selection(s)
        """
        for outcome_name, outcome in list(self.outcomes.items())[:4] if len(
                self.outcomes) > 4 else self.outcomes.items():
            self.outcomes = self.market.items_as_ordered_dict
            outcome.scroll_to()
            if 'Unnamed' not in outcome_name and not outcome.is_non_runner:
                self.assertTrue(outcome.has_show_summary_toggle(),
                                msg=f'Show more button is not present for "{outcome_name}"')
                if outcome.toggle_icon_name.lower() != vec.racing.SHOW_LESS.lower():
                    expected_button_name = 'Show More'
                    result = wait_for_result(
                        lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_MORE.lower(),
                        name=f'Button name {vec.racing.SHOW_MORE}',
                        timeout=1)
                    self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_MORE}" '
                                                f'is not same as expected "{expected_button_name}" for outcome: {outcome_name}')
                    outcome.show_summary_toggle.click()
                self.assertTrue(wait_for_result(lambda: outcome.has_expanded_summary(), timeout=5),
                                msg=f'Summary is not shown for outcome "{outcome_name}" after expanding selection')
                has_spotlight_info = outcome.expanded_summary.has_spotlight_info
                self.assertTrue(has_spotlight_info, msg="SPOTLIGHT info is not shown")

                expected_button_name = 'Show Less'
                result = wait_for_result(
                    lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_LESS.lower(),
                    name=f'Button name {vec.racing.SHOW_LESS}',
                    timeout=1)
                self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_LESS}" '
                                            f'is the same as expected "{expected_button_name}"for outcome: {outcome_name}')

    def test_002_tap_on_show_more_link(self):
        """
        DESCRIPTION: Tap on 'SHOW MORE' link
        EXPECTED: - Race card expands showing the Comment text
        EXPECTED: - 'SHOW MORE' link becomes 'SHOW LESS' link with up chevron arrow
        """
        # Covered in step 001

    def test_003_tap_on_show_less_link(self):
        """
        DESCRIPTION: Tap on 'SHOW LESS' link
        EXPECTED: - Race card collapses hiding the Comment text
        EXPECTED: - 'SHOW LESS' link returns to 'SHOW MORE' link with down chevron arrow
        """
        for outcome_name, outcome in list(self.outcomes.items())[:4] if len(
                self.outcomes) > 4 else self.outcomes.items():
            self.outcomes = self.market.items_as_ordered_dict
            outcome.scroll_to()
            if 'Unnamed' not in outcome_name and not outcome.is_non_runner:
                self.assertTrue(outcome.has_show_summary_toggle(),
                                msg=f'Show more button is not present for "{outcome_name}"')
                if outcome.toggle_icon_name.lower() != vec.racing.SHOW_MORE.lower():
                    expected_button_name = 'Show Less'
                    result = wait_for_result(
                        lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_LESS.lower(),
                        name=f'Button name {vec.racing.SHOW_LESS}',
                        timeout=1)
                    self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_LESS}" '
                                                f'is not same as expected "{expected_button_name}" for outcome: {outcome_name}')
                    outcome.show_summary_toggle.click()
                self.assertFalse(wait_for_result(lambda: outcome.has_expanded_summary(expected_result=False), timeout=5),
                                 msg=f'Summary is shown for outcome "{outcome_name}" after expanding selection')
                expected_button_name = 'Show More'
                result = wait_for_result(
                    lambda: outcome.toggle_icon_name.lower() == vec.racing.SHOW_MORE.lower(),
                    name=f'Button name {vec.racing.SHOW_MORE}',
                    timeout=1)
                self.assertTrue(result, msg=f'Button name "{vec.racing.SHOW_MORE}" '
                                            f'is the same as expected "{expected_button_name}"for outcome: {outcome_name}')

    def test_004_expand_in_2_or_more_race_cards_by_tapping_show_more_links(self):
        """
        DESCRIPTION: Expand in 2 or more Race cards by tapping 'SHOW MORE' links
        EXPECTED: - All selected Race cards expanded showing the Comments text
        EXPECTED: - 'SHOW MORE' links become 'SHOW LESS' links with up chevron arrow
        """
        # Covered in step 003

    def test_005_collapse_expanded_race_cards(self):
        """
        DESCRIPTION: Collapse expanded Race cards
        EXPECTED: - All selected Race cards collapsed, Comments text hided
        EXPECTED: - 'SHOW LESS' links returned to 'SHOW MORE' link with down chevron arrow
        """
        # Covered in step 003
