import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C16375073_Verify_CMS_configuration_changes_affect_on_ACCA_signposting_pop_up(Common):
    """
    TR_ID: C16375073
    NAME: Verify CMS configuration changes affect on ACCA signposting pop-up
    DESCRIPTION: Test case verifies changes of Acca static block configuration within CMS being applied and their affect on pop-up contents for Acca offer.
    PRECONDITIONS: * ACCA Insurance offer is configured through Openbet TI.
    PRECONDITIONS: * There are events with selections applicable for ACCA Offers(events from category "Football" and market "Match Result")
    PRECONDITIONS: * For configuration ACCA offers, please, use the following instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=MOB&title=How+to+setup+ACCA+offers
    PRECONDITIONS: * To verify ACCA Offer details please check requests in dev tools requests: BuildBet -> betOfferRef -> betTypeRef
    PRECONDITIONS: * 'superAcca' checkbox is checked in CMS -> System Configuration -> Structure -> 'Betslip' section
    PRECONDITIONS: In app
    PRECONDITIONS: * Oxygen app is opened and user is logged in
    PRECONDITIONS: * Add a certain number of selections applicable for ACCA Insurance offer from Football - Match Result market into the Betslip (in our case it will be 5) to become qualified -> ACCA Isnresence bet is present within Multiple section
    PRECONDITIONS: In CMS
    PRECONDITIONS: * Load CMS and log in
    """
    keep_browser_open = True

    def test_001_in_cms_go_to_static_blocks___acca_insurance_content_section_name_of_the_section_may_differ_but_its_uri_should_always_be_acca_insurance_content(self):
        """
        DESCRIPTION: In CMS, go to Static Blocks -> 'ACCA Insurance Content' section
        DESCRIPTION: (!) Name of the section may differ, but its 'Uri' should always be 'acca-insurance-content'
        EXPECTED: * Static block details page is opened;
        EXPECTED: * 'Uri' value is: 'acca-insurance-content';
        EXPECTED: * Html Markup contains 'Body' text(of the previously viewed pop-up), where two parameters might be present(depending on used text template):
        EXPECTED: - [['currency']] - value for this parameter is taken from user's account data;
        EXPECTED: - [['param1']] - value for this parameter is received from a 'freebetOffers?freebetOfferId={offerID}' request, where {offer ID} is taken from TI configured offer.
        """
        pass

    def test_002_change_the_uri_value_to_acca_insurance_click_save_changes_button_and_yes_on_a_confirmation_pop_up(self):
        """
        DESCRIPTION: Change the 'Uri' value to 'acca-insurance', click 'Save Changes' button and 'Yes' on a confirmation pop-up
        EXPECTED: Notification about saved changes is shown within a pop-up with 'OK' button
        """
        pass

    def test_003_reload_app_open_the_betslip_and_click_on_i_icon_in_5_fold_acca_bet(self):
        """
        DESCRIPTION: Reload app, open the Betslip and click on 'i' icon in '5 Fold ACCA' bet
        EXPECTED: * Pop-up is summoned on dark semi-transparent background containing:
        EXPECTED: - '5 Team Acca Insurance Offer' Header text;
        EXPECTED: - 'More' link-label;
        EXPECTED: - 'OK' button(yellow frame);
        EXPECTED: * Body text section is not shown.
        EXPECTED: ![](index.php?/attachments/get/33882)
        """
        pass

    def test_004_reopen_acca_insurance_content_sectionthat_was_edited_in_step_5_in_cms___static_blocks(self):
        """
        DESCRIPTION: Reopen 'ACCA Insurance Content' section(that was edited in step 5) in CMS -> Static Blocks
        EXPECTED: 
        """
        pass

    def test_005_provide_following_changeschange_uri_value_to_acca_insurance_contentchange_html_markup_value_by_adding_a_few_extra_symbols_to_its_text(self):
        """
        DESCRIPTION: Provide following changes:
        DESCRIPTION: change 'Uri' value to 'acca-insurance-content';
        DESCRIPTION: change 'Html Markup' value by adding a few extra symbols to its text
        EXPECTED: 
        """
        pass

    def test_006_save_changes_in_cms_and_repeat_step_3(self):
        """
        DESCRIPTION: 'Save Changes' in CMS and Repeat step #3
        EXPECTED: * Pop-up is summoned on dark semi-transparent background containing:
        EXPECTED: - '5 Team Acca Insurance Offer' Header text;
        EXPECTED: - 'More' link-label;
        EXPECTED: - 'OK' button(yellow frame);
        EXPECTED: * Body text section is now shown with changes applied to it in 'Html Markup' from step #5.
        """
        pass
