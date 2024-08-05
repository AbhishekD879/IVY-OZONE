import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod  # For Prod users acca offer has to be granted from OB
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.acca
@pytest.mark.ladbrokes_only
@pytest.mark.mobile_only
@pytest.mark.login
@vtest
class Test_C16375066_Verify_Signposting_pop_up_contents_for_user_that_is_qualified_for_the_offer(BaseCashOutTest):
    """
    TR_ID: C16375066
    VOL_ID: C23820431
    NAME: Verify Signposting pop-up contents for user that is qualified for the offer
    DESCRIPTION: Test case verifies contents of the Signposting pop-up(and results of interaction with it) summoned by a user that is qualified for the Insurance offer.
    PRECONDITIONS: * ACCA Insurance offer is configured through Openbet TI.
    PRECONDITIONS: * There are events with selections applicable for ACCA Offers(events from category "Football" and market "Match Result")
    PRECONDITIONS: * For configuration ACCA offers, please, use the following instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=MOB&title=How+to+setup+ACCA+offers
    PRECONDITIONS: * To verify ACCA Offer details please check requests in dev tools requests: BuildBet -> betOfferRef -> betTypeRef"
    PRECONDITIONS: * 'superAcca' checkbox is checked in CMS -> System Configuration -> Structure -> 'Betslip' section
    PRECONDITIONS: * Oxygen app is opened and user is logged in.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify Signposting pop-up contents for user that is qualified for the offer
        PRECONDITIONS: * 'superAcca' checkbox is checked in CMS -> System Configuration -> Structure -> 'Betslip' section
        PRECONDITIONS: Create test events
        PRECONDITIONS: * Oxygen app is opened and user is logged in.
        """
        betslip_config = self.get_initial_data_system_configuration().get('Betslip', {})
        if not betslip_config:
            betslip_config = self.cms_config.get_system_configuration_item('Betslip')
        if not betslip_config.get('superAcca'):
            self.cms_config.set_super_acca_toggle_component_status(super_acca_component_status=True)
        self.__class__.event_params = self.create_several_autotest_premier_league_football_events(
            number_of_events=5, is_upcoming=True)
        self.__class__.selection_ids = [list(event.selection_ids.values())[0] for event in self.event_params]
        self.site.login()

    def test_001_add_certain_number_of_selections_applicable_for_acca_insurance_offer_from_football_into_the_betslip(self):
        """
        DESCRIPTION: Add certain number of selections applicable for ACCA Insurance offer from Football
        DESCRIPTION: (!) Number of selections that will determine qualification for ACCA Insurance is determined via trigger set within the TI offer.
        EXPECTED: Betslip counter is increased by a number of added selections
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: * '5 Fold ACCA' bet is present within 'Multiple' section
        """
        multiples_section = self.get_betslip_sections(multiples=True).Multiples
        bet_name, self.__class__.bet = list(multiples_section.items())[0]
        self.assertEqual(bet_name, vec.betslip.ACC5,
                         msg=f'Actual: "{bet_name}" bet name is not matched with Expected: "{vec.betslip.ACC5}"')

    def test_003_click_on_i_icon_within_the_5_fold_acca(self):
        """
        DESCRIPTION: Click on 'i' icon within the '5 Fold ACCA' bet
        EXPECTED: Pop-up is summoned on dark semi-transparent background containing:
        EXPECTED: * '5 Team Acca Insurance Offer' Header text;
        EXPECTED: * Body text;
        EXPECTED: * 'More' link-label;
        EXPECTED: * 'OK' button(yellow frame);
        EXPECTED: Body text is configurable through a static block created for this pop-up in CMS -> 'Static Blocks' section
        """
        self.assertTrue(self.bet.information_button,
                        msg='"Information" icon is not displayed near the selection name')
        self.bet.information_button.click()
        self.__class__.selection_info_dialog = self.site.wait_for_dialog(vec.betslip.ACCA_INSURANCE_TITLE, timeout=20)
        self.assertTrue(self.selection_info_dialog, msg='"Acca Insurance offer popup" is not shown')
        self.assertEqual(self.selection_info_dialog.dialog_title.text, vec.betslip.ACCA_INSURANCE_TITLE,
                         msg=f'Actual: "{self.selection_info_dialog.dialog_title.text}" dialog header text is not matched with Expected: "{vec.betslip.ACCA_INSURANCE_TITLE}"')
        self.assertTrue(self.selection_info_dialog.description, msg='Dialog Body text is not displayed')
        self.assertTrue(self.selection_info_dialog.more_button.is_displayed(), msg='"MORE" button is not displayed')
        self.assertTrue(self.selection_info_dialog.ok_button.is_displayed(), msg='"OK" button is not displayed')
        self.assertEqual(self.selection_info_dialog.ok_button.background_color_value, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg='"OK" button is not highlighted in yellow')

    def test_004_click_ok_button(self):
        """
        DESCRIPTION: Click 'OK' button
        EXPECTED: * Pop-up is closed.
        EXPECTED: * User remains on Betslip.
        """
        self.selection_info_dialog.click_ok()
        self.assertTrue(self.selection_info_dialog.wait_dialog_closed(),
                        msg='Failed to close "Acca Insurance offer" dialog')
        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip was not opened')

    def test_005_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step 3
        """
        self.test_003_click_on_i_icon_within_the_5_fold_acca()

    def test_006_click_on_more_link_label(self):
        """
        DESCRIPTION: Click on 'More' link-label
        EXPECTED: * Betslip and pop-up are closed.
        EXPECTED: * User is redirected to 'Promotions' page.
        """
        self.selection_info_dialog.more_button.click()
        self.assertTrue(self.selection_info_dialog.wait_dialog_closed(),
                        msg='Failed to close "Acca Insurance offer" dialog')
        self.site.wait_content_state(vec.promotions.PROMOTIONS, timeout=5)
