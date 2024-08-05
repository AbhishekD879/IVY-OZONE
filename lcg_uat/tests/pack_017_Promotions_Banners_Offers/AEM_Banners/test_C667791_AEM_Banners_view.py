from urllib.parse import unquote
import pytest
import tests
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.AEM_Banners.BaseAEMBannersTest import BaseAEMBannersTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import cleanhtml
from voltron.utils.waiters import wait_for_result


# @pytest.mark.prod
# @pytest.mark.hl
# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.user_journey_promo_1
# @pytest.mark.banners
# @pytest.mark.aem_banners
# @pytest.mark.critical
# @pytest.mark.desktop
# @pytest.mark.promotions_banners_offers
# @pytest.mark.safari
# @vtest
@pytest.mark.na
class Test_C667791_AEM_Banners_view(BaseAEMBannersTest):
    """
    TR_ID: C667791
    NAME: AEM Banners view
    DESCRIPTION: This test case verifies AEM Banners view
    PRECONDITIONS: 1. AEM Banners should be enabled in CMS
    PRECONDITIONS: 2. To check data from **offer** response open Dev tools -> Network tab
    PRECONDITIONS: 3. This test case should be checked on Mobile, Tablet, Desktop
    """
    keep_browser_open = True

    def test_001_verify_dynamic_banners_presence(self):
        """
        DESCRIPTION: Verify Dynamic Banners presence
        EXPECTED: Dynamic Banners are displayed on Promotions Banner Carousel
        """
        result = self.site.home.aem_banner_section.wait_for_banners()
        self.assertTrue(result, msg='AEM Banners are not displayed')

    def test_002_verify_dynamic_banners_displaying(self):
        """
        DESCRIPTION: Verify Dynamic Banners displaying
        EXPECTED: * Number of Banners displayed correspond to quantity of Dynamic Banners configured in CMS (system-configuration/structure)
        EXPECTED: * Terms and Conditions placeholder is displayed below Banner image
        EXPECTED: * Progress bar is displayed under the Dynamic Banner if there are 2 or more banners received
        """
        self.__class__.offers_response = self.get_offers_response()
        cms_banners = self.get_initial_data_system_configuration().get('DynamicBanners', {})
        if not cms_banners:
            cms_banners = self.cms_config.get_system_configuration_item('DynamicBanners')
        offers_count = cms_banners.get('maxOffers')
        if offers_count is None:
            raise CmsClientException('maxOffers value not configured in CMS')
        number_of_banners_in_ui = self.site.home.aem_banner_section.number_of_banners
        # in case when number of Banners on UI is less than maxOffers value from cms
        if number_of_banners_in_ui < offers_count:
            self.assertEqual(number_of_banners_in_ui, len(self.offers_response),
                             msg=f'Number of Banners displayed "{number_of_banners_in_ui}" does not correspond to '
                                 f'number of Dynamic Banners received in **offer** response: '
                                 f'"{len(self.offers_response)}"')
        else:
            # VOL-3493 AEM banner quantity fix(quantity is limited by maxOffers from DynamicBanners in cms)
            self.assertEqual(number_of_banners_in_ui, offers_count,
                             msg=f'Number of Banners displayed "{number_of_banners_in_ui}" does not correspond to '
                                 f'number of Dynamic Banners from cms: "{offers_count}"')
        wait_for_result(lambda: self.site.home.aem_banner_section.active_banner.has_terms() is True,
                        name='AEM banner tab is active and has terms',
                        timeout=5)
        if offers_count >= 2:
            self.assertTrue(self.site.home.aem_banner_section.has_progress_bar(),
                            msg='Banner section does not have progress bar')

    def test_003_verify_dynamic_banner_image(self):
        """
        DESCRIPTION: Verify Dynamic Banner image
        EXPECTED: * Dynamic Banner image corresponds to **offer.[i].img_url** attribute from **offer** response
        EXPECTED: where [i] - the number of dynamic banners
        """
        active_banner_image_url = self.site.contents.aem_banner_section.active_banner.image_url

        unquoted_url = unquote(active_banner_image_url)
        actual_urls = [unquote(offer['imgUrl']) for offer in self.offers_response]

        self.assertIn(unquoted_url, actual_urls,
                      msg=f'Url of offer \n"{unquoted_url}" is not found in response urls \n"{actual_urls}"')

    def test_004_verify_dynamic_banners_size(self):
        """
        DESCRIPTION: Verify Dynamic Banners size
        EXPECTED: * Height of Dynamic Banner depends on the banner uploaded (max banner container's height is set to 400px)
        EXPECTED: * Width depends on screen resolution of device
        """
        expected_width = self.site.home.aem_banner_section.calculated_aem_banner_width
        banner_width = int(self.site.home.aem_banner_section.active_banner.width)
        if banner_width == 0:
            banner_width = int(self.site.home.aem_banner_section.active_banner.width)
        self.assertAlmostEqual(banner_width, expected_width, delta=1,
                               msg=f'Banner width "{banner_width}" is not the same as expected for device "{expected_width}" within delta 1')

    def test_005_verify_terms_and_conditions_placeholder_html_overlay(self):
        """
        DESCRIPTION: Verify Terms and Conditions placeholder (HTML Overlay)
        EXPECTED: Terms and Conditions placeholder corresponds to **offer.[i].web_t_and_c** attribute from **offer** response
        """
        self.wait_for_next_banner()  # TODO: VOL-1099 Should be changed to swipe when possible
        banner_name = self.site.home.aem_banner_section.active_banner.name
        if self.brand != 'ladbrokes':
            banner_name.replace(f'https://{tests.HOSTNAME}/', '')
        terms = self.site.home.aem_banner_section.active_banner.terms_and_conditions_text
        if terms:
            offer_terms = next((offer.get('webTandC') for offer in self.offers_response
                                if 'webTandC' in offer and offer.get('webTandCLink') == banner_name), None)
            self.assertTrue(offer_terms, msg=f'Terms and Conditions not found for "{banner_name}" offer')
            offer_terms_from_response = cleanhtml(offer_terms).rstrip()
            self.assertEqual(terms.strip(), offer_terms_from_response,
                             msg=f'Terms and Conditions of offer \n"{terms.strip()}" '
                                 f'is not the same as found in response \n"{offer_terms_from_response}"')
        else:
            self._logger.warning('*** Skipping Terms and Conditions verification as active banner does not have TC\'s')

    def test_006_verify_navigation_between_dynamic_banners(self):
        """
        DESCRIPTION: Verify navigation between Dynamic Banners
        EXPECTED: * User can scroll left or right within Banner Carousel
        EXPECTED: * Dynamic Banners are navigated automatically
        EXPECTED: * Dynamic Banners are shown in continuous loop
        """
        # self.swipe_to_next_banner() # TODO: VOL-1099 Should be changed to swipe when possible
        cms_banners = self.get_initial_data_system_configuration().get('DynamicBanners', {})
        if not cms_banners:
            cms_banners = self.cms_config.get_system_configuration_item('DynamicBanners')
        max_offer = cms_banners.get('maxOffers')
        if max_offer is None:
            raise CmsClientException('maxOffers value not configured in CMS')
        if max_offer > 1:
            result = self.wait_for_next_banner()
            self.assertTrue(result, msg='Next AEM banner was not loaded automatically')
