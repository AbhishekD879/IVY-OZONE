import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_haul



@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.bet_selection_details
@pytest.mark.insprint_auto
@pytest.mark.desktop
@vtest
class Test_C66113988_Verify_silks_stall_number_and_UI_for_horse_racing_bets_in_My_betsOpen_CashoutSettled(BaseRacing,BaseBetSlipTest):
    """
    TR_ID: C66113988
    NAME: Verify silks, stall number and UI for horse racing bets in My bets(Open, Cashout,Settled)
    DESCRIPTION: This testcase verifies silks, stall number and UI for horse racing bets in My bets(Open, Cashout,Settled)
    PRECONDITIONS: Horseracing bets should be available in Open,Cashout,Settled tabs
    """
    market_names_edp = []
    keep_browser_open = True
    selection_ids = None
    number_of_stakes = 1

    def test_000_preconditions(self):
        """
        TR_ID: C66113988
        NAME: Verify silks, stall number and UI for horse racing bets in My bets(Open, Cashout,Settled)
        DESCRIPTION: This testcase verifies silks, stall number and UI for horse racing bets in My bets(Open, Cashout,Settled)
        PRECONDITIONS: Horseracing bets should be available in Open,Cashout,Settled tabs
        """
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,additional_filters=cashout_filter, number_of_events=1)
        for event in events:
            market = next((market for market in event['event']['children'] if market['market']['templateMarketName'] == 'Win or Each Way'), None)
            outcomes_resp = market['market']['children']
            selection = next((i for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']), None)
            if not selection:
                continue
            self.__class__.selection_id = selection['outcome']['id']
            self.__class__.event_names = event['event']['name'].replace('|', '')
            self.market_names_edp.append(f"Win or Each Way, {market['market']['eachWayFactorNum']}/{market['market']['eachWayFactorDen']} odds - places {','.join([str(i) for i in range(1, int(market['market']['eachWayPlaces']) + 1)])}")
            if self.selection_id:
                break
        if not self.selection_id:
            raise SiteServeException('Enough Events are not available to place treble bet.')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.login()
        self.open_betslip_with_selections(selection_ids=[self.selection_id])

    def test_002_login_to_the_application_with_valid_credentials_with_precondition(self):
        """
        DESCRIPTION: Login to the application with valid credentials with precondition
        EXPECTED: User is logged in
        """
        self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        if self.device == "mobile":
            self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        self.__class__.bet_name, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_names)
        self.assertTrue(self.event_names in self.bet_name, msg=f'*** "{self.event_names}" bet not found in the openbets')
        self.assertEqual(self.bet.bet_type, f'{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE}',
                         msg=f'Bet type "{self.bet.bet_type}" is not the same as expected SINGLE')
        self.__class__.bet_legs = self.bet.items_as_ordered_dict
        betleg_name, betleg = list(self.bet_legs.items())[0]
        self.assertTrue(self.bet_legs, msg=f'No one bet leg was found for bet: "{self.bet_name}"')
        self.assertTrue(betleg.has_silk(), msg=f'Silk image for "{betleg_name}" is not shown')
        self.assertTrue(betleg.draw_number, msg=f'Bet leg draw number is not displayed')

    def test_004_verify_silksstall_number_and_ui_elements_for_horseracing_bets_in_open_tab(self):
        """
        DESCRIPTION: Verify silks,stall number and UI elements for horseracing bets in open tab
        EXPECTED: should be as per figma provided
        EXPECTED: ![](index.php?/attachments/get/2dda8ee3-a1f6-42b0-9d81-74288ab34e6d)
        """
        # Covered in above step

    def test_005_verify_silksstall_number_and_ui_elements_for_horseracing_bets_in_cashout_tab(self):
        """
        DESCRIPTION: Verify silks,stall number and UI elements for horseracing bets in Cashout tab
        EXPECTED: should be as per figma provided
        """
        self.site.open_my_bets_cashout()
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg=f'Bets are not found on "Cashout" page')
        bet = list(bets.values())[0]
        bet.buttons_panel.full_cashout_button.click()
        bet.buttons_panel.cashout_button.click()
        wait_for_haul(10)
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_names)
        self.assertTrue(self.event_names in self.bet_name, msg=f'*** "{self.event_names}" bet not found in the openbets')
        self.assertEqual(self.bet.bet_type, f'{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE}',
                         msg=f'Bet type "{self.bet.bet_type}" is not the same as expected SINGLE')
        self.__class__.bet_legs = self.bet.items_as_ordered_dict
        betleg_name, betleg = list(self.bet_legs.items())[0]
        self.assertTrue(self.bet_legs, msg=f'No one bet leg was found for bet: "{self.bet_name}"')
        self.assertTrue(betleg.has_silk(), msg=f'Silk image for "{betleg_name}" is not shown')
        self.assertTrue(betleg.draw_number, msg=f'Bet leg draw number is not displayed')

    def test_006_verify_silksstall_number_and_ui_elements_for_horseracing_bets_in_settled_tab(self):
        """
        DESCRIPTION: Verify silks,stall number and UI elements for horseracing bets in Settled tab
        EXPECTED: should be as per figma provided
        """
        self.site.open_my_bets_settled_bets()
        self.__class__.bet_name, self.__class__.bet = self.site.bet_history.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_names)
        self.assertTrue(self.event_names in self.bet_name, msg=f'*** "{self.event_names}" bet not found in the openbets')
        self.assertEqual(self.bet.bet_type, f'{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE}',
                         msg=f'Bet type "{self.bet.bet_type}" is not the same as expected SINGLE')
        self.__class__.bet_legs = self.bet.items_as_ordered_dict
        betleg_name, betleg = list(self.bet_legs.items())[0]
        self.assertTrue(self.bet_legs, msg=f'No one bet leg was found for bet: "{self.bet_name}"')
        self.assertTrue(betleg.has_silk(), msg=f'Silk image for "{betleg_name}" is not shown')
        self.assertTrue(betleg.draw_number, msg=f'Bet leg draw number is not displayed')