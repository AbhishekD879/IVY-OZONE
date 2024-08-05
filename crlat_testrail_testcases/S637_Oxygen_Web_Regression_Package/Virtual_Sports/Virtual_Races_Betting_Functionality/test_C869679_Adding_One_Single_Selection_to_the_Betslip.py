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
class Test_C869679_Adding_One_Single_Selection_to_the_Betslip(Common):
    """
    TR_ID: C869679
    NAME: Adding One Single Selection to the Betslip
    DESCRIPTION: This test case verifies whether selection with correct information is added to the betslip
    DESCRIPTION: NOTE, **User Story:** BMA-3156 [Customer can add VS selections to the BMA bet slip]
    PRECONDITIONS: In order to get information from the  SiteServer about event (Horse Racing class id 285) use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForClass/285?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: x.xx - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'name'** on outcome level to verify selection name
    PRECONDITIONS: **'name'** on market level - to verify market name
    PRECONDITIONS: **'name'** on event level - to verify event name
    PRECONDITIONS: **'startTime'** on event level - to verify event start time and event start date
    """
    keep_browser_open = True

    def test_001_go_to_virtual_sports(self):
        """
        DESCRIPTION: Go to "Virtual Sports"
        EXPECTED: Virtual Sports successfully opened
        EXPECTED: Next event is shown
        """
        pass

    def test_002_select_one_priceodds_button_for_verified_event(self):
        """
        DESCRIPTION: Select one 'Price/Odds' button for verified event
        EXPECTED: Selected 'Price/Odds' button is highlighted in green
        EXPECTED: Betslip icon with bet indicator appears
        """
        pass

    def test_003_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: Selection with bet details is displayed in the Betlsip
        EXPECTED: Section is entitled 'Singles (1)'
        """
        pass

    def test_004_verify_selection_information(self):
        """
        DESCRIPTION: Verify selection information
        EXPECTED: The following info is displayed on the Bet Slip:
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market name (**'name'** attribute on the market level)
        EXPECTED: 3.  Event start time and event name (**'start Time'** and event **'name'** attributes)
        EXPECTED: 4.  Selection odds (**'PriceNum'/'PriceDen' **attributes in fraction format or **'price Dec'** in decimal format)
        """
        pass

    def test_005_enter_amount_to_the_stake_field_manually_or_via_quick_buttons(self):
        """
        DESCRIPTION: Enter amount to the 'Stake' field manually or via quick buttons
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: *   Value in the **Stake **box
        EXPECTED: *   **Estimated Returns** (in format XXX.XX)
        EXPECTED: *   **Total Stake **(in format XXX.XX)
        EXPECTED: *   **Total Est. Returns** (in format XXX.XX)
        """
        pass

    def test_006_close_betslip(self):
        """
        DESCRIPTION: Close Betslip
        EXPECTED: The page where selections have been made to Bet Slip is opened
        """
        pass

    def test_007_open_betslip_again(self):
        """
        DESCRIPTION: Open Betslip again
        EXPECTED: Betslip is opened
        EXPECTED: All entered information is remembered
        """
        pass

    def test_008_repeat_this_test_case_for_all_virtual_racesvirtual_motorsports_class_id_288virtual_cycling_class_id_290virtual_horse_racing_class_id_285virtual_greyhound_racing_class_id_286virtual_grand_national_class_id_26604(self):
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
