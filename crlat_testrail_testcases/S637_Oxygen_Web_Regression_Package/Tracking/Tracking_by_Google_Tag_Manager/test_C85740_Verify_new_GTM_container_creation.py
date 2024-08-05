import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C85740_Verify_new_GTM_container_creation(Common):
    """
    TR_ID: C85740
    NAME: Verify new GTM container creation
    DESCRIPTION: This test case verifies new GTM container ID adding to the application
    PRECONDITIONS: 1. Load Oxygen application and go to Console -> Elements tab
    PRECONDITIONS: 2. Using ctrl + F combination (or any other way) find GTM container script in console
    PRECONDITIONS: 3. For testing guidance, please refer to the following confluence page:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Testing+of+Google+Analytics
    PRECONDITIONS: **Note:**
    PRECONDITIONS: For Coral PROD use the following GTM container ID: KW37JJ9
    PRECONDITIONS: For Ladbrokes PROD use the following GTM container ID: KGCS6GX
    """
    keep_browser_open = True

    def test_001_verify_script_and_gtm_container_id_in_the_script(self):
        """
        DESCRIPTION: Verify script and GTM Container ID in the script
        EXPECTED: Script is the following:
        EXPECTED: <!-- Google Tag Manager -->
        EXPECTED: <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXX"
        EXPECTED: height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
        EXPECTED: <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push(
        EXPECTED: {'gtm.start': new Date().getTime(),event:'gtm.js'}
        EXPECTED: );var f=d.getElementsByTagName(s)[0],
        EXPECTED: j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        EXPECTED: 'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        EXPECTED: })(window,document,'script','dataLayer','GTM-XXXXXX');</script>
        EXPECTED: <!-- End Google Tag Manager -->
        """
        pass

    def test_002_verify_gtm_container_id_navigating_through_application_in_network__collect___query_string_parameters_section_in_header(self):
        """
        DESCRIPTION: Verify GTM Container ID navigating through application in Network-> collect -> Query String Parameters section in Header
        EXPECTED: GTM Container ID is GTM-XXXXXX
        """
        pass
