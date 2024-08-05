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
class Test_C1933491_Verify_tracking_for_iOS_Smart_Banners_web(Common):
    """
    TR_ID: C1933491
    NAME: Verify tracking for iOS Smart Banners (web)
    DESCRIPTION: This test case verifies GTM tracking for user's actions with iOS Smart Banner
    PRECONDITIONS: 1. iOS device should be used for testing
    PRECONDITIONS: 2. Cache and cookie are cleared for Safari browser at the start of testing
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_in_safari_and_verify_smart_banner_displaying(self):
        """
        DESCRIPTION: Load Oxygen application in Safari and verify Smart Banner displaying
        EXPECTED: Smart Banner is displayed
        """
        pass

    def test_002_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: Following data is displayed in dataLayer:
        EXPECTED: {{dataLayer.push({   }}
        EXPECTED: {{    }}{{'event'}} {{: }}{{'trackEvent'}}{{,}}
        EXPECTED: {{    }}{{'eventCategory'}} {{: }}{{'iOS - smart banner'}}{{,}}
        EXPECTED: {{    }}{{'eventAction'}} {{: }}{{'display'}}{{,}}
        EXPECTED: {{    }}{{'eventLabel'}} {{: }}{{'<< BANNER NAME >>'}}
        EXPECTED: {{})}}
        """
        pass

    def test_003_tap_x_button_in_the_banner_to_close_it(self):
        """
        DESCRIPTION: Tap 'X' button in the Banner to close it.
        EXPECTED: 
        """
        pass

    def test_004_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: Following data is displayed in dataLayer:
        EXPECTED: {{dataLayer.push({   }}
        EXPECTED: {{    }}{{'event'}}{{: }}{{'trackEvent'}}{{,}}
        EXPECTED: {{    }}{{'eventCategory'}}{{: }}{{'iOS - smart banner'}}{{,}}
        EXPECTED: {{    }}{{'eventAction'}}{{: }}{{'close'}}{{,}}
        EXPECTED: {{    }}{{'eventLabel'}}{{: }}{{'<< BANNER NAME >>'}}
        EXPECTED: {{})}}
        """
        pass

    def test_005_clear_cache_and_cookie_or_login_with_another_userverify_smart_banner_displaying(self):
        """
        DESCRIPTION: Clear cache and cookie or login with another user.
        DESCRIPTION: Verify Smart Banner displaying.
        EXPECTED: Smart Banner is displayed
        """
        pass

    def test_006_tap_the_link_to_download_native_application(self):
        """
        DESCRIPTION: Tap the link to download native application
        EXPECTED: 
        """
        pass

    def test_007_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: Following data is displayed in dataLayer:
        EXPECTED: {{dataLayer.push({   }}
        EXPECTED: {{    }}{{'event'}} {{: }}{{'trackEvent'}}{{,}}
        EXPECTED: {{    }}{{'eventCategory'}} {{: }}{{'iOS - smart banner'}}{{,}}
        EXPECTED: {{    }}{{'eventAction'}} {{: }}{{'click'}}{{,}}
        EXPECTED: {{    }}{{'eventLabel'}} {{: }}{{'<< BANNER NAME >>'}}
        EXPECTED: {{})}}
        """
        pass
