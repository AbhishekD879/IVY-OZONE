import pytest
import tests
from tests.base_test import vtest
from crlat_ob_client.offer import Offer
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_014_Module_Selector_Ribbon.Private_Markets.BasePrivateMarketsTest import BasePrivateMarketsTest


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod # Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop_only
@pytest.mark.desktop
@pytest.mark.navigation
@vtest
class Test_C1391427_Verify_Hero_Header_displaying_on_Homepage_for_Desktop(BasePrivateMarketsTest, BaseSportTest):
    """
    TR_ID: C1391427
    NAME: Verify Hero Header displaying on Homepage for Desktop
    DESCRIPTION: This test case verifies Hero Header displaying on Homepage for Desktop.
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: The following data is available:
        PRECONDITIONS: - Enhanced Markets (Private Markets)
        PRECONDITIONS: - Enhanced Multiples
        PRECONDITIONS: - Banners
        PRECONDITIONS: - Offers
        PRECONDITIONS: - Banach events
        PRECONDITIONS: - Featured modules
        PRECONDITIONS: Oxygen app is loaded
        """
        self.user = tests.settings.default_username
        self.site.login(username=self.user)
        offer_id = self.ob_config.backend.ob.private_market_offer.offer_id
        offer = Offer(env=tests.settings.backend_env, brand=self.brand)
        self.trigger_private_market_appearance(user=self.user,
                                               expected_market_name=self.private_market_name)
        offer.give_offer(username=self.user, offer_id=offer_id)
        event_params = self.ob_config.add_football_event_to_england_premier_league()

        self.__class__.eventID = event_params.event_id
        self.site.wait_content_state("homepage")
        event_params = self.ob_config.add_football_event_enhanced_multiples()

        self.__class__.eventID2 = event_params.event_id

    def test_001_verify_hero_header_content_on_the_homepage(self):
        """
        DESCRIPTION: Verify Hero Header content on the Homepage
        EXPECTED: Main View 1 and Main View 2 columns are merged and contain the following element:
        EXPECTED: * AEM Banners section and Offer area (depends on screen width)
        EXPECTED: * Enhanced multiples carousel
        EXPECTED: Module Ribbon tabs are transformed in the next sections:
        EXPECTED: * Your Enhanced Markets
        EXPECTED: * In-Play & Live Stream
        EXPECTED: * Next Races Carousel
        EXPECTED: * Build Your Bet
        EXPECTED: * Featured area
        """
        self.site.wait_content_state("Homepage")
        aem = self.site.home.aem_banner_section.wait_for_banners()
        self.assertTrue(aem, msg='AEM Banners are not displayed')
        self.device.refresh_page()
        self.site.wait_content_state("homepage")
        sections = self.site.home.desktop_modules.items_as_ordered_dict
        self.assertIn('ENHANCED', sections[0], msg=f"{sections} ledh")
        self.assertTrue(sections, msg='Sections are not displayed')
