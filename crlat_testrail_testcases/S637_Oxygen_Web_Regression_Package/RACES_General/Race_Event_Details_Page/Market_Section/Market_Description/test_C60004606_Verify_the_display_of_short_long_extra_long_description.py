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
class Test_C60004606_Verify_the_display_of_short_long_extra_long_description(Common):
    """
    TR_ID: C60004606
    NAME: Verify the display of short/long/extra long description
    DESCRIPTION: Verify the description text displayed under the Market header when the description texts are short,long and Extra long
    PRECONDITIONS: 1.  Horse racing & Grey Hound racing event should be available
    PRECONDITIONS: 2. User should have admin role for CMS
    PRECONDITIONS: 3: Horse racing/ Greyhounds market description table should be enabled in CMS
    """
    keep_browser_open = True

    def test_001_login_to_cms(self):
        """
        DESCRIPTION: Login to CMS
        EXPECTED: User should be logged into CMS
        """
        pass

    def test_002_navigate_to_racing_edp_template_and_edit_the_market_description_table1_add_short_description_to_one_of_the_market_template2_add_long_description_to_another_market_template3_add_extra_long_description_to_another_market_template(self):
        """
        DESCRIPTION: Navigate to Racing EDP template and edit the Market description table
        DESCRIPTION: 1: Add Short Description to one of the market template
        DESCRIPTION: 2: Add Long Description to another market template
        DESCRIPTION: 3: Add Extra Long description to another market template
        EXPECTED: User should be able to Edit and save the changes successfully
        """
        pass

    def test_003_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral /Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_004_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: User should be navigated Horse racing landing page
        """
        pass

    def test_005_click_on_any_race_which_has_the_market_templates_available_for_which_description_are_added_in_cms(self):
        """
        DESCRIPTION: Click on any race which has the Market templates available for which description are added in CMS
        EXPECTED: User should be navigated to EDP page
        """
        pass

    def test_006_validate_the_description_below_the_market_tab_for_short_long_and_extra_long_textsindexphpattachmentsget120830388indexphpattachmentsget120830389indexphpattachmentsget120830390indexphpattachmentsget120830391indexphpattachmentsget120830392(self):
        """
        DESCRIPTION: Validate the description below the Market tab for Short, Long and Extra Long texts
        DESCRIPTION: ![](index.php?/attachments/get/120830388)
        DESCRIPTION: ![](index.php?/attachments/get/120830389)
        DESCRIPTION: ![](index.php?/attachments/get/120830390)
        DESCRIPTION: ![](index.php?/attachments/get/120830391)
        DESCRIPTION: ![](index.php?/attachments/get/120830392)
        EXPECTED: User should be displayed description as per the Zeplin styles
        """
        pass

    def test_007_repeat_the_same_for_grey_hound_racing(self):
        """
        DESCRIPTION: Repeat the same for Grey Hound racing
        EXPECTED: 
        """
        pass
