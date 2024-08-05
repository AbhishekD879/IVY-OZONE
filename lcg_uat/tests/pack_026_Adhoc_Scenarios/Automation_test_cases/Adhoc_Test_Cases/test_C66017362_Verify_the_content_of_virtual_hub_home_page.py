import json
import random
from urllib.parse import unquote
import pytest
import requests
from crlat_cms_client.utils.exceptions import CMSException
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.siteserve_exception import SiteServeException
import voltron.environments.constants as vec
from voltron.utils.helpers import get_response_url, do_request
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.virtual_sports
@pytest.mark.medium
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.adhoc24thJan24
@pytest.mark.reg167_fix
@vtest
class Test_C66017362_Verify_the_content_of_virtual_hub_home_page(Common):
    """
    TR_ID: C66017362
    NAME: Verify the content of virtual hub home page
    DESCRIPTION: To verify the content of virtual hub home page.
    PRECONDITIONS: Below fields should be enabled in CMS.
    PRECONDITIONS: CMS&gt;System configuration&gt; Structure&gt; Virtual hub home page&gt;
    PRECONDITIONS: header Banner
    PRECONDITIONS: top Sports
    PRECONDITIONS: nextEvents
    PRECONDITIONS: otherSports
    PRECONDITIONS: feature Zone
    PRECONDITIONS: enabled
    """
    keep_browser_open = True
    next_events = vec.virtuals.VIRTUAL_HUB_NEXT_EVENTS
    enable_bs_performance_log = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get list of active virtual sport categories
        DESCRIPTION: Open Coral/Ladbrokes test environment.
        DESCRIPTION: Go to 'Virtual Sports'.
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.virtuals_config.category_id)
        sports_list = ss_req.ss_class(query_builder=self.ss_query_builder.
                                      add_filter(simple_filter(LEVELS.CLASS,
                                                               ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                                               str(self.ob_config.virtuals_config.category_id))))
        if not sports_list:
            raise SiteServeException('There are no active virtual sports')
        virtual_sport_data = self.cms_config.get_parent_virtual_sports()
        self.__class__.top_sports = {}
        order_top_sports = {}
        self.__class__.other_sport = {}
        for virtual_sport in virtual_sport_data:
            if virtual_sport["topSports"] and virtual_sport['active']:
                self.__class__.top_sports.update({virtual_sport["title"].title(): virtual_sport})
                order_top_sports.update({virtual_sport['topSportsIndex']: virtual_sport["title"].title()})
            elif virtual_sport['active']:
                self.__class__.other_sport.update({virtual_sport["title"].title(): virtual_sport})
        self.__class__.sorted_sports = dict(sorted(order_top_sports.items()))
        self.__class__.virtual_hub_home_page = self.cms_config.get_system_configuration_structure().get(
            'VirtualHubHomePage')
        if not self.virtual_hub_home_page.get('enabled') and tests.settings.cms_env == 'prod0':
            raise CMSException(f' "VirtualHubHomePage" is not enabled in CMS')
        else:
            self.cms_config.update_system_configuration_structure(config_item='VirtualHubHomePage',
                                                                  field_name='enabled',
                                                                  field_value=True)
        virtual_next_events_config = self.cms_config.get_virtual_next_events_config()
        self.__class__.enabled_virtual_sports = {}
        for virtual_next_event in virtual_next_events_config:
            if not virtual_next_event.get('disabled'):
                self.__class__.enabled_virtual_sports[virtual_next_event.get('buttonText').upper()] = {'url': virtual_next_event.get('redirectionUrl'),
                                                                                'limit': virtual_next_event.get('limit'),
                                                                                'typeIds':virtual_next_event.get('typeIds')
                                                                                }





    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application
        EXPECTED: Application should be launched successfully.
        """
        self.site.open_sport(self.get_sport_title(category_id=self.ob_config.virtuals_config.category_id),
                             content_state='VirtualSports')
        # with the help of belwo request, We will get the data of the virtual sports.
        url = get_response_url(self, url='/api/content/teasers')
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "path": "VirtualHubSports",
            "prefetchDepth": 1,
            "subPaths": ["TopSports", "OtherSports", "FeatureZone"]
        }
        # Convert the data to JSON format
        payload = json.dumps(data)

        # Make the POST request
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            # Convert the response content (which is a JSON string) to a dictionary
            self.__class__.response = json.loads(response.content)

    def test_002_click_on_virtual_sports_menu_item_on_top_menu_or_left_side_menu(self):
        """
        DESCRIPTION: Click on 'Virtual Sports' menu item on top menu or left side menu
        EXPECTED: User should navigate to Virtual hub home page. Title of the page should be Virtual
        """
        # covered in above step

    def test_003_verify_the_display_of_header_banner_section(self):
        """
        DESCRIPTION: Verify the display of header banner section
        EXPECTED: Banners section with banners should be displayed. If banners are not configured banners section should not be displayed.
        """
        pass

    def test_004_verify_the_display_of_top_sport_section(self):
        """
        DESCRIPTION: Verify the display of top sport section.
        EXPECTED: Top sport section with header 'Top Sports' should be displayed. Top Sports along with images should be displayed.
        EXPECTED: Ex- Football, Horse racing etc.
        """
        if self.virtual_hub_home_page.get('topSports'):
            hub_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.title() == "Top Sports"), None)
            self.assertTrue(hub_section,
                            msg="top sports  section is not shown in frontend even when its enabled in cms")
            hub_section.scroll_to()
            if len(list(self.top_sports.keys())) > 0:
                section_sports = hub_section.items_as_ordered_dict
                sports_name = list(section_sports.keys())
                section_sports_names = [sport_name.title() for sport_name in section_sports]
                self.assertEqual(section_sports_names, list(self.sorted_sports.values()),
                                 msg=f" ui top sports {section_sports_names} is not same as cms top sports {self.sorted_sports} ")
                virtual_sport_name = random.choice(sports_name)
                virtual_sport = section_sports.get(virtual_sport_name)
                link = self.top_sports.get(virtual_sport_name.title()).get('redirectionURL').replace("/victoria-park",
                                                                                                     "/horse-racing")
                virtual_sport.click()
                sports = self.site.virtual_sports.sport_carousel.items_as_ordered_dict
                self.__class__.virtual_sports_fe = [name.title() for name in sports]
                current_url = self.device.get_current_url()
                self.assertIn(unquote(link), current_url,
                              msg=f"user is not navigated to the expected page {unquote(link)} navigated to page {current_url}")
            else:
                section_sports = hub_section.items_as_ordered_dict
                self.assertFalse(section_sports,
                                 msg=f"top section contains sport even when there are no sports are configered in cms")
        else:
            hub_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.title() == "Top Sports"), None)
            self.assertFalse(hub_section, msg="top sports  section is shown in frontend even when its disabled in cms")

    def test_005_click_on_any_virtual_sport_icon(self):
        """
        DESCRIPTION: Click on any virtual sport icon
        EXPECTED: User should navigate to respective virtual sport.
        """
        # covered in above step

    def test_006_now_navigate_back_to_virtual_hub_home_page(self):
        """
        DESCRIPTION: Now navigate back to virtual hub home page
        EXPECTED: Should navigate to Virtual hub home screen
        """
        if self.virtual_hub_home_page.get('topSports'):
            self.site.back_button_click()
            self.site.wait_content_state(state_name='VirtualSports')

    def test_007_verify_the_display_of_virtual_race_carousal_section(self):
        """
        DESCRIPTION: Verify the display of 'Virtual race carousal' section
        EXPECTED: Virtual race carousal section should be displayed with header "Next Events". Under the title virtual horse racing events should be displayed.
        EXPECTED: Should be able to scroll the events left and right.
        """
        if self.virtual_hub_home_page.get('nextEvents'):
            wait_for_result(lambda: next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.title() == "Next Events"), None) is not None, name=f'Waiting for next event section "',
                            timeout=5)
            hub_section = next(
                section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                section_name.title() == "Next Events")
            self.assertTrue(hub_section, msg="Next events hub is not shown in front end")
            hub_section.scroll_to()
            next_event_cards = hub_section.items_as_ordered_dict
            next_event_card_names = list(next_event_cards.keys())
            self.assertTrue(next_event_cards, msg="next events are not shown in Frontend virtual hub page")
            next_event_card_name = random.choice(next_event_card_names)
            next_event_card = next_event_cards.get(next_event_card_name)
            button_text = next_event_card.bottom_link_text.upper()
            if button_text is None:
                next_event_card_name = random.choice(next_event_card_names)
                next_event_card = next_event_cards.get(next_event_card_name)
                button_text = next_event_card.bottom_link_text.upper()
            redirection_url = self.enabled_virtual_sports.get(button_text).get("url")
            next_event_card.bottom_link.click()
            current_url = self.device.get_current_url()
            self.assertIn(unquote(redirection_url), current_url,
                          msg=f"user is not navigated to the expected page {unquote(redirection_url)} navigated to page {current_url}")
        else:
            hub_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.title() == "Next Events"), None)
            self.assertFalse(hub_section, msg="Next Events  section is shown in frontend even when its disabled in cms")

    def test_008_click_on_bet_here_link_mapped_to_the_event(self):
        """
        DESCRIPTION: Click on 'Bet here' link mapped to the event.
        EXPECTED: Should navigate to respective virtual racing event.
        """

    #     covered in above step

    def test_009_now_navigate_back_to_virtual_hub_home_page(self):
        """
        DESCRIPTION: Now navigate back to virtual hub home page
        EXPECTED: Should navigate to Virtual hub home screen
        """
        if self.virtual_hub_home_page.get('nextEvents'):
            self.site.back_button_click()
            self.site.wait_content_state(state_name='VirtualSports')

    def test_010_verify_the_display_of_all_sports_section(self):
        """
        DESCRIPTION: Verify the display of 'All sports' section
        EXPECTED: All sports section should be displayed with header as  'Other Sports". Under header all other sports thumbnail images should be displayed.
        EXPECTED: Should able to traverse left and right by clicking on left and right arrows of carousel.
        """
        # otherSports
        if self.virtual_hub_home_page.get('otherSports'):
            wait_for_result(lambda: next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.title() == "Other Sports"), None) is not None, name=f'Waiting for other sport section "',
                            timeout=5)
            hub_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.title() == "Other Sports"), None)
            self.assertTrue(hub_section,
                            msg="other sports  section is not shown in frontend even when its enabled in cms")
            hub_section.scroll_to()
            section_sports = hub_section.items_as_ordered_dict
            sports_name = list(section_sports.keys())
            section_sports_names = [sport_name.title() for sport_name in section_sports]
            self.assertEqual(sorted(section_sports_names), sorted(list(self.other_sport.keys())),
                             msg=f" ui top sports {sorted(section_sports_names)} is not same as cms top sports {sorted(list(self.other_sport.keys()))} ")
            virtual_sport_name = random.choice(sports_name)
            if virtual_sport_name not in self.virtual_sports_fe:
                virtual_sport_name = random.choice(sports_name)
            virtual_sport = section_sports.get(virtual_sport_name)
            link = self.other_sport.get(virtual_sport_name.title()).get('redirectionURL').replace("/victoria-park",
                                                                                                  "/horse-racing")
            virtual_sport.click()
            current_url = self.device.get_current_url()
            if virtual_sport_name.title() in self.virtual_sports_fe:
                self.assertIn(unquote(link), current_url,
                              msg=f"user is not navigated to the expected page {unquote(link)} navigated to page {current_url}")
            else:
                self.assertNotIn(unquote(link), current_url,
                                 msg=f"user is not navigated to the expected page {unquote(link)} navigated to page {current_url}")
        else:
            hub_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.title() == "Other Sports"), None)
            self.assertFalse(hub_section, msg="Other Sports section is shown in frontend even when its disabled in cms")

    def test_011_click_on_any_virtual_sport_icon(self):
        """
        DESCRIPTION: Click on any virtual sport icon
        EXPECTED: Should navigate to respective virtual sport.
        """
        pass

    def test_012_now_navigate_back_to_virtual_hub_home_page(self):
        """
        DESCRIPTION: Now navigate back to virtual hub home page
        EXPECTED: Should navigate to Virtual hub home screen
        """
        if self.virtual_hub_home_page.get('otherSports'):
            self.site.back_button_click()
            self.site.wait_content_state(state_name='VirtualSports')

    def test_013_verify_the_display_of_feature_zone_section(self):
        """
        DESCRIPTION: Verify the display of 'Feature Zone' section
        EXPECTED: Feature zone title should be displayed. Data should be displayed under it.
        """
        for res in self.response:
            if res['type'].upper() == 'FEATUREZONE':
                feature_data = res
        featured_sports = {}
        if feature_data:
            for data in feature_data['teasers']:
                try:
                    featured_sports.update({data['title'].title(): data})
                except KeyError:
                    continue
        if self.virtual_hub_home_page.get('featureZone') and feature_data:
            wait_for_result(lambda: next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.title() == "Feature Zone"), None) is not None, name=f'Waiting for Feature Zone section "',
                            timeout=5)
            hub_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.title() == "Feature Zone"), None)
            self.assertTrue(hub_section,
                            msg="Feature Zone  section is not shown in frontend even when its enabled in cms")
            hub_section.scroll_to()
            section_sports = hub_section.items_as_ordered_dict
            sports_name = list(section_sports.keys())
            section_sports_names = [sport_name.title() for sport_name in section_sports]
            for sport in section_sports_names:
                self.assertIn(sport, featured_sports,
                              msg=f"front-end sport with name {sport} is not in the teaser call sports {featured_sports}")
            virtual_sport_name = random.choice(sports_name)
            virtual_sport = section_sports.get(virtual_sport_name)
            link = featured_sports.get(virtual_sport_name.title()).get('bannerLink').get('url').replace(
                "/victoria-park",
                "/horse-racing")
            virtual_sport.click()
            current_url = self.device.get_current_url()
            self.assertIn(unquote(link), current_url,
                          msg=f"user is not navigated to the expected page {unquote(link)} navigated to page {current_url}")
        elif self.virtual_hub_home_page.get('featureZone') and not feature_data:
            raise SiteServeException("Feature zone data is not show in teaser call")
        else:
            hub_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.title() == "Feature Zone"), None)
            self.assertFalse(hub_section,
                             msg="Feature Zone  section is shown in frontend even when its disabled in cms")

    def test_015_click_on_any_icon_under_feature_zone_section(self):
        """
        DESCRIPTION: Click on any icon under 'Feature Zone' section
        EXPECTED: Should navigate to respective virtual sport.
        """
        # covered in above steps

    def test_016_select_a_selection_and_place_a_bet(self):
        """
        DESCRIPTION: Select a selection and place a bet.
        EXPECTED: User should be able to place a bet successfully.
        """
        # covered in regression virtual test cases and in sanity(C874323) as well
