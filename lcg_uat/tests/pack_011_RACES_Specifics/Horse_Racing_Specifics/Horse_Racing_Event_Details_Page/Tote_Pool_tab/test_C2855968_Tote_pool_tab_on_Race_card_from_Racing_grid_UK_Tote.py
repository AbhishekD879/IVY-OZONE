import pytest
import voltron.environments.constants as vec
from json import JSONDecodeError
from time import sleep
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import do_request


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2855968_Tote_pool_tab_on_Race_card_from_Racing_grid_UK_Tote(BaseRacing):
    """
    TR_ID: C2855968
    NAME: Tote pool tab on Race card from Racing grid (UK Tote)
    DESCRIPTION: Test case verifies tote pool tab availability after navigation to Race card from UK & IRE grid
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure: Enable_ UK_ Totepools = True
    PRECONDITIONS: UK&IRE events with tote pools are available
    PRECONDITIONS: **Instruction on UK tote pool mapping**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+UK+Tote+event+to+the+Regular+HR+event
    PRECONDITIONS: **Request from pool types on EDP**
    PRECONDITIONS: PoolForEvent/event_id
    PRECONDITIONS: **User is on Horse Racing Landing page**
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def get_response(self):
        url = 'PoolForEvent'
        perflog = self.device.get_performance_log()
        final_request_url = ''

        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    final_request_url = request_url
                    break
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

        response = do_request(url=final_request_url, method='GET')
        return response

    def test_001_tap_on_the_event_from_uk__ire_having_tote_pool(self):
        """
        DESCRIPTION: Tap on the event from UK & IRE having tote pool
        EXPECTED: - Event Race card is opened
        EXPECTED: - Totepool tab is present on Race card
        """
        status = self.cms_config.get_system_configuration_structure()['TotePools']['Enable_UK_Totepools']
        if not status:
            raise CmsClientException('"Enable_UK_Totepools" is disabled in CMS')

        # Navigate to the Horse Racing SLP page
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

        # Selects the 'MEETINGS' or 'FEATURED' tab based on the brand
        tabs = self.site.horse_racing.tabs_menu.items_as_ordered_dict
        tab = next((tab for name, tab in tabs.items() if (name.upper() == 'MEETINGS' and self.brand != 'bma') or (
                name.upper() == 'FEATURED' and self.brand == 'bma')), None)
        tab.click()

        # Getting a specific Meeting
        uk_irish_races = list(self.site.horse_racing.tab_content.accordions_list.get_items(
            name=vec.racing.UK_AND_IRE_TYPE_NAME.upper()).values())[0]
        self.assertTrue(uk_irish_races, msg='UK AND IRISH RACES meeting is not available in Horse Racing SLP')

        # click on the Meeting's event time
        meeting = list(uk_irish_races.get_items(number=1).values())[0]
        events = meeting.items_as_ordered_dict
        event = next(iter(events.values()))
        event.scroll_to_we()
        self.__class__.event_id = event.event_id
        event.click()
        self.site.wait_content_state(state_name='RACINGEVENTDETAILS')

    def test_002_tap_on_the_totepool_tab(self):
        """
        DESCRIPTION: Tap on the Totepool tab
        EXPECTED: - Totepool tab is selected
        EXPECTED: - Supported pool types (from request PoolForEvent) are displayed
        """
        if self.site.wait_for_stream_and_bet_overlay():
            self.site.stream_and_bet_overlay.close_button.click()
        if self.site.wait_for_my_stable_onboarding_overlay():
            self.site.my_stable_onboarding_overlay.close_button.click()
        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        if vec.racing.RACING_EDP_MARKET_TABS.totepool.upper() in market_tabs.keys():
            market_tabs[vec.racing.RACING_EDP_MARKET_TABS.totepool.upper()].click()
            current_tab = self.site.racing_event_details.tab_content.event_markets_list.current_market_tab_name
            self.assertEqual(current_tab, vec.racing.RACING_EDP_MARKET_TABS.totepool.upper(),
                             msg=f'"{current_tab}" tab is selected instead of "Totepool" tab')
        else:
            raise CmsClientException('There is no "Totepool" tab found')

        response = self.get_response()
        for i in range(len(response['SSResponse']['children']) - 1):
            sleep(1)
            self.status = True and bool(response['SSResponse']['children'][i]['pool']['type'])

        if self.status:
            sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No one section was found')
            section = list(sections.values())[0]
            pool_types = section.grouping_buttons
            self.__class__.current_pool = pool_types.current
            self.assertTrue(pool_types.items_names, msg='No Pool types are displayed')

    def test_003_verify_url_path(self):
        """
        DESCRIPTION: Verify url path
        EXPECTED: Path contains /{event_id}/totepool/{pool type}
        """
        current_url = self.device.get_current_url()
        expected_url = f'/{self.event_id}/totepool/{self.current_pool.lower()}'
        self.assertIn(expected_url, current_url,
                      msg=f'Expected Url part: "{expected_url}" is not present in the browser Url: "{current_url}"')
