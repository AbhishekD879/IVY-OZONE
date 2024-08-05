import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C44870202_Verify_that_User_sees_Bet_Filter_button_and_on_tap_Bet_Filter_page_is_displayed_with_back_button_and_Reset_button_both_fully_functional_Verify_that_page_displays_data_as_per_GDs_user_is_able_to_create_a_selection_choosing_in_meetings_selectin(Common):
    """
    TR_ID: C44870202
    NAME: "Verify that User sees Bet Filter button, and on tap, Bet Filter page is displayed (with back button and Reset button, both fully functional) Verify that page displays data as per GDs, user is able to create a selection choosing in meetings, selectin
    DESCRIPTION: "Verify that User sees Bet Filter button, and on tap, Bet Filter page is displayed (with back button and Reset button, both fully functional)
    DESCRIPTION: Verify that page displays data as per GDs, user is able to create a selection choosing in meetings, selecting specific ODDS,  and Form, Ground Type, Digital Tipsteer Filters, Star Rating, and user is able to save selection as per page functionality"
    PRECONDITIONS: User is logged in the application and is on Horse Racing Landing page.
    """
    keep_browser_open = True

    def test_001_verify_that_the_bet_filter_button_is_displayed(self):
        """
        DESCRIPTION: Verify that the Bet filter button is displayed.
        EXPECTED: The 'Bet Filter' button is displayed on Horse Racing Landing page (on the top right corner of the screen).
        """
        pass

    def test_002_tap_on_bet_filter_button_click_on_back_arrow_button_and_verify(self):
        """
        DESCRIPTION: Tap on Bet filter button. Click on back arrow button and verify.
        EXPECTED: The user is redirected to horse racing landing page.
        """
        pass

    def test_003_tap_on_bet_filter_button_and_create_a_selections_by_selecting_specific_meetingsoddsformgoingdigital_tipster_filtersstar_rating(self):
        """
        DESCRIPTION: Tap on Bet filter button and create a selection/s by selecting specific meetings/odds/form/Going/Digital tipster filters/star rating.
        EXPECTED: The Find bets button displays the number of selections available as per the filters set by the user.
        """
        pass

    def test_004_click_on_save_selection_verify(self):
        """
        DESCRIPTION: Click on Save Selection. Verify.
        EXPECTED: 1. The filters selected by the user are saved.
        EXPECTED: 2. The Save selection button is disabled.
        """
        pass

    def test_005_click_on_reset_button_and_verify(self):
        """
        DESCRIPTION: Click on Reset button and verify.
        EXPECTED: The fields filled earlier are reset and Save selection button is enabled.
        """
        pass

    def test_006_create_a_selections_by_selecting_specific_meetingsoddsformgoingdigital_tipster_filtersstar_rating_and_click_on_find_bets_button(self):
        """
        DESCRIPTION: Create a selection/s by selecting specific meetings/odds/form/Going/Digital tipster filters/star rating and click on Find bets button.
        EXPECTED: The bet filter results are displayed
        """
        pass
