import pytest
import tests
import json
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec
from voltron.utils.helpers import do_request


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #Cannot grant freebet
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C15931380_From_OX_99_Free_Bet_Pop_up(BaseBetSlipTest):
    """
    TR_ID: C15931380
    NAME: [From OX 99] Free Bet Pop up
    DESCRIPTION: This test case verifies Free Bets pop up
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has Free Bets available on their account
    PRECONDITIONS: * User has at least one selection added to the Betslip
    PRECONDITIONS: -----
    PRECONDITIONS: - For DEV/TST env. - https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: - For PROD/HL env.:
    PRECONDITIONS: Coral: https://sports.coral.co.uk/promotions/details/new-customer-offer (Open a new online, mobile or telephone account with Coral. Place a £5+ Win or £5+ Each Way bet on any sport. Coral will give you an instant four x £5 free bets.)
    PRECONDITIONS: Ladbrokes: https://m.ladbrokes.com/en-gb/#!/promotions/0 (Register a new Ladbrokes account on mobile or online using promo code '20FREE'. Place cumulative qualifying stakes to a total of £5 win or £5 each-way at odds totalling 1/2 or greater.)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        event1 = self.ob_config.add_volleyball_event_to_austrian_league()
        event2 = self.ob_config.add_volleyball_event_to_austrian_league()
        self.__class__.selection_id1 = list(event1.selection_ids.values())[0]
        self.__class__.selection_id2 = list(event2.selection_ids.values())[0]

        username = tests.settings.betplacement_user
        self.ob_config.grant_freebet(username)
        self.site.login(username=username)

    def test_001_open_bet_slip_and_press_on_use_free_bet_link(self):
        """
        DESCRIPTION: Open Bet Slip and press on "Use Free Bet" link
        EXPECTED: * Free Bet Pop up is shown with list of Free Bets available
        EXPECTED: * Each free bet is displayed in next format:
        EXPECTED: <Currency Symbol> <Free Bet Value> <Free Bet Name><Class/Type/Event etc for which this Free Bet can be applied>
        """
        self.open_betslip_with_selections(selection_ids=[self.selection_id1, self.selection_id2])
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='Singles section is not displayed.')
        stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.stake.use_free_bet_link.click()
        self.__class__.freebet_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, timeout=5, verify_name=False)
        self.assertTrue(self.freebet_dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" dialog is not shown')
        for free_bet_name, freebet in self.freebet_dialog.items_as_ordered_dict.items():
            self.assertTrue(freebet.radio_button.is_displayed(),
                            msg=f'Radio button is not displayed for freebet "{free_bet_name}"')
            self.assertTrue(freebet.name, msg='Freebet name is not displayed')

    def test_002_verify_list_of_free_bets_available_corresponds_to_list_of_free_bets_received_in_buildbet_request(self, url='buildBet'):
        """
        DESCRIPTION: Verify list of Free Bets available corresponds to list of Free Bets received in *buildBet request*
        EXPECTED: *[From OX99]*
        EXPECTED: Free Bets available corresponds to list of Free Bets received in *buildBet request*
        EXPECTED: *[After OX100.1]*
        EXPECTED: * Free Bets available corresponds to list of Free Bets received in *buildBet request*
        EXPECTED: * Only eligible Free Bets for selected bet are displayed. If [freebet value] / [lines number] is < 0.01 then filter out available freebets for this bet (e.g. if user has £0.10 free bet then it will NOT be available for multiple bets with x11 and more lines)
        """
        available_free_bets = len(self.freebet_dialog.items_as_ordered_dict)
        buildbet_freebets = 0
        url = f'{tests.settings.BETTINGMS}v1/buildBet'
        placebet_request = self.get_web_socket_response_by_url(url=url)
        post_data = placebet_request.get('postData')
        data = json.dumps(post_data)
        cookie_value = self.get_local_storage_cookie_value_as_dict(cookie_name='OX.USER')['bppToken']
        headers = {'token': cookie_value,
                   'Content-Type': 'application/json'}
        req = do_request(url=url, data=data, headers=headers)
        offers_available = req['bets'][0]['freebet']
        for offer in offers_available:
            if 'freebetOfferType' in offer and offer['type'] == 'SPORTS':
                buildbet_freebets+=1
        self.assertEqual(available_free_bets, buildbet_freebets,
                         msg=f'Free Bets available "{available_free_bets}" is not same as "{buildbet_freebets}"')

    def test_003_from_ox99_select_one_of_available_free_bets_from_free_bet_pop_upfrom_ox100_select_one_of_available_free_bets_from_free_bet_pop_up_and_click_on_add_button(self):
        """
        DESCRIPTION: *[From OX99]* Select one of available Free Bets from Free Bet pop up
        DESCRIPTION: *[From OX100]* Select one of available Free Bets from Free Bet pop up AND click on 'ADD' button.
        EXPECTED: *[From OX99]*
        EXPECTED: * Selected Free Bet has check box marked as selected
        EXPECTED: * Pop up is closed (in 0.2 sec)
        EXPECTED: * "Use Free Bet" link is changed to "- Remove Free Bet" link
        EXPECTED: *[From OX100]*
        EXPECTED: * Chosen Free Bet has radio button marked as selected
        EXPECTED: * 'ADD' button becomes active:
        EXPECTED: Coral Popup Design:
        EXPECTED: ![](index.php?/attachments/get/36071)
        EXPECTED: Ladbrokes Popup Design:
        EXPECTED: ![](index.php?/attachments/get/36072)
        EXPECTED: * Chosen Free Bet successfully added
        EXPECTED: * "Use Free Bet" link is changed to "- Remove Free Bet" link
        """
        freebet = list(self.freebet_dialog.items_as_ordered_dict.values())[0]
        freebet.click()
        self.assertTrue(freebet.radio_button.is_enabled(), msg='"Radio" button is not selected')
        self.assertTrue(self.freebet_dialog.add_button.is_displayed(), msg='"Add" button is not displayed')
        self.assertTrue(self.freebet_dialog.add_button.is_enabled(), msg='"Add" button is not enabled')
        self.freebet_dialog.add_button.click()
        self.assertTrue(self.stake.has_remove_free_bet_link(), msg='"Use Free Bet" link is not changed to "Remove Free Bet" link')

    def test_004_press_on___remove_free_bet_link(self):
        """
        DESCRIPTION: Press on "- Remove Free Bet" link
        EXPECTED: * "- Remove Free Bet" link is changed to "Use Free Bet" link
        EXPECTED: * 'Estimated Returns' is changed to 0.00
        """
        self.stake.remove_free_bet_link.click()
        self.assertTrue(self.stake.has_use_free_bet_link(),
                        msg='"Remove Free Bet" link is not changed to "Use Free Bet" link')
        estimated_returns = self.stake.est_returns
        expected_est_returns = '0.00'
        self.assertEqual(estimated_returns, expected_est_returns,
                         msg=f'Actual estimated returns "{estimated_returns}" is not same as Expected estimated returns "{expected_est_returns}"')
