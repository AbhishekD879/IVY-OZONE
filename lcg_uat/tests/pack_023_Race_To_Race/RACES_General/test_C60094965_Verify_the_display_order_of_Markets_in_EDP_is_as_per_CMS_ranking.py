import pytest
import voltron.environments.constants as vec
from copy import copy
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod events can't be created on Prod/Beta
@pytest.mark.desktop
@pytest.mark.greyhounds
@pytest.mark.horseracing
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60094965_Verify_the_display_order_of_Markets_in_EDP_is_as_per_CMS_ranking(BaseRacing):
    """
    TR_ID: C60094965
    NAME: Verify the display order of Markets in EDP is as per CMS ranking
    DESCRIPTION: Verify that display order of Markets tabs in EDP is as configured in CMS
    PRECONDITIONS: 1: Horse racing & Grey Hounds racing should be available
    PRECONDITIONS: 2: Markets should be available
    PRECONDITIONS: 3: User should have CMS access
    """
    keep_browser_open = True
    markets_back_up_order = None
    drag_market_id = None

    event_markets = [
        ('win_only',)]

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()

        # revert racing edp market ordering
        if cls.initial_markets_id_order:
            cms_config.set_racing_edp_markets_ordering(new_order=cls.initial_markets_id_order,
                                                       moving_item=cls.drag_market_id)

    def test_000_preconditions(self):
        """
        Events creation for horse racing and greyhound racing
        """
        event_params = self.ob_config.add_UK_racing_event(markets=self.event_markets)
        self.__class__.HR_eventID = event_params.event_id
        event_params1 = self.ob_config.add_UK_greyhound_racing_event(markets=self.event_markets)
        self.__class__.GH_eventID = event_params1.event_id

    def test_001_login_to_cms(self):
        """
        DESCRIPTION: Login to CMS
        EXPECTED: CMS should be logged in
        """
        if self.cms_config.get_system_configuration_structure()['RacingEDPMarketsDescription']['enabled']:
            self.cms_config.update_system_configuration_structure(config_item='RacingEDPMarketsDescription',
                                                                  field_name='enabled', field_value=True)
        racing_edp_market_list = self.cms_config.get_markets_with_description()
        self.__class__.initial_markets_order = [market['name'] for market in racing_edp_market_list]
        for market_name in range(len(self.initial_markets_order)):
            if self.initial_markets_order[market_name] == 'Win Only':
                self.__class__.drag_market_name = self.initial_markets_order[market_name]
        self.__class__.drag_market_id = next((market['id'] for market in racing_edp_market_list if market['name'] == self.drag_market_name), '')
        if not self.drag_market_id:
            raise VoltronException(f'Cannot find market id for {self.drag_market_name}')

        self.__class__.initial_markets_id_order = [market['id'] for market in racing_edp_market_list]
        self.__class__.new_order = copy(self.initial_markets_id_order)
        self.new_order.remove(self.drag_market_id)
        self.new_order.insert(0, self.drag_market_id)
        self.cms_config.set_racing_edp_markets_ordering(new_order=self.new_order, moving_item=self.drag_market_id)

    def test_002_navigate_to_racing_edp_in_cms_and_configure_the_markets__adding_the_markets_or_re_arranging_the_order_by_drag__drop(
            self):
        """
        DESCRIPTION: Navigate to Racing EDP in CMS and configure the Markets ( Adding the markets or re-arranging the order by drag & drop)
        EXPECTED: User should be able to save the changes successfully
        """
        # Covered into step 1

    def test_003_1launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: 1:Launch Coral/ Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state('Homepage')

    def test_004_2_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: 2: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: Horse Racing Landing page should be displayed
        """
        if self.device_type == 'desktop':
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertIn(vec.sb.HORSERACING.upper(), sports.keys(),
                          msg=f'"{vec.sb.HORSERACING.upper()}" is not found in the header sport menu')
            sports.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.navigate_to_page('horse-racing')
        self.site.wait_content_state(state_name='Horseracing')

    def test_005_click_on_any_event_with_markets_available(self):
        """
        DESCRIPTION: Click on any event with Markets available
        EXPECTED: User should be navigated to EDP
        """
        self.navigate_to_edp(event_id=self.HR_eventID, sport_name='horse-racing')
        self.site.wait_content_state(state_name='RacingEventDetails', timeout=10)

    def test_006_validate_the_display_order_of_markets(self, sport='HR'):
        """
        DESCRIPTION: Validate the display order of Markets
        EXPECTED: 1: Market tabs should be displayed as per CMS ranking
        EXPECTED: 2: If any market is unavailable the next market should take it's position
        """
        racing_edp_market_list = self.cms_config.get_markets_with_description()
        self.assertTrue(racing_edp_market_list, msg='"racing edp markets" is not displayed in CMS')
        if sport == 'HR':
            market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict.keys()
        else:
            market_tabs = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict.keys()
        self.assertTrue(market_tabs, msg='No market tabs found on EDP')
        self.__class__.new_markets_order = [market['name'] for market in racing_edp_market_list]
        for index, item in enumerate(self.new_markets_order):
            if item.upper() == vec.racing.RACING_EDP_WIN_OR_EACH_WAY_FULL_NAME:
                self.new_markets_order[index] = 'WIN OR E/W'
        market_index = 0
        order_flag = None
        for market in market_tabs:
            for index, item in enumerate(self.new_markets_order):
                if item.upper() == market.upper():
                    if index >= market_index:
                        order_flag = True
                        market_index = index
                    else:
                        order_flag = False
                    break
        self.assertTrue(order_flag,
                        msg=f'Actual market list "{market_tabs}" is not the same as expected "{self.new_markets_order}"')

    def test_007_navigate_to_grey_hounds_and_validate_the_same(self):
        """
        DESCRIPTION: Navigate to Grey Hounds and Validate the same
        EXPECTED:
        """
        self.navigate_to_page('greyhound-racing')
        self.site.wait_content_state('greyhound-racing')
        self.navigate_to_edp(event_id=self.GH_eventID, sport_name='greyhound-racing')
        self.site.wait_content_state(state_name='GreyHoundEventDetails')
        self.test_006_validate_the_display_order_of_markets(sport='GR')
