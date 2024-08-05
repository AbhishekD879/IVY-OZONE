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
class Test_C2601291_Verify_interaction_with_selections_of_the_CS_Coupon(Common):
    """
    TR_ID: C2601291
    NAME: Verify interaction with selections of the CS Coupon
    DESCRIPTION: 
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: 1. Prepare a coupon with a Correct Score market that applied to a few football events. CS market contains:
    PRECONDITIONS: * Selection(s) with a price
    PRECONDITIONS: * Suspended selection
    PRECONDITIONS: * Not Displayed selection
    PRECONDITIONS: * Selection with no price
    PRECONDITIONS: * Deleted selection (delete from the middle of the scope, like 0:0; **1:0**; 2:0)
    PRECONDITIONS: * Leave the maximal score selections as 7:0 for Home team and 8:0 for Away team and delete remaining higher scores
    PRECONDITIONS: 2. Coupon contains ONLY Correct Score markets
    PRECONDITIONS: 3. Coupon is added to Football > Coupons / ACCAS  > Some particular section.
    PRECONDITIONS: 4. Correct Score Coupon is opened
    """
    keep_browser_open = True

    def test_001_verify_the_default_state_of_the_score_switchers_and_the_minimal_available_score(self):
        """
        DESCRIPTION: Verify the default state of the score switchers and the minimal available score
        EXPECTED: - Default score is 0:0.
        EXPECTED: - 'Down' arrows are disabled (as 0 is the minimal available score).
        """
        pass

    def test_002_verify_up_arrow_disabling_when_the_max_configured_value_for_the_score_is_selected_find_in_preconditions(self):
        """
        DESCRIPTION: Verify 'Up' arrow disabling when the max configured value for the score is selected (find in preconditions).
        EXPECTED: If maximums are selected 'Up' Arrow becomes disabled.
        """
        pass

    def test_003_switch_between_the_scores_with_available_prices_and_verify_the_prices_are_updated_depending_on_selected_score_combinationplease_specify_response_in_which_price_is_received(self):
        """
        DESCRIPTION: Switch between the scores with available prices and verify the prices are updated depending on selected score combination.
        DESCRIPTION: Please specify response in which price is received.
        EXPECTED: * Odds are correct, properly shown and get changed accordingly
        EXPECTED: * Delay between score selection and price change is 1/4 sec
        EXPECTED: * Price button is enabled
        """
        pass

    def test_004_switch_to__suspended_selection__verify_the_price_button_is_disabled_if_selected_score_isnt_valid(self):
        """
        DESCRIPTION: Switch to _Suspended selection_. Verify the Price button is disabled if selected score isn't valid.
        EXPECTED: * Price button is disabled
        EXPECTED: * Odds are shown as N/A
        """
        pass

    def test_005_switch_to__not_displayed_selection__verify_the_price_button_is_disabled_if_selected_score_isnt_valid(self):
        """
        DESCRIPTION: Switch to _Not Displayed selection_. Verify the Price button is disabled if selected score isn't valid.
        EXPECTED: * Price button is disabled
        EXPECTED: * Odds are shown as N/A
        """
        pass

    def test_006_switch_to__selection_with_no_price__verify_the_price_button_is_disabled_if_selected_score_isnt_valid(self):
        """
        DESCRIPTION: Switch to _Selection with no price_. Verify the Price button is disabled if selected score isn't valid.
        EXPECTED: * Price button is disabled
        EXPECTED: * Odds are shown as N/A
        """
        pass

    def test_007_switch_to__deleted_selection__verify_the_price_button_is_disabled_if_selected_score_isnt_valid(self):
        """
        DESCRIPTION: Switch to _Deleted selection_. Verify the Price button is disabled if selected score isn't valid.
        EXPECTED: * Price button is disabled
        EXPECTED: * Odds are shown as N/A
        """
        pass

    def test_008_select_score_combination_for_the_event__and_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Select score combination for the event  and add selection to the Betslip
        EXPECTED: * Selection is successfully added
        EXPECTED: * Price button for this event becomes green
        """
        pass

    def test_009_verify_possibility_to_add_one_more_selection_to_the_betslip_for_the_same_event(self):
        """
        DESCRIPTION: Verify possibility to add one more selection to the Betslip for the same event
        EXPECTED: * User cannot add one more selection for the same event to the Betslip
        EXPECTED: * Score selectors and 'Up'/'Down' arrows are removed for the event
        """
        pass

    def test_010_remove_the_selection_from_the_betslip(self):
        """
        DESCRIPTION: Remove the selection from the Betslip
        EXPECTED: * Price button is not marked as added to the Betslip and enabled
        EXPECTED: * 'Up' and 'Down' arrows become enabled
        """
        pass

    def test_011_add_a_selection_to_betslip_and_check_if_its_status_is_saved_and_switchers_are_disabled_after_page_revisit_relogin(self):
        """
        DESCRIPTION: Add a selection to Betslip and check if it's status is saved and switchers are disabled after:
        DESCRIPTION: * Page revisit
        DESCRIPTION: * Relogin
        EXPECTED: * Selection status remains unchanged
        EXPECTED: * Price button is marked
        EXPECTED: * Score selection and arrows buttons are disabled
        """
        pass
