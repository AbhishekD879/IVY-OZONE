import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C869680_Making_a_Few_Singles_Selections(Common):
    """
    TR_ID: C869680
    NAME: Making a Few Singles Selections
    DESCRIPTION: This test case verifies how several single selections should be added to the Bet Slip
    DESCRIPTION: NOTE, **User Story:** BMA-3156 [Customer can add VS selections to the BMA bet slip]
    PRECONDITIONS: In order to get information from the  SiteServer about event (Horse Racing class id 285) use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForClass/285?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: x.xx - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: 'name' on outcome level to verify selection name
    PRECONDITIONS: 'name' on market level - to verify market name
    PRECONDITIONS: 'name' on event level - to verify event name
    PRECONDITIONS: 'startTime' on event level - to verify event start time and event start date​
    PRECONDITIONS: 'PriceNum', 'PriceDen' on the outcome level - to see odds for selection in fraction format​
    PRECONDITIONS: 'priceDec' in the outcome level - to see odds for selection in decimal format
    """
    keep_browser_open = True

    def test_001_go_to_virtual_sports(self):
        """
        DESCRIPTION: Go to "Virtual Sports"
        EXPECTED: Virtual Sports successfully opened
        EXPECTED: Next event is shown
        """
        pass

    def test_002_on_event_details_page_make_several_selections(self):
        """
        DESCRIPTION: On event details page make several selections
        EXPECTED: 1.  Selected price / odds buttons are highlighted in green
        EXPECTED: 2.  Betslip counter is increased to value which is equal to the number of added selections
        """
        pass

    def test_003_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: Betslip with bets details is opened
        """
        pass

    def test_004_verify_selections(self):
        """
        DESCRIPTION: Verify selections
        EXPECTED: The following info is displayed near each selection:
        EXPECTED: 1.  Selection name (**'name'** attribute on outcome level)
        EXPECTED: 2.  Market name (**'name'** attribute on market level)
        EXPECTED: 3.  Event start time (**'startTime'** and **'name'** on event level) in 12h AM/PM format
        EXPECTED: 4.  Event name (**'name'** on event level)
        EXPECTED: 5.  Odds value is shown: **'PriceNum' / 'PriceDen' **attributes in fraction format or **'price Dec'** in decimal format will be shown
        """
        pass

    def test_005_unselect_selection_from_the_event_page(self):
        """
        DESCRIPTION: Unselect selection from the event page
        EXPECTED: 1.  The price/odds button is no longer highlighted in green
        EXPECTED: 2.  Bet Slip counter is decreased by 1
        """
        pass

    def test_006_make_selections_from_different_events(self):
        """
        DESCRIPTION: Make selections from different events
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps__5___10(self):
        """
        DESCRIPTION: Repeat steps # 5 - 10
        EXPECTED: 
        """
        pass

    def test_008_make_selections_for_different_markets(self):
        """
        DESCRIPTION: Make selections for different markets
        EXPECTED: The same as in step №3
        """
        pass

    def test_009_repeat_steps_5___10(self):
        """
        DESCRIPTION: Repeat steps # 5 - 10
        EXPECTED: 
        """
        pass

    def test_010_add_several_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Add several selections to the Bet Slip
        EXPECTED: 
        """
        pass

    def test_011_close_browser_window(self):
        """
        DESCRIPTION: Close browser window
        EXPECTED: 
        """
        pass

    def test_012_load_oxygen_and_open_bet_slip(self):
        """
        DESCRIPTION: Load Oxygen and open Bet Slip
        EXPECTED: Added selections remain in the Bet Slip
        """
        pass

    def test_013_repeat_this_test_case_for_all_virtual_racesvirtual_motorsports_class_id_288virtual_cycling_class_id_290virtual_horse_racing_class_id_285virtual_greyhound_racing_class_id_286virtual_grand_national_class_id_26604(self):
        """
        DESCRIPTION: Repeat this test case for all Virtual Races:
        DESCRIPTION: Virtual Motorsports (Class ID 288)
        DESCRIPTION: Virtual Cycling (Class ID 290)
        DESCRIPTION: Virtual Horse Racing (Class ID 285)
        DESCRIPTION: Virtual Greyhound Racing (Class ID 286)
        DESCRIPTION: Virtual Grand National (Class ID 26604)
        EXPECTED: 
        """
        pass
