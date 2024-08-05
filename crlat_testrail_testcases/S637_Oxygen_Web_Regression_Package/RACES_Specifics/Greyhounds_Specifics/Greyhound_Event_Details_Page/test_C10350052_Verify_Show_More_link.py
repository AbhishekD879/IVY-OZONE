import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C10350052_Verify_Show_More_link(Common):
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

    def test_001_verify_that_show_more_link_is_displayed_for_selections(self):
        """
        DESCRIPTION: Verify that 'SHOW MORE' link is displayed for selection(s)
        EXPECTED: 'SHOW MORE' link with down chevron arrow is displayed after 'Form' information for selection(s)
        """
        pass

    def test_002_tap_on_show_more_link(self):
        """
        DESCRIPTION: Tap on 'SHOW MORE' link
        EXPECTED: - Race card expands showing the Comment text
        EXPECTED: - 'SHOW MORE' link becomes 'SHOW LESS' link with up chevron arrow
        """
        pass

    def test_003_tap_on_show_less_link(self):
        """
        DESCRIPTION: Tap on 'SHOW LESS' link
        EXPECTED: - Race card collapses hiding the Comment text
        EXPECTED: - 'SHOW LESS' link returns to 'SHOW MORE' link with down chevron arrow
        """
        pass

    def test_004_expand_in_2_or_more_race_cards_by_tapping_show_more_links(self):
        """
        DESCRIPTION: Expand in 2 or more Race cards by tapping 'SHOW MORE' links
        EXPECTED: - All selected Race cards expanded showing the Comments text
        EXPECTED: - 'SHOW MORE' links become 'SHOW LESS' links with up chevron arrow
        """
        pass

    def test_005_collapse_expanded_race_cards(self):
        """
        DESCRIPTION: Collapse expanded Race cards
        EXPECTED: - All selected Race cards collapsed, Comments text hided
        EXPECTED: - 'SHOW LESS' links returned to 'SHOW MORE' link with down chevron arrow
        """
        pass
