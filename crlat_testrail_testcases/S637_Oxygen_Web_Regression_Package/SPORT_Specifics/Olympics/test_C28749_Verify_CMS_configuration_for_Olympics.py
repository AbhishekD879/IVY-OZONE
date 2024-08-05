import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28749_Verify_CMS_configuration_for_Olympics(Common):
    """
    TR_ID: C28749
    NAME: Verify CMS configuration for Olympics
    DESCRIPTION: This Test Case verified CMS configuration for Olympics.
    DESCRIPTION: **Note:*** after BMA-55202 Configuration of Olympics will be done in Sports Categories by checkbox "isOlympic".
    PRECONDITIONS: **JIRA Ticket:**
    PRECONDITIONS: BMA-10143 Extend CMS to support Olympics
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_go_to_the_olympic_sports_sectionafter_bma_55202_go_to_sports_categories(self):
        """
        DESCRIPTION: Go to the 'Olympic Sports' section
        DESCRIPTION: after BMA-55202: Go to 'Sports Categories'
        EXPECTED: The 'Olympic Sports' section is opened
        EXPECTED: after BMA-55202: All Sports are loaded
        """
        pass

    def test_003_click_on_pluscreate_sport_button(self):
        """
        DESCRIPTION: Click on '+Create Sport' button
        EXPECTED: 'Create a new Sport' pop-up is appeared
        """
        pass

    def test_004_create_a_new_sport_pop_up_include(self):
        """
        DESCRIPTION: 'Create a new Sport' pop-up include:
        EXPECTED: -'Sport Title' field
        EXPECTED: -'Category Id' field
        EXPECTED: -'SS Category Code' field
        EXPECTED: -'Type Ids'
        EXPECTED: -'Create' button
        EXPECTED: -'cancel' button
        """
        pass

    def test_005_populate_all_fields_in_create_a_new_sport_pop_up(self):
        """
        DESCRIPTION: Populate all fields in 'Create a new Sport' pop-up
        EXPECTED: 
        """
        pass

    def test_006_click_on_create_button(self):
        """
        DESCRIPTION: Click on 'Create' button
        EXPECTED: -All changes saved
        EXPECTED: -Olympic <Sport> displayed on Oxygen (before BMA-55202)
        """
        pass

    def test_007_after_bma_55202_open_created_sportverify_checkbox_isolympictick_the_checkbox(self):
        """
        DESCRIPTION: after BMA-55202: Open created Sport.
        DESCRIPTION: Verify checkbox "isOlympic"
        DESCRIPTION: Tick the checkbox
        EXPECTED: All changes saved
        EXPECTED: Olympic <Sport> displayed on Oxygen
        """
        pass
