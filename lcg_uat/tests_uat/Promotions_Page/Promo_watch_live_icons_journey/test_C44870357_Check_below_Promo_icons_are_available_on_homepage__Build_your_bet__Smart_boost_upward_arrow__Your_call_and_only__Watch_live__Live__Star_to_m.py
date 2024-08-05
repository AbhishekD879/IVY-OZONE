import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C44870357_Check_below_Promo_icons_are_available_on_homepage__Build_your_bet__Smart_boost_upward_arrow__Your_call_and_only__Watch_live__Live__Star_to_make_it_fav__Check_if_Logos_are_tappable_if_configured_(Common):
    """
    TR_ID: C44870357
    NAME: "Check below Promo icons are available on homepage - Build your bet - Smart boost upward arrow - #Your call and only # - Watch live  - Live  - Star to make it fav   Check if Logo's are tappable if configured "
    DESCRIPTION: "Check below Promo icons are available on homepage
    DESCRIPTION: - Build your bet
    DESCRIPTION: - Smart boost upward arrow
    DESCRIPTION: - #Your call and only #
    DESCRIPTION: - Watch live
    DESCRIPTION: - Live
    DESCRIPTION: - Star to make it fav
    DESCRIPTION: Check if Logo's are tappable if configured "
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_verify_the_promo_icons_are_available_on_sports_landing_pages(self):
        """
        DESCRIPTION: Verify the Promo icons are available on sports landing pages
        EXPECTED: Promo icons configured should be available on sports landing pages
        EXPECTED: Cash out
        EXPECTED: - Build your bet
        EXPECTED: - Smart boost upward arrow
        EXPECTED: - #Your call and only #
        EXPECTED: - Watch live
        EXPECTED: - Live
        """
        pass

    def test_002_verify_this_behaviour_on_multiple_sports_pages_say_football_tennis_hr__gh_racing_pages__golf(self):
        """
        DESCRIPTION: Verify this behaviour on multiple sports pages say Football, Tennis, HR / GH Racing pages , Golf
        EXPECTED: Configured promos for specific sports should be shown on respective sport/race pages
        """
        pass
