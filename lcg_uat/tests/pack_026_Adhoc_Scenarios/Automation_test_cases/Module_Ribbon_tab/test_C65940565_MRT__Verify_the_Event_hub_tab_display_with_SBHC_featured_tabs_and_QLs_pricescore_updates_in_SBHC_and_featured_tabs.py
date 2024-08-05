import pytest
from datetime import datetime
import tests
from tests.base_test import vtest
from tests.Common import Common
from crlat_cms_client.utils.date_time import get_date_time_as_string
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import generate_name
from voltron.utils.waiters import wait_for_cms_reflection, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.module_ribbon
@pytest.mark.adhoc_suite
@vtest
class Test_C65940565_MRT__Verify_the_Event_hub_tab_display_with_SBHC_featured_tabs_and_QLs_pricescore_updates_in_SBHC_and_featured_tabs(
    Common):
    """
    TR_ID: C65940565
    NAME: MRT - Verify the Event hub tab display with SB,HC featured tabs and QLs, price,score updates in SB,HC and featured tabs.
    DESCRIPTION: This test case is to Verify the Event hub tab display with SB,HC featured tabs and QLs, price,score updates in SB,HC and featured tabs.
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: 2)Configuration for Event hub tab in the cms
    PRECONDITIONS: -click on sports pages  from left menu in Main navigation>event hub
    PRECONDITIONS: 3)Click on "+ Create Event hub tab" button to create new Event hub .
    PRECONDITIONS: 4)Enter the title click on create button.
    PRECONDITIONS: 5)click on add sport module and create the required modules and save the created module
    PRECONDITIONS: 6) Configuration for module ribbon tab in the cms
    PRECONDITIONS: -click on module ribbon tab option from left menu in Main navigation
    PRECONDITIONS: 7) Click on "+ Create Module ribbon tab" button to create new MRT.
    PRECONDITIONS: 8) Enter All mandatory Fields and click on save button:
    PRECONDITIONS: -Module ribbon tab title
    PRECONDITIONS: -Directive name option from dropdown like Featured, Coupon,In-play, Live stream,Multiples, next races, top bets, Build your bet(map the event hub created to MRT)
    PRECONDITIONS: -id
    PRECONDITIONS: -URL
    PRECONDITIONS: -Click on "Create" CTA button
    PRECONDITIONS: 9)Check and select below required fields in module ribbon tab configuration:
    PRECONDITIONS: -Active
    PRECONDITIONS: -IOS
    PRECONDITIONS: -Android
    PRECONDITIONS: -Windows Phone
    PRECONDITIONS: -Select Show tab on option from dropdown like Both, Desktop ,Mobile/tablet
    PRECONDITIONS: -Select radiobutton either Universal or segment(s) inclusion.
    PRECONDITIONS: -Click on "Save changes" button
    """
    keep_browser_open = True
    title = 'Auto_' + generate_name()
    svg_icon = 'tennis'
    destination_url = f'https://{tests.HOSTNAME}/sport/tennis'
    time_format = '%Y-%m-%dT%H:%M:%S.%f'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Configure 1 active Quick link for Homepage
        DESCRIPTION: Load Oxygen application and navigate to Featured tab
        """
        events = self.get_active_events_for_category(category_id=self.ob_config.tennis_config.category_id,
                                                     in_play_event=True, all_available_events=True)
        if len(events) <=2:
            raise SiteServeException(f'Two active events are not found in category id "{self.ob_config.tennis_config.category_id}"')
        event_1 = events[0]['event']
        event_id_2 = events[1]['event']['id']
        outcomes = next(((market['market']['children']) for market in event_1['children'] if
                         market['market'].get('children')), None)
        selections_id = [i['outcome']['id'] for i in outcomes]
        date_from = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                            url_encode=False, days=-1)[:-3] + 'Z'
        # create event hub
        response = self.create_eventhub(title=self.title)
        hub_index = response['hubIndex']
        self.event_hub_tab_name = self.get_module_data_by_directive_name_from_cms(directiveName='EventHub')

        self.cms_config.add_sport_module_to_event_hub(module_type='HIGHLIGHTS_CAROUSEL', page_id=hub_index)
        self.cms_config.add_sport_module_to_event_hub(module_type='SURFACE_BET', page_id=hub_index)
        self.cms_config.add_sport_module_to_event_hub(module_type='QUICK_LINK', page_id=hub_index)
        self.cms_config.add_sport_module_to_event_hub(module_type='FEATURED', page_id=hub_index)

        # create Highlights Carousel
        self.__class__.highlights_carousel = self.cms_config.create_highlights_carousel(title=self.title,
                                                                                        events=[event_1['id']],
                                                                                        page_type='eventhub',
                                                                                        sport_id=hub_index,
                                                                                        limit=1, inplay=True,
                                                                                        svgId=self.svg_icon)
        # created surface bet
        self.__class__.surface_bet = self.cms_config.add_surface_bet(selection_id=selections_id[0],
                                                                     title=self.title, highlightsTabOn=True,
                                                                     svg_icon=self.svg_icon, event_hub_id=hub_index,
                                                                     on_homepage=True)
        # create quick link
        self.__class__.quick_link = self.cms_config.create_quick_link(title=self.title, sport_id=hub_index,
                                                                      page_type='eventhub', date_from=date_from,
                                                                      destination=self.destination_url)
        # create featured tab
        self.__class__.feature_module = self.cms_config.add_featured_tab_module(select_event_by='Event',
                                                                                id=event_id_2, page_type='eventhub',
                                                                                page_id=hub_index,title=self.title,
                                                                                events_time_from_hours_delta=-20,
                                                                                module_time_from_hours_delta=-20)

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home page should be loaded succesfully
        """
        self.site.wait_content_state('Homepage')

    def test_002_verify_the_created_event_hub_in_the_mrt(self):
        """
        DESCRIPTION: Verify the created event hub in the MRT
        EXPECTED: Created event hub should be display at MRT
        """
        event_hub = wait_for_cms_reflection(
            lambda: self.site.home.tabs_menu.items_as_ordered_dict.get(self.title.upper()), expected_result=True,
            timeout=3, refresh_count=5, ref=self)
        self.assertTrue(event_hub, msg=f'{self.title.upper()} event hub is not displayed in home page')
        event_hub.click()

    def test_003_click_on_the_event_hub_in_the_mrt(self):
        """
        DESCRIPTION: Click on the event hub in the MRT
        EXPECTED: Created data from the cms should be loaded under event hub in the MRT
        """
        # Covered in 002 step

    def test_004_verify_the_created_sbhcql_in_the_fe(self):
        """
        DESCRIPTION: Verify the created SB,HC,QL in the FE
        EXPECTED: Created modules should be displayed at FE
        """
        # verify surface bet
        surface_bet_fe = wait_for_cms_reflection(
            lambda: self.site.home.tab_content.surface_bets.items_as_ordered_dict.get(self.title.upper()),
            expected_result=True, timeout=3,
            refresh_count=3, ref=self)
        self.assertTrue(surface_bet_fe, msg=f'surface bet is not displayed in the "{self.title.upper()}" event hub')

        # verify highlights carousel
        title = self.title if self.brand == 'bma' else self.title.upper()
        highlights_carousel_fe = wait_for_cms_reflection(
            lambda: self.site.home.tab_content.highlight_carousels.get(title), expected_result=True, timeout=3,
            refresh_count=3, ref=self)
        self.assertTrue(highlights_carousel_fe, msg=f'Highlights carousel is not displayed in the "{self.title.upper()}" event hub')

        # verify quick links
        quick_link_fe = wait_for_cms_reflection(
            lambda: self.site.home.tab_content.quick_links.items_as_ordered_dict.get(self.title), expected_result=True,
            timeout=3,refresh_count=3, ref=self)

        self.assertTrue(quick_link_fe, msg=f'Quick link is not displayed in the "{self.title.upper()}" event hub')

        # verify feature tab events
        fe_title = self.feature_module.get('title')
        featured_event_fe = wait_for_cms_reflection(
            lambda: self.site.home.tab_content.accordions_list.items_as_ordered_dict.get(fe_title.upper()),
            expected_result=True, timeout=3,refresh_count=3, ref=self)

        self.assertTrue(featured_event_fe, msg=f'Featured event tab is not displayed in the "{self.title.upper()}" event hub')

    def test_005_verify_the_created_the_sb_and_hc_with_live_events_and_check_price_updates_and_color_changes(self):
        """
        DESCRIPTION: Verify the created the SB and HC with live events and check price updates and color changes
        EXPECTED: Prices updates and color changes  need to be happen
        """
        # This step is covered in C65940560

    def test_006_verify_the_created__ql_navigation(self):
        """
        DESCRIPTION: Verify the created  QL navigation
        EXPECTED: Navigation need to be done as per cms
        """
        quick_link = self.site.home.tab_content.quick_links.items_as_ordered_dict.get(self.title)
        quick_link.click()
        wait_for_haul(2)
        self.site.wait_splash_to_hide()
        current_url = self.device.get_current_url()
        self.assertEqual(current_url, self.destination_url, msg=f' current url {current_url} is not equal to {self.destination_url}')
        self.site.back_button_click()

    def test_007_check_the_modules_by_keeping_status_as_activeinactive(self):
        """
        DESCRIPTION: Check the modules by keeping status as ACTIVE/INACTIVE
        EXPECTED: Modules shoudl reflect in FE as per cms config
        """
        # this step is covered in other quick link test case
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet['id'], disabled=True)
        surface_bet_fe = wait_for_cms_reflection(
            lambda: self.site.home.tab_content.surface_bets.items_as_ordered_dict.get(self.title.upper()),
            expected_result=False, refresh_count=2, ref=self)
        self.assertFalse(surface_bet_fe, msg=f'surface bet is displayed in the "{self.title.upper()}" event hub')

        # verify highlights carousel
        self.cms_config.update_highlights_carousel(self.highlights_carousel, disabled=True)
        highlights_carousel_fe = wait_for_cms_reflection(
            lambda: self.site.home.tab_content.highlight_carousels.get(self.title), expected_result=False,
            refresh_count=2, ref=self)
        self.assertFalse(highlights_carousel_fe, msg=f'Highlights carousel is displayed in the "{self.title.upper()}" event hub')

        # verify quick links
        self.cms_config.update_quick_link(quick_link_id=self.quick_link['id'], disabled=True)
        quick_link_fe = wait_for_cms_reflection(
            lambda: self.site.home.tab_content.quick_links.items_as_ordered_dict.get(self.title), expected_result=False,
            refresh_count=2, ref=self)
        self.assertFalse(quick_link_fe, msg=f'Quick link is displayed in the "{self.title.upper()}" event hub')

        # verify feature tab events
        self.cms_config.update_featured_tab_module(module_id=self.feature_module['id'], enabled=False)
        fe_title = self.feature_module.get('title')
        featured_event_fe = wait_for_cms_reflection(
            lambda: self.site.home.tab_content.accordions_list.items_as_ordered_dict.get(fe_title.upper()),
            expected_result=False, refresh_count=2, ref=self)
        self.assertFalse(featured_event_fe, msg=f'Featured event tab is displayed in the "{self.title.upper()}" event hub')
