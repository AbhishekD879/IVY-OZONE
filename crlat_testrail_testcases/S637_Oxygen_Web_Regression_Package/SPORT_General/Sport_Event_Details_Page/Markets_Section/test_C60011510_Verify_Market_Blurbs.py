import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60011510_Verify_Market_Blurbs(Common):
    """
    TR_ID: C60011510
    NAME: Verify Market Blurbs
    DESCRIPTION: Verify that Market blurbs are displayed as additional middle layer directly underneath the Market Title Header in all Market Collections for both In Play and Pre-Play Sports Event Details Page (EDP)
    DESCRIPTION: Verify that Market blurb is displayed only when configured in open bet
    PRECONDITIONS: 1: Blurb should be configured in Open Bet Market section
    PRECONDITIONS: ![](index.php?/attachments/get/120927837)
    PRECONDITIONS: 2: Events should be available
    """
    keep_browser_open = True

    def test_001_launch_coral_ladbrokes_urlfor_mobile_app_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral/ Ladbrokes URL
        DESCRIPTION: For Mobile App: Launch the app
        EXPECTED: URL should be launched
        """
        pass

    def test_002_navigate_to_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing Page
        EXPECTED: User should be navigated to <Sport> Landing Page
        """
        pass

    def test_003_clicktap_on_event_name_or_more_link_on_the_event_sectionevent_which_has_market_with_blurb_configured_in_openbet(self):
        """
        DESCRIPTION: Click/Tap on Event name or 'More' link on the event section
        DESCRIPTION: (Event which has Market with blurb configured in Openbet)
        EXPECTED: User should be navigated to <Sport> Event Details page
        """
        pass

    def test_004_validate_the_market_for_which_blurb_is_configured_in_open_betindexphpattachmentsget120927839indexphpattachmentsget120927840(self):
        """
        DESCRIPTION: Validate the Market for which blurb is configured in Open Bet
        DESCRIPTION: ![](index.php?/attachments/get/120927839)
        DESCRIPTION: ![](index.php?/attachments/get/120927840)
        EXPECTED: 1: User should be able to see the Market Header
        EXPECTED: 2: User should be able to see the blurb text as an additional middle layer underneath the market header
        EXPECTED: 3: Text which is configured in OB inside the Blurb section should be displayed
        EXPECTED: 4: Zeplin design styles should be maintained
        """
        pass

    def test_005_validate_the_market_for_which_blurb_is_not_configured_in_open_bet(self):
        """
        DESCRIPTION: Validate the market for which blurb is not configured in Open bet
        EXPECTED: 1:User should be able to see the Market Header
        EXPECTED: 2: No additional middle layer should be displayed when there are no blurbs configured for the market in Open bet
        """
        pass

    def test_006_validate_for_both__pre_play_and_in_play_events(self):
        """
        DESCRIPTION: Validate for both  Pre-play and In-play events
        EXPECTED: 
        """
        pass
