import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C28366_Verify_Responsible_Gambling_page(Common):
    """
    TR_ID: C28366
    NAME: Verify 'Responsible Gambling' page
    DESCRIPTION: This test case verifies the 'Responsible Gambling' page layout
    PRECONDITIONS: 1. 'Responsible Gambling EN' static block should be configured in CMS and set to active (CMS_ENDPOINT/static-blocks/, where CMS_ENDPOINT can be found using devlog)
    PRECONDITIONS: 2. User is logged in
    PRECONDITIONS: 3. User is viewing 'Responsible Gambling' page (to reach it, tap Right Menu > My account > Responsible Gambling)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_verify_responsible_gamblingpage_layout(self):
        """
        DESCRIPTION: Verify 'Responsible Gambling' page layout
        EXPECTED: 'Responsible Gambling' page is opened with 'Responsible Gambling' header and 'Back' button
        """
        pass

    def test_002_tapclick_on_back_button(self):
        """
        DESCRIPTION: Tap/click on 'Back' button
        EXPECTED: User is redirected to previously visited page
        """
        pass

    def test_003_verify_buttons_links_sections_and_text_on_responsible_gambling_page(self):
        """
        DESCRIPTION: Verify buttons, links, sections and text on 'Responsible Gambling' page
        EXPECTED: Buttons, links, sections and text correspond to configured in CMS and workable
        """
        pass
