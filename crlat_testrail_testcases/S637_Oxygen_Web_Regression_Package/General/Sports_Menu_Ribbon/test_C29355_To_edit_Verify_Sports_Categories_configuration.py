import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C29355_To_edit_Verify_Sports_Categories_configuration(Common):
    """
    TR_ID: C29355
    NAME: (To edit) Verify Sports Categories configuration
    DESCRIPTION: ************************************************************************************************
    DESCRIPTION: **To edit**
    DESCRIPTION: Steps 8 and 10 - expected results should be separated for mobile/tablet and desktop versions as they are different in the context of some menus availability.
    DESCRIPTION: Steps 8 and 10 - Also this part should be updated "5. Sport landing page (next to the sport name)" as there are no icons on sports landing page anymore.
    DESCRIPTION: ************************************************************************************************
    DESCRIPTION: This test case verifies Sports Categories Section in CMS
    DESCRIPTION: **JIRA Tickets : **
    DESCRIPTION: *   BMA-5201
    DESCRIPTION: *   BMA-14604 In-Play - please use Icon Image beside sport name
    PRECONDITIONS: CMS: https://**CMS_ENDPOINT**/keystone
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_go_to_sports_pages_item(self):
        """
        DESCRIPTION: Go to 'Sports Pages' item
        EXPECTED: 
        """
        pass

    def test_003_select_sport_categories_section(self):
        """
        DESCRIPTION: Select Sport Categories section
        EXPECTED: Sport Categories section is opened
        """
        pass

    def test_004_open_any_sport_item(self):
        """
        DESCRIPTION: Open any sport item
        EXPECTED: Sport item page is opened
        """
        pass

    def test_005_verify_textfield_scoreboard_url(self):
        """
        DESCRIPTION: Verify textfield 'ScoreBoard Url'
        EXPECTED: It is possible to enter and clear text for 'ScoreBoard Url' option and save changes
        """
        pass

    def test_006_verify_filename_option(self):
        """
        DESCRIPTION: Verify 'Filename' option
        EXPECTED: *   File format for uploading is **png** only
        EXPECTED: *   Uploaded file is displayed on Native Home page
        """
        pass

    def test_007_verify_icon_option(self):
        """
        DESCRIPTION: Verify 'Icon' option
        EXPECTED: At the moment, this field is **not used at all** on Sports Categories pages
        """
        pass

    def test_008_verify_svg_option(self):
        """
        DESCRIPTION: Verify 'SVG' option
        EXPECTED: *   File format for uploading is **svg** only
        EXPECTED: *   Uploaded file is displayed on:
        EXPECTED: 1. 'A-Z sport'
        EXPECTED: 2. 'In Play' page
        EXPECTED: 3. Global Left Navigation
        EXPECTED: 4. Sport Carousel
        EXPECTED: 5. Sport landing page (next to the sport name)
        """
        pass

    def test_009_upload_an_icon_for_any_olympic_sport_eg_archery_or_athletics_or_beach_soccer(self):
        """
        DESCRIPTION: Upload an icon for any Olympic sport (e.g., Archery or Athletics or Beach soccer)
        EXPECTED: The icon is uploaded to CMS
        """
        pass

    def test_010_check_the_icon_youve_uploaded_in_step_10_in_oxygen(self):
        """
        DESCRIPTION: Check the icon you've uploaded in step #10 in Oxygen
        EXPECTED: Correct icon is displayed in the following locations:
        EXPECTED: 1. 'A-Z sport'
        EXPECTED: 2. 'In Play' page
        EXPECTED: 3. Global Left Navigation
        EXPECTED: 4. Sport Carousel
        EXPECTED: 5. Sport landing page (next to the sport name)
        """
        pass
