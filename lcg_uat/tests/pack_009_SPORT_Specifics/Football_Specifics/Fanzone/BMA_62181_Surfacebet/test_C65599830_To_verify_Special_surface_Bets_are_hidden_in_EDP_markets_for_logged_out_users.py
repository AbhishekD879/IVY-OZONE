import voltron.environments.constants as vec
import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod     # cannot create special markets in prod and Beta
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65599830_To_verify_Special_surface_Bets_are_hidden_in_EDP_markets_for_logged_out_users_as_well(Common):
    """
    TR_ID: C65599830
    NAME: To verify Special surface Bets are hidden in EDP markets for logged out users as well
    DESCRIPTION: To verify Special surface Bets are hidden in EDP markets for logged out users as well
    PRECONDITIONS: 1) Evens should be created and Special Marktes should be configured in Open Bet
    PRECONDITIONS: Event Creation-->Market Creation page--> Flags section-> Enable FANZONE checkbox
    PRECONDITIONS: 2) Fanzone should be enabled in CMS-->System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 3) Surface Bets should be configured using selections from Special Markets
    PRECONDITIONS: CMS--> Sports Pages--> Sports Categeories--> Fanzone-->Surface Bets
    PRECONDITIONS: 4) User should not subscribe to any Fanzone team
    """
    keep_browser_open = True
    price_num = 4
    price_den = 9

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1) Evens should be created and Special Marktes should be configured in Open Bet
        PRECONDITIONS: Event Creation-->Market Creation page--> Flags section-> Enable FANZONE checkbox
        PRECONDITIONS: 2) Fanzone should be enabled in CMS-->System Configuration--> Structure-->Fanzone
        PRECONDITIONS: 3) Surface Bets should be configured using selections from Special Markets
        PRECONDITIONS: CMS--> Sports Pages--> Sports Categeories--> Fanzone-->Surface Bets
        PRECONDITIONS: 4) User should not subscribe to any Fanzone team
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score
        event_params = self.ob_config.add_autotest_premier_league_football_event(special=True, default_market_name=market_name)
        self.__class__.event_id = event_params.event_id
        actual_market_name, market_id = \
            next(iter(self.ob_config.market_ids.get(self.event_id).items()))
        selection_id = event_params.selection_ids[event_params.team1]
        market_template_id = next(iter(self.ob_config.football_config.autotest_class.
                                       autotest_premier_league.markets.get(actual_market_name).values()))
        self.ob_config.make_market_special(
            market_id=market_id,
            market_template_id=market_template_id,
            event_id=self.event_id,
            flags='FZ')

        self.cms_config.add_fanzone_surface_bet(selection_id=selection_id,
                                                              priceNum=self.price_num,
                                                              priceDen=self.price_den)

    def test_001_navigate_to_event_details_page_for_which_special_markets_are_configured(self):
        """
        DESCRIPTION: Navigate to Event details page for which Special Markets are configured
        EXPECTED: User should be navigated to EDP
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails', timeout=20)

    def test_002_verify_special_markets_are_not_displayed_for_logged_out_user(self):
        """
        DESCRIPTION: Verify Special Markets are not displayed to logged out user
        EXPECTED: Special markets shouldn't be displayed to logged out users.
        """
        markets = self.site.sport_event_details.tab_content.has_no_events_label()
        self.assertTrue(markets, msg='Special markets are displayed')
