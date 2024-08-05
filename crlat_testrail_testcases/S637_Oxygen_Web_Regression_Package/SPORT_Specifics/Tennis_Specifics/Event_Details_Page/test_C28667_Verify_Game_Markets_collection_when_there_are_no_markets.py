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
class Test_C28667_Verify_Game_Markets_collection_when_there_are_no_markets(Common):
    """
    TR_ID: C28667
    NAME: Verify 'Game Markets' collection when there are no markets
    DESCRIPTION: This test case verifies 'Game Markets' collection when there are no markets.
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: BMA-5349 (Tennis Game Markets - Hide when all outcomes are suspended)
    PRECONDITIONS: Make sure that there is 'Game Markets' collection on Event Detail Page and there are a few market available
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXXXXX - event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_tennis_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Tennis' icon from the Sports Menu Ribbon
        EXPECTED: 'Tennis' landing page is opened
        """
        pass

    def test_003_tap_in_play_tab(self):
        """
        DESCRIPTION: Tap 'In-Play' tab
        EXPECTED: 'In-Play' tab is opened
        """
        pass

    def test_004_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to Event Details Page
        EXPECTED: Event Details Page is opened
        EXPECTED: 'Main Markets' collection is opened by default
        """
        pass

    def test_005_go_to_game_markets_collection(self):
        """
        DESCRIPTION: Go to 'Game Markets' collection
        EXPECTED: 'Game Markets' collection is opened
        EXPECTED: Make sure that there are no markets with all suspended outcomes
        """
        pass

    def test_006_trigger_the_following_situations_for_all_markets_within_game_markets_collectionmarketstatuscodesorfor_all_outcomes_within_particular_marketoutcomestatuscodes(self):
        """
        DESCRIPTION: Trigger the following situations for all markets within 'Game Markets' collection
        DESCRIPTION: **marketStatusCode="S" **
        DESCRIPTION: or
        DESCRIPTION: for all outcomes within particular market
        DESCRIPTION: **outcomeStatusCode="S"**
        EXPECTED: All markets/outcomes become suspended
        EXPECTED: Verified markets are shown only 3 seconds and then disappears from 'Game Markets' collection
        """
        pass

    def test_007_verify_game_markets_section(self):
        """
        DESCRIPTION: Verify 'Game Markets' section
        EXPECTED: 'Game Markets' section is hidden from user
        EXPECTED: User is redirected to  'Main Markets' collection
        """
        pass

    def test_008_tap_in_play_icon_on_the_sports_menu_ribbon___go_to_tennis_section_and_repeat_steps_4_7(self):
        """
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon -> go to 'Tennis' section and repeat steps №4-7
        EXPECTED: 
        """
        pass

    def test_009_tap_in_play_tab_on_the_module_selector_ribbon___go_to_tennis_section_and_repeat_steps_4_7(self):
        """
        DESCRIPTION: Tap 'In-Play' tab on the Module Selector Ribbon -> go to 'Tennis' section and repeat steps №4-7
        EXPECTED: 
        """
        pass

    def test_010_tap_in_play_on_the_sport_menu_ribbon___tap_tennis_icon_and_repeat_steps_4_7(self):
        """
        DESCRIPTION: Tap 'In-Play' on the Sport Menu Ribbon -> tap 'Tennis' icon and repeat steps №4-7
        EXPECTED: 
        """
        pass

    def test_011_tap_live_stream_icon_fromsportmenu_ribbon__go_to_tennis_section_and_repeat_steps_4_7(self):
        """
        DESCRIPTION: Tap 'Live Stream' icon from Sport Menu Ribbon-> go to 'Tennis' section and repeat steps №4-7
        EXPECTED: 
        """
        pass

    def test_012_tap_live_stream_on_the_module_selector_ribbon_go_to_tennis_section_and_repeat_steps4_7(self):
        """
        DESCRIPTION: Tap 'Live Stream' on the Module Selector Ribbon->go to 'Tennis' section and repeat steps №4-7
        EXPECTED: 
        """
        pass

    def test_013_go_to_featured_tab___find_bip_tennis_event_and_repeat_steps4_7(self):
        """
        DESCRIPTION: Go to Featured tab -> find BIP Tennis event and repeat steps №4-7
        EXPECTED: 
        """
        pass
