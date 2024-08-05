import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # We can not change live prices on PROD
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.sanity
@pytest.mark.homepage_featured
@vtest
class Test_C43885008_Verify_live_updates_on_Surface_Bets_module(BaseFeaturedTest):
    """
    TR_ID: C43885008
    NAME: Verify  live updates on 'Surface Bets' module
    DESCRIPTION: Test case verifies live updates on 'Surface Bets' module
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Homepage -> 'Featured' tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: 1) 'Surface Bets' module should be "Active" in CMS > Sport Pages > Homepage > Surface Bets module
    PRECONDITIONS: 2) You should have active 'Surface Bets' module with active events in CMS > Sport Pages > Homepage > Surface Bets module
    PRECONDITIONS: - Surface Bets module should be configured by EventIDs
    PRECONDITIONS: - Surface Bets module should be configured by SelectionID
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 2) To verify data for created 'Surface Bets' module use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket (featured-sports...) -> response with type: "FEATURED_STRUCTURE_CHANGED" -> modules -> @type: "SurfaceBetModuleData" and choose the appropriate module.
    PRECONDITIONS: ![](index.php?/attachments/get/37874412)
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Surface Bets" module should be "Active" in CMS > Sport Pages > Homepage > Surface Bets module
    PRECONDITIONS: - You should have an active Surface Bets module with active events in CMS > Sport Pages > Homepage > Surface Bets module
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True
    prices = {'odds_home': '1/12', 'odds_draw': '1/13', 'odds_away': '1/14'}
    increased_price = '3/1'
    decreased_price = '5/2'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Surface Bet to the SLP/Homepage in the CMS
        DESCRIPTION: Open this SLP/Homepage page in the application
        """
        cms_surface_bet = self.cms_config.get_sport_module(sport_id=self.ob_config.backend.ti.football.category_id,
                                                           module_type='SURFACE_BET')[0]
        if cms_surface_bet['disabled']:
            self.cms_config.change_sport_module_state(sport_module=cms_surface_bet)

        event = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices)
        selection_ids, self.__class__.team1 = event.selection_ids, event.team1
        self.__class__.selection_id = selection_ids[self.team1]
        surface_bet = self.cms_config.add_surface_bet(selection_id=self.selection_id,
                                                      categoryIDs=self.ob_config.football_config.category_id)

        surface_bet_title = surface_bet.get('title').upper()

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

        result = self.wait_for_surface_bets(name=surface_bet_title, timeout=1, poll_interval=1,
                                            raise_exceptions=False)
        if result is None:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.wait_for_surface_bets(name=surface_bet_title, timeout=15, poll_interval=1)

        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{surface_bet_title}" not found in "{list(surface_bets.keys())}"')

    def test_001___in_ti_tool_increase_the_price_for_one_of_the_selections_of_event_displayed_in_surface_bets_module__verify_live_updates_in_surface_bets_module(
            self):
        """
        DESCRIPTION: - In TI tool increase the price for one of the selections of event displayed in Surface Bets module
        DESCRIPTION: - Verify live updates in Surface Bets module
        EXPECTED: - Corresponding 'Price/Odds' button immediately displays new price
        EXPECTED: - The outcome button changes its color to red for a few seconds
        """
        self.ob_config.change_price(selection_id=self.selection_id, price=self.increased_price)

        result = self.wait_for_price_update_from_live_serv(selection_id=self.selection_id,
                                                           price=self.increased_price)
        self.assertTrue(result,
                        msg=f'Price update for selection "{self.team1}" with id "{self.selection_id}" is not received')

    def test_002___in_ti_tool_decrease_the_price_for_one_of_the_selections_of_event_displayed_in_surface_bets_module__verify_live_updates_in_surface_bets_module(
            self):
        """
        DESCRIPTION: - In TI tool decrease the price for one of the selections of event displayed in Surface Bets module
        DESCRIPTION: - Verify live updates in Surface Bets module
        EXPECTED: - Corresponding 'Price/Odds' button immediately displays new price
        EXPECTED: - The outcome button changes its color to blue for a few seconds
        """
        self.ob_config.change_price(selection_id=self.selection_id, price=self.decreased_price)
        result = self.wait_for_price_update_from_live_serv(selection_id=self.selection_id,
                                                           price=self.decreased_price)
        self.assertTrue(result,
                        msg=f'Price update for selection "{self.team1}" with id "{self.selection_id}" is not received')
