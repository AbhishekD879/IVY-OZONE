import pytest
from datetime import datetime
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tzlocal import get_localzone


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.adhoc_suite
@pytest.mark.mobile_only
@pytest.mark.module_ribbon
@pytest.mark.other
@vtest
class Test_C65940567_MRT__Verify_the_Featured_highlights_tab_is_displaying_with_content(Common):
    """
    TR_ID: C65940567
    NAME: MRT - Verify the Featured/highlights tab is displaying with content
    DESCRIPTION: This test case is to verify the Featured tab is displaying with content
    """
    keep_browser_open = True
    mrt_title = "Auto mrt_C567"
    timezone = str(get_localzone())

    def filtered_data(self, **kwargs):
        filtered_super_buttons = []
        filtered_featured_modules = []
        filtered_highlights_carousels = []
        filtered_Surface_bets = []
        filtered_quicklinks = []
        if self.timezone.upper() == "UTC":
            now = get_date_time_as_string(date_time_obj=datetime.now(),
                                          time_format='%Y-%m-%dT%H:%M:%S.%f',
                                          url_encode=False)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            now = get_date_time_as_string(date_time_obj=datetime.now(),
                                          time_format='%Y-%m-%dT%H:%M:%S.%f',
                                          url_encode=False, hours=-1)[:-3] + 'Z'
        else:
            now = get_date_time_as_string(date_time_obj=datetime.now(),
                                          time_format='%Y-%m-%dT%H:%M:%S.%f',
                                          url_encode=False, hours=-5.5)[:-3] + 'Z'
        if kwargs.get('cms_super_buttons'):
            for item in kwargs.get('cms_super_buttons'):
                if "/home/featured" in item.get('homeTabs') and item.get('enabled') and item.get('validityPeriodStart') <= now <= item.get('validityPeriodEnd'):  # Modified this line to use equality comparison
                    filtered_super_buttons.append(item)
            return filtered_super_buttons

        if kwargs.get('cms_featured_modules'):
            for item in kwargs.get('cms_featured_modules'):
                if item.get('visibility').get('displayFrom') <= now <= item.get('visibility').get('displayTo') and item.get(
                        'visibility').get('enabled') and item.get('pageId') == '0':
                    filtered_featured_modules.append(item)
            return filtered_featured_modules

        if kwargs.get('cms_highlight_carousels'):
            for item in kwargs.get('cms_highlight_carousels'):
                if item.get('displayFrom') <= now <= item.get('displayTo') and not item.get('disabled') and item.get(
                        'pageId') == '0':
                    filtered_highlights_carousels.append(item)
            return filtered_highlights_carousels

        if kwargs.get('cms_surface_bets'):
            for item in kwargs.get('cms_surface_bets'):
                if item.get('displayFrom') <= now <= item.get('displayTo') and not item.get('disabled') and item.get(
                        'highlightsTabOn'):
                    filtered_Surface_bets.append(item)
            return filtered_Surface_bets

        if kwargs.get('cms_quicklinks'):
            for item in kwargs.get('cms_quicklinks'):
                if item.get('validityPeriodStart') <= now <= item.get('validityPeriodEnd') and not item.get('disabled') and item.get('pageId')=='0':
                    filtered_quicklinks.append(item)
            return filtered_quicklinks

    def verifying_home_page_contents(self):
        expected_url = '/home/featured'
        self.assertTrue(expected_url in self.device.get_current_url(),
                        msg=f'Actual opened window URL: \n"{self.device.get_current_url()}", '
                            f'\nexpected configured in CMS: \n"{expected_url}"')

        # verifying super buttons in cms and front end
        cms_super_buttons = []
        if self.brand == 'ladbrokes':
            cms_super_buttons = self.cms_config.get_mobile_special_super_buttons()
        cms_super_buttons.extend(self.cms_config.get_mobile_super_buttons())
        all_active_super_buttons_on_fe = self.filtered_data(cms_super_buttons=cms_super_buttons)
        if len(all_active_super_buttons_on_fe) > 0:
            expected_super_buttons_visible_on_fe = all_active_super_buttons_on_fe[0]['title'].upper().strip()
            actual_super_buttons_on_fe = self.site.home.super_button_section.super_button.button.name.upper().strip()
            self.assertEqual(expected_super_buttons_visible_on_fe, actual_super_buttons_on_fe,
                             msg=f' actual super buttons "{actual_super_buttons_on_fe} are not same as expected super buttons on fe "{expected_super_buttons_visible_on_fe}"')
        else:
            super_button_presence = self.site.home.has_quick_link_section()
            self.assertFalse(super_button_presence,
                             msg=f' no super button is configured in cms but available in home page "{super_button_presence}"')

        # verifying featured modules in cms and front end
        self.__class__.sections = None
        cms_featured_modules = self.cms_config.get_feature_modules()
        if len(cms_featured_modules) > 0:
            all_featured_modules_on_cms = self.filtered_data(cms_featured_modules=cms_featured_modules)
            if len(all_featured_modules_on_cms) > 0:
                expected_featured_modules_on_fe = [item.get('title').upper().strip() for item in
                                                  all_featured_modules_on_cms]
                self.device.refresh_page()
                wait_for_haul(3)
                featured_module = self.site.home.get_module_content(
                    self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
                featured_module.scroll_to()
                self.sections = featured_module.accordions_list.items_as_ordered_dict
                self.sections = [section.upper().strip() for section in self.sections]
                actual_featured_modules_on_fe = self.sections
                self.assertListEqual(expected_featured_modules_on_fe, actual_featured_modules_on_fe,
                                     msg=f'expected featured modules "{expected_featured_modules_on_fe}" are not same as actual featured modules "{actual_featured_modules_on_fe}"')
            else:
                featured_module = self.site.home.get_module_content(self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
                featured_module.scroll_to()
                self.sections = featured_module.accordions_list.items_as_ordered_dict
                if len(self.sections) > 0:
                    self.assertFalse(self.sections,
                                 msg=f'no featured is configured in cms but available in homepage"{featured_module}')

        # verifing highlight_carousels in cms and frontend
        cms_highlight_carousels = self.cms_config.get_all_highlights_carousels()
        if len(cms_highlight_carousels) > 0:
            all_highlights_carousels_on_cms = self.filtered_data(cms_highlight_carousels=cms_highlight_carousels)
            if len(all_highlights_carousels_on_cms) > 0:
                expected_highlights_carousels_on_fe = [item.get('title').upper().strip() for item in all_highlights_carousels_on_cms]
                highlights_carousels_on_fe = self.site.home.tab_content.highlight_carousels
                actual_highlights_carousels_on_fe = [item.upper().strip() for item in highlights_carousels_on_fe]
                for item in actual_highlights_carousels_on_fe:
                    self.assertIn(item, expected_highlights_carousels_on_fe,
                                        msg=f'expected highlights carousels "{expected_highlights_carousels_on_fe}" are not same as actual highlights carousels "{actual_highlights_carousels_on_fe}"')
            else:
                highlights_carousel_presence = self.site.home.tab_content.has_highlight_carousels()
                self.assertFalse(highlights_carousel_presence,
                                     msg=f'no highlight carousel is configured in cms but available in homepage "{highlights_carousel_presence}"')

        # verifying surface_bet in cms and frontend
        cms_surface_bets = self.cms_config.get_all_surface_bets()
        if len(cms_surface_bets) > 0:
            all_surface_bets_on_cms = self.filtered_data(cms_surface_bets=cms_surface_bets)
            if len(all_surface_bets_on_cms) > 0:
                expected_surface_bets_on_fe = [item.get('title').upper().strip() for item in all_surface_bets_on_cms]
                surface_bets_on_fe = self.site.home.tab_content.surface_bets.items_as_ordered_dict
                actual_surface_bets_on_fe = [item.upper().strip() for item in surface_bets_on_fe]
                for item in actual_surface_bets_on_fe:
                    self.assertIn(item, expected_surface_bets_on_fe,
                                  msg=f'items in "{expected_surface_bets_on_fe}" are not in "{actual_surface_bets_on_fe}"')
            else:
                surface_bets_presence = self.site.home.tab_content.has_surface_bets()
                self.assertFalse(surface_bets_presence,
                                 msg=f'no surfacebets is configured in cms but available in homepage"{surface_bets_presence}"')

        # verifying quicklinks in cms and frontend
        cms_quicklinks = self.cms_config.get_quick_links(sport_id='0')
        if len(cms_quicklinks) > 0:
            all_quicklinks_on_cms = self.filtered_data(cms_quicklinks=cms_quicklinks)
            if len(all_quicklinks_on_cms) > 0:
                expected_quicklinks_on_fe = [item.get('title').upper().strip() for item in all_quicklinks_on_cms]
                self.device.refresh_page()
                wait_for_haul(3)
                actual_quicklinks_on_fe = self.site.home.tab_content.quick_links.items_as_ordered_dict
                actual_quicklinks_on_fe = [item.upper().strip() for item in actual_quicklinks_on_fe]
                self.assertListEqual(actual_quicklinks_on_fe, expected_quicklinks_on_fe,
                                     msg=f'actual_links_on_fe"{actual_quicklinks_on_fe}" are not same as expected_quicklinks_on_fe"{expected_quicklinks_on_fe}"')
            else:
                quicklinks_presence = self.site.home.tab_content.has_quick_link_section()
                self.assertFalse(quicklinks_presence,
                                 msg=f'no quicklinks is configured in cms but availabke in homepage "{quicklinks_presence}"')

        # verifying of inplay module as per cms configuration
        # covered on testcase id C65818639

        # verifying of recently played games as per cms configuration
        # covered in testcase id C65939806


    def test_000_preconditions(self):
        """
        "PRECONDITIONS: 1) User should have oxygen CMS access
        PRECONDITIONS: 2) Configuration for module ribbon tab in the CMS
        PRECONDITIONS: -click on module ribbon tab option from left menu in Main navigation
        PRECONDITIONS: 3) Click on "+ Create Module ribbon tab" button to create new MRT.
        PRECONDITIONS: 4) Enter All mandatory Fields and click on save button:
        PRECONDITIONS: -Module ribbon tab title
        PRECONDITIONS: -Directive name option from dropdown like Featured, Coupon,In-play, Live stream,Multiples, next races, top bets, Build your bet
        PRECONDITIONS: -id - tab-featured/
        PRECONDITIONS: -URL - /home/featured
        PRECONDITIONS: -Click on "Create" CTA button
        PRECONDITIONS: 5)Check and select below required fields in module ribbon tab configuration:
        PRECONDITIONS: -Active
        PRECONDITIONS: -IOS
        PRECONDITIONS: -Android
        PRECONDITIONS: -Windows Phone
        PRECONDITIONS: -Select Show tab on option from dropdown like Both, Desktop ,Mobile/tablet
        PRECONDITIONS: -Select radio button either Universal or segment(s) inclusion.
        PRECONDITIONS: -Click on "Save changes" button
        """
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.__class__.internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(title=self.mrt_title,
                                                                           directive_name='Featured',
                                                                           internal_id=self.internal_id,
                                                                           hub_index=index_number,
                                                                           url='/home/featured')
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
    def test_001_launch_the_lads_coral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home Page should be loaded successfully
        """
        self.site.login()
        self.site.wait_content_state('Home')

    def test_002_verify_featured_highlights_tab_present_in_mrt(self):
        """
        DESCRIPTION: verify Featured/Highlights tab present in MRT
        EXPECTED: Featured/Highlights tab should be present in MRT.
        """
        wait_for_haul(5)
        available_mrt_tabs = list(self.site.home.tabs_menu.items_as_ordered_dict.keys())
        for i in range(5):
            if self.event_hub_tab_name not in available_mrt_tabs:
                wait_for_haul(5)
            else:
                break
        self.assertIn(self.event_hub_tab_name, available_mrt_tabs, msg=f'Expected Mrt_tab "{self.event_hub_tab_name}" is not present in "{available_mrt_tabs}"')

    def test_003_click_on_featured_highlights_tab(self):
        """
        DESCRIPTION: Click on Featured/Highlights tab
        EXPECTED: Featured/Highlights tab should displayed.
        """
        self.site.home.tabs_menu.items_as_ordered_dict.get(self.event_hub_tab_name).click()

    def test_004_verify_home_page_modules_display_as_per_cms_configuration(self):
        """
        DESCRIPTION: Verify Home page modules display as per CMS configuration
        EXPECTED: Home Page modules should be displayed as per CMS configuration Like:
        EXPECTED: -Surface bet module----
        EXPECTED: -Featured Module---
        EXPECTED: -Quick LinksVerify Home page modules display as per CMS configuration-----------
        EXPECTED: -Super button----
        EXPECTED: -Highlights carousal---
        EXPECTED: -Recently played games
        EXPECTED: -Inplay module
        """
        self.verifying_home_page_contents()
        self.site.logout()
        self.navigate_to_page('/')
        self.site.wait_content_state('Home Page')
        self.test_002_verify_featured_highlights_tab_present_in_mrt()
        self.test_003_click_on_featured_highlights_tab()
        self.verifying_home_page_contents()














