import pytest
from crlat_cms_client.utils.exceptions import CMSException
import tests
import datetime as dt
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.hl
@pytest.mark.cms
@pytest.mark.desktop
@pytest.mark.quick_links
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.desktop_only
@vtest
class Test_C65940590_Verify_the_display_of_quick_links_on_Desktop(BaseFeaturedTest):
    """
    TR_ID: C65940590
    NAME: Verify the display of quick links on Desktop
    DESCRIPTION: This test case is to validate whether  quick links are not displayed on desktop.
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: 2) Navigate to Sportspage->Home-> Module order ->quick link-> Click on create quick link button
    PRECONDITIONS: 3) Check the Active check box
    PRECONDITIONS: 4) Enter the valid data for following fields
    PRECONDITIONS: a. Enter title
    PRECONDITIONS: b. Enter destination
    PRECONDITIONS: c. Select start and end date.
    PRECONDITIONS: d.Select SVG icon
    PRECONDITIONS: e.Select segment (by default universal will be selected)
    PRECONDITIONS: f.Click on create button.
    PRECONDITIONS: Quick link should be in running state.
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    quick_link_name = 'Auto C65940590'
    destination_url = f'https://{tests.HOSTNAME}/sport/football'
    homepage_id = 0

    def test_001_launch_the_application_on_desktop(self):
        """
        DESCRIPTION: Launch the application on desktop
        EXPECTED: Application should be loaded successfully.
        """
        featured_module = self.cms_config.get_sport_module(sport_id=0, module_type='FEATURED')[0]
        if featured_module.get('disabled'):
            self.cms_config.update_recently_played_games(disabled=False)

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            type_id = event['event']['typeId']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            type_id = event.ss_response['event']['typeId']
        featured_module = self.cms_config.add_featured_tab_module(select_event_by='Type',
                                                                  id=type_id,
                                                                  max_rows=5,
                                                                  events_time_from_hours_delta=-4.5,
                                                                  module_time_from_hours_delta=-10,
                                                                  title="C65940590"
                                                                  )
        self.assertTrue(featured_module, msg=f'Featured module is not created')
        def is_within_display_date_range(quick_link_data):
            current_time = dt.datetime.utcnow().isoformat()
            condition_result = quick_link_data.get('validityPeriodStart') <= current_time <= quick_link_data.get('validityPeriodEnd')
            return condition_result

        if not self.is_quick_links_enabled():
            self.cms_config.update_system_configuration_structure(config_item='Sport Quick Links',
                                                                  field_name="enabled",
                                                                  field_value=True)

        sport_quick_links = self.cms_config.get_system_configuration_item('Sport Quick Links')
        max_amount_quick_link = sport_quick_links.get('maxAmount')
        if not max_amount_quick_link:
            raise CmsClientException('Max number of quick links is not configured in CMS')
        self.__class__.cms_number_of_quick_links = int(max_amount_quick_link)

        # reading existing quick links for universal segment
        existing_quick_links = []
        cms_quick_links = self.cms_config.get_quick_links(sport_id=self.homepage_id)

        for cms_quick_link_data in cms_quick_links:
            if is_within_display_date_range(quick_link_data=cms_quick_link_data) and not cms_quick_link_data['disabled']:
                existing_quick_links.append(cms_quick_link_data['title'].upper().strip())

        # If there are no active or valid quick links available in CMS, then create it
        if not existing_quick_links:
            # updating max amount of Quick link in CMS
            # Maximum expected count of Quick Link in Frontend is '6'
            expected_count = 6
            if max_amount_quick_link == 0:
                self.cms_config.update_system_configuration_structure(config_item='Sport Quick Links',
                                                                      field_name='maxAmount',
                                                                      field_value=expected_count)
                result = wait_for_result(
                    lambda: int(self.cms_config.get_system_configuration_item('Sport Quick Links').get(
                        'maxAmount')) == expected_count,
                    name='Sport Quick Links "maxAmount" value to be changed', poll_interval=5)
                self.assertTrue(result, msg=f'"maxAmount" value is not set to: {expected_count}')

            self.cms_config.create_quick_link(title=self.quick_link_name,
                                              sport_id=self.homepage_id,
                                              destination=self.destination_url)


    def test_002_verify_the_display_of_quick_links(self):
        """
        DESCRIPTION: Verify the display of quick links
        EXPECTED: Quicklinks should not be displayed on desktop.
        """
        self.navigate_to_page('/')
        featured_module = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
        featured_module.scroll_to()
        quick_links_status = wait_for_result(lambda: featured_module.has_quick_links(expected_result=False),
                                             timeout=10)
        self.assertFalse(quick_links_status, msg='Quick link module should not be displayed in Desktop mode, '
                                                 'but still Quick link module is displaying in desktop mode')
