import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.homepage_featured
@vtest
class Test_C29407_Verify_Handicap_Value_Displaying_on_Event_Landing_Page(Common):
    """
    TR_ID: C29407
    NAME: Verify Handicap Value Displaying on Event Landing Page
    DESCRIPTION: This test case verifies handicap value on Event Landin Page for events which outcomes have handicap value available
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'handicapValueDec' **on outcome level- to see whether handicap value is available for outcome
    """
    keep_browser_open = True

    def test_001_on_cms_configure_featured_tab_in_such_way_that_event_whose_selections_for_primary_market_have_handicap_market_available(self):
        """
        DESCRIPTION: On CMS configure Featured tab in such way that event whose selections for primary market have handicap market available
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_load_invictus(self):
        """
        DESCRIPTION: Load Invictus
        EXPECTED: 
        """
        pass

    def test_003_go_to_the_featured_tab___find_verified_event(self):
        """
        DESCRIPTION: Go to the 'Featured' tab -> find verified event
        EXPECTED: 
        """
        pass

    def test_004_verify_selections_for_primary_market(self):
        """
        DESCRIPTION: Verify selections for Primary market
        EXPECTED: Event section is shown
        EXPECTED: Selections are shown with a handicap values
        """
        pass

    def test_005_verify_the_handicap_value_correctness(self):
        """
        DESCRIPTION: Verify the handicap value correctness
        EXPECTED: Handicap value corresponds to the **'handicapValueDec'** from the Site Server response
        """
        pass

    def test_006_verify_the_handicap_value_displaying(self):
        """
        DESCRIPTION: Verify the handicap value displaying
        EXPECTED: Handicap value is displayed within the event name. (corresponding handicap value is shown just after the team name)
        EXPECTED: e.g. 'Roma (+1) vs Barselona (-2)'
        EXPECTED: Handicap value is displayed in parentheses
        """
        pass

    def test_007_verify_sign_for_handicap_value(self):
        """
        DESCRIPTION: Verify sign for handicap value
        EXPECTED: *   If **'handicapValueDec' **contains '-' sign - display it with this '-' sign (negative value) on the front end
        EXPECTED: *   If **'handicapValueDec'** contains '+' sign in the response - display '+' sign before the value on front end
        EXPECTED: *   If If **'handicapValueDec'** doesn't contain any sign (e.g. 2) - display '+' sign before the value on the front end
        """
        pass

    def test_008_verify_selections_without_handicap_value_available(self):
        """
        DESCRIPTION: Verify selections without handicap value available
        EXPECTED: Handicap value is NOT shown near the outcome name
        """
        pass
