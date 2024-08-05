import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod ---can't settle the bet
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.promotions_banners_offers
@vtest
class Test_C15392960_Verify_Signposting_Extra_Place_promo_on_Cash_out_Open_Settled_bets_tab(BaseCashOutTest):
    """
    TR_ID: C15392960
    NAME: Verify Signposting Extra Place promo on Cash out/Open/Settled bets tab
    DESCRIPTION:
    PRECONDITIONS: In OB(back office) signposting Extra Place promo flag is configured.
    PRECONDITIONS: Configuration steps for Signposting Promos in OB:
    PRECONDITIONS: Open tst2/stg2 back office Env--> Go to Admin
    PRECONDITIONS: Expand Betting set up from LHs-->Enter a valid event ID and click Search
    PRECONDITIONS: In the event display page select Market
    PRECONDITIONS: In the Market display page scroll down to see Flags section
    PRECONDITIONS: Select Extra Place Promo(tick the check box)
    PRECONDITIONS: Click on Update Market button.
    PRECONDITIONS: In Cms PromoSignPosting should be enabled.
    PRECONDITIONS: User is logged in.
    PRECONDITIONS: User placed Single/ Multiple bets where Cash Out offer and Extra Place Promo is available on Market level.
    PRECONDITIONS: User have some open/settled bets.
    """
    keep_browser_open = True
    price1 = {0: '1/4'}

    def test_000_preconditions(self):
        event = self.ob_config.add_UK_racing_event(number_of_runners=1, market_extra_place_race=True,
                                                   lp_prices=self.price1)
        self.__class__.event_id = event.event_id
        self.__class__.market_id = event.market_id
        self.__class__.selection_id = list(event.selection_ids.values())[0]
        self.__class__.event_name = event.ss_response['event']['name']
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.assertEqual(self.site.bet_receipt.promo_label_text, vec.bma.EXTRA_PLACE.upper(),
                         msg=f'Actual text:"{self.site.bet_receipt.promo_label_text}" is not changed to Expected text:"{vec.bma.EXTRA_PLACE.upper()}".')
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_my_bets__go_to_cash_out_tab(self):
        """
        DESCRIPTION: 1.Navigate to My Bets-->Go to Cash out tab
        EXPECTED: Cash out tab should be opened
        """
        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            wait_for_result(lambda: self.site.cashout.tab_content.accordions_list.is_displayed(timeout=10) is True,
                            timeout=60)
            _, cashout_bet = self.site.cashout.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name, number_of_bets=1)
            bets = list(cashout_bet.items_as_ordered_dict.values())[0]
            self.assertTrue(bets.has_promo_icon(),
                            msg='Extra place icon is not present on bet receipt')
            self.assertEqual(bets.promo_label_text, vec.bma.EXTRA_PLACE,
                             msg=f'Actual text:"{bets.promo_label_text}" is not changed to Expected text:"{vec.bma.EXTRA_PLACE}".')

    def test_002_verify_signposting_extra_place_promo(self):
        """
        DESCRIPTION: 2.Verify Signposting 'Extra Place' Promo
        EXPECTED: The Signpost Extra Place promo should be displayed in Cash out section below the Market/Event name.
        EXPECTED: ![](index.php?/attachments/get/33475)
        EXPECTED: ![](index.php?/attachments/get/33476)
        """
        # covered in step 1

    def test_003_navigate_to_my_bets__go_to_open_bets_tab(self):
        """
        DESCRIPTION: 3.Navigate to My Bets-->Go to Open bets tab
        EXPECTED: Open bets tab should be Opened.
        EXPECTED: ![](index.php?/attachments/get/33477)
        EXPECTED: ![](index.php?/attachments/get/33478)
        """
        self.site.open_my_bets_open_bets()
        wait_for_result(lambda: self.site.open_bets.tab_content.accordions_list.is_displayed(timeout=10) is True,
                        timeout=60)
        _, open_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name, number_of_bets=1)
        bets = list(open_bet.items_as_ordered_dict.values())[0]
        self.assertTrue(bets.has_promo_icon(expected_result=True),
                        msg='Extra place icon is not present on bet receipt')
        self.assertEqual(bets.promo_label_text, vec.bma.EXTRA_PLACE,
                         msg=f'Actual text:"{bets.promo_label_text}" is not changed to Expected text:"{vec.bma.EXTRA_PLACE}".')

    def test_004_verify_signposting_extra_place_promo(self):
        """
        DESCRIPTION: 4.Verify Signposting Extra Place promo
        EXPECTED: The Signpost Extra Place promo should be displayed in Open bets section below the Market/Event name.
        """
        # covered in step 3

    def test_005_navigate_to_my_bets___go_to_settled_bet_tab(self):
        """
        DESCRIPTION: 5.Navigate to My Bets--> Go to Settled bet tab
        EXPECTED: Settled bets tab should be opened
        """
        self.site.go_to_home_page()
        # Setteling the bet
        self.ob_config.update_selection_result(event_id=self.event_id, selection_id=self.selection_id,
                                               market_id=self.market_id)
        sleep(5)
        self.device.refresh_page()
        self.site.wait_content_state('homepage')
        self.site.open_my_bets_settled_bets()
        wait_for_result(lambda: self.site.bet_history.tab_content.accordions_list.is_displayed(timeout=10) is True,
                        timeout=60)
        _, settle_bet = self.site.bet_history.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name, number_of_bets=1)
        bets = list(settle_bet.items_as_ordered_dict.values())[0]
        self.assertTrue(bets.has_promo_icon(expected_result=True),
                        msg='Extra place icon is not present on bet receipt')
        self.assertEqual(bets.promo_label_text, vec.bma.EXTRA_PLACE,
                         msg=f'Actual text:"{bets.promo_label_text}" is not changed to Expected text:"{vec.bma.EXTRA_PLACE}".')

    def test_006_verify_signposting_extra_place_promo(self):
        """
        DESCRIPTION: 6.Verify Signposting Extra Place Promo
        EXPECTED: The Signpost Extra Place promo should be displayed in Settled bets section below , below the Market/Event name.
        EXPECTED: ![](index.php?/attachments/get/33471)
        EXPECTED: ![](index.php?/attachments/get/33472)
        """
        # covered in step 5
