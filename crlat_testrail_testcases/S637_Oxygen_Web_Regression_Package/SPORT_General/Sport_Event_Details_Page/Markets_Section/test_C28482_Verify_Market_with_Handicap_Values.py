import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28482_Verify_Market_with_Handicap_Values(Common):
    """
    TR_ID: C28482
    NAME: Verify Market with Handicap Values
    DESCRIPTION: This test case verifies markets which selections have handicap values available on SS response.
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: BMA-5049
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'handicapValueDec' **on outcome level- to see whether handicap value is available for outcome
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_sporticon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '<Sport>'  icon on the Sports Menu Ribbon
        EXPECTED: <Sport> Landing Page is opened
        """
        pass

    def test_003_go_to_the_outright_event_details_page(self):
        """
        DESCRIPTION: Go to the Outright Event details page
        EXPECTED: Event Details page is opened
        """
        pass

    def test_004_open_market_which_selections_have_handicap_value_available(self):
        """
        DESCRIPTION: Open market which selections have handicap value available
        EXPECTED: 
        """
        pass

    def test_005_verify_the_handicap_value(self):
        """
        DESCRIPTION: Verify the handicap value
        EXPECTED: Handicap value corresponds to the **'handicapValueDec'** from the Site Server response
        """
        pass

    def test_006_verify_the_handicap_value_displaying(self):
        """
        DESCRIPTION: Verify the handicap value displaying
        EXPECTED: Handicap value is displayed directly to the right of the outcome names
        EXPECTED: Handicap value is displayed in parentheses
        EXPECTED: (e.g. <Outcome Name> (handicap value))
        """
        pass

    def test_007_verify_sign_for_handicap_value(self):
        """
        DESCRIPTION: Verify sign for handicap value
        EXPECTED: *   If **'handicapValueDec' **contains '-' sign - display it with this '-' sign (negative value) on the front end
        EXPECTED: *   If **'handicapValueDec'** contains '+' sign in the response - display '+' sign before the value on front end
        EXPECTED: *   If If **'handicapValueDec'** doesn't contain any sign (e.g. 2) - display '+' sign before the value on the front end
        """
        pass

    def test_008_verify_selections_without_handicap_value_available(self):
        """
        DESCRIPTION: Verify selections without handicap value available
        EXPECTED: Handicap value is NOT shown near the outcome name
        """
        pass
