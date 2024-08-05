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
class Test_C869683_Verify_Each_Way_Option_for_Several_Virtual_Race_Single_Selections(Common):
    """
    TR_ID: C869683
    NAME: Verify Each Way Option for Several 'Virtual Race' Single Selections
    DESCRIPTION: This test case verifies how Each Way option influence 'Total Est. Returns' and 'Total Stake' values when  several 'Virtual Sports' single selections are added to the Bet Slip
    DESCRIPTION: NOTE, **User Story:** BMA-3156 [Customer can add VS selections to the BMA bet slip]
    PRECONDITIONS: In order to get information from the  SiteServer about event (Horse Racing class id 285) use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForClass/285?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: x.xx - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes:
    PRECONDITIONS: **'priceTypeCodes'**='LP on a market level
    PRECONDITIONS: **'isEachWayAvaiable'** on market level to see whether Each Way checkbox should be displayedon the Bet Slip
    PRECONDITIONS: **'eachWayFactorNum', 'eachWayFactorDen', 'eachWayPlaces'** on market level to see market terms attributes
    PRECONDITIONS: **'priceNum', 'priceDen'** in the outcome level - to see odds for selection in fraction format
    PRECONDITIONS: **'priceDec'** in the outcome level - to see odds for selection in decimal format
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_tap_virtuals_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Load 'Oxygen' application and tap 'Virtuals' icon from the sports menu ribbon
        EXPECTED: Virtual Sports successfully opened
        """
        pass

    def test_002_go_to_the_events_detail_pages_which_has_an_attribute_iseachwayavailabletrue_on_market_level_in_the_site_server_response(self):
        """
        DESCRIPTION: Go to the events detail pages which has an attribute **'isEachWayAvailable'**='true'  on market level in the Site Server response
        EXPECTED: Event details pages are opened
        """
        pass

    def test_003_add_several_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Add several selections to the Bet Slip
        EXPECTED: Bet Slip counter is increased
        """
        pass

    def test_004_open_bet_slip(self):
        """
        DESCRIPTION: Open Bet Slip
        EXPECTED: 1.  Bet Slip with bet details is opened
        EXPECTED: 2.  Each Way option is displayed under the bet details
        """
        pass

    def test_005_verify_each_way_checkbox(self):
        """
        DESCRIPTION: Verify Each Way checkbox
        EXPECTED: 1.  Checkbox is not selected by default
        EXPECTED: 2.  Checkbox label is 'E/W'
        """
        pass

    def test_006_enter_stake_values_in_stake_field(self):
        """
        DESCRIPTION: Enter stake values in 'Stake' field
        EXPECTED: **'Total Est. Retunrs**' is equal to the sum of all **'Estimated Returns'**
        """
        pass

    def test_007_on_the_bet_slip_select_checkbox_each_way(self):
        """
        DESCRIPTION: On the Bet Slip select checkbox 'Each Way'
        EXPECTED: Each Way option is enabled
        """
        pass

    def test_008_enter_a_stake_values_in_a_stake_field_for_few_lp_selections(self):
        """
        DESCRIPTION: Enter a stake values in a stake field for few 'LP' selections
        EXPECTED: 1.  **'Stake'** value corresponds to the entered stake
        EXPECTED: 2.  **'Total Stake'** value is calculated according to formula
        EXPECTED: 3.  **'Total Est. Returns' **is shown and calculated accourding to the formula
        """
        pass

    def test_009_verify_total_est_returns_correctness(self):
        """
        DESCRIPTION: Verify 'Total Est. Returns' correctness
        EXPECTED: 'Total Est. Returns' is calculated according to the formula:
        EXPECTED: ***'Total Est. Returns'* = *'Estimated Returns 1' + 'Estimated Returns 2' +...+ 'Estimated Returns N'* **
        EXPECTED: ***Estimated Returns1 ='stake' *+ *'profit' + 'extra_profit'*, - **when Each Way option is enabled
        EXPECTED: where
        EXPECTED: ***'stake'* **- is entered value in a stake field
        EXPECTED: ***'profit'*** = (**'priceNum'** / **'priceDen'**) * ***'stake'   ***
        EXPECTED: ***'extra_profit'***= ***'stake'*** + ***[*** (**'eachWayFactorNum'** / **'eachWayFactorDen' *) **** (**'priceNum'/'priceDen'*****) **** ***'stake' ]***
        EXPECTED: ***'Estimated Returns 2' ***= ***'stake' *+ *'profit'*, -** when Each Way optin is disabled
        """
        pass

    def test_010_verify_total_stake_correctness(self):
        """
        DESCRIPTION: Verify 'Total Stake' correctness
        EXPECTED: ***'Total Stake' = Stake1+ Stake2+...***
        EXPECTED: Stake 1 - is doubled stake for selection where Each Way is enabled
        EXPECTED: Stake2 - is enetered stake value for selection where Each Way is disabled
        """
        pass

    def test_011_go_to_the_event_details_page_where_event_doesnt_have_attribute_iseachwayavailable_for_its_markets(self):
        """
        DESCRIPTION: Go to the event details page where event doesn't have attribute **'isEachWayAvailable'** for its markets
        EXPECTED: Event details page is opened
        """
        pass

    def test_012_add_several_lp_selections_to_the_bet_slip_for_such_events(self):
        """
        DESCRIPTION: Add several 'LP' selections to the Bet Slip for such events
        EXPECTED: Each Way option is absent on the Bet Slip
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
