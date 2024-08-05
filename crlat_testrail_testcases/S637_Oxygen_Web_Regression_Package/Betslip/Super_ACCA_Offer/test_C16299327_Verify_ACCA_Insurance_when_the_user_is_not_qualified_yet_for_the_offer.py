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
class Test_C16299327_Verify_ACCA_Insurance_when_the_user_is_not_qualified_yet_for_the_offer(Common):
    """
    TR_ID: C16299327
    NAME: Verify ACCA Insurance when the user is not qualified yet for the offer
    DESCRIPTION: Verify ACCA Insurance when the user is not qualified yet for the offer for logged in user (Ladbrokes)
    DESCRIPTION: AUTOTESTS:
    DESCRIPTION: Mobile [C23237902]
    DESCRIPTION: Desktop [C23547560]
    PRECONDITIONS: * There are events with available ACCA Offers.
    PRECONDITIONS: * For configuration ACCA offers, please, use the following instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=MOB&title=How+to+setup+ACCA+offers
    PRECONDITIONS: * To verify ACCA Offer details please check requests in dev tools requests: BuildBet  -> betOfferRef -> [i]-> offerType, where i - the array of returned bets
    PRECONDITIONS: *  **In order to become eligible for ACCA Insurance offer please use category "Football" and market "Match Result"**
    PRECONDITIONS: * 'superAcca' checkbox is checked in CMS -> System Configuration -> Structure -> 'Betslip' section
    PRECONDITIONS: * Open app and log in
    PRECONDITIONS: Design is attached below:
    PRECONDITIONS: ![](index.php?/attachments/get/33815)
    """
    keep_browser_open = True

    def test_001_add_a_certain_number_of_selections_to_betslip_which_is_lacking_1_selection_to_be_eligible_for_acca_insurance_offerfor_example_4_selections_from__football___match_result_market(self):
        """
        DESCRIPTION: Add a certain number of selections to betslip which is lacking 1 selection to be eligible for ACCA Insurance offer(for example, 4 selections from  football - Match Result market)
        EXPECTED: * The selections are added to betslip successfully
        EXPECTED: * " **offerType:suggested** " is returned in buildBet response in Dev Tools
        """
        pass

    def test_002_pay_attention_to_the_warning_message_that_appears_on_the_top_of_betslip(self):
        """
        DESCRIPTION: Pay attention to the warning message that appears on the top of betslip
        EXPECTED: The warning message appears on the top of betslip with the following text: "Add 1 more selection to qualify for 5+ Acca Insurance"
        """
        pass

    def test_003_observe_how_long_the_warning_message_persists(self):
        """
        DESCRIPTION: Observe how long the warning message persists
        EXPECTED: The warning message persists for 5 seconds and disappears
        """
        pass

    def test_004_clear_betslip_by_removing_all_added_selections(self):
        """
        DESCRIPTION: Clear betslip by removing all added selections
        EXPECTED: The betslip is cleared and empty
        """
        pass

    def test_005_add_a_certain_number_of_selections_to_betslip_which_is_lacking_2_selections_to_be_eligible_for_acca_insurance_offerfor_example_3_selections_from__football___match_result_market(self):
        """
        DESCRIPTION: Add a certain number of selections to betslip which is lacking 2 selections to be eligible for ACCA Insurance offer(for example, 3 selections from  football - Match Result market)
        EXPECTED: The selections are added to betslip successfully
        """
        pass

    def test_006_pay_attention_to_the_betslip(self):
        """
        DESCRIPTION: Pay attention to the betslip
        EXPECTED: No message is displayed regarding Acca Insurance
        """
        pass

    def test_007_repeat_steps_5_6_with_acca_where_3_and_4_selections_are_lacking_to_be_eligible_for_acca_insurance_offer(self):
        """
        DESCRIPTION: Repeat steps 5-6 with ACCA where 3 and 4 selections are lacking to be eligible for ACCA Insurance offer
        EXPECTED: No message is displayed regarding Acca Insurance
        """
        pass

    def test_008_add_a_certain_number_of_selections_to_betslip_with_1_or_more_selections_which_are_not_applicable_for_acca_insurance_offer_into_the_betslipnot_applicable_selections_are_hrgr_selections_selections_from_live_events_selections_from_same_event_that_is_applicable_but_one_selection_is_already_used_from_it(self):
        """
        DESCRIPTION: Add a certain number of selections to betslip with 1 or more selections which are not applicable for ACCA Insurance offer into the Betslip
        DESCRIPTION: (Not applicable selections are: HR/GR selections; Selections from Live events; Selections from same event that is applicable, but one selection is already used from it)
        EXPECTED: No message is displayed regarding Acca Insurance
        """
        pass
