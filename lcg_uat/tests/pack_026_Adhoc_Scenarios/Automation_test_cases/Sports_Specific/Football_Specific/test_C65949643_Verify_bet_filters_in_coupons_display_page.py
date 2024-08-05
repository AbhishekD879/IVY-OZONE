import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65949643_Verify_bet_filters_in_coupons_display_page(Common):
    """
    TR_ID: C65949643
    NAME: Verify bet filters in coupons display page
    DESCRIPTION: this test case verify bet filters in coupons display page
    PRECONDITIONS: CMS->sport category->football->(enable)accumulators
    """
    keep_browser_open = True

    def test_001_1launch_bma_application(self):
        """
        DESCRIPTION: 1.launch BMA application
        EXPECTED: Application Launched successfully
        """
        pass

    def test_002_navigate_to_football_page_and_clickon_coupons_tabnote_for_coral_accumulators(self):
        """
        DESCRIPTION: Navigate to football page and click
        DESCRIPTION: on coupons tab
        DESCRIPTION: Note for coral: Accumulators
        EXPECTED: Navigated to football page and coupons
        EXPECTED: tab opened
        """
        pass

    def test_003_find_the_popular_coupons_displayedbelow_the_featured_coupons_incoupons_tab(self):
        """
        DESCRIPTION: Find the popular coupons displayed
        DESCRIPTION: below the featured coupons in
        DESCRIPTION: coupons tab
        EXPECTED: Popular coupons displayed below the
        EXPECTED: featured coupons
        """
        pass

    def test_004_click_on_any_of_the_popular_couponand_navigate_to_coupons_page(self):
        """
        DESCRIPTION: Click on any of the popular coupon
        DESCRIPTION: and navigate to coupons page
        EXPECTED: Coupons page is open an found the
        """
        pass

    def test_005_verify_edp_page_with_respectivecoupon_leagues_events_in_expanded_mode(self):
        """
        DESCRIPTION: Verify EDP page with respective
        DESCRIPTION: coupon leagues events in expanded mode
        EXPECTED: EDP page should be displayed with respective leagues and events in expanded mode
        """
        pass

    def test_006_find_the_bet_filter_shown_above_the_change_coupon(self):
        """
        DESCRIPTION: Find the Bet filter shown above the change coupon
        EXPECTED: Bet filter shown above the change coupon
        """
        pass

    def test_007_click_on_bet_filter_and_navigate_to_thefootball_bet_filter_page(self):
        """
        DESCRIPTION: Click on bet filter and navigate to the
        DESCRIPTION: football Bet filter page
        EXPECTED: Navigated to football Bet filter page
        """
        pass

    def test_008_click_on_the_tabs_shown_in_the_footballbet_filter_page_and_verify_respectivetab_data_displayed(self):
        """
        DESCRIPTION: Click on the tabs shown in the football
        DESCRIPTION: bet filter page and verify respective
        DESCRIPTION: tab data displayed
        EXPECTED: Tabs are selectable and loaded with the
        EXPECTED: respective data
        """
        pass

    def test_009_verify_data_in_tabsyour_teams_the_opposition_saved_filtersare_selectable_and_filters_count_shown_on_find_bets_cta_button(self):
        """
        DESCRIPTION: Verify data in tabs(your teams, the opposition, saved filters)are selectable and filters count shown on find bets CTA button
        EXPECTED: Data selected and filter respective
        EXPECTED: data count shown on the find bets CTA button
        """
        pass

    def test_010_verify_save_filter_cta__pop_up_cancelsave_operations_when_filter_saved(self):
        """
        DESCRIPTION: verify save filter CTA  pop up cancel,
        DESCRIPTION: save operations when filter saved
        EXPECTED: Filter selected ,save CTA enabled clicked
        EXPECTED: on save filter CTA ,pop up opened with text filed, save and cancel CTA's
        """
        pass

    def test_011_open_save_filters_tab_and_click_on_apply_cta_and_on_applying_it_should_navigate_back_to_the_you_teams_tab(self):
        """
        DESCRIPTION: Open save filters tab and click on apply CTA and on applying it should navigate back to the you teams tab
        EXPECTED: Opened save filters tab and clicked on apply CTA and on applying it navigated back to the you teams tab
        """
        pass

    def test_012_verify_information_icon_i_shown_below_the_tabs_of_edp_and_displayrespective_message(self):
        """
        DESCRIPTION: Verify information icon 'i' shown below the tabs of EDP and display
        DESCRIPTION: respective message
        EXPECTED: Information icon 'i' and displayed with
        EXPECTED: respective message
        """
        pass

    def test_013_verify_reset_of_selected_filters_by_clicking_on_reset_which_shown_above_the_save_filters_tab(self):
        """
        DESCRIPTION: Verify reset of selected filters by clicking on RESET which shown above the save filters tab
        EXPECTED: Selected filters deselected on performing RESET
        """
        pass
