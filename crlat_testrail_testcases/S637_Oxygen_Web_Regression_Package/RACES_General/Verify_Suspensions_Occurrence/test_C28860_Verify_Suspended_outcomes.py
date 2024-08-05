import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28860_Verify_Suspended_outcomes(Common):
    """
    TR_ID: C28860
    NAME: Verify Suspended outcomes
    DESCRIPTION: This test case verifies Horse Racing events with suspended outcome/outcomes.
    PRECONDITIONS: Make sure there is event with at least one suspended outcome: **outcomeStatusCode="S"**
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYYYY?racingForm=outcome&translationLang=LL
    PRECONDITIONS: Where,
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   YYYYYY is an event ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_race_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon on the sports menu ribbon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_go_to_race_event_details_page_for_event_which_has_suspended_outcomes_outcomestatuscodes(self):
        """
        DESCRIPTION: Go to <Race> event details page for event which has suspended outcomes (**'outcomeStatusCode'**='S')
        EXPECTED: Event Details Page is opened
        """
        pass

    def test_004_go_to_market_section_that_contains_suspended_outcome(self):
        """
        DESCRIPTION: Go to Market section that contains suspended outcome
        EXPECTED: Market section is shown
        """
        pass

    def test_005_verify_suspended_selections(self):
        """
        DESCRIPTION: Verify suspended selections
        EXPECTED: *   Selections are greyed out
        EXPECTED: *   Selections are disabled
        EXPECTED: *   The rest event's selections are enabled with prices
        """
        pass
