import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result
from collections import OrderedDict
from time import sleep


@pytest.mark.lad_tst2  # Acca Insurance signpost is applicable for Ladbrokes only.
@pytest.mark.lad_stg2
# @pytest.mark.prod # cannot settle the events in Prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.acca
@pytest.mark.desktop
@pytest.mark.promotions_banners_offers
@vtest
class Test_C15392967_Verify_Signposting_ACCA_Insurance_on_Open_Settled_bets_tab(BaseCashOutTest):
    """
    TR_ID: C15392967
    NAME: Verify Signposting ACCA Insurance on Open/Settled bets tab
    DESCRIPTION:
    PRECONDITIONS: In OB(back office) signposting ACCA Insurance promo flag is configured.
    PRECONDITIONS: User is logged in.
    PRECONDITIONS: User placed Single/ Multiple bets where Cash Out offer and Extra ACCA Insurance Promo is available on Events/Event levels.
    PRECONDITIONS: User should have some open and settled bets.
    """
    keep_browser_open = True
    prices = OrderedDict([('odds_home', '3/1'),
                          ('odds_draw', '1/17'),
                          ('odds_away', '1/4')])
    event_ids = []
    market_ids = []
    selection_ids = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User is logged in.
        PRECONDITIONS: User placed Single/ Multiple bets where Cash Out offer and Extra ACCA Insurance Promo is available on Events/Event levels.
        PRECONDITIONS: User should have some open and settled bets.
        """
        ema_config = self.get_initial_data_system_configuration().get('EMA')
        if not ema_config:
            ema_config = self.cms_config.get_system_configuration_item('EMA')
        if not ema_config:
            raise CmsClientException('"EMA" section not found in System Config')
        if not ema_config.get('enabled'):
            self.cms_config.set_my_acca_section_cms_status(ems_status=True)

        self.site.login()
        self.assertTrue(self.site.wait_content_state('HOMEPAGE', timeout=60), msg='User is not navigated to homepage')
        for index in range(6):
            event = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True, lp=self.prices)
            self.event_ids.append(event.event_id)
            self.market_ids.append(event.default_market_id)
            self.selection_ids.append(list(event.selection_ids.values())[0])

        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.has_acca_sign_post(),
                        msg='"5+" Acca issurance signpost icon is not shown')
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_my_bets__go_to_open_bets_tab(self):
        """
        DESCRIPTION: 1.Navigate to My Bets-->Go to Open bets tab
        EXPECTED: Open bets tab should be Opened.
        """
        self.site.open_my_bets_open_bets()
        open_bets = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(open_bets, msg='No bets found in open bet')
        self.assertTrue(open_bets.has_acca_insurance_icon(), msg='"5+" Acca issurance signpost icon is not shown')
        # odds boost text xpath is representing here for acca insurance text
        self.assertEqual(open_bets.odds_boost_text, vec.bma.ACCA_INSURANCE,
                         msg=f'Actual text:"{open_bets.odds_boost_text}" is not as Expected text:"{vec.bma.ACCA_INSURANCE}".')

    def test_002_verify_signposting_acca_insurance_promo(self):
        """
        DESCRIPTION: 2.Verify Signposting ACCA Insurance promo
        EXPECTED: The Signposting ACCA Insurance promo should be displayed in Open bets section at top level of the overall bet.
        """
        # covered in step 1

    def test_003_navigate_to_my_bets__go_to_settled_bet_tab(self):
        """
        DESCRIPTION: 3.Navigate to My Bets-->Go to Settled bet tab
        EXPECTED: Settled bets tab should be opened.
        """
        self.site.go_to_home_page()
        # Setteling the bet
        self.ob_config.update_selection_result(event_id=self.event_ids[0],
                                               selection_id=self.selection_ids[0],
                                               market_id=self.market_ids[0], result='L')
        sleep(5)
        self.device.refresh_page()
        self.site.wait_content_state('homepage')
        self.site.open_my_bets_settled_bets()
        wait_for_result(lambda: self.site.bet_history.tab_content.accordions_list.is_displayed(timeout=10) is True,
                        timeout=60)
        settle_bet = list(self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(settle_bet.has_acca_insurance_icon(), msg='"5+" Acca issurance signpost icon is not shown')
        self.assertEqual(settle_bet.odds_boost_text, vec.bma.ACCA_INSURANCE,
                         msg=f'Actual text:"{settle_bet.odds_boost_text}" is not as Expected text:"{vec.bma.ACCA_INSURANCE}".')

    def test_004_verify_signposting_acca_insurance_promo(self):
        """
        DESCRIPTION: 4.Verify SignPosting ACCA Insurance Promo
        EXPECTED: The Signposting ACCA Insurance promo should be displayed in Settled bets section at top level of the overall bet.
        """
        # covered in step 3
