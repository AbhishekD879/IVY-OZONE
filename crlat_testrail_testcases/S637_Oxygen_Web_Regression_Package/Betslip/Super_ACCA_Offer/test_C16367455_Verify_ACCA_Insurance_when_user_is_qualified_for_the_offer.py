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
class Test_C16367455_Verify_ACCA_Insurance_when_user_is_qualified_for_the_offer(Common):
    """
    TR_ID: C16367455
    NAME: Verify ACCA Insurance when user is qualified for the offer
    DESCRIPTION: Test case verifies ACCA Insurance presence when logged in user is qualified for the offer.
    DESCRIPTION: AUTOTESTS:
    DESCRIPTION: Mobile [C23657383]
    PRECONDITIONS: * ACCA Insurance offer is configured through Openbet TI.
    PRECONDITIONS: * There are events with selections applicable for ACCA Offers(events from category "Football" and market "Match Result")
    PRECONDITIONS: * For configuration ACCA offers, please, use the following instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=MOB&title=How+to+setup+ACCA+offers
    PRECONDITIONS: * To verify ACCA Offer details please check requests in dev tools requests: BuildBet -> betOfferRef -> betTypeRef
    PRECONDITIONS: * 'superAcca' checkbox is checked in CMS -> System Configuration -> Structure -> 'Betslip' section
    PRECONDITIONS: * Oxygen app is opened and user is logged in.
    PRECONDITIONS: In this current case, TI offer was configured for 'eligible' response when 5 applicable selections were added into Betslip. (number is set through the trigger within the offer).
    """
    keep_browser_open = True

    def test_001_add_certain_number_of_selections_applicable_for_acca_insurance_offer_from_football___match_result_market_into_the_betslip_in_our_case_it_will_be_5(self):
        """
        DESCRIPTION: Add certain number of selections applicable for ACCA Insurance offer from Football - Match Result market into the Betslip (in our case it will be 5)
        EXPECTED: Betslip counter is increased by a number of added selections
        """
        pass

    def test_002_open_betslip_and_view_xhr_requestsresponses_for_it(self):
        """
        DESCRIPTION: Open Betslip and view XHR requests/responses for it
        EXPECTED: * Selections are present to betslip
        EXPECTED: * **'offerType:elligible'** is shown in 'buildBet' response in Dev Tools
        EXPECTED: * '5 Fold ACCA' bet is present within 'Multiple' section
        EXPECTED: * '5 Fold ACCA' row contains:
        EXPECTED: - (5+) icon;
        EXPECTED: - 'Acca Insurance' label;
        EXPECTED: - 'i' icon
        EXPECTED: ![](index.php?/attachments/get/33864)
        EXPECTED: * Signposting message is shown at the header of betslip for 5 seconds and disappears - text of the message is: "Your selections qualify for Acca Insurance"
        EXPECTED: ![](index.php?/attachments/get/33859)
        """
        pass

    def test_003_add_1_more_selection_which_is_not_applicable_for_acca_insurance_offer_into_the_betslipnot_applicable_selections_are_hrgr_selections_selections_from_live_events_selections_from_same_event_that_is_applicable_but_one_selection_is_already_used_from_it(self):
        """
        DESCRIPTION: Add 1 more selection which is not applicable for ACCA Insurance offer into the Betslip
        DESCRIPTION: (Not applicable selections are: HR/GR selections; Selections from Live events; Selections from same event that is applicable, but one selection is already used from it).
        EXPECTED: * Betslip counter is increased by 1
        EXPECTED: * Selection is added to betslip
        """
        pass

    def test_004_open_betslip_and_view_xhr_requestsresponses_for_it(self):
        """
        DESCRIPTION: Open Betslip and view XHR requests/responses for it
        EXPECTED: * No 'betOfferRef' is received in 'buildBet' response in Dev Tools
        EXPECTED: * Signposting message is not shown at the header of betslip
        EXPECTED: * Labels within row are: '# Fold ACCA' and 'Accumulator Bet'
        EXPECTED: ![](index.php?/attachments/get/34125)
        """
        pass

    def test_005_remove_the_not_applicable_selection_from_betslip(self):
        """
        DESCRIPTION: Remove the *not applicable* selection from Betslip
        EXPECTED: * Betslip counter is decreased by 1
        EXPECTED: * The expected result matches the ER from step #2
        """
        pass

    def test_006_add_1_more_selection_applicable_for_acca_insurance_offer_from_football___match_result_market_into_the_betslip(self):
        """
        DESCRIPTION: Add 1 more selection *applicable* for ACCA Insurance offer from Football - Match Result market into the Betslip
        EXPECTED: Betslip counter is increased by 1
        """
        pass

    def test_007_open_betslip_and_view_xhr_requestsresponses_for_it(self):
        """
        DESCRIPTION: Open Betslip and view XHR requests/responses for it
        EXPECTED: * Expected result matches ER from step #2
        EXPECTED: * Label within row is shown as: '6 Fold ACCA'
        """
        pass

    def test_008_enter_value_that_doesnt_exceed_your_users_current_balance_into_the_stake_field_of_6_fold_acca_row_and_place_bet(self):
        """
        DESCRIPTION: Enter value that doesn't exceed your user's current balance into the 'Stake' field of '6 Fold ACCA' row and 'Place Bet'
        EXPECTED: * Bet Receipt modal is shown
        EXPECTED: * Bet is successfully placed.
        """
        pass
