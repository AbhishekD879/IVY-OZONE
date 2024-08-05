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
class Test_C58446795_Verify_HR_Coral_Ladbrokes_Legends_section(Common):
    """
    TR_ID: C58446795
    NAME: Verify HR 'Coral/Ladbrokes Legends' section
    DESCRIPTION: This test case verifies displaying of 'Ladbrokes Legends'/'Coral Legends' (name depends on brand) section with its relevant races within the Horse Racing Landing Page.
    PRECONDITIONS: 1. 'Ladbrokes Legends'/'Coral Legends' section should be turned on in CMS:
    PRECONDITIONS: CMS/Sports Pages/Sport Categories/Horse Racing/Ladbrokes/Coral Legends module
    PRECONDITIONS: 2. Virtual Horse Racing events are available in TI
    PRECONDITIONS: Request to check data: https://ss-aka-ori-dub.ladbrokes.com/openbet-ssviewer/Drilldown/2.54/EventForClass/285 (this link can be different depends on the TI you use during testing)
    PRECONDITIONS: 3. User is on Horse Racing landing page
    """
    keep_browser_open = True

    def test_001_verify_the_hr_quantum_leap_virtuals_section_name(self):
        """
        DESCRIPTION: Verify the HR Quantum Leap Virtuals section name.
        EXPECTED: The HR Quantum Leap Virtuals section name is 'Ladbrokes Legends'/'Coral Legends' for Ladbrokes and Coral brands respectively.
        """
        pass

    def test_002_verify_races_within_ladbrokes_legendscoral_legends_section(self):
        """
        DESCRIPTION: Verify races within 'Ladbrokes Legends'/'Coral Legends' section.
        EXPECTED: HR Virtual races with typeFlagCodes: VR ('Virtual Racing' flag on Type level in TI) are displayed within 'Ladbrokes Legends'/'Coral Legends' section.
        EXPECTED: Races are ordered by start time by ascending.
        """
        pass

    def test_003_clicktap_on_any_hr_virtual_race_within_ladbrokes_legendscoral_legends_section(self):
        """
        DESCRIPTION: Click/Tap on any HR Virtual race within 'Ladbrokes Legends'/'Coral Legends' section.
        EXPECTED: Respective virtual EDP is opened.
        """
        pass

    def test_004_undisplay_ladbrokes_legendscoral_legends_section_data_in_ti_on_virtual_sports_categoryvirtual_hr_classtype_levelevent_level_save_the_changes_and_go_to_the_hr_landing_page(self):
        """
        DESCRIPTION: Undisplay 'Ladbrokes Legends'/'Coral Legends' section data in TI on 'Virtual Sports' category/'Virtual HR' class/Type level/Event level, save the changes and go to the HR landing page.
        EXPECTED: 'Ladbrokes Legends'/'Coral Legends' section is not displayed when there is no data to display.
        """
        pass

    def test_005_display_ladbrokes_legendscoral_legends_section_data_in_ti_on_virtual_sports_categoryvirtual_hr_classtype_levelevent_level_save_the_changes_and_to_go_the_hr_landing_page(self):
        """
        DESCRIPTION: Display 'Ladbrokes Legends'/'Coral Legends' section data in TI on 'Virtual Sports' category/'Virtual HR' class/Type level/Event level, save the changes and to go the HR landing page.
        EXPECTED: 'Ladbrokes Legends'/'Coral Legends' section is displayed with the respective virtual races.
        """
        pass
