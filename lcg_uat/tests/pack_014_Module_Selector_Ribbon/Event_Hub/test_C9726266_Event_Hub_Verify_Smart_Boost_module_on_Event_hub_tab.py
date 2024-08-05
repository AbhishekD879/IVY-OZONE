import pytest
from tests.base_test import vtest
from faker import Faker
import voltron.environments.constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot create Event hub in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.other
@vtest
class Test_C9726266_Event_Hub_Verify_Smart_Boost_module_on_Event_hub_tab(BaseSportTest):
    """
    TR_ID: C9726266
    NAME: Event Hub: Verify 'Smart Boost' module on Event hub tab
    DESCRIPTION: This test case verifies the Smart Boost module and its content on Event Hub tab
    PRECONDITIONS: 1. Event Hub module is configured in CMS > Sport Pages > Event Hub
    PRECONDITIONS: 2. Smart Boost module is configured in CMS (with 'Select Events by: Selection' option while configuring) and is Active
    PRECONDITIONS: 3. Module has selections with Price Boost flags in Open Bet TI
    PRECONDITIONS: 4. Selection contains 'Was price' value in its name in brackets in Open Bet TI (in decimal format)
    PRECONDITIONS: 5. User is on Event Hub tab
    """
    keep_browser_open = True
    required_qty = 1
    fake = Faker()
    content = fake.paragraph()
    price_num = fake.random_int(min=1, max=10)
    price_den = fake.random_int(min=20, max=50)

    def test_000_preconditions(self):
        """
        DESCRIPTION:- Create Events and Event hub with smart boost
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        selection_ids, team1 = event.selection_ids, event.team1
        self.__class__.eventID = event.event_id

        # Create Event Hub module
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]

        # need a unique non-existing index for new Event hub
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)

        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='SURFACE_BET')

        self.__class__.surface_bet = self.cms_config.add_surface_bet(selection_id=selection_ids[team1],
                                                                     content=self.content,
                                                                     priceNum=self.price_num,
                                                                     priceDen=self.price_den,
                                                                     eventIDs=self.eventID,
                                                                     categoryIDs=[0, 16],
                                                                     event_hub_id=index_number,
                                                                     edpOn=True,
                                                                     highlightsTabOn=True)
        self.__class__.surface_bet_title = self.surface_bet.get('title').upper()

        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()

    def test_001_verify_selections_within_the_module(self):
        """
        DESCRIPTION: Verify selections within the module
        EXPECTED: Only 1 selection is present within the module with smart boost available
        """
        self.site.login()
        self.site.wait_content_state_changed(timeout=15)
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        self.site.back_button_click()
        self.site.wait_content_state_changed()
        event_hub = True
        while event_hub:
            module_tab = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.keys()
            if self.event_hub_tab_name in module_tab:
                self.site.home.module_selection_ribbon.tab_menu.click_button(self.event_hub_tab_name)
                event_hub = False
            else:
                self.device.refresh_page()
                self.site.wait_content_state_changed()

        while not event_hub:
            try:
                self.site.wait_content_state_changed()
                self.__class__.surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict.get(
                    self.surface_bet['title'].upper())
                event_hub = True
            except Exception as e:
                self._logger.info(msg=f' Surface module not found got {e} Exception')
                event_hub = False

        bet_buttons_qty = self.surface_bets.items_as_ordered_dict
        self.assertEqual(len(bet_buttons_qty), self.required_qty,
                         msg=f'Actual Bet Qty: "{bet_buttons_qty}" is not same as'
                             f'Expected Bet Qty: "{self.required_qty}" , Only 1 selection not present')

        self.assertIn(vec.sb.WAS_PRICE, self.surface_bets.old_price.label,
                      msg='Smart Boost not Available ')
        self.check_odds_format(odds=list(bet_buttons_qty.keys())[0], expected_odds_format='decimal')

    def test_002_verify_the_format_of_selection(self):
        """
        DESCRIPTION: Verify the format of selection
        EXPECTED: * Selection name is displayed on the left
        EXPECTED: * Price odds button is displayed opposite to the selection name (on the right)
        EXPECTED: * Previous price of selection is placed under price odds button (on the right)
        EXPECTED: * Start time/date of event is displayed under selection name (on the left)
        """
        self.assertTrue(self.surface_bets.content, msg='Selection name is not present ')
        self.assertTrue(self.surface_bets.bet_button, msg='Price odds button is not displayed')
        self.assertTrue(self.surface_bets.old_price, msg='Previous price of selection is not placed')

    def test_003_switch_to_fractional_format_top_right_menu__settings__odds_format(self):
        """
        DESCRIPTION: Switch to fractional format (top right menu-> Settings-> odds format)
        EXPECTED: Selection previous price remains crossed out and displayed under odd price button
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Fractional')

        self.site.back_button_click()
        self.site.wait_content_state_changed()
        self.site.home.module_selection_ribbon.tab_menu.click_button(self.event_hub_tab_name)

        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict.get(
            self.surface_bet['title'].upper())
        self.assertIn(vec.sb.WAS_PRICE, surface_bets.old_price.label,
                      msg='Smart Boost not Available ')
        bet_buttons_qty = surface_bets.items_as_ordered_dict
        self.check_odds_format(odds=list(bet_buttons_qty.keys())[0])

    def test_004_click_on_the_selection_within_the_module_on_event_hub_tab(self):
        """
        DESCRIPTION: Click on the selection within the module on Event Hub tab
        EXPECTED: User is redirected to its EDP
        """
        # need to check in edp whether surface bet is displayed or not as step need modification
        self.navigate_to_edp(event_id=self.eventID)
        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        ui_surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(ui_surface_bet, msg='surface bets is not found in edp')
