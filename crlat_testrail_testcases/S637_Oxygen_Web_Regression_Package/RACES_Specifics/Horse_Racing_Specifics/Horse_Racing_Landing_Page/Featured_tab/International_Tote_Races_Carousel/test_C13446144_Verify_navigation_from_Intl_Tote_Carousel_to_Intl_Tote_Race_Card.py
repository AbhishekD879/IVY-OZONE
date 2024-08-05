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
class Test_C13446144_Verify_navigation_from_Intl_Tote_Carousel_to_Intl_Tote_Race_Card(Common):
    """
    TR_ID: C13446144
    NAME: Verify navigation from Intl Tote Carousel to Intl Tote Race Card
    DESCRIPTION: This test case verifies navigation from Intl Tote Carousel to Intl Tote Race Card
    PRECONDITIONS: Preconditions:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: Regular Horse Racing event is linked to the International Tote event
    PRECONDITIONS: -  -  -  -
    PRECONDITIONS: * Checkbox Enable_ International_ Totepools is __disabled__
    PRECONDITIONS: * Checkbox Enable_International_Totepools_On_RaceCard is __disabled__
    PRECONDITIONS: * International Tote Carousel should not be shown on the Horse Races Landing Page within International section (below UK&IRE section)
    PRECONDITIONS: * Tote Pool Tabs on the Race card for the relevant races should not be shown
    PRECONDITIONS: * Int Tote is placed
    """
    keep_browser_open = True

    def test_001_navigate_to_hr_lp(self):
        """
        DESCRIPTION: Navigate to HR LP
        EXPECTED: * Tote Carousel is NOT displayed On LP
        EXPECTED: * Redirect from the Landing page to Tote Tab in Race card is impossible
        EXPECTED: * Tote Tab in Race card is NOT displayed
        """
        pass

    def test_002_verify_navigation_from_bet_history_through_international_tote_bet_from_preconditions(self):
        """
        DESCRIPTION: Verify navigation from Bet history through International Tote bet from preconditions
        EXPECTED: User is navigated to the International Tote page of respective Meeting
        """
        pass

    def test_003__go_to_cms_and_navigate_to_system_configurationenable_enable__international__totepools_checkboxdisable_enable_international_totepools_on_racecard_checkboxand_save_changes_verify_checkboxes_are_updated(self):
        """
        DESCRIPTION: * Go to CMS and navigate to System configuration:
        DESCRIPTION: **Enable** Enable_ International_ Totepools checkbox
        DESCRIPTION: **Disable** Enable_International_Totepools_On_RaceCard checkbox
        DESCRIPTION: and save changes
        DESCRIPTION: * Verify checkboxes are updated.
        EXPECTED: * Changes are submitted successfully
        EXPECTED: * 'International Tote carousel' is enabled within Oxygen app
        """
        pass

    def test_004__navigate_to_hr_lp_tap_any_int_tote_active_event_from_the_carousel(self):
        """
        DESCRIPTION: * Navigate to HR LP
        DESCRIPTION: * Tap any Int Tote active event from the carousel
        EXPECTED: * Tote Carousel is displayed On LP
        EXPECTED: * Tote Tab in Race card is NOT displayed
        EXPECTED: * User is navigated to the International Tote page of respective Meeting
        """
        pass

    def test_005_repeat_step_2(self):
        """
        DESCRIPTION: Repeat Step 2
        EXPECTED: 
        """
        pass

    def test_006__go_to_cms_and_navigate_to_system_configurationenable_enable__international__totepools_checkboxenable_enable_international_totepools_on_racecard_checkboxand_save_changes_verify_checkboxes_are_updated(self):
        """
        DESCRIPTION: * Go to CMS and navigate to System configuration:
        DESCRIPTION: **Enable** Enable_ International_ Totepools checkbox
        DESCRIPTION: **Enable** Enable_International_Totepools_On_RaceCard checkbox
        DESCRIPTION: and save changes
        DESCRIPTION: * Verify checkboxes are updated.
        EXPECTED: * Changes are submitted successfully
        EXPECTED: * 'International Tote carousel' is enabled within Oxygen app
        """
        pass

    def test_007__navigate_to_hr_lp_tap_any_int_tote_active_event_from_the_carousel(self):
        """
        DESCRIPTION: * Navigate to HR LP
        DESCRIPTION: * Tap any Int Tote active event from the carousel
        EXPECTED: * Tote Carousel is displayed On LP
        EXPECTED: * User is navigated to the Race card of respective Meeting
        EXPECTED: * 'Tote Pool' Tab should be selected
        EXPECTED: * First default pool should be selected and content is loaded
        """
        pass

    def test_008_repeat_step_2(self):
        """
        DESCRIPTION: Repeat Step 2
        EXPECTED: User is redirected to the Race card page, correspondent event, Tote tab
        """
        pass

    def test_009__go_to_cms_and_navigate_to_system_configurationdisable_enable__international__totepools_checkboxenable_enable_international_totepools_on_racecard_checkboxand_save_changes_verify_checkboxes_are_updated(self):
        """
        DESCRIPTION: * Go to CMS and navigate to System configuration:
        DESCRIPTION: **Disable** Enable_ International_ Totepools checkbox
        DESCRIPTION: **Enable** Enable_International_Totepools_On_RaceCard checkbox
        DESCRIPTION: and save changes
        DESCRIPTION: * Verify checkboxes are updated.
        EXPECTED: * Changes are submitted successfully
        EXPECTED: * 'International Tote carousel' is disabled within Oxygen app
        """
        pass

    def test_010_navigate_to_hr_lp(self):
        """
        DESCRIPTION: Navigate to HR LP
        EXPECTED: * Tote Carousel is NOT displayed On LP
        EXPECTED: * Redirect from the Landing page to Tote Tab in Race card is impossible
        EXPECTED: * Tote Tab in Race card is NOT displayed
        """
        pass

    def test_011_repeat_step_2(self):
        """
        DESCRIPTION: Repeat Step 2
        EXPECTED: User is navigated to the International Tote page of respective Meeting
        """
        pass
