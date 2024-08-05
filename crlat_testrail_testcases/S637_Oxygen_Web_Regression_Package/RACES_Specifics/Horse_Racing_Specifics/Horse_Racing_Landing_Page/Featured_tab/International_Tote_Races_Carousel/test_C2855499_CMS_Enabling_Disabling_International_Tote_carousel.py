import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2855499_CMS_Enabling_Disabling_International_Tote_carousel(Common):
    """
    TR_ID: C2855499
    NAME: [CMS] Enabling/Disabling International Tote carousel
    DESCRIPTION: This Test case verifies enabling/disabling International Tote carousel in CMS
    PRECONDITIONS: - Checkbox **Enable_ International_ Totepools** should be disabled in CMS > System configuration >International Tote Pool
    PRECONDITIONS: - **International Tote Carousel** should not be shown on the HR Landing Page within International section (below UK&IRE section)
    PRECONDITIONS: - **Tote Pool Tabs** on the Race card for the relevant races should not be shown
    """
    keep_browser_open = True

    def test_001__go_to_cms_and_navigate_to_system_configuration__enable_enable__international__totepools__checkboxenable_enable__international__totepools_on_racecard_checkboxand_save_changes_verify_checkboxes_are_updated(self):
        """
        DESCRIPTION: * Go to CMS and navigate to System configuration ->
        DESCRIPTION: **Enable** 'Enable_ International_ Totepools  checkbox
        DESCRIPTION: **Enable** 'Enable_ International_ Totepools_On_RaceCard' checkbox
        DESCRIPTION: and save changes
        DESCRIPTION: * Verify checkboxes are updated
        EXPECTED: * Changes are submitted successfully
        EXPECTED: * 'International Tote carousel' is enabled within Oxygen app
        """
        pass

    def test_002___go_to_oxygen_app_navigate_to_horse_racing_landing_page_and_scroll_down_to_international_section__verify_that_international_tote_carousel_is_displayed(self):
        """
        DESCRIPTION: - Go to Oxygen app, navigate to Horse Racing Landing Page and scroll down to International section
        DESCRIPTION: - Verify that 'International Tote carousel' is displayed.
        EXPECTED: * International Tote Carousel should be shown on the HR Landing Page
        EXPECTED: * Tote Pool Tabs on the Race card for the relevant races should be shown
        """
        pass

    def test_003__go_to_cms_and_navigate_to_system_configuration__disable_enable__international__totepools_checkboxenable_enable_international_totepools_on_racecard_checkboxand_save_changes_verify_checkboxes_are_updated(self):
        """
        DESCRIPTION: * Go to CMS and navigate to System configuration ->
        DESCRIPTION: **Disable** Enable_ International_ Totepools checkbox
        DESCRIPTION: **Enable** Enable_International_Totepools_On_RaceCard checkbox
        DESCRIPTION: and save changes
        DESCRIPTION: * Verify checkboxes are updated.
        EXPECTED: * Changes are submitted successfully
        EXPECTED: * 'International Tote carousel' is disabled within Oxygen app
        """
        pass

    def test_004___go_to_oxygen_app_and_navigate_to_horse_racing_landing_page_and_scroll_down_to_international_section__verify_that_international_tote_carousel_is_not_displayed(self):
        """
        DESCRIPTION: - Go to Oxygen app and navigate to Horse Racing Landing Page and scroll down to International section
        DESCRIPTION: - Verify that 'International Tote carousel' is not displayed.
        EXPECTED: * International Tote Carousel should NOT be shown on the HR Landing Page
        EXPECTED: * Tote Pool Tabs on the Race card for the relevant races should NOT be shown
        """
        pass
