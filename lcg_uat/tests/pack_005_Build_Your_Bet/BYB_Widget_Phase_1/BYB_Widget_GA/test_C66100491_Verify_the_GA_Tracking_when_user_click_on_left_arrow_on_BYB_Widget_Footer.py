import pytest
import tests
import voltron.environments.constants as vec
from crlat_cms_client.utils.exceptions import CMSException
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_haul
from urllib.parse import urlparse


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.byb_widget
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C66100491_Verify_the_GA_Tracking_when_user_click_on_left_arrow_on_BYB_Widget_Footer(BaseDataLayerTest):
    """
    TR_ID: C66100491
    NAME: Verify the GA Tracking when user click on left arrow on BYB Widget Footer
    DESCRIPTION: This test case is to verify the GA Tracking when user click on left arrow on BYB Widget Footer
    PRECONDITIONS: 1. BYB Widget sub section should be created under BYB main section and active for the Football Home page
    PRECONDITIONS: 2. Navigation to go CMS -> BYB -> BYB Widget
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        Description: checking Byb_module is enabled in Football SLP
        Expected:
        """
        # verifying BYB Widget enabled or not in Football SLP page
        BYb_widget_football = self.cms_config.get_sport_module(module_type='BYB_WIDGET')
        id_ = BYb_widget_football[0].get('id')
        if BYb_widget_football[0]['disabled']:
            raise CMSException('"BYB Widget" module is disabled on Football SLP')
        # getting byb widget data
        self.__class__.byb = self.cms_config.get_byb_widget()
        self.__class__.byb_widget_container_title = self.byb.get('title')
        byb_widget_datas = self.byb.get('data')
        self.__class__.byb_widget_card_locations = []
        byb_widget_cards_ids = []
        for byb_widget_data in byb_widget_datas:
            byb_widget_cards_ids.append(byb_widget_data['id'])
            self.byb_widget_card_locations.append(byb_widget_data.get('locations'))
        if len(self.byb_widget_card_locations) == 0:
            self.cms_config.create_new_market_cards(title='Test1', event_id='', market_id='',
                                                    location='Football Homepage')
        elif 'Football Homepage' in [item for sublist in self.byb_widget_card_locations for item in sublist]:
            self._logger.info('BYB Widget is enabled in Football SLP')
        else:
            self.cms_config.update_market_cards(market_card_id=byb_widget_cards_ids[0], location='Football Homepage')

    def test_001_launch_the_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the application and login with valid credentials
        EXPECTED: Able to launch the application and login successfully
        """
        self.site.login()

    def test_002_navigate_to_the_football_home_page(self):
        """
        DESCRIPTION: Navigate to the Football Home page
        EXPECTED: User can able to navigate to the Football Home page successfully
        """
        self.navigate_to_page(name='sport/football')
        football_page = self.site.wait_content_state(vec.siteserve.FOOTBALL_TAB)
        self.assertTrue(football_page, msg='User not on Football page')
        self.__class__.location_byb_event = \
            self.device.get_current_url().replace(f'https://{tests.HOSTNAME}', '').split('?')[0]
        self.__class__.expected_sport_tab = self.site.football.tabs_menu.current
        sport_tab_from_cms = \
            self.get_sport_tab_name(
                self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                self.ob_config.football_config.category_id)
        self.assertEqual(self.expected_sport_tab, sport_tab_from_cms,
                         msg=f'Default tab is not "{sport_tab_from_cms}", it is "{self.expected_sport_tab}"')

    def test_003_verify_the_display_of_byb_widget_on_the_byb_homepage(self):
        """
        DESCRIPTION: Verify the display of BYB Widget on the BYB Homepage
        EXPECTED: User can able to see the BYB Widget
        """
        # verifying BYB Widget container present or not...........
        byb_widget_containers = self.site.home.byb_widget.items_as_ordered_dict
        self.assertTrue(byb_widget_containers, msg='BYB Widget container is not present in Football SLP')
        for byb_widget_container_name, byb_widget_container in byb_widget_containers.items():
            self.assertEqual(byb_widget_container_name.upper(), self.byb_widget_container_title.upper(),
                             msg=f'Actual BYB Widget container Title from CMS: {self.byb_widget_container_title.upper()} and '
                                 f'Expected BYB Widget Container Title from FE:{byb_widget_container_name.upper()} both are not same')
            # Verifying BYB Widget accordions
            byb_widgets = byb_widget_container.items_as_ordered_dict_inc_dup
            self.assertTrue(byb_widgets, msg='BYB Widget is not present in Football SLP')
            for byb_widget_name, byb_widget in byb_widgets.items():
                self.__class__.byb_widget_name_v = byb_widget.name
                byb_footer_menu = byb_widget.has_byb_widget_footer
                self.assertTrue(byb_footer_menu,
                                msg=f'BYB Widget Footer Menu is not showing in :{self.byb_widget_name_v}')
                byb_footer_left_arrow = byb_widget.has_left_arrow
                self.assertTrue(byb_footer_left_arrow, msg=f'BYB Widget Footer left arrow is not showing in :{self.byb_widget_name_v}')
                byb_widget.left_arrow.click()
                byb_footer_page_count = byb_widget.byb_footer_page_counter
                #  Checking GA Tracking for left arrow
                expected_resp = {
                    'event': 'Event.Tracking',
                    'component.CategoryEvent': 'widgets',
                    'component.LabelEvent': 'build your own bet',
                    'component.ActionEvent': 'left',
                    'component.PositionEvent': byb_footer_page_count,
                    'component.LocationEvent': self.location_byb_event.lstrip('/'),
                    'component.EventDetails': self.byb_widget_name_v,
                    'component.URLClicked': self.device.get_current_url()
                }
                actual_resp = self.get_data_layer_specific_object(object_key='event',
                                                                  object_value='Event.Tracking')

                self.assertEqual(actual_resp, expected_resp)

                # clicking right arrow
                byb_footer_right_arrow = byb_widget.has_right_arrow
                self.assertTrue(byb_footer_right_arrow,
                                msg=f'BYB Widget Footer left arrow is not showing in :{self.byb_widget_name_v}')
                byb_widget.right_arrow.click()
                byb_footer_page_count_right = byb_widget.byb_footer_page_counter

                # checking GA tracking for right arrow
                expected_resp = {
                    'event': 'Event.Tracking',
                    'component.CategoryEvent': 'widgets',
                    'component.LabelEvent': 'build your own bet',
                    'component.ActionEvent': 'right',
                    'component.PositionEvent': byb_footer_page_count_right,
                    'component.LocationEvent': self.location_byb_event.lstrip('/'),
                    'component.EventDetails': self.byb_widget_name_v,
                    'component.URLClicked': self.device.get_current_url()
                }
                actual_resp = self.get_data_layer_specific_object(object_key='event',
                                                                  object_value='Event.Tracking')

                self.assertEqual(actual_resp, expected_resp)

                break
            break

    def test_004_click_on_the_left_arrow_on_byb_widget_footer(self):
        """
        DESCRIPTION: Click on the left arrow on BYB widget footer
        EXPECTED: User can able to click on the left arrow
        """
        # covered in above step

    def test_005_verify_ga_tracking(self):
        """
        DESCRIPTION: Verify GA Tracking
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'widgets',
        EXPECTED: component.LabelEvent: 'build your own bet',
        EXPECTED: component.ActionEvent: {right/left},
        EXPECTED: component.PositionEvent: {page of page no)ex: 1 of 3,
        EXPECTED: component.LocationEvent: {home,edp, etc},
        EXPECTED: component.EventDetails: {match name} ,
        EXPECTED: component.URLClicked: {clicked url/ not applicable}
        EXPECTED: }]
        EXPECTED: });
        """
        # covered in above steps

