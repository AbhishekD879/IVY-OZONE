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
class Test_C28442_Old_Functionality_Verify_Handicap_Value_Displaying_on_Event_Landing_Page(Common):
    """
    TR_ID: C28442
    NAME: [Old Functionality] Verify Handicap Value Displaying on Event Landing Page
    DESCRIPTION: This test case verifies handicap value on Event Landin Page for events which outcomes have handicap value available
    DESCRIPTION: **Jira Tickets:** BMA - 5049
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'handicapValueDec' **on outcome level- to see whether handicap value is available for outcome
    """
    keep_browser_open = True

    def test_001_load_oxygen(self):
        """
        DESCRIPTION: Load Oxygen
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_sport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on the Sports Menu Ribbon
        EXPECTED: <Sport> Landign page is opened
        """
        pass

    def test_003_go_to_the_event_section_whose_selections_for_primary_market_have_handicap_value_available(self):
        """
        DESCRIPTION: Go to the event section whose selections for Primary market have handicap value available
        EXPECTED: Event section is shown
        """
        pass

    def test_004_verify_the_handicap_value_correctness(self):
        """
        DESCRIPTION: Verify the handicap value correctness
        EXPECTED: Handicap value corresponds to the **'handicapValueDec'** from the Site Server response
        """
        pass

    def test_005_verify_the_handicap_value_displaying(self):
        """
        DESCRIPTION: Verify the handicap value displaying
        EXPECTED: Handicap value is displayed within the event name. (corresponding handicap value is shown just after the team name)
        EXPECTED: e.g. 'Roma (+1) vs Barselona (-2)'
        EXPECTED: Handicap value is displayed in parentheses
        """
        pass

    def test_006_verify_sign_for_handicap_value(self):
        """
        DESCRIPTION: Verify sign for handicap value
        EXPECTED: *   If **'handicapValueDec' **contains '-' sign - display it with this '-' sign (negative value) on the front end
        EXPECTED: *   If **'handicapValueDec'** contains '+' sign in the response - display '+' sign before the value on front end
        EXPECTED: *   If If **'handicapValueDec'** doesn't contain any sign (e.g. 2) - display '+' sign before the value on the front end
        """
        pass

    def test_007_verify_selections_without_handicap_value_available(self):
        """
        DESCRIPTION: Verify selections without handicap value available
        EXPECTED: Handicap value is NOT shown near the outcome name
        """
        pass

    def test_008_check_events_for_all_tabsin_play_matches_coupons_outrights(self):
        """
        DESCRIPTION: Check events for all tabs:
        DESCRIPTION: **In-Play, Matches, Coupons, Outrights**
        EXPECTED: 
        """
        pass
