import datetime
import pytest
import tests
from collections import OrderedDict
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.lad_tst2  # Ladbrokes only feature
@pytest.mark.lad_uat
@pytest.mark.acca
@pytest.mark.desktop
# @pytest.mark.prod #It doesnt applicable for prod as acca signposting offer cant be granted
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870226_Acca_Insurance__Verify_Signposting_Betslip_BetReceipt_My_Bets(BaseCashOutTest):
    """
    TR_ID: C44870226
    NAME: Acca Insurance - Verify Signposting (Betslip/BetReceipt/My Bets)
    PRECONDITIONS: Football only.
    PRECONDITIONS: W-D-W only
    PRECONDITIONS: 5+ selections minimum.
    PRECONDITIONS: Valid on only 1st acca placed during the day.
    PRECONDITIONS: Minimum selection price 1/10.
    PRECONDITIONS: Minimum acca price 3/1.
    PRECONDITIONS: Up to Â£10 returned if 1 selection lets you down as a free bet
    """
    keep_browser_open = True
    prices = OrderedDict([('odds_home', '3/1'),
                          ('odds_draw', '1/17'),
                          ('odds_away', '1/4')])
    event_ids = []
    market_ids = []
    selection_ids = []
    suspension_status = False

    def test_001_user_launches_the_siteapp_and_logs_in(self):
        """
        DESCRIPTION: User launches the site/app and logs in
        EXPECTED: User is able to place a bet as logged in customer
        """
        ema_config = self.get_initial_data_system_configuration().get('EMA')
        if not ema_config:
            ema_config = self.cms_config.get_system_configuration_item('EMA')
        if not ema_config:
            raise CmsClientException('"EMA" section not found in System Config')
        if not ema_config.get('enabled'):
            self.cms_config.set_my_acca_section_cms_status(ems_status=True)
        now = datetime.datetime.now()
        shifted_year = str(now.year + 5)
        username = self.gvc_wallet_user_client.register_new_user().username
        status = self.gvc_wallet_user_client.add_payment_card_and_deposit(amount="20",
                                                                          card_number=tests.settings.visa_card,
                                                                          card_type='visa',
                                                                          expiry_month=f'{now.month:02d}',
                                                                          expiry_year=shifted_year,
                                                                          cvv=tests.settings.visa_card_cvv)
        self.assertTrue(status, msg='The card is not added successfully')
        self.site.login(username=username)
        self.assertTrue(self.site.wait_content_state('HOMEPAGE', timeout=60), msg='User is not navigated to homepage')
        for index in range(6):
            event = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True, lp=self.prices)
            self.event_ids.append(event.event_id)
            self.market_ids.append(event.default_market_id)
            self.selection_ids.append(list(event.selection_ids.values())[0])

    def test_002_navigate_to_football_slp(self):
        """
        DESCRIPTION: Navigate to Football SLP
        EXPECTED: User navigated to Football SLP
        """
        self.site.open_sport(name='FOOTBALL')
        self.site.wait_content_state(state_name='Football')

    def test_003_place_5plus_w_d_w_acca_preplay_bet(self):
        """
        DESCRIPTION: Place 5+ W-D-W Acca (Preplay) bet
        EXPECTED: User has successfully placed a 5+ Acca and the Acca Insurance signposting is available in the bet slip,bet receipt and open bets and settled bets as per design
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.ACC5, sections.keys(),
                      msg=f'No "{vec.betslip.ACC5}" stake was found in "{sections.keys()}"')
        stake = list(sections.values())[0]
        self.assertTrue(stake.has_acca_insurance_icon(), msg='Acca Insurance Icon is not displayed')
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()

        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        first_section = list(betreceipt_sections.values())[0]
        self.assertTrue(first_section, msg='Betreceipt not found')
        self.assertTrue(first_section.has_acca_sign_post(),
                        msg='"5+ Acca Insurance" Sign post is not present on betreceipt')
        self.site.bet_receipt.close_button.click()
        self.site.wait_content_state_changed()
        if self.device_type == 'mobile':
            self.site.open_my_bets_open_bets()
        else:
            self.navigate_to_page('open-bets')
        self.site.close_all_dialogs()
        self.site.wait_content_state('open-bets')
        open_bets = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(open_bets, msg='No bets found in open bet')
        self.assertTrue(open_bets.has_acca_insurance_icon(), msg='"5+" Acca issurance signpost icon is not shown')
        self.ob_config.update_selection_result(event_id=self.event_ids[0], market_id=self.market_ids[0],
                                               selection_id=self.selection_ids[0], result='L')
        self.device.refresh_page()
        self.site.wait_content_state_changed()
        if self.device_type == 'mobile':
            self.site.open_my_bets_settled_bets()
        else:
            self.navigate_to_page('bet-history')
            self.site.wait_content_state('bet-history')
        self.site.close_all_dialogs()
        self.device.refresh_page()
        self.device.refresh_page()
        settled_bets = list(self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(settled_bets, msg='No bets found in open bet')
        self.site.wait_content_state_changed()
        self.assertTrue(settled_bets.has_acca_insurance_icon(timeout=10),
                        msg='"5+" Acca insurance signpost is not shown')
