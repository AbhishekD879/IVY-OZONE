import pytest
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_haul
from voltron.utils.helpers import get_inplay_sports_by_section


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.sports_specific
@pytest.mark.rugby_league_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C66007746_Verify_data_displayed_on_Rugby_League_Sport_Landing_page(Common):
    """
    TR_ID: C66007746
    NAME: Verify data displayed on Rugby League Sport Landing page
    DESCRIPTION: This test case validates the details displayed in the Rugby League Sports Landing Page.
    PRECONDITIONS: In CMS, Sport pages-&gt; Sport Categories-&gt; Rugby league sport -&gt; Tabs and modules should be configured already.
    PRECONDITIONS: System configuration-&gt; Structure-&gt; Dynamic Banners-&gt; Data should be configured
    PRECONDITIONS: Under SEO -&gt; Manual -&gt; SEO should be configured.
    PRECONDITIONS: For inplay widget:System configuration-&gt; Structure-&gt; Search for Desktop widget toggle should be configured
    """
    keep_browser_open = True
    default_date_tab = vec.sb.SPORT_DAY_TABS.today
    default_current_tab = vec.sb.MATCHES.upper()
    enable_bs_performance_log = True

    def get_events_details(self, type_of_events='LIVE NOW'):
        """
        @param
        'type_of_events' : accepts value in ('LIVE_EVENT', 'UPCOMING_EVENT')
        @return:
            {
                'typesDetails': {
                                    'type_name1': details1,
                                    'types_name2': details2, .. typenameN: detailsN
                                }
                'eventsIds' : list of event ids (list : []),
                'eventsCount' : total no of events (int),
                'typeNames' : list of type names (list : []),
                'typesCount' : number of types (int)
            }
             """
        types_of_events = {'LIVE NOW': 'LIVE_EVENT', 'UPCOMING': 'UPCOMING_EVENT'}
        res = {'typesDetails': {}, 'eventsIds': [], 'eventsCount': 0, 'typeNames': [], 'typesCount': 0}
        sections = get_inplay_sports_by_section(type=types_of_events.get(type_of_events))
        if sections:
            if self.brand != 'bma' and self.device_type != "mobile":
                types = get_inplay_sports_by_section(type=types_of_events.get(type_of_events)).get('eventsByTypeName')
            else:
                types = get_inplay_sports_by_section(type=types_of_events.get(type_of_events))[0].get(
                    'eventsByTypeName')
            res['typesDetails'] = {f"{type['className']} - {type['typeName']}".upper(): type for type in types}
            res['typeNames'] = res['typesDetails'].keys()
            res['eventsCount'] = sum([type['eventCount'] for type in types])
            res['eventsIds'] = [id for type in types for id in type['eventsIds']]
            res['typesCount'] = len(types)
        else:
            res['typesCount'] = 0
            return res

    def mobile_validations(self):
        name = vec.sb.RUGBYLEAGUE if self.brand != 'bma' else vec.sb.RUGBYLEAGUE.upper()
        self.site.home.menu_carousel.click_item(name)
        wait_for_haul(10)

    def desktop_validations(self):
        name = vec.sb.RUGBYLEAGUE if self.brand != 'bma' else vec.sb.RUGBYLEAGUE.upper()
        self.site.sport_menu.click_item(name)

        self.site.sport_menu.click_item(name)
        wait_for_haul(10)
        # verifying Breadcrumbs
        breadcrumbs_for_tab = {'IN-PLAY': 'IN PLAY', 'MATCHES': 'MATCHES'}
        for tab_name, tab in self.site.sports_page.tabs_menu.items_as_ordered_dict.items():
            if tab_name not in breadcrumbs_for_tab:
                continue
            tab.click()
            wait_for_haul(5)
            expected_breadcrumb = f'HOME > RUGBY LEAGUE > {breadcrumbs_for_tab.get(tab_name).upper()}'
            breadcrumbs = self.site.sports_page.breadcrumbs.items_as_ordered_dict
            actual_breadcrumb = ' > '.join(breadcrumbs.keys()).upper()
            self.assertEqual(expected_breadcrumb, actual_breadcrumb,
                             msg=f'Actual Bread Crumb is "{actual_breadcrumb}" is not same as Expected Breadcrumb'
                                 f': "{expected_breadcrumb}"')

            sub_tabs = self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict.keys()
            for tab_name in sub_tabs:
                self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict.get(tab_name).click()
                events_details = self.get_events_details(type_of_events=tab_name)
                if events_details.get('eventsCount') == 0:
                    error_msg = self.site.sports_page.tab_content.has_no_events_label()
                    self.assertTrue(error_msg, 'Error Message is Not Displayed even though events unavailable')
                    break
                count_of_events_on_fe = self.site.sports_page.tab_content.grouping_buttons.items_as_ordered_dict.get(
                    tab_name).counter
                self.assertEqual(events_details.get('eventsCount'), count_of_events_on_fe,
                                 msg=f'Actual Events Count : "{count_of_events_on_fe}" is not same'
                                     f'as Expected Events Count : "{events_details.get("eventsCount")}" in "{tab_name}" tab')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: In CMS--&gt; Sport Pages--&gt;Sport Category--&gt; General Sport Configuration--&gt; Enter the mandatory details and save.
        PRECONDITIONS: Primary and Top markets and Save Changes with required fields
        PRECONDITIONS: In CMS -&gt; System Config -&gt; Structure -&gt; Enable the Market Switcher for the Rugby League sport.
        """
        list_of_tabs_response = self.cms_config.get_sport_tabs(self.ob_config.rugby_league_config.category_id)
        self.__class__.events_status = {tab['displayName'].upper(): tab['hasEvents'] for tab in list_of_tabs_response if
                                        tab['enabled']}
        try:
            in_play = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                              self.ob_config.rugby_league_config.category_id)
        except:
            in_play = "IN-PLAY"
        if in_play not in self.events_status:
            in_play_events = self.get_active_events_for_category(
                category_id=self.ob_config.rugby_league_config.category_id,
                in_play_event=True, raise_exceptions=False)
            self.__class__.events_status[in_play.upper()] = bool(in_play_events)

        if self.device_type == 'desktop':
            self.__class__.sport_tabs_from_cms = [tab['displayName'].upper() for tab in list_of_tabs_response if
                                                  tab['enabled']]
        else:
            self.__class__.sport_tabs_from_cms = [tab['displayName'].upper() for tab in list_of_tabs_response if
                                                  not (not tab['enabled'] or (
                                                          tab['checkEvents'] and not tab['hasEvents']))]

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application
        EXPECTED: Application should be launched successfully.
        """
        self.site.wait_content_state("Home")

    def test_002_from_a_z_sport_menu_or_top_menu_navigate_to_rugby_league_sport(self):
        """
        DESCRIPTION: From A-Z sport menu or top Menu, Navigate to Rugby League sport
        EXPECTED: Navigation should be successful
        """
        if self.device_type == "mobile":
            self.mobile_validations()
        else:
            self.desktop_validations()

    def test_003_verify_the_presence_of_sport_name(self):
        """
        DESCRIPTION: Verify the presence of Sport name
        EXPECTED: Sport name should be displayed.
        """
        # This step is covered in above  steps

    def test_004_verify_the_presence_of_navigation_bread_crumbs_under_sport_nameex__home__ampgt_rugby_union__ampgt_events(
            self):
        """
        DESCRIPTION: Verify the presence of navigation bread crumbs under sport name.
        DESCRIPTION: Ex- Home -&amp;gt; Rugby Union -&amp;gt; Events
        EXPECTED: Desktop:
        EXPECTED: Navigation Bread crumb should be available and that is clickable.
        EXPECTED: Mobile:
        EXPECTED: Bread crumbs will not be displayed in mobiles.
        """
        # This step is covered in above  steps

    def test_005_verify_the_presence_of_banners_section(self):
        """
        DESCRIPTION: Verify the presence of banners section.
        EXPECTED: Banners section should be present and all the configured banners should be displayed.
        """
        aem_banner_section = self.site.sports_page.aem_banner_section

        sport_id = self.ob_config.rugby_league_config.category_id
        tab_name = vec.sb.MATCHES.lower()
        sports_tab_data = self.cms_config.get_sports_tab_data(sport_id=sport_id, tab_name=tab_name)
        if sports_tab_data['interstitialBanners']:
            if sports_tab_data['interstitialBanners']['desktopBannerId'] and \
                    sports_tab_data['interstitialBanners']['mobileBannerId']:
                self.assertTrue(aem_banner_section, msg='AEM banner section is not present')

    def test_006_verify_the_tabs_display(self):
        """
        DESCRIPTION: Verify the tabs display.
        EXPECTED: All the tabs configured for the sport in CMS should be displayed.
        EXPECTED: By default user should land on 'Matches' tab and 'Today' sub tab.
        """
        self.__class__.tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
        if self.device_type != "mobile":
            try:
                in_play = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                                  self.ob_config.rugby_union_config.category_id)
            except:
                in_play = "IN-PLAY"
            if in_play not in self.sport_tabs_from_cms:
                self.__class__.sport_tabs_from_cms.append(in_play)

            for tab_name in self.tabs:
                self.assertIn(tab_name, self.sport_tabs_from_cms, msg=f"Tab : {tab_name} is not in CMS tabs : {self.sport_tabs_from_cms}")

            current_tab = self.site.sports_page.tabs_menu.current
            self.assertEqual(current_tab, self.default_current_tab,
                             msg=f'Default tab is not "{self.default_current_tab}", it is "{current_tab}"')
            current_date_tab = self.site.sports_page.date_tab.current_date_tab
            self.assertEqual(current_date_tab, self.default_date_tab,
                             msg=f'"{self.default_date_tab}" is not active date tab, active is "{current_date_tab}"')
        else:
            self.assertListEqual(list(self.tabs.keys()), self.sport_tabs_from_cms,
                                 msg=f'Actual Sport Tabs on FE :"{list(self.tabs.keys())}" are not same as Expected '
                                     f'Sport Tabs configured in CMS : "{self.sport_tabs_from_cms}"')

    def test_007_validate_the_order_of_tabs_display(self):
        """
        DESCRIPTION: Validate the order of tabs display
        EXPECTED: In FE, tabs should be displayed as per CMS configuration.
        """
        # This step is covered in above  steps

    def test_008_verify_data_display_under_each_tab(self):
        """
        DESCRIPTION: Verify data display under each tab
        EXPECTED: Data should be displayed under each tab.
        """
        matches_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                  self.ob_config.rugby_union_config.category_id, raise_exceptions=False)
        for tab_name, tab in self.tabs.items():
            tab.click()
            if tab_name == vec.siteserve.IN_PLAY_TAB and not self.events_status[tab_name]:
                self.assertTrue(self.site.sports_page.tab_content.grouping_buttons.current != vec.inplay.LIVE_NOW_SWITCHER, f'"{vec.inplay.LIVE_NOW_SWITCHER}" tab is enabled. Expected Tab is "{vec.inplay.UPCOMING_SWITCHER}"')
                continue
            elif tab_name == matches_tab_name and self.events_status.get(tab_name.upper()):
                fe_status = False
                if self.device_type == 'desktop':
                    for date_tab_name, date_tab in self.site.sports_page.date_tab.items_as_ordered_dict.items():
                        date_tab.click()
                        fe_status = not self.site.sports_page.tab_content.has_no_events_label()
                        if fe_status:
                            break
                else:
                    fe_status = not self.site.sports_page.tab_content.has_no_events_label()
                self.assertEqual(fe_status, self.events_status.get(tab_name.upper()),
                                 msg=f'Events Available Status from CMS: {self.events_status.get(tab_name.upper())} Events Available '
                                     f'Status in FE : {fe_status}')
            else:
                self.assertEqual(self.site.sports_page.tabs_menu.current, tab_name, msg=f'Unable to switch on {tab_name}')
                self.site.wait_content_state_changed()
                current_tab_events_status_fe = not self.site.sports_page.tab_content.has_no_events_label()
                tab_events_status_from_cms = self.events_status.get(tab_name.upper())
                self.assertEqual(current_tab_events_status_fe, tab_events_status_from_cms,
                                 msg=f'Events Available Status from CMS: {tab_events_status_from_cms} Events Available '
                                     f'Status in FE : {current_tab_events_status_fe}')
