import pytest
from tests.base_test import vtest
from collections import OrderedDict
import tests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports_specific
@pytest.mark.basketball_specific
@pytest.mark.desktop
@pytest.mark.adhoc_suite
@pytest.mark.sports
@vtest
class Test_C66007948_Validate_signposting_display_in_Basketball_sport_landing_page(BaseUserAccountTest, BaseCashOutTest):
    """
    TR_ID: C66007948
    NAME: Validate signposting display in Basketball  sport landing page.
    DESCRIPTION: This test case needs to verify signposting display in Basketball sports landing page.
    PRECONDITIONS: 1.Signpostings created from Openbet needs to reflect in FE
    PRECONDITIONS: 2.User must be logged in /logout
    PRECONDITIONS: Note: In mobile when no events are available Basketball sport is not displayed in A-Z sports menu and on clicking Basketball  from Sports ribbon user is navigated back to the sports homepage.
    """
    keep_browser_open = True
    co_selection_ids = []
    number_of_events =2

    def watch_live_events(self, sections=[]):
        all_live_events_for_type = self.get_active_events_for_category(category_id=self.ob_config.basketball_config.category_id,
                                                                       all_available_events=True, in_play_event=True)
        filtered_events = []
        for event in all_live_events_for_type:
            is_watch_live = any(tag in event['event']['drilldownTagNames'] for tag in
                                ['EVFLAG_AVA', 'EVFLAG_IVM', 'EVFLAG_PVM', 'EVFLAG_RVA', 'EVFLAG_RPM',
                                 'EVFLAG_GVM'])

            filtered_event = {
                'name': event['event']['name'].upper(),
                'isWatchLive': is_watch_live
            }
            filtered_events.append(filtered_event)

        live_basketball_items = OrderedDict()
        for events in sections:
            for name, value in events.n_items_as_ordered_dict(no_of_items=6).items():
                for event in filtered_events:
                    if event['name'].upper() == name.upper():
                        live_basketball_items[name] = {
                            "value": value,
                            "isWatchLive": event['isWatchLive']
                        }
        return live_basketball_items

    def test_000_preconditions(self):
        """
                PRECONDITIONS: - Create or retrieve the events with cashout available
                """
        if tests.settings.backend_env == 'prod':
            # Filtering Cashout events
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                           'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                               OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.basketball_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.number_of_events)
            for event in events:
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                self.__class__.eventid = match_result_market['eventId']
                all_selection_ids = [i['outcome']['id'] for i in outcomes]
                selection_id = list(all_selection_ids)[0]
                self.co_selection_ids.append(selection_id)
            events = self.co_selection_ids
            # in-play events verification
            inplay_event = self.get_active_events_for_category(category_id=self.ob_config.basketball_config.category_id,
                                                               additional_filters=cashout_filter,
                                                               in_play_event=True)
            if not inplay_event:
                raise VoltronException("IN-PLAY events are not available in basketball")
        else:
            event_params = self.create_several_autotest_premier_league_football_events(
                number_of_events=self.number_of_events)
            self.__class__.co_selection_ids = [list(event.selection_ids.values())[0] for event in event_params]

    def test_001_launch_the_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes/Coral application
        EXPECTED: Home page should loaded successfully
        """
        self.site.login()

    def test_002_click_on_basketball_sport(self):
        """
        DESCRIPTION: Click on Basketball sport.
        EXPECTED: User should be able to navigate Basketball landing page.
        """
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')

    def test_003_verify_signposting(self):
        """
        DESCRIPTION: Verify signposting.
        EXPECTED: Signposting's need to be display as per OB creation
        """
        # verifying live and watch Live signposting
        if self.device_type == 'desktop':
            self.site.sports_page.tabs_menu.click_button(vec.inplay.BY_IN_PLAY.upper())
        else:
            current_tab = self.site.sports_page.tabs_menu.current.upper()
            matches_tab = vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper()
            if current_tab != matches_tab:
                self.site.sports_page.tabs_menu.click_button(matches_tab)
        inplay = self.site.sports_page.tab_content.accordions_list
        sections = list(inplay.n_items_as_ordered_dict(no_of_items=5).values())
        check_live = True
        live_events_for_basketball = self.watch_live_events(sections=sections)
        for event_name, event in live_events_for_basketball.items():
            event_object = event['value']
            live_icon = wait_for_result(lambda: event_object.live_button, expected_result=True, timeout=1)
            # watch_live_button
            if check_live:
                self.assertTrue(live_icon, msg=f"Live icon for event inplay '{event_name} not found'")
                if event['isWatchLive']:
                    self.assertTrue(event_object.watch_live_button,
                                    msg=f"Watch Live icon for event inplay '{event_name} not found'")
            else:
                self.assertFalse(live_icon, msg=f"Live icon for event inplay '{event_name} Found'")
            # verifying Special Signposting
            events = self.get_active_events_for_category(category_id=self.ob_config.basketball_config.category_id)
            for event in events:
                self._logger.info(msg='Event name is' + event['event']['name'])
                self.assertIn('M', event['event']['siteChannels'],
                              msg=f'Event attribute siteChannels does not contain "M" for "{event["event"]["name"]}"')
                if 'EVFLAG_SPL' in event['event']['drilldownTagNames']:
                    specials_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.specials.upper()
                    specials_tab = self.site.sports_page.tabs_menu.click_button(specials_tab_name)
                    current_tab_name = self.site.sports_page.tabs_menu.current.upper()
                    self.assertEqual(current_tab_name, specials_tab_name,
                                     msg=f'{current_tab_name} is not expected as {specials_tab_name}')
                    self.assertTrue(specials_tab, msg=f'"{specials_tab_name}" is not opened')
                    sections = self.site.sports_page.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=5)
                    self.assertTrue(sections, msg=f'no accordions are found')
                    event_type = sections.get(
                        f"{event['event']['className']} - {event['event']['typeName']}".upper())
                    event_type.expand()
                    events_FE = event_type.items_as_ordered_dict
                    events_name = [name.upper() for name in events_FE]
                    self.assertIn(event['event']['name'].upper(), events_name,
                                  msg="special event is not displayed under special tab")
                # Verifying Price Boost Signposting
                if 'EVFLAG_PB' in event['event']['drilldownTagNames']:
                    matches_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper()
                    matches_tab = self.site.sports_page.tabs_menu.click_button(matches_tab_name)
                    current_tab_name = self.site.sports_page.tabs_menu.current.upper()
                    self.assertEqual(current_tab_name, matches_tab_name,
                                     msg=f'{current_tab_name} is not expected as {matches_tab_name}')
                    self.assertTrue(matches_tab, msg=f'"{matches_tab_name}" is not opened')
                    sections = self.site.sports_page.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=5)
                    self.assertTrue(sections, msg=f'no accordions are found')
                    event_type = sections.get(
                        f"{event['event']['className']} - {event['event']['typeName']}".upper())
                    event_type.expand()
                    events_FE = event_type.items_as_ordered_dict
                    events_name = [name.upper() for name in events_FE]
                    self.assertIn(event['event']['name'].upper(), events_name,
                                  msg="price boost event is not displayed under matches tab")

            # verifying cash out signposting
        self.navigate_to_edp(event_id=self.eventid)
        market = 'MATCH BETTING' if self.brand == 'bma' and self.device_type=='mobile' else 'Match Betting'
        edp_cashout_label = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict.get(market)
        self.assertTrue(edp_cashout_label.section_header.has_cash_out_mark(), msg=f'"Cashout" label not displayed')
        edp_cashout_label.expand()
        edp_cashout_label.add_to_betslip_button.click()
        if self.device_type == 'mobile':
            self.site.wait_for_quick_bet_panel()
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.wait_quick_bet_overlay_to_hide()
        self.site.open_betslip()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        self.assertTrue(self.site.bet_receipt.has_cashout_label(), msg='"Cashout" label not displayed')

    def test_004_verify_by_clicking_on_sign_postings(self):
        """
        DESCRIPTION: Verify by clicking on sign postings.
        EXPECTED: User should be able to see popup text which is related to signposting.
        """
        # covered in above step

    def test_005_verify_signpostings_by_placing_the_bets(self):
        """
        DESCRIPTION: Verify signpostings by placing the bets
        EXPECTED: User should able to see sign postings wherever bet details are displayed (Bet Receipt/My Bets section)
        """
        # covered in above step
