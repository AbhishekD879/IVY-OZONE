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
class Test_C29345_TO_BE_UPDATEDVerify_Sport_Header_Template_Configuration(Common):
    """
    TR_ID: C29345
    NAME: [TO BE UPDATED]Verify <Sport> Header Template Configuration
    DESCRIPTION: This test case verifies <Sport> header template configuration in CMS
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   BMA-10958 Odds Card Refactoring
    DESCRIPTION: **Note:** after BMA-55202 Configuration of Olympics will be done in Sports Categories by checkbox "isOlympic".
    PRECONDITIONS: CMS: https://**CMS_ENDPOINT**/keystone
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: Make sure there is Featured tab module available with <Sport> events
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_go_to_olympic_sport_and_choose_some_sportnoteolympic_sport_will_be_transformed_into_sport_soonafter_bma_55202_go_to_sports_categories_and_choose_sport_with_checkbox_isolympicenabled(self):
        """
        DESCRIPTION: Go to Olympic Sport and choose some <Sport>
        DESCRIPTION: NOTE: Olympic Sport will be transformed into Sport soon
        DESCRIPTION: after BMA-55202: Go to 'Sports Categories' and choose sport with checkbox "isOlympic"enabled
        EXPECTED: <Sport> section is opened
        """
        pass

    def test_003_choose_home_draw_away_type_from_template_type_section_and_save_change(self):
        """
        DESCRIPTION: Choose 'Home Draw Away' type from Template type section and save change
        EXPECTED: Change is saved successfully
        """
        pass

    def test_004_load_oxygen_app_and_go_to_sport_landing_page(self):
        """
        DESCRIPTION: Load Oxygen app and go to <Sport> landing page
        EXPECTED: <Sport> landing page is opened
        """
        pass

    def test_005_verify_odds_dispaying(self):
        """
        DESCRIPTION: Verify odds dispaying
        EXPECTED: Odds are displayed grouped into 'Home', 'Draw', 'Away' colums
        """
        pass

    def test_006_go_to_in_play_page___sport_sectionand_repeat_step_5(self):
        """
        DESCRIPTION: Go to 'In Play' page -> <Sport> section and repeat step №5
        EXPECTED: 
        """
        pass

    def test_007_go_to_featured_tab_and_repeat_step_5(self):
        """
        DESCRIPTION: Go to Featured tab and repeat step №5
        EXPECTED: 
        """
        pass

    def test_008_go_back_to_sport_section_in_cms(self):
        """
        DESCRIPTION: Go back to <Sport> section in CMS
        EXPECTED: <Sport> section is opened
        """
        pass

    def test_009_choose_one_two_type_from_template_type_section_and_save_change(self):
        """
        DESCRIPTION: Choose 'One Two' type from Template type section and save change
        EXPECTED: Change is saved successfully
        """
        pass

    def test_010_load_oxygen_app_and_go_to_sport_landing_page(self):
        """
        DESCRIPTION: Load Oxygen app and go to <Sport> landing page
        EXPECTED: <Sport> landing page is opened
        """
        pass

    def test_011_verify_odds_dispaying(self):
        """
        DESCRIPTION: Verify odds dispaying
        EXPECTED: *   Odds are displayed grouped into '1' , '2' colums
        EXPECTED: *   'Draw' outcomes are NOT displayed
        """
        pass

    def test_012_go_to_in_play_page___sport_sectionand_repeat_step_11(self):
        """
        DESCRIPTION: Go to 'In Play' page -> <Sport> section and repeat step №11
        EXPECTED: 
        """
        pass

    def test_013_go_to_featured_tab_and_repeat_step_11(self):
        """
        DESCRIPTION: Go to Featured tab and repeat step №11
        EXPECTED: 
        """
        pass

    def test_014_go_back_to_sport_section_in_cms(self):
        """
        DESCRIPTION: Go back to <Sport> section in CMS
        EXPECTED: <Sport> section is opened
        """
        pass

    def test_015_check_is_multi_template_sport_checkbox_and_save_change(self):
        """
        DESCRIPTION: Check 'Is Multi Template Sport' checkbox and save change
        EXPECTED: Change is saved successfully
        """
        pass

    def test_016_load_oxygen_app_and_go_to_sport_landing_page(self):
        """
        DESCRIPTION: Load Oxygen app and go to <Sport> landing page
        EXPECTED: <Sport> landing page is opened
        """
        pass

    def test_017_verify_odds_dispaying(self):
        """
        DESCRIPTION: Verify odds dispaying
        EXPECTED: Odds are displayed according to quantity of outcomes recieved from SS on main market level
        """
        pass
