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
class Test_C1317027_Verify_Goalscorer_Coupon_with_tree_types_of_markets(Common):
    """
    TR_ID: C1317027
    NAME: Verify Goalscorer Coupon with tree types of markets
    DESCRIPTION: This test case verifies Goalscorer Coupons
    DESCRIPTION: AUTOTEST [C1489824]
    PRECONDITIONS: 1. The Football event with First Goalscorer / Last Goalscorer  / Anytime Goalscorer markets (templateMarketName='First Goalscorer', templateMarketName="Last Goalscorer", templateMarketName="Anytime Goalscorer") are available
    PRECONDITIONS: 2. In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: 3. The following market templates are used: |First Goalscorer| |Last Goalscorer| |Anytime Goalscorer|
    PRECONDITIONS: 4. List of Coupons depends on TI tool configuration data for Coupons. All available Coupons from OB response will be displayed on the page
    PRECONDITIONS: 5. For testing purposes the following Classes and Types should be used:
    PRECONDITIONS: - Football England - Premier League, Championship, League One, League Two
    PRECONDITIONS: - Football UEFA Club Competitions - UEFA Champions League, UEFA Europa League
    PRECONDITIONS: Note: The ‘New’ badge on Coupons page is CMS configurable (‘System-configuration’ -> ‘FOOTBALLCOUPONSNEWBADGE’ > check/uncheck ‘enableCouponNewBadge’ check box)
    PRECONDITIONS: **User is navigated to Coupon tab on Football and Goalscorer coupon is available**
    PRECONDITIONS: step5: verify Goalscorer market header https://app.zeplin.io/project/5b45be4e98f74086659ba6e9/screen/5b617efed86fcf4152051273
    PRECONDITIONS: **COUPONS** for Coral (CMS configurable)
    PRECONDITIONS: **ACCAS** for Ladbrokes (CMS configurable)
    """
    keep_browser_open = True

    def test_001_select_goalscorer_coupon(self):
        """
        DESCRIPTION: Select 'Goalscorer' coupon
        EXPECTED: - When events are not available for a coupon:
        EXPECTED: * “No events found” text is shown
        EXPECTED: - When events are available for a coupon:
        EXPECTED: * Market Selector is NOT shown
        """
        pass

    def test_002_verify_competition_section_displaying(self):
        """
        DESCRIPTION: Verify competition section displaying
        EXPECTED: - First competition is expanded by default;
        EXPECTED: - All competitions are collapsible, expandable.
        """
        pass

    def test_003_verify_event_section_displaying(self):
        """
        DESCRIPTION: Verify event section displaying
        EXPECTED: - First event section(2nd level of accordion) within first Competitions accordion is expanded by default
        EXPECTED: - All other event sections are collapsed by default
        EXPECTED: - Event section is expandable / collapsible with "Show more" button
        EXPECTED: - 'SEE ALL' link is shown
        """
        pass

    def test_004_click_on_the_see_all_link(self):
        """
        DESCRIPTION: Click on the 'SEE ALL' link
        EXPECTED: User is redirected to the event details page
        """
        pass

    def test_005_verify_goalscorer_markets_collection_tab(self):
        """
        DESCRIPTION: Verify Goalscorer markets collection tab
        EXPECTED: * 'Goalscorer' market headers are displayed:
        EXPECTED: - Date of event is displayed
        EXPECTED: - '1st'
        EXPECTED: - 'Last'
        EXPECTED: - 'Anytime'
        EXPECTED: * Available selections are displayed in the grid, odds of each are shown in correct market section (1st, Last, Anytime)
        EXPECTED: * Selection name(footballer name), footballer team are displayed for each selection (if available)
        EXPECTED: * If some markets are not created or do not contain at least 1 available selection - their header is not displayed
        EXPECTED: * Odds on 'Odds/Prices' buttons are displayed in fractional format by default
        EXPECTED: * Maximum 5 selections are displayed within event section
        EXPECTED: * 'SHOW MORE' button is present if there are more than 5 selections within events section
        """
        pass

    def test_006_verify_show_more_button(self):
        """
        DESCRIPTION: Verify 'SHOW MORE' button
        EXPECTED: All available selections are present after clicking / tapping 'SHOW MORE button
        """
        pass

    def test_007_verify_selection_attribute_for_player_in_ss_response(self):
        """
        DESCRIPTION: Verify selection attribute for player in SS response
        EXPECTED: 1. First team's name in event's name is (Home) and second is (Away)
        EXPECTED: 2. OutcomeMeaningMinorCode:
        EXPECTED: - H (Home team)
        EXPECTED: - A (Away team)
        EXPECTED: - N (No score)
        """
        pass

    def test_008_verify_ordering_of_selections(self):
        """
        DESCRIPTION: Verify ordering of selections
        EXPECTED: * Selections are ordered by odds in first available market (e.g. 1st/Last/Anytime) in ascending order (lowest to highest)
        EXPECTED: * If odds of selections are the same -> display alphabetically by footballer name (in ascending order)
        EXPECTED: * If prices are absent for selections - display alphabetically by footballer name (in ascending order)
        """
        pass

    def test_009_in_ti_change_price_for_one_of_the_selections_with_enabled_liveserve_updates_see_preconditions__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Change price for one of the selections with enabled liveServe updates (see Preconditions) > Navigate to application and observe changes
        EXPECTED: - Corresponding 'Price/Odds' buttons immediately display new prices and for a few seconds they will change their color to:
        EXPECTED: * blue color if price has decreased
        EXPECTED: * pink color if price has increased
        """
        pass

    def test_010_in_ti_suspend_marketone_of_the_selections_with_enabled_liveserve_updates_see_preconditions__navigate_to_application_and_observe_changes(self):
        """
        DESCRIPTION: In TI: Suspend market/one of the selections with enabled liveServe updates (see Preconditions) > Navigate to application and observe changes
        EXPECTED: - ***If market is suspended:*** All Price/Odds buttons under specific market column are displayed immediately as greyed out and become disabled for selected market but still displaying the prices
        EXPECTED: - ***If some selections are suspended:***
        EXPECTED: Price/Odds button of changed outcome are displayed immediately as greyed out and become disabled
        EXPECTED: The rest outcomes and market tabs are not changed
        """
        pass

    def test_011_add_selections_to_the_quickbetbetslip(self):
        """
        DESCRIPTION: Add selection(s) to the QuickBet/Betslip
        EXPECTED: Added selection(s) is/are displayed within the 'Quick Bet' (for 1 selection)/'Betslip' (for more than 1 selection)
        """
        pass

    def test_012_enter_stake_for_a_bet_manually_or_using_quick_stakes_buttons_tap_place_bet__in_quick_betbet_now_in_betslip(self):
        """
        DESCRIPTION: Enter 'Stake' for a bet manually or using 'Quick Stakes' buttons> Tap 'Place Bet'  in 'Quick Bet'/'Bet Now' in Betslip
        EXPECTED: - Bet is successfully placed
        EXPECTED: - 'Quick Bet'/Betslip is replaced with 'Bet Receipt' view, displaying bet information
        EXPECTED: - Balance is decreased accordingly
        """
        pass

    def test_013_change_price_format_to_decimal_in_my_account__settings_and_repeat_steps_7___14(self):
        """
        DESCRIPTION: Change price format to Decimal in My Account > Settings and Repeat steps 7 - 14
        EXPECTED: All Prices/Odds are displayed in Decimal format
        """
        pass
