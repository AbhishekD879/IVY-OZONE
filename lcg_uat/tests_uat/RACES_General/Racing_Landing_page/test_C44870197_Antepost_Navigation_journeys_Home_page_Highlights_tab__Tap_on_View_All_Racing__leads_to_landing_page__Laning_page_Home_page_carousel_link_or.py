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
class Test_C44870197_Antepost_Navigation_journeys_Home_page_Highlights_tab__Tap_on_View_All_Racing__leads_to_landing_page__Laning_page_Home_page_carousel_link_or_Tab_bar__App_Sports_Menu_Tap_on_HR_GH_leads_to_landing_page_and_next_user_taps_on_Special(Common):
    """
    TR_ID: C44870197
    NAME: Antepost : "Navigation journeys: Home page, Highlights tab -> Tap on ""View All Racing "" - leads to landing page - Laning page Home page, carousel link or Tab bar - App Sports (Menu): Tap on HR/GH leads to landing page and next, user taps on Special
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_hr__verify_the_contents_of_featured_tab(self):
        """
        DESCRIPTION: HR:  Verify the contents of FEATURED TAB
        EXPECTED: User should be view all Racing Events with Event Places and Timings.
        EXPECTED: -Enhanced Races
        EXPECTED: -Next Races
        EXPECTED: -UK & IRE/THURSDAY FRIDAY SATURDAY (These races are shown for three days)
        EXPECTED: -INTERNATIONAL
        EXPECTED: -TOTE EVENTS
        EXPECTED: -OTHER INTERNATIONAL
        EXPECTED: -VIRTUALS
        """
        pass

    def test_002_hr_verify_the_contents_of_future_tab(self):
        """
        DESCRIPTION: HR: Verify the contents of FUTURE TAB
        EXPECTED: User should be able to see different tabs and contents in it.
        EXPECTED: -FLAT     NATIONAL HUNT    INTERNATIONAL
        """
        pass

    def test_003_hr_verify_the_contents_of_specials_tab(self):
        """
        DESCRIPTION: HR: Verify the contents of SPECIALS TAB
        EXPECTED: User should be able to see
        EXPECTED: RACING SPECIALS (Expandable/Collapsible)
        EXPECTED: YOURCALL SPECIALS (Expandable/Collapsible)
        """
        pass

    def test_004_hr_verify_yourcall_tab(self):
        """
        DESCRIPTION: HR: Verify YOURCALL TAB
        EXPECTED: User should be able to see
        EXPECTED: TWEET NOW
        EXPECTED: YOURCALL SPECIALS etc
        """
        pass

    def test_005_gh__verify_the_contents_today_tomorrow_future(self):
        """
        DESCRIPTION: GH:  Verify the contents TODAY TOMORROW FUTURE
        EXPECTED: User should be able to see
        EXPECTED: BY MEETING  BY TIME
        EXPECTED: UK & IRE
        EXPECTED: TRAP CHALLENGES
        EXPECTED: WINNING DISTANCES
        """
        pass
