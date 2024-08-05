import pytest
import tests
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import cleanhtml


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.cms
@pytest.mark.desktop
@pytest.mark.banach
@pytest.mark.build_your_bet
@pytest.mark.critical
@pytest.mark.sports
@vtest
class Test_C2553355_Build_Your_Bet_tab_content(BaseBanachTest):
    """
    TR_ID: C2553355
    NAME: Verify 'Build Your Bet'/'Bet Builder' tab content
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Static block CMS config
    PRECONDITIONS: YourCall > YourCall Static blocks > yourcall-tab static block is enabled
    PRECONDITIONS: Dev Tools> Network > XHR: Request to Banach for /events/event_id on EDP should return data
    PRECONDITIONS: To check response from Banach with markets:  **markets-grouped** request
    PRECONDITIONS: To check which of markets are added to CMS : cms/api/bma/byb-markets (BYB > BYB markets in CMS)
    PRECONDITIONS: **Event details page of Banach event is loaded**
    """
    keep_browser_open = True
    yc_cms_static_title = 'yourcall-page'
    is_yc_static_block_enabled = None
    yc_static_block_text = ''
    byb_cms_markets = []
    expanded_count = 2
    maxDiff = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Preconditions
        DESCRIPTION: Get event with BYB available
        DESCRIPTION: Enable YC static block
        DESCRIPTION: Get list of available BYB markets
        DESCRIPTION: Open EDP
        EXPECTED: Event details page of Banach event is loaded
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.proxy = None
            self.__class__.eventID = self.get_ob_event_with_byb_market()
        else:
            self.__class__.eventID = self.create_ob_event_for_mock(team1='Test team 1', team2='Test team 2')

        is_yc_static_block_enabled = self.cms_config.is_your_call_static_block_enabled(title=self.yc_cms_static_title)
        if tests.settings.cms_env == 'prd0':
            if not is_yc_static_block_enabled:
                raise CmsClientException(f'"{self.yc_cms_static_title}" is disabled in CMS')
            self.__class__.is_yc_static_block_enabled = is_yc_static_block_enabled
        else:
            self.cms_config.update_your_call_static_block(title=self.yc_cms_static_title, enabled=True)
            self.__class__.is_yc_static_block_enabled = True

        yc_static_block = self.cms_config.get_your_call_static_block_by_title(title=self.yc_cms_static_title)
        self.__class__.yc_static_block_text = cleanhtml(yc_static_block['htmlMarkup'])

        byb_markets = self.cms_config.get_build_your_bet_markets()
        byb_cms_markets = []
        for market in byb_markets:
            if 'Participant_1' in market['bybMarket']:  # todo: check on mock
                market_name = market['name'].replace('Home', self.team1).upper() \
                    if self.device_type != 'desktop' \
                    else market['name'].replace('Home', self.team1).title()
            elif 'Participant_2' in market['bybMarket']:
                market_name = market['name'].replace('Away', self.team2).upper() \
                    if self.device_type != 'desktop' \
                    else market['name'].replace('Away', self.team2).title()
            else:
                market_name = market['name'].upper() \
                    if self.device_type != 'desktop' \
                    else market['name'].title()
            byb_cms_markets.append(market_name)
        self.__class__.byb_cms_markets = byb_cms_markets

        self.navigate_to_edp(event_id=self.eventID)

    def test_001_tap_on_the_build_your_bet_tab(self):
        """
        DESCRIPTION: Tap on the Build Your Bet tab
        EXPECTED: Build Your Bet tab is opened and selected
        EXPECTED: Url path ends with /build-your-bet
        """
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        url = self.device.get_current_url()
        url_expected = '/bet-builder' if self.brand == 'ladbrokes' else '/build-your-bet'
        self.assertTrue(url.endswith(url_expected), msg=f'Current url "{url}" does not end with "{url_expected}"')

    def test_002_verify_static_block_display(self):
        """
        DESCRIPTION: Verify static block display
        EXPECTED: yourcall-tab static block text is displayed above markets accordions
        """
        static_block = self.site.sport_event_details.tab_content.static_block
        self.assertEqual(static_block.is_displayed(expected_result=self.is_yc_static_block_enabled),
                         self.is_yc_static_block_enabled,
                         msg=f'Static block shown status is not "{self.is_yc_static_block_enabled}"')

        if tests.settings.cms_env == 'prd0' and not self.is_yc_static_block_enabled:
            self._logger.warning('*** Cannot check static block text as it\'s disabled on production')
        else:
            text = static_block.static_text
            expected_text = self.yc_static_block_text.strip().replace('\r', '')
            self.assertEqual(text, expected_text,
                             msg=f'Actual text "{text}" is not same as '
                                 f'Expected text "{expected_text}"')

    def test_003_verify_markets_accordions(self):
        """
        DESCRIPTION: Verify markets accordions
        EXPECTED: 2 markets accordions are expanded by default
        EXPECTED: Markets which are coming in **markets-grouped** request and are added in CMS are displayed as market accordions
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets found')
        if self.device_type == 'desktop':
            expanded_count = 0
            for (market_name, market) in list(markets.items()):
                if market.is_expanded():
                    expanded_count = expanded_count + 1
                else:
                    self.assertFalse(market.is_expanded(expected_result=False),
                                     msg=f'"{market_name}" is not collapsed by default')
            self.assertEqual(expanded_count, self.expanded_count,
                             msg=f'Actual expanded  count expanded_count{self.expanded_count}'
                                 f' is not same as expected expanded by default {expanded_count}')
        else:
            [self.assertTrue(market.is_expanded(), msg=f'"{market_name}" is not expanded by default')
             for (market_name, market) in list(markets.items())[:self.expanded_count]]

            [self.assertFalse(market.is_expanded(expected_result=False), msg=f'"{market_name}" is not collapsed by default')
             for (market_name, market) in list(markets.items())[self.expanded_count:]]

        market_names = [key.title() for key in markets.keys() if '/' in key and self.device_type == 'desktop']
        self.assertTrue(set(market_names).issubset(set(self.byb_cms_markets)),
                        msg=f'Unexpected markets {set(market_names) - set(self.byb_cms_markets)} not found in CMS')
