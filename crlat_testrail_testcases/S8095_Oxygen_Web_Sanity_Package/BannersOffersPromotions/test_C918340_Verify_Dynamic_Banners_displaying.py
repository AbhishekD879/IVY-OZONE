import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C918340_Verify_Dynamic_Banners_displaying(Common):
    """
    TR_ID: C918340
    NAME: Verify Dynamic Banners displaying
    DESCRIPTION: This test case verifies Dynamic Banners displaying
    DESCRIPTION: AUTOTESTS [C49399483] [C49405231]
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
        pass

    def test_002_verify_dynamic_banners_configuration(self):
        """
        DESCRIPTION: Verify Dynamic Banners configuration
        EXPECTED: The next parameters are sent in **offer** request (dev tools -> network -> all -> type response.json -> Headers -> Request URL in dev tools) to retrieve Dynamic Banners:
        EXPECTED: * channels (e.g connect, app, mobile)
        EXPECTED: * page (e.g homepage, football)
        EXPECTED: * userType (e.g anonymous)
        EXPECTED: * imsLevel (e.g. 4) if not anonymous user
        """
        pass

    def test_003_verify_dynamic_banners_displaying(self):
        """
        DESCRIPTION: Verify Dynamic Banners displaying
        EXPECTED: * Navigation arrows are displayed at the left and right side of Banner(for Desktop)
        EXPECTED: * Number of Banners displayed correspond to quantity of Dynamic Banners received in response
        EXPECTED: * Terms and Conditions placeholder is displayed below Banner image
        EXPECTED: * Progress bar is displayed under the Dynamic Banner if there are 2 or more banners received
        """
        pass

    def test_004_verify_navigation_between_dynamic_banners(self):
        """
        DESCRIPTION: Verify navigation between Dynamic Banners
        EXPECTED: * User can scroll left or right within Banner Carousel
        EXPECTED: * Dynamic Banners are navigated automatically
        EXPECTED: * Dynamic Banners are shown in continuous loop
        """
        pass

    def test_005_go_to_any_sportrace_page_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Go to any <Sport>/<Race> page and repeat steps #2-4
        EXPECTED: 
        """
        pass
