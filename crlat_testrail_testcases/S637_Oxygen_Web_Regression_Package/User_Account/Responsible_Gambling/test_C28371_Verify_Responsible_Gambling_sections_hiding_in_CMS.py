import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C28371_Verify_Responsible_Gambling_sections_hiding_in_CMS(Common):
    """
    TR_ID: C28371
    NAME: Verify 'Responsible Gambling' sections hiding in CMS
    DESCRIPTION: This test case verifies hiding 'Responsible Gambling' sections in CMS to be not shown on the front-end, but still be present in CMS, so that Content Manager should not delete and create them again in case of need to hide/show them
    PRECONDITIONS: 1.  'Responsible Gambling EN' static block should be configured in CMS and set to active  (CMS_ENDPOINT/static-blocks/, where CMS_ENDPOINT can be found using devlog)
    PRECONDITIONS: 2. User is logged in
    PRECONDITIONS: 3. User is viewing 'Responsible Gambling' page (to reach it, tap Right Menu > My account > Responsible Gambling)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_verify_responsible_gamblingpage_content(self):
        """
        DESCRIPTION: Verify 'Responsible Gambling' page content
        EXPECTED: Content of 'Responsible Gambling' page corresponds to the list of CMS-configurable sections
        """
        pass

    def test_002_go_to_responsible_gambling_en_static_block_in_cms(self):
        """
        DESCRIPTION: Go to 'Responsible Gambling EN' static block in CMS
        EXPECTED: 
        """
        pass

    def test_003_go_to_html_markup_field__click_on_source_code_icon(self):
        """
        DESCRIPTION: Go to 'Html Markup' field -> Click on 'Source Code' icon
        EXPECTED: 'Source Code' overlay appears with configured sections html code
        """
        pass

    def test_004_pick_section_to_be_hidden___find_the_very_first_div_related_to_the_picked_section___enter_styledisplay_none_just_after_thevery_first_div(self):
        """
        DESCRIPTION: Pick section to be hidden -> Find the very first '<div' related to the picked section -> Enter '**style="display: none;"**' just after the very first '<div'
        EXPECTED: Entered code is shown after very first '<div' related to the section that needs to be hidden
        """
        pass

    def test_005_press_ok_button_on_source_code_overlay___press_save_button_on_responsible_gambling_page(self):
        """
        DESCRIPTION: Press 'OK' button on 'Source Code' overlay -> Press 'Save' button on 'Responsible Gambling' page
        EXPECTED: Changes are successfully saved in CMS
        """
        pass

    def test_006_navigate_to_responsible_gambling_page_on_frontend(self):
        """
        DESCRIPTION: Navigate to 'Responsible Gambling' page on frontend
        EXPECTED: 
        """
        pass

    def test_007_check_the_presence_of_verified_section_within_responsible_gambling_page(self):
        """
        DESCRIPTION: Check the presence of verified section within 'Responsible Gambling' page
        EXPECTED: Verified section is no more shown within 'Responsible Gambling' page
        """
        pass

    def test_008_go_back_to_cms___remove_added_code_from_the_source_code_of_verified_section___save_the_changes(self):
        """
        DESCRIPTION: Go back to CMS -> Remove added code from the source code of verified section -> Save the changes
        EXPECTED: Changes are successfully saved in CMS
        """
        pass

    def test_009_navigate_to_responsible_gambling_page_on_frontend(self):
        """
        DESCRIPTION: Navigate to 'Responsible Gambling' page on frontend
        EXPECTED: 
        """
        pass

    def test_010_check_the_presense_of_verified_section_within_responsible_gambling_page(self):
        """
        DESCRIPTION: Check the presense of verified section within 'Responsible Gambling' page
        EXPECTED: Verified section is shown again within 'Responsible Gambling' page
        """
        pass
