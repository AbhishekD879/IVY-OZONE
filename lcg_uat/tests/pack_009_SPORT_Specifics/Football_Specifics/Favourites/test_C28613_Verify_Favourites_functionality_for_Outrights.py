import time

import pytest
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

import tests
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
import voltron.environments.constants as vec
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_prod  # Coral only
@pytest.mark.crl_hl
@pytest.mark.crl_stg2
@pytest.mark.crl_tst2
@pytest.mark.football
@pytest.mark.favourites
@pytest.mark.outrights
@pytest.mark.bet_placement
@pytest.mark.cash_out
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.portal_dependant
@vtest
class Test_C28613_Verify_Favourites_functionality_for_Outrights(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C28613
    NAME: Verify Favourites functionality for Outrights
    DESCRIPTION: This Test Case verified Favourites functionality for Outrights
    PRECONDITIONS: JIRA Ticket: BMA-9827 Hide Favourites Icon For non-match Football Events
    """
    keep_browser_open = True
    market_name = None
    outright_name = None
    selection_name = None
    section_name = None
    sport_name = 'Football'

    def basic_active_events_filter(self):
        return self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME,
                                      OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date_minus))

    def test_001_create_outright_event(self):
        """
        DESCRIPTION: Create outright event
        """
        if self.cms_config.get_widgets(widget_type='favourites')[0]['disabled']:
            raise CmsClientException('"Favourites" widget is disabled in CMS')

        if tests.settings.backend_env == 'prod':
            class_ids = self.get_class_ids_for_category(category_id=self.ob_config.football_config.category_id)

            ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                       class_id=class_ids,
                                       brand=self.brand)
            events_filter = self.basic_active_events_filter() \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M'))\
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_SORT_CODE, OPERATORS.INTERSECTS,
                                          vec.siteserve.OUTRIGHT_EVENT_SORT_CODES))

            resp = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter)
            event = next((event for event in resp if
                          event.get('event') and event['event'] and event['event'].get('children')), None)
            if not event:
                raise SiteServeException(f'No active events found for category id "{self.ob_config.football_config.category_id}"')
            self.__class__.outright_name = normalize_name(event['event']['name'])
            self.__class__.eventID = event['event']['id']
            class_name = event['event']['className'].split()[-1].upper()
            type_name = event['event']['typeName'].upper()
            self.__class__.section_name = f'{class_name} - {type_name}'
            outcomes = event['event']['children'][0]['market']['children']
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}

        else:
            self.__class__.outright_name = 'Outright %s' % int(time.time())
            params = self.ob_config.add_autotest_premier_league_football_outright_event(event_name=self.outright_name,
                                                                                        selections_number=1)
            self.__class__.eventID = params.event_id
            self.__class__.selection_ids = params.selection_ids
            self.__class__.section_name = tests.settings.football_autotest_league
            event = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID, query_builder=self.ss_query_builder)[0]
        self.__class__.market_name = next((market['market']['name'] for market in event['event']['children']
                                           if market['market']['templateMarketName'] == 'Outright'), None)
        if not self.market_name:
            raise SiteServeException('No market with templateMarketName Outright')

        self.__class__.selection_name = list(self.selection_ids.keys())[0]

    def test_002_login(self):
        """
        DESCRIPTION: Login as user that has sufficient funds to place a bet
        DESCRIPTION: Disable Quick Bet
        EXPECTED: User is logged in
        EXPECTED: Quick Bet is disabled for user
        """
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)
        self.site.close_all_dialogs()
        if self.device_type == 'mobile':
            self.navigate_to_page(name='settings')
            self.site.wait_content_state('Settings')
            self.site.settings.allow_quick_bet.click()
            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')

    def test_003_tap_football(self):
        """
        DESCRIPTION: Tap on Football icon on the Sports Menu Ribbon
        EXPECTED: Football landing page is opened
        """
        self.site.open_sport(name=self.sport_name)

    def test_004_tap_outrights_tab(self):
        """
        DESCRIPTION: Tap on Outrights tab
        EXPECTED: Outrights page is opened
        """
        self.site.football.tabs_menu.click_button(self.expected_sport_tabs.outrights)
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, self.expected_sport_tabs.outrights,
                         msg=f'"{active_tab}" tab is not active, active tab is: "{self.expected_sport_tabs.outrights}"')

    def test_005_tap_competition_header(self):
        """
        DESCRIPTION: Tap on Competition header
        EXPECTED: Competition header is expanded
        EXPECTED: Outright and Relegation sections is shown
        """
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='*** No event sections are present on page')
        self.assertIn(self.section_name, sections)
        section = sections[self.section_name]
        section_header = section.group_header
        section_header.click()
        is_section_expanded = section.is_expanded()
        self.assertTrue(is_section_expanded, msg=f'Section "{self.section_name}" is not expanded')
        outrights = section.items_as_ordered_dict
        self.assertTrue(outrights, msg=f'*** No event outright is present in section: "{self.section_name}"')
        self.assertIn(self.outright_name, outrights)
        outright = outrights[self.outright_name]
        outright.click()

    def test_006_add_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add selection to the Bet Slip
        """
        self.site.wait_content_state(state_name='EventDetails')
        self.add_outright_selection(selection_name=self.selection_name, market_name=self.market_name)

        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

    def test_007_place_bet(self):
        """
        DESCRIPTION: Navigate to the Bet Slip and place a bet
        DESCRIPTION: Tap on Done button
        EXPECTED: Bet Receipt page is opened
        EXPECTED: Outright selection is shown on Bet Receipt page
        EXPECTED: Favourites Matches functionality is not included on Bet Receipt page
        """
        self.site.header.bet_slip_counter.click()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        for section_name, section in betreceipt_sections.items():
            receipts = section.items_as_ordered_dict
            self.assertTrue(receipts, msg='No Receipt legs found')
            for receipt_name, receipt in receipts.items():
                receipt_type = receipt.__class__.__name__
                if receipt_type == 'ReceiptSingles':
                    self.__class__.event_name = receipt.event_name
                    self.__class__.market_name = receipt.event_market.strip(' /')
                    self.__class__.total_stake = receipt.total_stake
                    self.__class__.estimate_returns = receipt.estimate_returns
                    if self.event_name == self.outright_name:
                        self.__class__.bet_id = receipt.bet_id
                        break
        self.assertTrue(self.bet_id, msg='Bet id is not found on Bet Receipt')
        has_match_center = self.site.bet_receipt.has_match_center
        self.assertFalse(has_match_center, msg="'Add all to favourites' and match center section are displayed")

        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state('EventDetails')

    def test_008_go_to_my_bets(self):
        """
        DESCRIPTION: Navigate to the My Bets page
        DESCRIPTION: Tap on Outright name
        EXPECTED: My Bets page is opened
        EXPECTED: Outright selection is shown on Cashout tab
        EXPECTED: Favourites Matches functionality is not included for current Outright selection
        """
        self.site.open_my_bets_cashout()
        bet_name, self.__class__.single_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.outright_name, number_of_bets=1)
        bet_legs = self.single_bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg='No one bet leg was found for bet: %s' % bet_name)

        # Stake and Returns
        self.assertEqual(self.single_bet.stake.stake_value, '{0:.2f}'.format(self.bet_amount),
                         msg='Total Stake amount "%s" is not equal to expected "%s" for bet "%s"' %
                             (self.single_bet.stake.value, self.total_stake, self.single_bet.name))

        self.assertEqual(self.single_bet.est_returns.stake_value, self.estimate_returns,
                         msg='Estimated returns: "%s" does not match with required: "%s"'
                             % (self.single_bet.est_returns.stake_value, self.estimate_returns))

        for betleg_name, betleg in bet_legs.items():
            name = f'{self.selection_name} - {self.outright_name}'
            self.assertIn(name, betleg_name, msg=f'"{name}" not found in "{betleg_name}"')
            self.assertEqual(betleg.market_name, self.market_name,
                             msg=f'"{betleg.market_name}" not found in "{self.market_name}"')

    def test_009_check_outright_page(self):
        """
        DESCRIPTION: Verify:
        EXPECTED: Outright details page is opened
        EXPECTED: My Bets tab is present
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name=self.sport_name)
        self.site.wait_content_state('EventDetails')
        tabs = self.site.sport_event_details.event_user_tabs_list.items_as_ordered_dict
        self.assertIn(self.my_bets_tab_name, tabs.keys())

    def test_010_go_to_my_bets(self):
        """
        DESCRIPTION: Go to My Bets:
        EXPECTED: 'My Bets' tab is opened
        EXPECTED: Outright selection is shown on 'My Bets' tab
        EXPECTED: 'Favourites Matches' functionality is not included for current Outright selection
        """
        self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)
        sections = wait_for_result(lambda: self.site.sport_event_details.my_bets.accordions_list.items_as_ordered_dict,
                                   name='Sections to load',
                                   timeout=2,
                                   bypass_exceptions=(StaleElementReferenceException, VoltronException, NoSuchElementException))
        self.assertTrue(sections, msg='Outright selection is not shown on "My Bets" tab')
        has_add_to_favourites = self.site.sport_event_details.has_favourite_icon(expected_result=False)
        self.assertFalse(has_add_to_favourites, msg='"Add favourites" button is displayed on Outright page')
