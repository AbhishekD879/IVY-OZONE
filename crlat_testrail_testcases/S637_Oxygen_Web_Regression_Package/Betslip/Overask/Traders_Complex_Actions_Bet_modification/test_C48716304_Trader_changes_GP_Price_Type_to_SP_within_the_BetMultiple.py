import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C48716304_Trader_changes_GP_Price_Type_to_SP_within_the_BetMultiple(Common):
    """
    TR_ID: C48716304
    NAME: Trader changes GP Price Type to SP within the Bet(Multiple)
    DESCRIPTION: This test case verifies Price Type update during Overask review process for the GP selections within multiple bet
    DESCRIPTION: Applicable for <Race> events type only.
    PRECONDITIONS: 1) User is logged in to the app, has positive balance and no restrictions on betting
    PRECONDITIONS: 2) Bet Intercept is checked(enabled) for the 'Class' and 'Type' levels of the Sport, within which the tested event is located
    PRECONDITIONS: ![](index.php?/attachments/get/55427671) ![](index.php?/attachments/get/55427667)
    PRECONDITIONS: 3) Overask(conditional) is enabled in one of 2 places:
    PRECONDITIONS: a) for the User within /ti/customer - Account Rules('MBA' value is set)
    PRECONDITIONS: ![](index.php?/attachments/get/55427672)
    PRECONDITIONS: b) Max Bet(LP)/(SP) value(s) is(are) set for the selection(s) that will be used in this test, on market level of the tested event
    PRECONDITIONS: ![](index.php?/attachments/get/55427674)
    PRECONDITIONS: 4) **At least 2** <Race> events with a Primary Market should have 'GP Available' checked(enabled), with selections having 'Live Price' values
    PRECONDITIONS: ![](index.php?/attachments/get/55427675)
    """
    keep_browser_open = True

    def test_001_add_2_selections_from_event_from_pre_conditions_to_the_betslip(self):
        """
        DESCRIPTION: Add 2 selections from event from pre-conditions to the Betslip
        EXPECTED: Selections are successfully added
        """
        pass

    def test_002_open_betslip_and_enter_stake_value_into_a_double_field_which_is_higher_then_maximum_limit_for_added_selectionstheir_combined_sum_or_users_mba_value(self):
        """
        DESCRIPTION: Open Betslip and Enter stake value into a 'Double' field, which is higher then maximum limit for added selections(their combined sum or user's MBA value)
        EXPECTED: 
        """
        pass

    def test_003_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: Button text changes to a spinner, following with a modal pop-in being shown above it(and the entire betslip/quickbet interface) with following content present in it:
        EXPECTED: **Header** : "Bet is being reviewed by our trading team"
        EXPECTED: Loading **spinner** (shown between header and body text)
        EXPECTED: **Body Text 1** : "Your bet has not gone through as total stake entered exceeds the max stake allowed"
        EXPECTED: **Body Text 2** : "Would you like to see alternative offers similar to your bet? Bear with us this may take up to 2 minutes"
        EXPECTED: * 'Place Bet' button is no longer accessible
        EXPECTED: * 'Stake' field is shown in the background and is not editable
        """
        pass

    def test_004_in_ti_go_through_bet___bi_requestsindexphpattachmentsget55427679within_bet_intercept_search_modal_window_switch_to_results_tab_and_click_within_a_bet_lane_that_has_your_client_name_shownindexphpattachmentsget55427680(self):
        """
        DESCRIPTION: In TI, go through BET - BI Requests
        DESCRIPTION: ![](index.php?/attachments/get/55427679)
        DESCRIPTION: Within 'Bet Intercept Search' modal window switch to 'Results' tab, and click within a Bet lane that has your 'Client Name' shown
        DESCRIPTION: ![](index.php?/attachments/get/55427680)
        EXPECTED: Bet Intercept advanced editing interface is opened
        """
        pass

    def test_005_provide_a_following_change_for_1_out_of_2_selections_and_submit_it_within_bet_intercept_advanced_editing_interfaceprice_type__gp___spindexphpattachmentsget55427684(self):
        """
        DESCRIPTION: Provide a following change for 1 out of 2 selections and submit it within Bet Intercept advanced editing interface:
        DESCRIPTION: 'Price Type' : GP -> SP
        DESCRIPTION: ![](index.php?/attachments/get/55427684)
        EXPECTED: Bet Intercept Report modal is shown with 'OK' Status/Result of your bet
        """
        pass

    def test_006_verify_changes_within_the_betslip_interface_of_app(self):
        """
        DESCRIPTION: Verify changes within the Betslip interface of app
        EXPECTED: Betslip content changes, with following contents being shown:
        EXPECTED: **Header** : 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message
        EXPECTED: 'Offer expires: X:XX' **counter**
        EXPECTED: **Bet cells** that contain: 'Selection Name'; 'Market Name'; 'Event Name'; 'Price Type'; 'Stake value'; 'Est. Returns'; 'x' button.
        EXPECTED: 'Total Stake' **lane**(with value); 'Estimated Returns' **lane**(with value)
        EXPECTED: Enabled 'Cancel' and 'Place Bet' **buttons**
        """
        pass

    def test_007_verify_updated_price_type_displaying_in_betslip(self):
        """
        DESCRIPTION: Verify updated Price Type displaying in Betslip
        EXPECTED: 'Old' Price is crossed out with a 'New' Price one being shown on its right side, highlighted in yellow color **only within cell of the selection that was changed**.
        EXPECTED: ![](index.php?/attachments/get/55427685)
        EXPECTED: where,
        EXPECTED: * 'Old' Price was a fractional value
        EXPECTED: * 'New' Price = SP
        EXPECTED: Stake value remains the same in the placeholder shown above 'Est. Returns' value
        """
        pass

    def test_008_verify_new_estimated_returns_value(self):
        """
        DESCRIPTION: Verify new 'Estimated Returns' value
        EXPECTED: * The 'Estimated Returns' value corresponds to bet.[i].payout.potential attribute from readBet response,
        EXPECTED: where 'i' is taken from the object where isOffer="Y"
        EXPECTED: * The 'Estimated Returns' value is equal to 'N/A' since no attribute is returned
        EXPECTED: ![](index.php?/attachments/get/55427683)
        """
        pass

    def test_009_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: The bet is placed as per normal process on the updated price type from step 7.
        EXPECTED: Estimated Returns value remains the same as on counter-offer screen(from step 8).
        """
        pass
