import pytest
import tests
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
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.bet_filter
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C59889800_Verify_Top_bar_Horse_Racing_is_no_longer_displayed(BaseRacing):
    """
    TR_ID: C59889800
    NAME: Verify Top bar "Horse Racing" is no longer displayed
    DESCRIPTION: Verify that Top bar "Horse Racing" is no longer displayed.
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Bet Filter should be enabled in CMS
    """
    keep_browser_open = True

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
        self.site.wait_content_state(state_name='RacingEventDetails')

    def test_004_validate_top_barindexphpattachmentsget118703003indexphpattachmentsget118703004(self):
        """
        DESCRIPTION: Validate Top bar
        DESCRIPTION: ![](index.php?/attachments/get/118703003)
        DESCRIPTION: ![](index.php?/attachments/get/118703004)
        EXPECTED: User should not be displayed "Horse racing" top bar
        """
        events_ribbon = self.site.racing_event_details.tab_content.event_off_times_list.items_as_ordered_dict
        self.assertTrue(events_ribbon, msg='Horse racing event timeline is not displayed.'
                                           'event timeline should be displayed instead of horse racing top bar')
