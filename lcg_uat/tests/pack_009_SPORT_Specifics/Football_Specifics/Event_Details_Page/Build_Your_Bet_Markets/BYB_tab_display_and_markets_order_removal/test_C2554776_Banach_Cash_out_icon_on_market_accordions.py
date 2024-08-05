import pytest
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest


@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.banach
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C2554776_Banach_Cash_out_icon_on_market_accordions(BaseBanachTest):
    """
    TR_ID: C2554776
    NAME: Banach. Cash out icon on market accordions
    DESCRIPTION: This test case verifies 'cash out' icon being displayed/not displayed on Banach market accordions on 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab
    PRECONDITIONS: **Config:**
    PRECONDITIONS: Build Your Bet tab is available on Event Details Page : In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableTab' is selected
    PRECONDITIONS: Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: Event belonging to Banach league is mapped (on Banach side) and created in OpenBet (T.I.)
    PRECONDITIONS: BYB markets are added in CMS -> BYB -> BYB Markets
    PRECONDITIONS: Guide for Banach CMS configuration: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Banach
    PRECONDITIONS: **Requests:**
    PRECONDITIONS: Request for Banach leagues : https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach event data: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events/obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/selections?marketIds=[ids]&obEventId=xxxxx
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. Navigate to the Event Details page where 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab is available
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
         PRECONDITIONS: BYB markets are added in CMS -> BYB -> BYB Markets
        """
        self.__class__.proxy = None
        self.__class__.eventID = self.get_ob_event_with_byb_market()
        byb_markets = self.cms_config.get_build_your_bet_markets()
        byb_cms_markets = []
        for market in byb_markets:
            if 'Participant_1' in market['bybMarket']:  # todo: check on mock
                market_name = market['name'].replace('Home', self.team1).title()
            elif 'Participant_2' in market['bybMarket']:
                market_name = market['name'].replace('Away', self.team2).title()
            else:
                market_name = market['name'].title()
            byb_cms_markets.append(market_name)
        self.__class__.byb_cms_markets = byb_cms_markets
        self.navigate_to_edp(event_id=self.eventID)

    def test_001_clicktap_on_build_your_bet_coral__bet_builder_ladbrokes_tab(self):
        """
        DESCRIPTION: Click/Tap on 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab
        EXPECTED: * 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab is opened and selected
        EXPECTED: * Markets which are coming in **markets-grouped** request and are added in CMS are displayed as market accordions
        """
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        self.__class__.markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets, msg='No markets found')
        market_names = [key.title() for key in self.markets.keys()]
        self.assertTrue(set(market_names).issubset(set(self.byb_cms_markets)),
                        msg=f'Unexpected markets {set(market_names) - set(self.byb_cms_markets)} not found in CMS')

    def test_002_verify_cash_out_icon(self):
        """
        DESCRIPTION: Verify 'cash out' icon
        EXPECTED: * 'Cash out' icon is displayed on all market accordions apart from 'Player Bets'
        EXPECTED: * 'Cash out' icon is hard-coded
        """
        for market_name, market in list(self.markets.items()):
            if market_name == 'Player Bets':
                market_value = self.markets.get(market_name)
                self.assertFalse(market_value.market_section_header.has_cash_out_mark(),
                                 msg=f'Market "{market_value}" has cashout label')
            else:
                market_value = self.markets.get(market_name)
                self.assertTrue(market_value.market_section_header.has_cash_out_mark(),
                                msg=f'Market "{market_value}" has no cashout label')
