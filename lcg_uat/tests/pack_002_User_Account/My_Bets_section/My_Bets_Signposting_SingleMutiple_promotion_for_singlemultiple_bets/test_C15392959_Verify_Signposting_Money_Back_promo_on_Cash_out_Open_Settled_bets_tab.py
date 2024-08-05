import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.waiters import wait_for_result
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can not create event on Market level with MoneyBack promo icon
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.promotions_banners_offers
@vtest
class Test_C15392959_Verify_Signposting_Money_Back_promo_on_Cash_out_Open_Settled_bets_tab(BaseCashOutTest):
    """
    TR_ID: C15392959
    NAME: Verify Signposting Money Back promo on Cash out/Open/Settled bets tab
    DESCRIPTION:
    PRECONDITIONS: In OB(back office) signposting Money Back promo flag is configured.
    PRECONDITIONS: Configuration steps for Signposting Promos in OB:
    PRECONDITIONS: Open tst2/stg2 back office Env--> Go to Admin
    PRECONDITIONS: Expand Betting set up from LHs-->Enter a valid event ID and click Search
    PRECONDITIONS: In the event display page select Market
    PRECONDITIONS: In the Market display page scroll down to see Flags section
    PRECONDITIONS: Select Money Back promo(tick the check box)
    PRECONDITIONS: Click on Update Market button.
    PRECONDITIONS: Money Back Promo signposting is enabled in cms
    PRECONDITIONS: User is logged in.
    PRECONDITIONS: User has placed Single/ Multiple bets where Cash Out offer and Money Back Promo is available on market level.
    PRECONDITIONS: User have some open/settled bets
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        event = self.ob_config.add_autotest_premier_league_football_event(market_money_back=True)
        self.__class__.created_event_name = event.team1 + ' v ' + event.team2
        self.__class__.selection_id = event.selection_ids[event.team1]
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.event_id = event.event_id
        self.__class__.market_id = self.ob_config.market_ids[event.event_id][market_short_name]

        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.assertEqual(self.site.bet_receipt.promo_label_text, vec.bma.MONEY_BACK.upper(),
                         msg=f'Actual text:"{self.site.bet_receipt.promo_label_text}" is not changed to Expected text:"{vec.bma.MONEY_BACK.upper()}".')
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_my_bets___go_to_cash_out_tab(self):
        """
        DESCRIPTION: 1.Navigate to My Bets--> Go to Cash out tab
        EXPECTED: Cash out tab should be opened
        """
        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            wait_for_result(lambda: self.site.cashout.tab_content.accordions_list.is_displayed(timeout=10) is True,
                            timeout=60)
            _, bet = self.site.cashout.tab_content.accordions_list. \
                get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.created_event_name,
                        number_of_bets=1)
            # odds boost text xpath is representing here for money back text
            self.assertEqual(bet.odds_boost_text, vec.bma.MONEY_BACK,
                             msg=f'Actual text:"{bet.odds_boost_text}" is not as Expected text:"{vec.bma.MONEY_BACK}".')
            self.assertTrue(bet.moneyback_icon, msg='moneyback icon is not present')

    def test_002_verify_signposting_money_back_promo(self):
        """
        DESCRIPTION: 2.Verify Signposting Money Back Promo
        EXPECTED: The Signpost Money Back promo should be displayed in Cash out section below and above the overall  bet.![](index.php?/attachments/get/33493)
        EXPECTED: ![](index.php?/attachments/get/33494)
        EXPECTED: ![](index.php?/attachments/get/33495)
        """
        # covered in step 1

    def test_003_navigate_to_my_bets__go_to_open_bet_tab(self):
        """
        DESCRIPTION: 3.Navigate to My Bets-->Go to Open bet tab
        EXPECTED: Open bets tab should be Opened.
        """
        self.site.open_my_bets_open_bets()
        wait_for_result(lambda: self.site.open_bets.tab_content.accordions_list.is_displayed(timeout=10) is True,
                        timeout=60)
        _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.created_event_name, number_of_bets=1)
        self.assertEqual(bet.odds_boost_text, vec.bma.MONEY_BACK,
                         msg=f'Actual text:"{bet.odds_boost_text}" is not changed to Expected text:"{vec.bma.MONEY_BACK.upper()}".')
        self.assertTrue(bet.moneyback_icon, msg='moneyback icon is not present')

    def test_004_verify_signposting_money_back_promo(self):
        """
        DESCRIPTION: 4.Verify Signposting Money Back promo
        EXPECTED: The Signpost Money Back promo should be displayed in Open bet section below and above of the overall the bet .![](index.php?/attachments/get/33496)
        EXPECTED: ![](index.php?/attachments/get/33497)
        """
        # covered in step 3

    def test_005_navigate_to_my_bets__go_to_settled_bets_tab(self):
        """
        DESCRIPTION: 5.Navigate to My Bets-->Go to Settled bets tab
        EXPECTED: Settled bets tab should be opened.
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
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.created_event_name, number_of_bets=1)
        self.assertEqual(settle_bet.odds_boost_text, vec.bma.MONEY_BACK,
                         msg=f'Actual text:"{settle_bet.odds_boost_text}" is not as Expected text:"{vec.bma.MONEY_BACK}".')
        self.assertTrue(settle_bet.moneyback_icon, msg='moneyback icon is not present')

    def test_006_verify_signposting_money_back_promo(self):
        """
        DESCRIPTION: 6.Verify Signposting Money Back promo
        EXPECTED: The Signpost Money Back promo should be displayed in Settled bets section (Sport)below and above the overall the bet.![](index.php?/attachments/get/33498)
        EXPECTED: ![](index.php?/attachments/get/33499)
        """
        # covered in step 5
