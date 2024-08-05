import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59754376_Verify_Dont_Show_Me_This_Again_checkbox_functionality_on_Odds_Boost_pop_up(Common):
    """
    TR_ID: C59754376
    NAME: Verify 'Don't Show Me This Again' checkbox functionality on Odds Boost pop-up
    DESCRIPTION: This test case verifies that 'Don't Show Me This Again' checkbox on Odds Boost pop-up adds valid parameter to local storage depending on option picked by user
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: User with Odds Boost tokens is available OR Generate token for user Odds boost token in Backoffice
    PRECONDITIONS: * How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: 'Allow User To Toggle Visibility option' is enabled in CMS > Odds Boost
    PRECONDITIONS: User has at least 1 available Odds Boosts token. Token is NOT expired
    PRECONDITIONS: 1. Clean site local storage for the environment (DevTools > Application > Clear storage > 'Clear site data')
    PRECONDITIONS: 2. Refresh the app
    """
    keep_browser_open = True

    def test_001_log_in_with_user_from_preconditions(self):
        """
        DESCRIPTION: Log in with user from preconditions
        EXPECTED: * Odds Boost pop-up is displayed
        EXPECTED: * 'Don't Show Me This Again' checkbox is present
        EXPECTED: * Initial data request to CMS returns data for checkbox parameters
        EXPECTED: ![](index.php?/attachments/get/118618156)
        """
        pass

    def test_002__do_not_tick_dont_show_me_this_again_checkbox_presstap_ok_thanks(self):
        """
        DESCRIPTION: * Do NOT tick 'Don't Show Me This Again' checkbox
        DESCRIPTION: * Press/Tap 'Ok, thanks'
        EXPECTED: Pop-up is closed
        """
        pass

    def test_003__in_devtools__application__local_storage_find_current_app_environment_check_for_oxkeepoddsboostpopuphidden_parameter(self):
        """
        DESCRIPTION: * In DevTools > Application > Local storage, find current app environment
        DESCRIPTION: * Check for OX.keepOddsBoostPopupHidden parameter
        EXPECTED: 'OX.keepOddsBoostPopupHidden' parameter is present and is empty ('{}')
        """
        pass

    def test_004__clean_site_local_storage_for_the_environment_devtools__application__clear_storage__clear_site_data_refresh_application_login_with_the_same_user(self):
        """
        DESCRIPTION: * Clean site local storage for the environment (DevTools > Application > Clear storage > 'Clear site data')
        DESCRIPTION: * Refresh application
        DESCRIPTION: * Login with the same user
        EXPECTED: * Odds Boost pop-up is displayed again with checkbox
        """
        pass

    def test_005__tick_dont_show_me_this_again_checkbox_presstap_ok_thanks_check_local_storage_for_oxkeepoddsboostpopuphidden_parameter(self):
        """
        DESCRIPTION: * Tick 'Don't Show Me This Again' checkbox
        DESCRIPTION: * Press/Tap 'Ok, thanks'
        DESCRIPTION: * Check Local storage for OX.keepOddsBoostPopupHidden parameter
        EXPECTED: * 'OX.keepOddsBoostPopupHidden' parameter is present
        EXPECTED: * Parameter contains setDate-%username% parameter with valid date and time when checkbox was set
        EXPECTED: ![](index.php?/attachments/get/118618183)
        """
        pass

    def test_006__disable_allow_user_to_toggle_visibility_in_cms__odds_boost_wait_few_minutes_for_changes_to_be_applied(self):
        """
        DESCRIPTION: * Disable 'Allow User To Toggle Visibility' in CMS > Odds boost
        DESCRIPTION: * Wait few minutes for changes to be applied
        EXPECTED: 
        """
        pass

    def test_007__clean_site_local_storage_for_the_environment_devtools__application__clear_storage__clear_site_data_refresh_application_login_with_the_same_user(self):
        """
        DESCRIPTION: * Clean site local storage for the environment (DevTools > Application > Clear storage > 'Clear site data')
        DESCRIPTION: * Refresh application
        DESCRIPTION: * Login with the same user
        EXPECTED: * Initial data request to CMS returns valid data for checkbox state
        EXPECTED: * Odds Boost pop-up is displayed
        EXPECTED: * 'Don't Show Me This Again' checkbox is NOT present
        EXPECTED: * 'OX.keepOddsBoostPopupHidden' parameter is NOT present in Local storage
        """
        pass
