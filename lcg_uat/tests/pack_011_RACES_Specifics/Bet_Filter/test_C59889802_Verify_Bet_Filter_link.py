import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.bet_filter
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.races
@vtest
class Test_C59889802_Verify_Bet_Filter_link(BaseRacing):
    """
    TR_ID: C59889802
    NAME: Verify Bet Filter link
    DESCRIPTION: Verify that user is able to click Bet Filter link.
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Bet Filter should be enabled in CMS
    """
    keep_browser_open = True

    def verify_bet_filter_page(self):
        self.site.wait_content_state(state_name='HorseRacingBetFilterPage')
        bet_filter = self.site.horseracing_bet_filter
        self.assertEqual(bet_filter.page_title.text, vec.bet_finder.BF_HEADER_TITLE,
                         msg=f'Bet filter page\'s title is incorrect.\n Expected is "{bet_filter.page_title.text}", '
                             f'Actual is "{vec.bet_finder.BF_HEADER_TITLE}"')

        if self.brand == 'bma':
            self.assertEqual(bet_filter.header_line.page_title.sport_title, vec.bet_finder.BF_HEADER_TITLE,
                             msg=f'Bet filter header line title is incorrect.\n '
                             f'Expected is "{bet_filter.header_line.page_title.sport_title}",'
                             f'Actual is "{vec.bet_finder.BF_HEADER_TITLE}"')

        self.assertEqual(bet_filter.description.text, vec.bet_finder.BF_HEADER_TEXT,
                         msg=f'Bet filter page description is incorrect.\n '
                         f'Expected is "{bet_filter.description.text}", '
                         f'Actual is "{vec.bet_finder.BF_HEADER_TEXT}"')

    def test_000_create_racing_event(self):
        """
        DESCRIPTION: Create racing event
        EXPECTED: racing event is created
        """
        cms_config = self.get_initial_data_system_configuration().get('BetFilterHorseRacing')
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('BetFilterHorseRacing')

        if not cms_config:
            raise CmsClientException('"BetFilterHorseRacing" is absent in CMS')
        if not cms_config.get('enabled'):
            raise CmsClientException('"Horseracing Bet Filter" is disabled')

        if tests.settings.backend_env == 'prod':
            ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                       brand=self.brand,
                                       class_id=self.horse_racing_live_class_ids,
                                       category_id=self.ob_config.backend.ti.horse_racing.category_id)
            query_params = self.basic_active_events_filter() \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS,
                                          self.ob_config.backend.ti.horse_racing.category_id)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_RESULTED, OPERATORS.IS_FALSE)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CLASS_ID, OPERATORS.NOT_INTERSECTS, '227')) \
                .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.TEMPLATE_MARKET_NAME, OPERATORS.EQUALS,
                                          self.ob_config.horseracing_config.default_market_name)) \
                .add_filter(exists_filter(LEVELS.EVENT,
                                          simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                        OPERATORS.NOT_INTERSECTS, 'MKTFLAG_SP')))
            events = ss_req.ss_event_to_outcome_for_class(query_builder=query_params)
            event = next((event for event in events if
                          event.get('event') and event['event'] and event['event'].get('children')), None)
            self.__class__.eventID = event.get('event').get('id')
            self._logger.info(f'*** Found event with id "{self.eventID}"')

        else:
            self.__class__.eventID = self.ob_config.add_UK_racing_event(number_of_runners=1).event_id

    def test_001_launch_ladbrokes_coral_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral App
        EXPECTED: App should be opened
        """
        # Covered in step 2

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        self.navigate_to_page('horse-racing')
        self.site.wait_content_state('horse-racing')
        self.assertTrue(self.site.horse_racing.bet_filter_link.is_displayed(),
                        msg='The bet filter button is not displayed on the Horse Racing Landing page')

    def test_003_click_on_any_race(self):
        """
        DESCRIPTION: Click on any race
        EXPECTED: User should be navigated to the Event details page
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

    def test_004_click_on_bet_filter_link(self):
        """
        DESCRIPTION: Click on "Bet Filter" link
        EXPECTED: 1: User should be able to click the "Bet Filter" link
        EXPECTED: 2: User should be navigated to Bet Filter section
        """
        self.site.racing_event_details.bet_filter_link.click()
        self.site.wait_content_state_changed(timeout=10)
        self.verify_bet_filter_page()
