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
class Test_C16375066_Verify_Signposting_pop_up_contents_for_user_that_is_qualified_for_the_offer(Common):
    """
    TR_ID: C16375066
    NAME: Verify Signposting pop-up contents for user that is qualified for the offer
    DESCRIPTION: Test case verifies contents of the Signposting pop-up(and results of interaction with it) summoned by a user that is qualified for the Insurance offer.
    DESCRIPTION: AUTOTEST
    DESCRIPTION: MOBILE: [C23820431]
    PRECONDITIONS: * ACCA Insurance offer is configured through Openbet TI.
    PRECONDITIONS: * There are events with selections applicable for ACCA Offers(events from category "Football" and market "Match Result")
    PRECONDITIONS: * For configuration ACCA offers, please, use the following instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=MOB&title=How+to+setup+ACCA+offers
    PRECONDITIONS: * To verify ACCA Offer details please check requests in dev tools requests: BuildBet -> betOfferRef -> betTypeRef"
    PRECONDITIONS: * 'superAcca' checkbox is checked in CMS -> System Configuration -> Structure -> 'Betslip' section
    PRECONDITIONS: * Oxygen app is opened and user is logged in.
    """
    keep_browser_open = True

    def test_001_add_certain_number_of_selections_applicable_for_acca_insurance_offer_from_football___match_result_market_into_the_betslip_in_our_case_it_will_be_5_to_become_qualified_number_of_selections_that_will_determine_qualification_for_acca_insurance_is_determined_via_trigger_set_within_the_ti_offer(self):
        """
        DESCRIPTION: Add certain number of selections applicable for ACCA Insurance offer from Football - Match Result market into the Betslip (in our case it will be 5) to become qualified
        DESCRIPTION: (!) Number of selections that will determine qualification for ACCA Insurance is determined via trigger set within the TI offer.
        EXPECTED: Betslip counter is increased by a number of added selections
        """
        pass

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: * '5 Fold ACCA' bet is present within 'Multiple' section
        """
        pass

    def test_003_click_on_i_icon_within_the_5_fold_acca_betindexphpattachmentsget34259(self):
        """
        DESCRIPTION: Click on 'i' icon within the '5 Fold ACCA' bet
        DESCRIPTION: ![](index.php?/attachments/get/34259)
        EXPECTED: Pop-up is summoned on dark semi-transparent background containing:
        EXPECTED: * '5 Team Acca Insurance Offer' Header text;
        EXPECTED: * Body text;
        EXPECTED: * 'More' link-label;
        EXPECTED: * 'OK' button(yellow frame);
        EXPECTED: Body text is configurable through a static block created for this pop-up in CMS -> 'Static Blocks' section
        EXPECTED: ![](index.php?/attachments/get/33867)
        """
        pass

    def test_004_click_ok_button(self):
        """
        DESCRIPTION: Click 'OK' button
        EXPECTED: * Pop-up is closed.
        EXPECTED: * User remains on Betslip.
        """
        pass

    def test_005_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step 3
        EXPECTED: 
        """
        pass

    def test_006_click_on_more_link_label(self):
        """
        DESCRIPTION: Click on 'More' link-label
        EXPECTED: * Betslip and pop-up are closed.
        EXPECTED: * User is redirected to 'Promotions' page.
        """
        pass
