import tests
import pytest
from random import choice
from selenium.common.exceptions import StaleElementReferenceException
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - cannot test Featured on prod endpoints
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.featured
@pytest.mark.homepage_featured
@pytest.mark.cms
@pytest.mark.sports
@pytest.mark.football
@vtest
class Test_C12561661_Verify_user_navigation_from_Featured_tab_to_CMS_configured_hardcoded_pages_in_application(BaseFeaturedTest):
    """
    TR_ID: C12561661
    NAME: Verify user navigation from Featured tab to CMS configured/hardcoded pages in application
    DESCRIPTION: This test case verifies user navigation from Featured tab to CMS configured page in application
    PRECONDITIONS: 1. Featured modules by Sport/race type id are configured in CMS
    PRECONDITIONS: 2. For these Featured modules internal links  are configured in 'CMS in Footer link URL field'
    """
    keep_browser_open = True

    def get_football_event_name(self, event_id):
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        event_name = normalize_name(event_resp[0]['event']['name'])

    # this is to handle event names like 'FC KAMAZ Kazan v IFK Karlberg'
        if self.device_type == 'desktop':
            for w in event_name.split():
                if not w.isupper() and w != 'v':
                    event_name = event_name.replace(w, w.capitalize(), 1)
            event_name = event_name.replace(' v ', ' V ')

        return event_name

    def get_races_event_name(self, event_id):
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        event_name = normalize_name(event_resp[0]['event']['name'])

        event_name = event_name.title()
        if ' Uk' in event_name:
            event_name = event_name.replace(' Uk', ' UK')
        return event_name

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Featured modules by 'Type ID'/'Race Type ID' are configured in CMS
        PRECONDITIONS: 2. For these 'Featured' modules internal links are configured in CMS in 'Footer link URL field'
        PRECONDITIONS: 3. Load the app
        PRECONDITIONS: 4. Navigate to 'Featured' tab/section
        PRECONDITIONS: **Configurations**
        PRECONDITIONS: 1) For creating the module in the 'Featured' tab/section via CMS use the following instruction:
        PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=126685715
        PRECONDITIONS: 2) For reaching the appropriate CMS per env use the following link:
        PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
        PRECONDITIONS: **Note:**
        PRECONDITIONS: 1) To verify data for created 'Featured' module use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket (featured-sports...) -> response with type: "FEATURED_STRUCTURE_CHANGED" -> modules -> @type: "EventsModule" an choose the appropriate module.
        PRECONDITIONS: ![](index.php?/attachments/get/32612728)
        """
        football_markets = [('last_goalscorer', {'cashout': True}),
                            ('extra_time_result', {'cashout': True})]

        if tests.settings.backend_env == 'prod':
            event = choice(self.get_active_events_for_category(
                category_id=self.ob_config.football_config.category_id, all_available_events=True))
            type_id = event['event']['typeId']
            event = choice(self.get_active_events_for_category(
                category_id=self.ob_config.horseracing_config.category_id, all_available_events=True))
            race_type_id = event['event']['typeId']
        else:
            self.ob_config.add_autotest_premier_league_football_event(markets=football_markets)
            type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
            self.ob_config.add_UK_racing_event(number_of_runners=1)
            race_type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id

        self.__class__.football_url = '/sport/football/matches'
        self.__class__.module_football_type = self.cms_config.add_featured_tab_module(select_event_by='Type',
                                                                                      id=type_id,
                                                                                      footer_link_url=self.football_url,
                                                                                      show_all_events=True,
                                                                                      events_time_from_hours_delta=-10,
                                                                                      module_time_from_hours_delta=-10)

        self.__class__.module_football_type_name = self.module_football_type['title'].upper()

        self.__class__.race_url = '/horse-racing/featured'
        self.__class__.module_race_type = self.cms_config.add_featured_tab_module(select_event_by='RaceTypeId',
                                                                                  id=race_type_id,
                                                                                  footer_link_url=self.race_url,
                                                                                  show_all_events=True,
                                                                                  events_time_from_hours_delta=-10,
                                                                                  module_time_from_hours_delta=-10)
        self.__class__.module_race_type_name = self.module_race_type['title'].upper()
        self.site.wait_content_state('HomePage')
        if not self.is_safari:
            self.wait_for_featured_module(name=self.module_football_type_name)
            self.wait_for_featured_module(name=self.module_race_type_name)
        self.__class__.featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)

    def test_001_select_featured_module_by_sport_type_idtap_cms_configurable_link_at_the_bottom_of_the_moduleverify_users_navigation_to_appropriate_page_configured_in_cms_for_selected_module(self):
        """
        DESCRIPTION: Select Featured module by Sport type ID.
        DESCRIPTION: Tap CMS configurable link at the bottom of the module.
        DESCRIPTION: Verify user's navigation to appropriate page configured in CMS for selected module
        EXPECTED: User is navigated to the page configured in CMS for selected module
        """
        module = self.get_module(module_content_name=self.featured_tab_name, module_name=self.module_football_type_name)
        self.assertTrue(module, msg=f'Football module "{self.module_football_type_name}" not found')

        footer_link_text = self.module_football_type['footerLink']['text']
        if self.device_type == 'desktop':
            footer_link_text = footer_link_text.upper()
        try:
            actual_footer_text = module.footer.text
            self.assertEqual(actual_footer_text, footer_link_text,
                             msg=f'Footer link text "{actual_footer_text}" '
                                 f'is not as expected "{footer_link_text}"')

            module.footer.click()
        except StaleElementReferenceException:
            module = self.get_module(module_content_name=self.featured_tab_name, module_name=self.module_football_type_name)
            self.assertEqual(module.footer.text, footer_link_text,
                             msg=f'Footer link text "{module.footer.text}" '
                                 f'is not as expected "{footer_link_text}"')
            module.footer.click()

        self.site.wait_content_state('Football', timeout=20)

        if tests.settings.backend_env == 'tst2' or self.is_safari:
            self.navigate_to_page(name='/')
        else:
            self.site.go_to_home_page()

    def test_002_select_featured_module_by_sport_type_idtap_hardcoded_link_with_number_of_available_markets_for_selected_event_within_the_moduleverify_that_user_is_navigated_to_selected_event_details_page(self):
        """
        DESCRIPTION: Select Featured module by Sport type ID.
        DESCRIPTION: Tap hardcoded link with number of available markets for selected event within the module.
        DESCRIPTION: Verify that user is navigated to selected event details page
        EXPECTED: User is navigated to selected event details page
        """
        module = self.get_module(module_content_name=self.featured_tab_name, module_name=self.module_football_type_name)
        self.assertTrue(module, msg=f'Football module "{self.module_football_type_name}" not found')

        events = module.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.featured_tab_name}" module')
        try:
            list(events.items())[0][1].scroll_to()
        except StaleElementReferenceException:
            events = module.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events found in "{self.featured_tab_name}" module')

        events_with_markets = False
        for _, event in events.items():
            event.scroll_to()
            if event.has_markets():
                events_with_markets = True
                event_name = self.get_football_event_name(event.event_id)
                event.more_markets_link.click()
                self.site.wait_content_state('EventDetails', timeout=20)
                edp_event_name = self.site.sport_event_details.event_title_bar.event_name
                self.softAssert(self.assertEqual, event_name.upper(), edp_event_name.upper(),
                                msg=f'User navigated to wrong page. Current event name is "{edp_event_name}" '
                                    f'while "{event_name}" is expected')
                break
            else:
                continue

        if not events_with_markets:
            raise VoltronException(f'No events with multiple markets were found in "{self.module_football_type_name}"')

    def test_003_select_featured_module_by_race_type_idtap_cms_configurable_link_at_the_bottom_of_the_moduleverify_users_navigation_to_appropriate_page_configured_in_cms_for_selected_module(self):
        """
        DESCRIPTION: Select Featured module by Race type ID.
        DESCRIPTION: Tap CMS configurable link at the bottom of the module.
        DESCRIPTION: Verify user's navigation to appropriate page configured in CMS for selected module
        EXPECTED: User is navigated to the page configured in CMS for selected module
        """
        if tests.settings.backend_env == 'tst2' or self.is_safari:
            self.navigate_to_page(name='/')
        else:
            self.site.go_to_home_page()
        module = self.get_module(module_content_name=self.featured_tab_name, module_name=self.module_race_type_name)
        self.assertTrue(module, msg=f'Horse race module "{self.module_race_type_name}" not found')

        footer_link_text = self.module_race_type['footerLink']['text']
        if self.device_type == 'desktop':
            footer_link_text = footer_link_text.upper()

        try:
            actual_footer_text = module.footer.text
            self.assertEqual(actual_footer_text, footer_link_text,
                             msg=f'Footer link text "{actual_footer_text}" '
                                 f'is not as expected "{footer_link_text}"')

            module.footer.click()
        except StaleElementReferenceException:
            module = self.get_module(module_content_name=self.featured_tab_name, module_name=self.module_race_type_name)
            self.assertEqual(module.footer.text, footer_link_text,
                             msg=f'Footer link text "{module.footer.text}" '
                                 f'is not as expected "{footer_link_text}"')
            module.footer.click()

        self.site.wait_content_state('Horseracing', timeout=20)

        if tests.settings.backend_env == 'tst2' or self.is_safari:
            self.navigate_to_page(name='/')
        else:
            self.site.go_to_home_page()

    def test_004_select_featured_module_by_race_type_idtap_hardcoded_link_more_with_number_of_available_markets_for_selected_event_within_the_module_headerverify_that_user_is_navigated_to_selected_event_details_page(self):
        """
        DESCRIPTION: Select Featured module by Race type ID.
        DESCRIPTION: Tap hardcoded link 'More' with number of available markets for selected event within the module header.
        DESCRIPTION: Verify that user is navigated to selected event details page
        EXPECTED: User is navigated to selected event details page
        """
        module = self.get_module(module_content_name=self.featured_tab_name, module_name=self.module_race_type_name)
        self.assertTrue(module, msg=f'Horse race module "{self.module_race_type_name}" not found')

        events = module.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.featured_tab_name}" module')

        try:
            list(events.items())[0][1].scroll_to()
        except StaleElementReferenceException:
            events = module.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events found in "{self.featured_tab_name}" module')

        for _, event in events.items():
            event.scroll_to()
            if event.has_view_full_race_card():
                event_name = self.get_races_event_name(event.event_id)
                event.full_race_card.click()
                self.site.wait_content_state('RacingEventDetails', timeout=30)
                race_name = self.site.racing_event_details.event_title
                if self.brand == 'bma':
                    race_name = race_name.replace('\n', ' ')
                self.softAssert(self.assertEqual, event_name, race_name, msg='User navigated to wrong page. '
                                                                             f'Current event name is "{race_name}" while "{event_name}" is expected')
                break
            else:
                continue
