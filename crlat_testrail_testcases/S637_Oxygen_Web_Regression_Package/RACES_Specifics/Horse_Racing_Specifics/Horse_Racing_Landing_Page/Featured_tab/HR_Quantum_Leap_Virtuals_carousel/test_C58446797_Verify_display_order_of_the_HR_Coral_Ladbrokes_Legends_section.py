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
class Test_C58446797_Verify_display_order_of_the_HR_Coral_Ladbrokes_Legends_section(Common):
    """
    TR_ID: C58446797
    NAME: Verify display order of the HR 'Coral/Ladbrokes Legends' section
    DESCRIPTION: This test case verifies display order of 'Ladbrokes Legends'/'Coral Legends' (name depends on brand) section on the Horse Racing Landing Page.
    PRECONDITIONS: 1. 'Ladbrokes Legends'/'Coral Legends' section should be turned on in CMS:
    PRECONDITIONS: CMS/Sports Pages/Sport Categories/Horse Racing/Ladbrokes/Coral Legends module
    PRECONDITIONS: 2. Display order of 'Ladbrokes Legends'/'Coral Legends' can be set in CMS by drag and drop between existing modules ('UK and Irish Races', 'International Tote Carousel', 'International Races','Virtual Race Carousel'):
    PRECONDITIONS: CMS/Sports Pages/Sport Categories/Horse Racing
    PRECONDITIONS: 3. Virtual Horse Racing events are available in TI
    PRECONDITIONS: Request to check data: https://ss-aka-ori-dub.ladbrokes.com/openbet-ssviewer/Drilldown/2.54/EventForClass/285 (this link can be different depends on the TI you use during testing)
    PRECONDITIONS: 4. User is on Horse Racing landing page
    """
    keep_browser_open = True

    def test_001_verify_display_order_of_ladbrokes_legendscoral_legends_section(self):
        """
        DESCRIPTION: Verify display order of 'Ladbrokes Legends'/'Coral Legends' section.
        EXPECTED: Display order of 'Ladbrokes Legends'/'Coral Legends' section corresponds to the order, set in Preconditions # 2.
        """
        pass

    def test_002_change_the_display_order_of_ladbrokes_legendscoral_legends_section_to_be_for_example_above_uk_and_irish_races_section_and_go_to_the_hr_landing_page(self):
        """
        DESCRIPTION: Change the display order of 'Ladbrokes Legends'/'Coral Legends' section, to be, for example, above 'UK and Irish Races' section and go to the HR landing page.
        EXPECTED: 'Ladbrokes Legends'/'Coral Legends' section is displayed above 'UK and Irish Races' section.
        """
        pass
