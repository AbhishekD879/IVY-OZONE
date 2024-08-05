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
class Test_C58446976_Verify_enabling_disabling_HR_Coral_Ladbrokes_Legends_section(Common):
    """
    TR_ID: C58446976
    NAME: Verify enabling/disabling HR 'Coral/Ladbrokes Legends' section.
    DESCRIPTION: This test case verifies feature toggle (enabling/disabling) of 'Ladbrokes Legends'/'Coral Legends' (name depends on brand) section on the Horse Racing Landing Page.
    PRECONDITIONS: 1. 'Ladbrokes Legends'/'Coral Legends' section should be turned on in CMS:
    PRECONDITIONS: CMS/Sports Pages/Sport Categories/Horse Racing/Ladbrokes/Coral Legends module
    PRECONDITIONS: 2. Virtual Horse Racing events are available in TI
    PRECONDITIONS: Request to check data: https://ss-aka-ori-dub.ladbrokes.com/openbet-ssviewer/Drilldown/2.54/EventForClass/285 (this link can be different depends on the TI you use during testing)
    PRECONDITIONS: 3. User is on Horse Racing landing page
    """
    keep_browser_open = True

    def test_001_turn_off_ladbrokes_legendscoral_legends_section_in_cms_save_the_changes_and_go_to_the_hr_landing_page(self):
        """
        DESCRIPTION: Turn off 'Ladbrokes Legends'/'Coral Legends' section in CMS, save the changes and go to the HR landing page.
        EXPECTED: 'Ladbrokes Legends'/'Coral Legends' section is not displayed.
        """
        pass

    def test_002_turn_on_ladbrokes_legendscoral_legends_section_in_cms_save_the_changes_and_go_to_the_hr_landing_page(self):
        """
        DESCRIPTION: Turn on 'Ladbrokes Legends'/'Coral Legends' section in CMS, save the changes and go to the HR landing page.
        EXPECTED: 'Ladbrokes Legends'/'Coral Legends' section is displayed.
        """
        pass

    def test_003_repeat_the_same_steps_for_uk_and_irish_races_international_tote_carousel_international_races_and_virtual_race_carousel_modules(self):
        """
        DESCRIPTION: Repeat the same steps for 'UK and Irish Races', 'International Tote Carousel', 'International Races' and 'Virtual Race Carousel' modules.
        EXPECTED: Sections are displayed/not displayed based on the CMS setup.
        """
        pass
