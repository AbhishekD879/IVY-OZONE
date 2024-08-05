import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2765444_Verify_SSBT_OTC_barcodes_retrieving_via_connect_endpoint_User_History(Common):
    """
    TR_ID: C2765444
    NAME: Verify SSBT/OTC barcodes retrieving via 'connect' endpoint (User History)
    DESCRIPTION: This test case verify SSBT/OTC EPOS1/ OTC EPOS2 Bet barcodes support for 'connect' endpoint (user history)
    DESCRIPTION: (rcomb/v7/connect added)
    DESCRIPTION: [EPOS2 collection https://confluence.egalacoral.com/display/SPI/Postman+Collections ]
    PRECONDITIONS: Request creation of
    PRECONDITIONS: SSBT barcodes (settled/ unsettled);
    PRECONDITIONS: OTC (EPOS1 and EPOS2) barcodes (settled/ unsettled; assigned to user connect card / not assigned)
    PRECONDITIONS: Open [/rcomb/v7/connect](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getEpos1Epos2SSBTBetsByUsernameUsingPOST) request
    PRECONDITIONS: To Get OTC (EPOS1) bets from Bet Tracker Apollo API: use [Bet Tracker accountHistory](https://confluence.egalacoral.com/display/SPI/Postman+Collections) postman collection
    PRECONDITIONS: To Get OTC (EPOS2) bets from DF and OXI API: use [EPOS2](https://confluence.egalacoral.com/download/attachments/53838690/EPOS2.postman_collection.json?version=2&modificationDate=1528197240159&api=v2) postman collection
    PRECONDITIONS: To Get SSBT bets from DX service: use [Bet tracking via SSBT](https://confluence.egalacoral.com/display/SPI/Postman+Collections) postman collection
    PRECONDITIONS: _______________________________________________
    PRECONDITIONS: OTC coupons are retrieved via "username" and SSBT coupons are retrieved via "car number"
    PRECONDITIONS: so if user is multi channel (has username and card number) these to parameters should be set respectively
    PRECONDITIONS: if user is in-shop (has only card number) these 2 parameters should be populated with card number
    """
    keep_browser_open = True

    def test_001_to_verify_correct_retrieving_of_n_coupons_assigned_to_the_userset_bet_request_parameters_and_tap_on_try_it_nowdeletedids_existingids_filter_allnextlimit_nsavedids_tab_allusername_usernamecardnumber_card_number(self):
        """
        DESCRIPTION: To verify correct retrieving of **N** coupons assigned to the user
        DESCRIPTION: set bet request parameters and tap on 'Try it now':
        DESCRIPTION: {
        DESCRIPTION: "deletedIds": [
        DESCRIPTION: ],
        DESCRIPTION: "existingIds": [
        DESCRIPTION: ],
        DESCRIPTION: "filter": "ALL",
        DESCRIPTION: "nextLimit": **N**,
        DESCRIPTION: "savedIds": [
        DESCRIPTION: ],
        DESCRIPTION: "tab": "ALL",
        DESCRIPTION: "username": **"username"**
        DESCRIPTION: "cardNumber": **"card number"**
        DESCRIPTION: }
        EXPECTED: Parameters are set
        EXPECTED: Response with all available coupons are received
        """
        pass

    def test_002_verify_response_for_step_1(self):
        """
        DESCRIPTION: Verify response for step 1
        EXPECTED: * **N** or less **'Open'** Coupons, assigned to the **username** and **card number**, returned with all available Bets for them
        EXPECTED: * **N** or less **'Settled'** Coupons, assigned to the **username** and **card number**, returned with all available Bets for them
        EXPECTED: * These should be the most recent **N** bets
        EXPECTED: * **'Open'** and **'Settled'** coupons can be with empty array if no bets available
        EXPECTED: * **'total'** value for unsettled coupons is equal to quantity of all unsettled coupons assigned to the user
        EXPECTED: * **'total'** value for settled coupons is equal to quantity of all settled coupons assigned to the user
        """
        pass

    def test_003_to_verify_manually_submitted_coupons_are_going_first_before_coupons_assigned_to_the_userset_bet_request_parameters_and_tap_on_try_it_nowdeletedids_existingids_filter_allnextlimit_nsavedids__coma_separated_openbet_and_ssbt_bets_cash_out_and_non_cash_out_settled_and_unsettled_not_assigned_to_any_usertab_allusername_usernamecardnumber_card_number(self):
        """
        DESCRIPTION: To verify manually submitted coupons are going first (before coupons assigned to the user)
        DESCRIPTION: set bet request parameters and tap on 'Try it now':
        DESCRIPTION: {
        DESCRIPTION: "deletedIds": [
        DESCRIPTION: ],
        DESCRIPTION: "existingIds": [
        DESCRIPTION: ],
        DESCRIPTION: "filter": "ALL",
        DESCRIPTION: "nextLimit": **N**,
        DESCRIPTION: "savedIds": [ **coma separated OpenBet and SSBT bets (cash out and non cash out; settled and unsettled) not assigned to any user**
        DESCRIPTION: ],
        DESCRIPTION: "tab": "ALL",
        DESCRIPTION: "username": **"username"**
        DESCRIPTION: "cardNumber": **"card number"**
        DESCRIPTION: }
        EXPECTED: Parameters are set
        EXPECTED: Response with all available coupons are received
        """
        pass

    def test_004_verify_response_for_step_3(self):
        """
        DESCRIPTION: Verify response for step 3
        EXPECTED: * *'Open'* coupons not assigned to the username/ card number (from **"savedIds"**) are going first and sorted by sequence they have been added
        EXPECTED: * **'Settled'** coupons not assigned to the username/ card number (from **"savedIds"**) are going first and sorted by sequence they have been added
        EXPECTED: * Coupons (settled and unsettled) received in response for step 1 are going next
        EXPECTED: * Altogether **N** 'Open' coupons and **N** 'Settled' coupons are returned
        EXPECTED: * **'total'** value for settled coupons  is increased on quantity of all settled coupons from **'savedIds'** section
        EXPECTED: * **'total'** value for unsettled coupons is increased on quantity of all unsettled
        EXPECTED: coupons from **'savedIds'** section
        """
        pass

    def test_005_to_verify_correct_pagination_returning_of_next_n_coupons_after__tapping_load_more_link_taking_into_account_that_some_coupons_were_submitted_manuallyset_bet_request_parameters_and_tap_on_try_it_nowdeletedids_existingids__coma_separated_bets_each_taken_in_quotation_marks_received_in_response_for_step_3filter_allnextlimit_nplusnsavedids__the_same_data_as_in_step_3_tab_allusername_usernamecardnumber_card_number(self):
        """
        DESCRIPTION: To verify correct pagination (returning of next **N** coupons after  tapping 'Load more' link (taking into account that some coupons were submitted manually))
        DESCRIPTION: set bet request parameters and tap on 'Try it now':
        DESCRIPTION: {
        DESCRIPTION: "deletedIds": [
        DESCRIPTION: ],
        DESCRIPTION: "existingIds": [ **coma separated bets (each taken in quotation marks) received in response for step 3**
        DESCRIPTION: ],
        DESCRIPTION: "filter": "ALL",
        DESCRIPTION: "nextLimit": **N+N**,
        DESCRIPTION: "savedIds": [ **the same data as in step 3** ],
        DESCRIPTION: "tab": "ALL",
        DESCRIPTION: "username": **"username"**
        DESCRIPTION: "cardNumber": **"card number"**
        DESCRIPTION: }
        EXPECTED: Parameters are set
        EXPECTED: Response with all available coupons are received
        """
        pass

    def test_006_verify_response_for_step_5(self):
        """
        DESCRIPTION: Verify response for step 5
        EXPECTED: * Next **N** (from N to 2N) or less **'Open'** coupons are returned with all available Bets
        EXPECTED: * Next **N** (from N to 2N) or less **'Settled'** coupons are returned with all available Bets
        EXPECTED: * *(This should not the same Bet as on response for step 3)*
        EXPECTED: * **'Open'** and **'Settled'** coupons can be with empty array if no bets available
        EXPECTED: * **'total'** values remain the same as in response from step 3
        """
        pass

    def test_007_to_verify_that_deleted_coupons_manually_submitted_ones_are_not_returned_any_moreset_bet_request_parameters_and_tap_on_try_it_nowdeletedids__some_openbet_and_ssbt_coupons_from_savedids_section__cash_out_and_non_cash_out_settled_and_unsettledexistingids__coma_separated_bets_each_taken_in_quotation_marks_received_in_response_for_step_3filter_allnextlimit_nplusnsavedids__the_same_data_as_in_step_3_tab_allusername_usernamecardnumber_card_number(self):
        """
        DESCRIPTION: To verify that deleted coupons (manually submitted ones), are not returned any more
        DESCRIPTION: set bet request parameters and tap on 'Try it now':
        DESCRIPTION: {
        DESCRIPTION: "deletedIds": [ **some OpenBet and SSBT coupons from 'savedIds' section  (cash out and non cash out; settled and unsettled**
        DESCRIPTION: ],
        DESCRIPTION: "existingIds": [ **coma separated bets (each taken in quotation marks) received in response for step 3**
        DESCRIPTION: ],
        DESCRIPTION: "filter": "ALL",
        DESCRIPTION: "nextLimit": **N+N**,
        DESCRIPTION: "savedIds": [ **the same data as in step 3** ],
        DESCRIPTION: "tab": "ALL",
        DESCRIPTION: "username": **"username"**
        DESCRIPTION: "cardNumber": **"card number"**
        DESCRIPTION: }
        EXPECTED: Parameters are set
        EXPECTED: Response with all available coupons are received
        """
        pass

    def test_008_verify_response_for_step_7(self):
        """
        DESCRIPTION: Verify response for step 7
        EXPECTED: * From **N** to **2N** **'Open'** coupons are returned except unsettled coupons in **'deletedIds'** section
        EXPECTED: * From **N** to **2N** **'Settled'** coupons are returned except settled coupons  in **'deletedIds'** section
        EXPECTED: * **'total'** value for settled bets is decreased on quantity of all settled coupons from  **'deletedIds'** section
        EXPECTED: * **'total'** value for unsettled bets is decreased on quantity of all unsettled coupons from **'deletedIds'** sections
        """
        pass

    def test_009_to_verify_that_deleted_coupons_those_which_assigned_to_the_user_are_not_returned_any_moreset_bet_request_parameters_and_tap_on_try_it_nowdeletedids__some_coupons_openbet_assigned_to_the_user_username__cash_out_and_non_cash_out_settled_and_unsettledexistingids__coma_separated_bets_each_taken_in_quotation_marks_received_in_response_for_step_3filter_allnextlimit_nplusnsavedids__the_same_data_as_in_step_3_tab_allusername_usernamecardnumber_card_number(self):
        """
        DESCRIPTION: To verify that deleted coupons (those which assigned to the user), are not returned any more
        DESCRIPTION: Set bet request parameters and tap on 'Try it now':
        DESCRIPTION: {
        DESCRIPTION: "deletedIds": [ **some coupons (OpenBet) assigned to the user ***username*  (cash out and non cash out; settled and unsettled**
        DESCRIPTION: ],
        DESCRIPTION: "existingIds": [ **coma separated bets (each taken in quotation marks) received in response for step 3**
        DESCRIPTION: ],
        DESCRIPTION: "filter": "ALL",
        DESCRIPTION: "nextLimit": **N+N**,
        DESCRIPTION: "savedIds": [ **the same data as in step 3** ],
        DESCRIPTION: "tab": "ALL",
        DESCRIPTION: "username": **"username"**
        DESCRIPTION: "cardNumber": **"card number"**
        DESCRIPTION: }
        EXPECTED: Parameters are set
        EXPECTED: Response with all available coupons are received
        """
        pass

    def test_010_verify_response_for_step_9(self):
        """
        DESCRIPTION: Verify response for step 9
        EXPECTED: * From **N** to **2N** **'Open'** coupons are returned except unsettled coupons in **'deletedIds'** section
        EXPECTED: * From **N** to **2N** **'Settled'** coupons are returned except settled coupons  in **'deletedIds'** section
        EXPECTED: * **'total'** value for settled bets is decreased on quantity of all settled coupons from  **'deletedIds'** section
        EXPECTED: * **'total'** value for unsettled bets is decreased on quantity of all unsettled coupons from **'deletedIds'** sections
        """
        pass

    def test_011_to_verify_that_expirednot_valid_coupons_are_added_to_removed_resulted__sectionset_bet_request_parameters_and_tap_on_try_it_nowdeletedids__leave_the_same_data_as_in_previous_step_plus_add_not_existingexpired_coupon_barcodesexistingids__coma_separated_bets_each_taken_in_quotation_marks_received_in_response_for_step_3filter_allnextlimit_nplusnsavedids__leave_the_same_data_as_in_previous_step_plus_add_not_existingexpired_coupon_barcodetab_allusername_usernamecardnumber_card_number(self):
        """
        DESCRIPTION: To verify that expired/not valid coupons are added to removed resulted  section
        DESCRIPTION: Set bet request parameters and tap on 'Try it now':
        DESCRIPTION: {
        DESCRIPTION: "deletedIds": [ **leave the same data as in previous step + add not existing/expired coupon barcodes**
        DESCRIPTION: ],
        DESCRIPTION: "existingIds": [ **coma separated bets (each taken in quotation marks) received in response for step 3**
        DESCRIPTION: ],
        DESCRIPTION: "filter": "ALL",
        DESCRIPTION: "nextLimit": **N+N**,
        DESCRIPTION: "savedIds": [ **leave the same data as in previous step + add not existing/expired coupon barcode**
        DESCRIPTION: ],
        DESCRIPTION: "tab": "ALL",
        DESCRIPTION: "username": **"username"**
        DESCRIPTION: "cardNumber": **"card number"**
        DESCRIPTION: }
        EXPECTED: Parameters are set
        EXPECTED: Response with all available coupons are received
        """
        pass

    def test_012_verify_response_for_step_11(self):
        """
        DESCRIPTION: Verify response for step 11
        EXPECTED: * Result is the same as in Step 10 + **'removed'** section is present
        EXPECTED: * **'removed'** section contains expired/invalid barcodes from **"deletedIds"** and **"savedIds"**
        """
        pass

    def test_013_repeat_steps_1_12_for_epos2_barcodes(self):
        """
        DESCRIPTION: Repeat Steps #1-12 for EPOS2 barcodes
        EXPECTED: 
        """
        pass
