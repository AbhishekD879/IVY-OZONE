import pytest
from tenacity import stop_after_attempt, retry, retry_if_exception_type, wait_fixed
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # events can't be created on Prod/Beta
@pytest.mark.desktop
@pytest.mark.greyhounds
@pytest.mark.horseracing
@pytest.mark.slow
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60094966_Verify_the_display_order_of_Markets_when_they_are_not_configured_in_CMS(Common):
    """
    TR_ID: C60094966
    NAME: Verify the display order of Markets when they are not configured in CMS
    DESCRIPTION: Verify the display order of Markets when they are not configured in CMS
    PRECONDITIONS: 1: Horse racing & Grey Hounds racing should be available
    PRECONDITIONS: 2: Markets should be available which are not configured in CMS
    PRECONDITIONS: 3: User should have CMS access
    """
    keep_browser_open = True
    markets = [('win_only',),
               ('betting_without',),
               ('top_2_finish',),
               ('to_finish_second',)
               ]

    @retry(stop=stop_after_attempt(10), retry=retry_if_exception_type(VoltronException), wait=wait_fixed(wait=2),
           reraise=True)
    def wait_for_markets_to_reflect(self, sport=None):
        if not self.cms_config.get_system_configuration_structure()['RacingEDPMarketsDescription']['enabled']:
            self.cms_config.update_system_configuration_structure(config_item='RacingEDPMarketsDescription',
                                                                  field_name='enabled',
                                                                  field_value=True)
        win_ew = self.cms_config.create_and_update_markets_with_description(name='Win or Each Way', description='This description of Win or Each Way market is for testing purpose.')
        win_only = self.cms_config.create_and_update_markets_with_description(name='Win Only', description='An each way bet is a bet made up of two parts: a WIN bet and a PLACE bet.')
        betting_without = self.cms_config.create_and_update_markets_with_description(name='Betting Without', description='An each way bet is a bet made up of two parts: a WIN bet and a PLACE bet.')
        if sport:
            cms_order = [win_ew['name'].replace('Each Way', 'E/W').upper(), win_only['name'].upper(),
                         betting_without['name'].upper()]
            self.device.refresh_page()
            if sport == 'HR':
                market_tabs = list(self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.
                                   items_as_ordered_dict.keys())
            else:
                market_tabs = list(self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.
                                   items_as_ordered_dict.keys())
            self.assertListEqual(market_tabs[:2], cms_order[:2],
                                 msg=f'Actual market tabs order(FE): "{market_tabs[:2]}" is not same as Expected market tabs order(CMS): "{cms_order[:2]}"')
            self.assertNotEqual(list(market_tabs), cms_order,
                                msg=f'actual order"{cms_order}" and "{list(market_tabs)}" expected are same')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1: Horse racing & Grey Hounds racing should be available
        PRECONDITIONS: 2: Markets should be available which are not configured in CMS
        """
        self.wait_for_markets_to_reflect()
        self.__class__.hr_event = self.ob_config.add_UK_racing_event(markets=self.markets, number_of_runners=1)
        self.__class__.gh_event = self.ob_config.add_UK_greyhound_racing_event(markets=self.markets,
                                                                               number_of_runners=1)

    def test_001_1launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: 1:Launch Coral/ Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state("HomePage")

    def test_002_2_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: 2: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: Horse Racing Landing page should be displayed
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('horse-racing')

    def test_003_click_on_any_event_with_markets_available(self):
        """
        DESCRIPTION: Click on any event with Markets available
        EXPECTED: User should be navigated to EDP
        """
        self.navigate_to_edp(event_id=self.hr_event.event_id, sport_name='horse-racing')
        self.site.wait_content_state(state_name='RacingEventDetails')

    def test_004_validate_the_display_order_of_markets_which_are_not_configured_in_cms(self, sport='HR'):
        """
        DESCRIPTION: Validate the display order of Markets which are not Configured in CMS
        """
        self.wait_for_markets_to_reflect(sport=sport)

    def test_005_navigate_to_grey_hounds_and_validate_the_same(self):
        """
        DESCRIPTION: Navigate to Grey Hounds and Validate the same
        """
        self.navigate_to_page('greyhound-racing')
        self.site.wait_content_state('greyhound-racing')
        self.navigate_to_edp(event_id=self.gh_event.event_id, sport_name='greyhound-racing')
        self.site.wait_content_state(state_name='GreyHoundEventDetails')
        self.test_004_validate_the_display_order_of_markets_which_are_not_configured_in_cms(sport='GR')
