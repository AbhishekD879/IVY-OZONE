import pytest
from selenium.common.exceptions import StaleElementReferenceException
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod CMS configurations needs to updated
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.homepage_featured
@vtest
class Test_C9138173_Verify_users_navigation_to_the_appropriate_Event_Details_sport_landing_page_from_Featured_module(BaseFeaturedTest, BaseRacing):
    """
    TR_ID: C9138173
    NAME: Verify user's navigation to the appropriate Event Details/sport landing page from Featured module
    DESCRIPTION: This test case verifies user's navigation to the appropriate Event Details/sport landing page from Featured module
    PRECONDITIONS: Featured modules by Type id/Race type id are created and displayed in application
    PRECONDITIONS: Featured tab is opened in app
    PRECONDITIONS: Note: Virtual HR/GH events are supported in featured module created by RaceTypeID so this case should check them as well.
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
        DESCRIPTION: Create event and add it to Featured Module
        """
        football_markets = [('last_goalscorer', {'cashout': True}),
                            ('extra_time_result', {'cashout': True})]

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
        self.__class__.featured_tab_name = self.get_ribbon_tab_name(
            self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)

    def test_001_select_module_created_by_sport_type_idtap_link_for_selected_event_with_number_of_markets_available(self):
        """
        DESCRIPTION: Select module created by Sport type id.
        DESCRIPTION: Tap link for selected event with number of markets available
        EXPECTED: user is navigated to the selected event details page
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

        self.navigate_to_page(name='/')

    def test_002_select_module_created_by_race_type_iddesktop_tap_view_full_race_card_link_under_the_selected_race_eventmobile_tap_more_link_on_the_selected_race_event(self):
        """
        DESCRIPTION: Select module created by Race type ID.
        DESCRIPTION: Desktop: Tap 'View full race card' link under the selected race event
        DESCRIPTION: Mobile: Tap 'More' link on the selected race event
        EXPECTED: user is navigated to the selected event details page
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
                race_name = self.site.racing_event_details.event_title.replace('\n', ' ')
                self.softAssert(self.assertEqual, event_name, race_name, msg='User navigated to wrong page. '
                                                                             f'Current event name is "{race_name}" while "{event_name}" is expected')
                break
            else:
                continue

        self.navigate_to_page(name='/')

    def test_003_select_module_with_configured_link_to_sport_landing_pagetap_the_link(self):
        """
        DESCRIPTION: Select module with configured link to Sport landing page.
        DESCRIPTION: Tap the link
        EXPECTED: user is navigated to the configured sport landing page
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
            module = self.get_module(module_content_name=self.featured_tab_name,
                                     module_name=self.module_football_type_name)
            self.assertEqual(module.footer.text, footer_link_text,
                             msg=f'Footer link text "{module.footer.text}" '
                                 f'is not as expected "{footer_link_text}"')
            module.footer.click()

        self.site.wait_content_state('Football', timeout=20)
        self.navigate_to_page(name='/')

    def test_004_select_module_with_the_link_that_should_navigate_user_to_any_other_configured_in_cms_pagetap_the_link(self):
        """
        DESCRIPTION: Select module with the link that should navigate user to any other configured in CMS page.
        DESCRIPTION: Tap the link.
        EXPECTED: User is navigated to the page configure in CMS for the module
        """
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
