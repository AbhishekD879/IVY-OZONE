import pytest
import voltron.environments.constants as vec
from faker import Faker
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create CMS modules on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.mobile_only
@vtest
class Test_C2855508_Vertify_Smart_Boost_module_on_Featured_tab(BaseSportTest):
    """
    TR_ID: C2855508
    NAME: Vertify 'Smart Boost' module on Featured tab
    DESCRIPTION: This test case verifies the Smart Boost module and its content on featured tab
    PRECONDITIONS: 1. User is on Featured Home page
    PRECONDITIONS: 2. Smart Boost module is configured in CMS (with 'Select Events by: Selection' option while configuring) and is Active
    PRECONDITIONS: 3. Module has selections with Price Boost flags in Open Bet TI
    PRECONDITIONS: 4. Selection contains 'Was price' value in its name in brackets in Open Bet TI (in decimal format)
    """
    keep_browser_open = True
    fake = Faker()
    content = fake.paragraph()
    price_num = fake.random_int(min=1, max=10)
    price_den = fake.random_int(min=20, max=50)
    required_qty = 1

    def test_000_preconditions(self):
        category_id = self.ob_config.football_config.category_id
        event = self.ob_config.add_autotest_premier_league_football_event()
        selection_ids, team1 = event.selection_ids, event.team1
        self.__class__.eventID = event.event_id

        surface_bet = self.cms_config.add_surface_bet(selection_id=selection_ids[team1],
                                                      categoryIDs=category_id,
                                                      content=self.content,
                                                      eventIDs=self.eventID,
                                                      edpOn=True,
                                                      priceNum=self.price_num,
                                                      priceDen=self.price_den,
                                                      highlightsTabOn=True
                                                      )
        self.__class__.surface_bet_title = surface_bet.get('title').upper()
        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Selection', id=selection_ids[team1])['title'].upper()
        self.site.login()
        self.site.wait_content_state_changed(timeout=15)

    def test_001_verify_selections_within_the_module(self, odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC):
        """
        DESCRIPTION: Verify selections within the module
        EXPECTED: Only 1 selection is present within the module with smart boost available
        """

        format_changed = self.site.change_odds_format(odds_format)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        self.site.back_button_click()
        self.site.wait_content_state_changed()
        self.__class__.surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict.get(
            self.surface_bet_title)
        self.surface_bets.scroll_to()
        bet_buttons_qty = self.surface_bets.items_as_ordered_dict
        self.assertEqual(len(bet_buttons_qty), self.required_qty,
                         msg=f'Actual Bet Qty: "{len(bet_buttons_qty)}" is not same as'
                             f'Expected Bet Qty: "{self.required_qty}" , Only 1 selection not present')
        self.assertIn(vec.sb.WAS_PRICE, self.surface_bets.old_price.label,
                      msg='Smart Boost not Available ')
        if odds_format == vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC:
            self.check_odds_format(odds=list(bet_buttons_qty.keys())[0], expected_odds_format='decimal')
        else:
            self.check_odds_format(odds=list(bet_buttons_qty.keys())[0])

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
        self.test_001_verify_selections_within_the_module(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC)

    def test_004_click_on_the_selection_within_the_module_on_featured_tab(self):
        """
        DESCRIPTION: Click on the selection within the module on Featured tab
        EXPECTED: User is redirected to its EDP
        """
        # need to check in edp whether surface bet is displayed or not as step need modification
        self.navigate_to_edp(event_id=self.eventID)
        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        ui_surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(ui_surface_bet, msg='surface bets is not found in edp')
