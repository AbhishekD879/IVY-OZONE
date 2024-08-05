import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.timeline
@vtest
class Test_C59918109_Verify_header_text_displaying_and_arrows_on_Tutorial_Splash_page(Common):
    """
    TR_ID: C59918109
    NAME: Verify header text displaying and arrows  on Tutorial/Splash page
    DESCRIPTION: This test cases verifies displaying header text based on CMS configurations
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.User is logged in
    PRECONDITIONS: 3.User haven't seen Splash page (OX.timelineTutorialOverlay is missed in the local storage)
    PRECONDITIONS: Toggles for Timeline:
    PRECONDITIONS: 4.Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox )
    PRECONDITIONS: 5.Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: 6.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: 7.Live Campaign is created
    PRECONDITIONS: 8.Toggle for Splash page is turned on (Timeline->Timeline Splash Page-> Show Splash Page : checked on)
    PRECONDITIONS: 9.All pop-ups are closed
    PRECONDITIONS: Navigate to CMS-> TimeLine->Timeline Splash Page->Splash Page Header Text
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_change_text_in_rich_text_editor__click_on_the__pfollow_all_todays_action_live_in_theppspan_stylecolor_ffff00newnbspladbrokes_loungespanp(self):
        """
        DESCRIPTION: Change text in Rich Text Editor ( click on the **'<>'** ):
        DESCRIPTION: <p>Follow all today's action live in the</p>
        DESCRIPTION: <p><span style="color: #ffff00;">NEW&nbsp;LADBROKES LOUNGE</span></p>
        EXPECTED: Text is saved
        EXPECTED: (Use editor to change color for the text or source code mode)
        """
        pass

    def test_002_navigate_to_page_where_timeline_is_configured_and_check_header_displaying(self):
        """
        DESCRIPTION: Navigate to page where timeline is configured and check header displaying
        EXPECTED: Header should show exactly what was configured on CMS including changed text color, text weight
        EXPECTED: -timeline-splash-config' attribute with configured information in CMS is received in devtools (Network -> ALL -> 'timeline-splash-config')
        """
        pass

    def test_003_navigate_to_cms__image_manager_add_new_icon_to_timeline_sprite_with_name_if_arrows_already_added_then_verify_arrows_on_uitlt_arrsvgandrefresh_both_the_brands_ui(self):
        """
        DESCRIPTION: Navigate to CMS-> Image Manager->add new icon to 'timeline' sprite with name (If arrows already added then verify arrows on UI):
        DESCRIPTION: 'tlt_arr.svg'
        DESCRIPTION: And
        DESCRIPTION: Refresh both the brands UI
        EXPECTED: Arrows should be shown on Timeline Tutorial on both brands in UI
        """
        pass
