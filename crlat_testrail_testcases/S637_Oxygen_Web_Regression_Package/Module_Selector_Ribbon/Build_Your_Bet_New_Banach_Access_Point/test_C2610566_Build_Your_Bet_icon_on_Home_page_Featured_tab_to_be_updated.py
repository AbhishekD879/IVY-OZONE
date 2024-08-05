import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C2610566_Build_Your_Bet_icon_on_Home_page_Featured_tab_to_be_updated(Common):
    """
    TR_ID: C2610566
    NAME: 'Build Your Bet' icon on Home page: Featured tab (to be updated)
    DESCRIPTION: This test case verifies displaying of Build Your Bet (BYB) on the homepage within mobile, tablet
    PRECONDITIONS: CMS configuration:
    PRECONDITIONS: Build Your Bet tab is available on homepage:
    PRECONDITIONS: 1)BYB is enabled in CMS
    PRECONDITIONS: mobile/tablet/desktop
    PRECONDITIONS: Module Ribbon Tab -> 'Build Your Bet'; 'Visible' = True;
    PRECONDITIONS: Leagues is available when:
    PRECONDITIONS: 1) Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: 2) Banach league is mapped on Banach side
    PRECONDITIONS: 3) User is on Home page
    """
    keep_browser_open = True

    def test_001_on_home_page_featured_tab_verify_accordions_of_events_with_build_your_bet_signposting_feature_available(self):
        """
        DESCRIPTION: On Home page: Featured tab verify accordions of events with Build Your Bet signposting feature available
        EXPECTED: * Accordions have '#' (Yourcall) icon in the header (if available)
        EXPECTED: * There is NO 'BuildYourBet' icon in the header of the event card
        """
        pass

    def test_002_verify_events_card_view(self):
        """
        DESCRIPTION: Verify events card view
        EXPECTED: 'BuildYourBet' icon is present on event card footer (blue letters with yellow background)
        """
        pass

    def test_003_verify_the_icon_placement_on_the_event_card(self):
        """
        DESCRIPTION: Verify the icon placement on the event card
        EXPECTED: The 'BuildYourBet' icon in placed before 'N more' link on the right bottom corner
        """
        pass

    def test_004_verify_the_icon_size_when_other_signposting_icons_are_present_on_event_card(self):
        """
        DESCRIPTION: Verify the icon size when other signposting icons are present on event card
        EXPECTED: The 'BuildYourBet' icon is displayed in its small size (just '+B 'icon is displayed)
        """
        pass
