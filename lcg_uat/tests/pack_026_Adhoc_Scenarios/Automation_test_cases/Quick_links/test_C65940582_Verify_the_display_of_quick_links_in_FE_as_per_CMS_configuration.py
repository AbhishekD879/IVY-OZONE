from datetime import datetime
import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from faker import Faker
from selenium.common.exceptions import StaleElementReferenceException
from tzlocal import get_localzone
import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.cms
@pytest.mark.mobile_only
@pytest.mark.quick_links
@pytest.mark.other
@pytest.mark.homepage_featured
@vtest
# this test case covers C65940584, C65940585, C65940586, C65940587, C65940583, C65940589
class Test_C65940582_Verify_the_display_of_quick_links_in_FE_as_per_CMS_configuration(BaseFeaturedTest):
    """
    TR_ID: C65940582
    NAME: Verify the display of quick links in FE as per CMS configuration
    DESCRIPTION: This test case is to validate quick links displaying in FE as per CMS configuration
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
    """
    keep_browser_open = True
    device_name = tests.mobile_default
    destination_url = f'https://{tests.HOSTNAME}/sport/football'
    now = datetime.now()
    svg_id = 'football'
    timezone = str(get_localzone())
    is_max_amount_increased = False
    cms_number_of_quick_links = 6

    @classmethod
    def custom_tearDown(cls):
        if cls.is_max_amount_increased:
            cls.get_cms_config().update_system_configuration_structure(
                config_item='Sport Quick Links', field_name='maxAmount', field_value=cls.cms_number_of_quick_links)

    def wait_up_to_time_complete(self, end_time):
        now = datetime.now()  # taking now time
        now = get_date_time_as_string(date_time_obj=now,
                                      time_format='%Y-%m-%dT%H:%M:%S.%f',
                                      url_encode=False)[:-3] + 'Z'
        if now > end_time:
            return
        else:
            wait_for_haul(20)
            return self.wait_up_to_time_complete(end_time)

    def ql_status(self, ql_name=None, time=1, expected_result=True):
        ql_name = self.quick_link_name if not ql_name else ql_name
        if time > 120:
            return not expected_result
        try:
            ql_stat = next(
                (True for fe_ql_name, ql in self.site.home.tab_content.quick_links.items_as_ordered_dict.items()
                 if fe_ql_name == ql_name or
                 (fe_ql_name[-3:] == '...' and ql_name[:len(fe_ql_name) - 3] + '...' == fe_ql_name)), False)
        except StaleElementReferenceException:
            ql_stat = not expected_result
            time -= 1
        if ql_stat == expected_result:
            return expected_result
        else:
            wait_for_haul(1)
            return self.ql_status(ql_name=ql_name, time=time + 1, expected_result=expected_result)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Configure 1 active Quick link for Homepage
        DESCRIPTION: Load Oxygen application and navigate to Featured tab
        """
        if not self.is_quick_links_enabled():
            self.cms_config.update_system_configuration_structure(config_item='Sport Quick Links',
                                                                  field_name="enabled",
                                                                  field_value=True)

        sport_quick_links = self.get_initial_data_system_configuration().get('Sport Quick Links', {})

        if not sport_quick_links:
            sport_quick_links = self.cms_config.get_system_configuration_item('Sport Quick Links')

        if not sport_quick_links.get('maxAmount'):
            raise CmsClientException('Max number of quick links is not configured in CMS')

        self.__class__.cms_number_of_quick_links = int(sport_quick_links['maxAmount'])

        self.cms_config.update_system_configuration_structure(config_item='Sport Quick Links',
                                                              field_name='maxAmount', field_value=self.cms_number_of_quick_links + 1)
        self.__class__.is_max_amount_increased = True

        self.__class__.quick_link_name = 'Autotest QL ' + Faker().city()

        if self.is_quick_link_disabled_for_sport_category(sport_id=0):
            raise CmsClientException('"Quick links" module is disabled for homepage')

        self.__class__.quick_link_response = self.cms_config.create_quick_link(title=self.quick_link_name,
                                                                               sport_id=0,
                                                                               destination=self.destination_url,
                                                                               svgId=self.svg_id
                                                                               )

    def test_001_launch_mobile_application(self):
        """
        DESCRIPTION: Launch mobile application.
        EXPECTED: Application should be loaded successfully. By default, home page should be loaded.
        """
        self.site.wait_content_state(state_name='Home')

    def test_002_verify_display_of_created_quick_link_on_fe(self, login=False):
        """
        DESCRIPTION: Verify display of created quick link on FE
        EXPECTED: Quick link should be displayed.
        EXPECTED: Quick link should not be displayed if current system date and time is less then configured date and time
        """
        login_status = 'after login' if login else 'before login'
        status_of_quick_link_section = self.site.home.tab_content.has_quick_links()
        self._logger.info(f'Quick Link Section Status {status_of_quick_link_section}')
        self.assertTrue(status_of_quick_link_section, f'Quick Link Section is not displayed')
        self.site.home.tab_content.quick_links.scroll_to_we()
        self._logger.info(f'all quick links : {list(self.site.home.tab_content.quick_links.items_as_ordered_dict.keys())}')
        self.device.driver.refresh()
        wait_for_haul(5)
        self.assertIsNotNone(self.ql_status(), f'{self.quick_link_name} is not visible in front end {login_status}')
        ql_obj = next((ql for ql_name, ql in self.site.home.tab_content.quick_links.items_as_ordered_dict.items()
                       if ql_name == self.quick_link_name or
                       (ql_name[-3:] == '...' and self.quick_link_name[:len(ql_name) - 3] + '...' == ql_name)), None)

        # verifying svg icon
        self.assertEqual(f'#{self.svg_id}', ql_obj.svg_icon,
                         f'"{ql_obj.svg_icon}" is not same as expected "#{self.svg_id}"')

        # verifying quick link destination url journey as per CMS configuration
        ql_obj.click()
        self.site.wait_content_state('football')
        current_url = self.device.get_current_url()
        self.assertEqual(current_url, self.destination_url,
                         msg=f'Current url: "{current_url}" is not the same as expected: "{self.destination_url}"')
        self.site.back_button.click()
        self.site.wait_content_state(state_name='Home')

    def test_003_verify_title(self):
        """
        DESCRIPTION: Verify title
        EXPECTED: Title should be displayed as per CMS configured.
        EXPECTED: If title is too long, after certain number of characters ellipse(...) symbol should be displayed.
        """
        # after login checking quick link is appeared or not
        self.site.login()
        self.test_002_verify_display_of_created_quick_link_on_fe(login=True)

    def test_004_verify_after_validity_period_ends_quick_link_status(self):
        """
        DESCRIPTION: wait up to validity period ends
        EXPECTED: Quick link should disappear
        """
        # can't put the time in past as network call is not allowing
        # actual_end_time = self.quick_link_response.get('validityPeriodEnd')
        # end_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format='%Y-%m-%dT%H:%M:%S.%f',
        #                                            url_encode=False, minutes=1)[:-3] + 'Z'
        # if self.timezone.upper() == "UTC":
        #     end_time_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format='%Y-%m-%dT%H:%M:%S.%f',
        #                                            url_encode=False, minutes=1)[:-3] + 'Z'
        # elif self.timezone.upper() == 'EUROPE/LONDON':
        #     end_time_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format='%Y-%m-%dT%H:%M:%S.%f',
        #                                            url_encode=False, minutes=-59)[:-3] + 'Z'
        # else:
        #     end_time_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format='%Y-%m-%dT%H:%M:%S.%f',
        #                                            url_encode=False, hours=-5.5, minutes=1)[:-3] + 'Z'
        #
        # self.quick_link_response = self.cms_config.update_quick_link(quick_link_id=self.quick_link_response['id'],
        #                                                              validityPeriodEnd=end_time_cms)
        # status = self.ql_status(ql_name=self.quick_link_name, expected_result=True)
        # self.assertTrue(status, f'"{self.quick_link_name}" is not displayed in frontend before validity period end')
        # self._logger.info(f'"{self.quick_link_name}" is displayed before end time')
        #
        # self.wait_up_to_time_complete(end_time)
        # status = self.ql_status(ql_name=self.quick_link_name, expected_result=False)
        # self.assertFalse(status, f'"{self.quick_link_name}" is displayed in frontend after validity period ends')
        # self._logger.info(f'"{self.quick_link_name}" is disabled')
        #
        # self.quick_link_response = self.cms_config.update_quick_link(quick_link_id=self.quick_link_response['id'],
        #                                                              validityPeriodEnd=actual_end_time)
        # status = self.ql_status(ql_name=self.quick_link_name, expected_result=True)
        # self.assertTrue(status, f'"{self.quick_link_name}" is not displayed in frontend before validity period end')
        # self._logger.info(f'"{self.quick_link_name}" is enabled')
        #
        # # title updation
        # self.__class__.quick_link_name = 'Autotest QL ' + Faker().city()
        # self.__class__.quick_link_response = self.cms_config.update_quick_link(quick_link_id=self.quick_link_response['id'],
        #                                                              title=self.quick_link_name)
        # status = self.ql_status(ql_name=self.quick_link_name, expected_result=True)
        # self.assertTrue(status, f'"{self.quick_link_name}" is not displayed in frontend after updation')

    def test_005_verify_the_quick_link_status_on_front_end_when_deactivate_and_activate(self):
        """
        DESCRIPTION : Deactivate the quick link in CMS
        EXPECTED : Quick link should disappear from Front end
        DESCRIPTION : activate the quick link in CMS
        EXPECTED : Quick link should be visible in front end
        """
        self.cms_config.change_quick_link_state(quick_link_object=self.quick_link_response, active=False)
        self.quick_link_response = self.cms_config.get_quick_link(self.quick_link_response['id'])
        status = self.ql_status(ql_name=self.quick_link_name, expected_result=False)
        self.assertFalse(status, f'"{self.quick_link_name}" is displayed in frontend after deactivate')

        self.cms_config.change_quick_link_state(quick_link_object=self.quick_link_response, active=True)
        self.cms_config.get_quick_link(self.quick_link_response['id'])
        status = self.ql_status(ql_name=self.quick_link_name, expected_result=True)
        self.assertTrue(status, f'"{self.quick_link_name}" is not displayed in frontend after activated')

    def test_006_verify_the_quick_link_status_on_front_end_after_deletion_in_cms(self):
        """
        DESCRIPTION : Remove the Quick link from CMS
        EXPECTED : Quick link disappear in front end
        """
        self.cms_config.delete_quick_link(quick_link_id=self.quick_link_response['id'])
        self.cms_config._created_quick_links.pop()
        status = self.ql_status(ql_name=self.quick_link_name, expected_result=False)
        self.assertFalse(status, f'"{self.quick_link_name}" is displayed in frontend after deletion')
