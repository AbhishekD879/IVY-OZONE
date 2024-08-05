import pytest
import tests
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.AEM_Banners.BaseAEMBannersTest import BaseAEMBannersTest


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
# @pytest.mark.prod_incident
# @pytest.mark.user_journey_promo_1
# @pytest.mark.banners
# @pytest.mark.aem_banners
# @pytest.mark.medium
# @pytest.mark.desktop
# @pytest.mark.promotions_banners_offers
# @pytest.mark.desktop
# @pytest.mark.safari
# @vtest
@pytest.mark.na
class Test_C667796_AEM_Banners_links_opening(BaseAEMBannersTest):
    """
    TR_ID: C667796
    NAME: AEM Banners links opening
    DESCRIPTION: This test case verifies AEM Banners links opening
    PRECONDITIONS: 1. AEM Banners should be enabled in CMS
    PRECONDITIONS: 2. To check data from **offer** response open Dev tools -> Network tab
    PRECONDITIONS: 3. This test case should be checked on Mobile, Tablet
    """
    keep_browser_open = True
    base_url = f'https://{tests.HOSTNAME}'

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        EXPECTED: Dynamic Banners are displayed on Promotions Banner Carousel
        """
        result = self.site.home.aem_banner_section.wait_for_banners()
        self.assertTrue(result, msg='AEM Banners are not displayed')

    def test_002_tap_dynamic_banner(self):
        """
        DESCRIPTION: Tap Dynamic Banner
        EXPECTED: * New browser tab is opened if app_target:"_blank" received in  **offers**, otherwise in same browser tab
        EXPECTED: * User is navigated to URL received in **offers.[i].link_url** response,
        EXPECTED: where [i] - the number of dynamic banners
        """
        self.__class__.offers_response = self.get_offers_response()
        self.assertTrue(self.offers_response, msg='Offers response is empty')

        targets_from_response = []
        for offer in self.offers_response:
            target = offer.get('roxanneAppUrl', '/null')  # ladbrokes ONLY URL keys
            if target == '/null':
                target = offer.get('appUrl', '/null')  # Coral ONLY URL keys + some ladbrokes related banners
            if target != '':
                target = '/' + target if not target.startswith('/') and not target.startswith('http') else target
            targets_from_response.append(target)

        self.__class__.banners = self.site.contents.aem_banner_section.banners
        self.assertTrue(self.banners, msg='No banners found')
        ui_banners_url = []
        for banner in self.banners:
            url = banner.url
            url = url if url else self.base_url + '/null'
            ui_banners_url.append(url)

        for target in targets_from_response:
            expected_url = self.base_url + target if not target.startswith('http') else target
            self.softAssert(self.assertIn, expected_url, ui_banners_url, msg=f'Banner from response with "{expected_url}" URL was not '
                            f'found on UI in list of banners: "{ui_banners_url}"')

    def test_003_tap_on_toggle_html_overlay_on_the_banner(self):
        """
        DESCRIPTION: Tap on toggle/HTML overlay on the Banner
        EXPECTED: * New browser tab is opened if app_target:"_blank" received in  **offers**, otherwise in same browser tab
        EXPECTED: * User is navigated to URL received in **offers.[i].mob_t_and_c_link:** response,
        EXPECTED: where [i] - the number of dynamic banners
        """
        tac_from_response = []
        for offer in self.offers_response:
            web_tand_c_link = offer.get('webTandCLink', '')
            mob_tand_c_link = offer.get('mobTandCLink', '')
            tac_from_response.append(web_tand_c_link)
            tac_from_response.append(mob_tand_c_link)
        tacs = []
        for banner in self.banners:
            tac_url = banner.terms_and_conditions_url
            banner_tacs = [tac for tac in tac_from_response if tac_url in tac or self.base_url + tac in tac]
            for tac in banner_tacs:
                tacs.append(tac)
        for tac in tac_from_response:
            self.assertIn(tac, tacs, msg=f'Banner with "{tac}" T&C URL was not found on UI: "{tacs}"')
