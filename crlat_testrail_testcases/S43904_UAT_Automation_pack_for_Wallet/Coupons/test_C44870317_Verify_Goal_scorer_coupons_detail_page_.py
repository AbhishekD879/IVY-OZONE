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
class Test_C44870317_Verify_Goal_scorer_coupons_detail_page_(Common):
    """
    TR_ID: C44870317
    NAME: "Verify  Goal scorer coupons detail page  "
    DESCRIPTION: -Verify below on the Goal scorer coupons detail page
    DESCRIPTION: - Verify user can navigate to Goal scorer coupons detail page
    DESCRIPTION: - Verify the single and multiple bet placement for Goal scorer coupons events
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Home Page is displayed
        """
        pass

    def test_002_go_to_football_coupons_and_select_goalscorer_coupon(self):
        """
        DESCRIPTION: Go to Football coupons and Select 'Goalscorer' coupon
        EXPECTED: Goalscorer coupon detail page opened
        """
        pass

    def test_003_verify_competition_section_displaying(self):
        """
        DESCRIPTION: Verify competition section displaying
        EXPECTED: First competition is expanded by default;
        EXPECTED: All competitions are collapsible & expandable.
        """
        pass

    def test_004_verify_event_section_displaying(self):
        """
        DESCRIPTION: Verify event section displaying
        EXPECTED: First event section(2nd level of accordion) within first Competitions accordion is expanded by default
        EXPECTED: All other event sections are collapsed by default
        EXPECTED: Event section is expandable / collapsible with "Show more" button
        EXPECTED: 'SEE ALL' link is shown
        """
        pass

    def test_005_click_on_the_see_all_link(self):
        """
        DESCRIPTION: Click on the 'SEE ALL' link
        EXPECTED: User is redirected to the event details page
        """
        pass

    def test_006_user_is_navigated_to_the_goalscorer_coupon_verify_goalscorer_markets_collection_tab(self):
        """
        DESCRIPTION: User is navigated to the Goalscorer coupon &
        DESCRIPTION: Verify Goalscorer markets collection tab
        EXPECTED: -'Goalscorer' market headers are displayed:
        EXPECTED: -Date of event is displayed
        EXPECTED: '1st'
        EXPECTED: 'Last'
        EXPECTED: 'Anytime'
        EXPECTED: -Available selections are displayed in the grid, odds of each are shown in correct market section (1st, Last, Anytime)
        EXPECTED: -Selection name(footballer name), footballer team are displayed for each selection (if available)
        EXPECTED: -If some markets are not created or do not contain at least 1 available selection - their header is not displayed
        EXPECTED: -Odds on 'Odds/Prices' buttons are displayed in fractional format by default
        EXPECTED: -Maximum 5 selections are displayed within event section
        EXPECTED: -'SHOW MORE' button is present if there are more than 5 selections within events section
        """
        pass

    def test_007_verify_show_more_button(self):
        """
        DESCRIPTION: Verify 'SHOW MORE' button
        EXPECTED: All available selections are present after clicking / tapping 'SHOW MORE button
        """
        pass

    def test_008_verify_ordering_of_selections(self):
        """
        DESCRIPTION: Verify ordering of selections
        EXPECTED: -Selections are ordered by odds in first available market (e.g. 1st/Last/Anytime) in ascending order (lowest to highest)
        EXPECTED: -If odds of selections are the same -> display alphabetically by footballer name (in ascending order)
        EXPECTED: -If prices are absent for selections - display alphabetically by footballer name (in ascending order)
        """
        pass

    def test_009_add_selections_to_the_quickbetbetslip(self):
        """
        DESCRIPTION: Add selection(s) to the QuickBet/Betslip
        EXPECTED: Added selection(s) is/are displayed within the 'Quick Bet' (for 1 selection)/'Betslip' (for more than 1 selection)
        """
        pass

    def test_010_enter_stake_for_a_bet_manually_or_using_quick_stakes_buttons_tap_place_bet_in_quick_betbet_now_in_betslip(self):
        """
        DESCRIPTION: Enter 'Stake' for a bet manually or using 'Quick Stakes' buttons> Tap 'Place Bet' in 'Quick Bet'/'Bet Now' in Betslip
        EXPECTED: -Bet is successfully placed
        EXPECTED: -'Quick Bet'/Betslip is replaced with 'Bet Receipt' view, displaying bet information
        EXPECTED: -Balance is decreased accordingly
        """
        pass

    def test_011_change_price_format_to_decimal_in_my_account__settings_and_repeat_steps_7___11(self):
        """
        DESCRIPTION: Change price format to Decimal in My Account > Settings and Repeat steps 7 - 11
        EXPECTED: All Prices/Odds are displayed in Decimal format
        """
        pass
