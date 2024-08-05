import pytest

import tests
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.AEM_Banners.BaseAEMBannersTest import BaseAEMBannersTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.banners
@pytest.mark.aem_banners
@pytest.mark.promotions_banners_offers
@pytest.mark.desktop
@pytest.mark.safari
@vtest
class Test_C918340_Verify_Dynamic_Banners_displaying(BaseAEMBannersTest):
    """
    TR_ID: C918340
    NAME: Verify Dynamic Banners displaying
    DESCRIPTION: This test case verifies Dynamic Banners displaying
    DESCRIPTION: AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_order=asc&group_id=740709
    PRECONDITIONS: 1. AEM Banners should be enabled in CMS -> System Configuration -> DYNAMICBANNERS' item
    PRECONDITIONS: 2. To check data from offer response open Dev tools -> Network tab
    PRECONDITIONS: AEM Banner is configured in: https://author-ladbrokes-stage65.adobecqms.net/
    PRECONDITIONS: How to create AEM Banner: https://confluence.egalacoral.com/display/SPI/AEM+Admin+guide?preview=/96687399/96687395/AEM%20-%20Admin%20Guide.pdf
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: * Homepage is opened
        EXPECTED: * Dynamic Banners are displayed on Promotions Banner Carousel
        """
        self.site.wait_content_state('Homepage')

    def test_002_verify_dynamic_banners_configuration(self, page='homepage'):
        """
        DESCRIPTION: Verify Dynamic Banners configuration
        EXPECTED: The next parameters are sent in **offer** request (dev tools -> network -> all -> type response.json -> Headers -> Request URL in dev tools) to retrieve Dynamic Banners:
        EXPECTED: * channels (e.g connect, app, mobile)
        EXPECTED: * page (e.g homepage, football)
        EXPECTED: * userType (e.g anonymous)
        EXPECTED: * imsLevel (e.g. 4) if not anonymous user
        """
        offer_call = self.get_offers_url()
        self.assertIn('channels/mobile/', offer_call, msg=f'Parameter "channels/mobile/" not in "{offer_call}"')
        self.assertIn(f'pages/{page}/', offer_call, msg=f'Parameter "pages/{page}/" not in "{offer_call}"')
        parameter = 'userType/anonymous/' if self.brand == 'bma' else 'userType/new/'
        self.assertIn(parameter, offer_call, msg=f'Parameter "{parameter}" not in "{offer_call}"')
        self.assertNotIn('imsLevel/', offer_call, msg=f'Parameter "imsLevel/" not in "{offer_call}"')  # for not logged in user

    def test_003_verify_dynamic_banners_displaying(self):
        """
        DESCRIPTION: Verify Dynamic Banners displaying
        EXPECTED: * Navigation arrows are displayed at the left and right side of Banner(for Desktop)
        EXPECTED: * Number of Banners displayed correspond to quantity of Dynamic Banners received in response
        EXPECTED: * Terms and Conditions placeholder is displayed below Banner image
        EXPECTED: * Progress bar is displayed under the Dynamic Banner if there are 2 or more banners received
        """
        offers_response = self.get_offers_response()
        dynamic_banners_config = self.get_initial_data_system_configuration().get('DynamicBanners', {})
        if not dynamic_banners_config:
            dynamic_banners_config = self.cms_config.get_system_configuration_item('DynamicBanners')
        offers_count = dynamic_banners_config.get('maxOffers')

        self.softAssert(self.assertIsNotNone, offers_count, msg=f'Max offers count is not specified in CMS.')

        number_of_banners_in_ui = self.site.home.aem_banner_section.number_of_banners
        # in case when number of Banners on UI is less than maxOffers value from cms
        assertion_method = self.assertEqual if tests.settings.backend_env == 'prod' else self.assertLessEqual
        if number_of_banners_in_ui < offers_count:
            self.softAssert(assertion_method, number_of_banners_in_ui, len(offers_response),
                            msg=f'Number of Banners displayed "{number_of_banners_in_ui}" does not '
                            f'correspond to number of Dynamic Banners received in **offer** response: '
                            f'"{len(offers_response)}"')
        else:
            self.softAssert(assertion_method, number_of_banners_in_ui, offers_count,
                            msg=f'Number of Banners displayed "{number_of_banners_in_ui}" does not '
                            f'correspond to number of Dynamic Banners from cms: "{offers_count}"')
        banners = self.site.contents.aem_banner_section.banners
        for banner in banners:
            img_url = banner.image_url
            if 'terms_and_conditions_container_visible=1' in img_url:
                result = wait_for_result(lambda: self.site.home.aem_banner_section.active_banner.has_terms() is True,
                                         name='AEM banner tab is active and has terms',
                                         timeout=5)
                self.assertTrue(result,
                                msg='Banner section does not have Terms and Conditions placeholder')
            else:
                self._logger.warning('*** Banner does not have  Terms and Conditions')
        if offers_count >= 2:
            self.assertTrue(self.site.home.aem_banner_section.has_progress_bar(),
                            msg='Banner section does not have progress bar')

    def test_004_verify_navigation_between_dynamic_banners(self):
        """
        DESCRIPTION: Verify navigation between Dynamic Banners
        EXPECTED: * User can scroll left or right within Banner Carousel
        EXPECTED: * Dynamic Banners are navigated automatically
        EXPECTED: * Dynamic Banners are shown in continuous loop
        """
        dynamic_banners_config = self.get_initial_data_system_configuration().get('DynamicBanners', {})
        if not dynamic_banners_config:
            dynamic_banners_config = self.cms_config.get_system_configuration_item('DynamicBanners')
        offers_count = dynamic_banners_config.get('maxOffers')

        self.softAssert(self.assertIsNotNone, offers_count, msg=f'Max offers count is not specified in CMS.')

        if offers_count > 1:
            result = self.wait_for_next_banner()
            self.assertTrue(result, msg='Next AEM banner was not loaded automatically')

    def test_005_go_to_any_sportrace_page_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Go to any <Sport>/<Race> page and repeat steps #2-4
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')
        self.test_002_verify_dynamic_banners_configuration(page='football')
        self.test_003_verify_dynamic_banners_displaying()
        self.test_004_verify_navigation_between_dynamic_banners()
