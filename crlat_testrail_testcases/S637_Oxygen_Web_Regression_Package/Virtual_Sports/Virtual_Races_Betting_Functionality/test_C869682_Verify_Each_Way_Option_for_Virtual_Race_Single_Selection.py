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
class Test_C869682_Verify_Each_Way_Option_for_Virtual_Race_Single_Selection(Common):
    """
    TR_ID: C869682
    NAME: Verify Each Way Option for 'Virtual Race' Single Selection
    DESCRIPTION: This test case verifies how Each Way option influence 'Total Est. Returns' and 'Total Stake' values when 'Virtual Sport' single selection
    DESCRIPTION: NOTE, **User Story:** BMA-3156 [Customer can add VS selections to the BMA bet slip]
    PRECONDITIONS: In order to get information from the  SiteServer about event (Horse Racing class id 285) use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForClass/285?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: x.xx - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes:
    PRECONDITIONS: **'priceTypeCodes'**='LP on a market level
    PRECONDITIONS: **'isEachWayAvaiable'** on market level to see whether Each Way checkbox should be displayedon the Bet Slip
    PRECONDITIONS: **'eachWayFactorNum', 'eachWayFactorDen', 'eachWayPlaces'** on market level to see market terms attributes
    PRECONDITIONS: **'priceNum', 'priceDen'** in the outcome level - to see odds for selection in fraction format
    PRECONDITIONS: **'priceDec'** in the outcome level - to see odds for selection in decimal format
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_tap_virtuals_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Load 'Oxygen' application and tap 'Virtuals' icon from the Sports Menu Ribbon
        EXPECTED: Virtual Sports successfully opened
        """
        pass

    def test_002_go_to_the_event_which_has_an_attribute_iseachwayavailabletrue_on_market_level_in_the_site_server_response(self):
        """
        DESCRIPTION: Go to the event which has an attribute **'isEachWayAvailable'**='true'  on market level in the Site Server response
        EXPECTED: Event landing page is opened
        """
        pass

    def test_003_add_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add selection to the Bet Slip
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

    def test_006_enter_stake_in_a_stake_field__select_quick_stake(self):
        """
        DESCRIPTION: Enter stake in a stake field / select quick stake
        EXPECTED: 1.  'Stake' field corresponds to the entered stake
        EXPECTED: 2.  'Total Stake' is equal to the enetered stake
        EXPECTED: 3.  'Total Est. Returns' value is shown
        """
        pass

    def test_007_verify_total_est_returns_correctness(self):
        """
        DESCRIPTION: Verify 'Total Est. Returns' correctness
        EXPECTED: 'Total Est. Returns' is calculated according to the formula:
        EXPECTED: ***'Total Est. Returns'* = *'stake' *+ *'profit'*, **
        EXPECTED: where
        EXPECTED: ***'stake'* **- is entered value in a stake field
        EXPECTED: ***'profit'*** = (**'priceNum'** / **'priceDen'**) * ***'stake'    -*** in case when price/odds have a fractional format
        """
        pass

    def test_008_on_a_bet_slip_select_checkbox_each_way(self):
        """
        DESCRIPTION: On a Bet Slip select checkbox 'Each Way'
        EXPECTED: Each Way option is enabled
        """
        pass

    def test_009_enter_a_stake_in_a_stake_field__select_quick_stake(self):
        """
        DESCRIPTION: Enter a stake in a stake field / select quick stake
        EXPECTED: 1.  'Stake' value corresponds to the entered stake
        EXPECTED: 2.  'Total Stake' value is doubled
        EXPECTED: 3.  'Total Est. Returns' is shown and calculated accourding to the formula
        """
        pass

    def test_010_verify_total_est_returns_correctness(self):
        """
        DESCRIPTION: Verify 'Total Est. Returns' correctness
        EXPECTED: 'Total Est. Returns' is calculated according to the formula:
        EXPECTED: ***'Total Est. Returns'* = *'stake' *+ *'profit' + 'extra_profit'*, **
        EXPECTED: where
        EXPECTED: ***'stake'* **- is entered value in a stake field
        EXPECTED: ***'profit'*** = (**'priceNum'** / **'priceDen'**) * ***'stake'    -*** in case when price/odds have a fractional format
        EXPECTED: ***'extra_profit'***= ***'stake'*** + ***[*** (***'eachWayFactorNum'*** / ***'eachWayFactorDen' ) **** (***'priceNum'/'priceDen') **** ***'stake' ]***
        """
        pass

    def test_011_go_to_the_event_details_page_without_attribute_iseachwayavailable_for_its_markets(self):
        """
        DESCRIPTION: Go to the event details page without attribute **'isEachWayAvailable'** for its markets
        EXPECTED: Event details page is opened
        """
        pass

    def test_012_add_a_selection_to_the_bet_slip_for_such_event(self):
        """
        DESCRIPTION: Add a selection to the Bet Slip for such event
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
