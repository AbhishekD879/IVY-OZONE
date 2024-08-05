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
class Test_C28491_Verify_Market_with_Handicap_Values_for_Outright_Event_Details_Page(Common):
    """
    TR_ID: C28491
    NAME: Verify Market with Handicap Values for Outright Event Details Page
    DESCRIPTION: This test case verifies markets which selections have handicap values available on SS response.
    DESCRIPTION: NOTE, User Story **BMA-5049**
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'handicapValueDec' **on outcome level- to see whether handicap value is available for outcome
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_ltsportgticon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '&lt;Sport&gt;'  icon on the Sports Menu Ribbon
        EXPECTED: &lt;Sport&gt; Landing Page is opened
        """
        pass

    def test_003_tap_event_name_on_the_event_section(self):
        """
        DESCRIPTION: Tap Event Name on the event section
        EXPECTED: &lt;Sport&gt; Event Details page is opened
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
        EXPECTED: (e.g. &lt;Outcome Name&gt; (handicap value))
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
