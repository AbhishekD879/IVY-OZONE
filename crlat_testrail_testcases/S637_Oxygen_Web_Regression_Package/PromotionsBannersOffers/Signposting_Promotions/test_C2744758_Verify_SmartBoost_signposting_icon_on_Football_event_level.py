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
class Test_C2744758_Verify_SmartBoost_signposting_icon_on_Football_event_level(Common):
    """
    TR_ID: C2744758
    NAME: Verify SmartBoost signposting icon on Football event level
    DESCRIPTION: This test case verifies "SmartBoost" Promo Icon on Football event card (event level)
    PRECONDITIONS: * 'PriceBoost' promo flag should be added to the Football Event on Event level
    PRECONDITIONS: * There has to be a Football event with Smart Boost promotion available in next places:
    PRECONDITIONS: * Homepage -> Featured tab
    PRECONDITIONS: * Homepage -> In Play tab
    PRECONDITIONS: * Homepage -> Live Stream tab
    PRECONDITIONS: * Homepage -> Coupons tab
    PRECONDITIONS: * Football -> In Play
    PRECONDITIONS: * In Play page -> All Sports (Football accordion)
    PRECONDITIONS: * In Play page -> Football
    PRECONDITIONS: * Football -> Matches
    PRECONDITIONS: * Football -> Coupons tab
    PRECONDITIONS: * Football -> Competitions tab
    PRECONDITIONS: * Favorites page
    PRECONDITIONS: * In Play widget
    PRECONDITIONS: * Live Stream widget
    PRECONDITIONS: * Favorites widget
    PRECONDITIONS: * Make sure that there are promotion created in CMS and linked to active signposting promotions (by Event Flag)
    PRECONDITIONS: **NOTE:** Information about promotions, available for the event, is received in **<drilldownTagNames>** attribute in SiteServer response for the event
    PRECONDITIONS: Parameters:
    PRECONDITIONS: * **EVFLAG_PB** - eventFlag
    PRECONDITIONS: Link to response on TST2 endpoints:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForEvent/yyyyyyy?translationLang=en
    PRECONDITIONS: WHERE
    PRECONDITIONS: x.xx is the current version of SiteServer
    PRECONDITIONS: yyyyyyy is the OpenBet event ID
    """
    keep_browser_open = True

    def test_001_navigate_to__the_event_with_smartboost_promotion_on_the_homepage(self):
        """
        DESCRIPTION: Navigate to  the event with **SmartBoost** promotion on the Homepage
        EXPECTED: * SmartBoost promo icon is shown on the event odds card
        EXPECTED: * SmartBoost icon is placed below odds buttons, on the left side of 'xx more' link
        """
        pass

    def test_002_tap_on_the_smartboost_icon(self):
        """
        DESCRIPTION: Tap on the 'SmartBoost' icon
        EXPECTED: SmartBoost Promo pop-up is displayed after tapping the icon
        """
        pass

    def test_003_repeat_steps_1_2_in_the_places_listed_in_preconditions_homepage___featured_tab_homepage___in_play_tab_homepage___live_stream_tab_homepage___coupons_tab_football___in_play_in_play_page___all_sports_football_accordion_in_play_page___football_football___matches___today_football___matches___tomorrow_football___matches___future_football___coupons_tab_football___competitions_tab_favorites_page_in_play_widget_live_stream_widget_favorites_widget(self):
        """
        DESCRIPTION: Repeat steps 1-2 in the places listed in preconditions:
        DESCRIPTION: * Homepage -> Featured tab
        DESCRIPTION: * Homepage -> In Play tab
        DESCRIPTION: * Homepage -> Live Stream tab
        DESCRIPTION: * Homepage -> Coupons tab
        DESCRIPTION: * Football -> In Play
        DESCRIPTION: * In Play page -> All Sports (Football accordion)
        DESCRIPTION: * In Play page -> Football
        DESCRIPTION: * Football -> Matches -> Today
        DESCRIPTION: * Football -> Matches -> Tomorrow
        DESCRIPTION: * Football -> Matches -> Future
        DESCRIPTION: * Football -> Coupons tab
        DESCRIPTION: * Football -> Competitions tab
        DESCRIPTION: * Favorites page
        DESCRIPTION: * In Play widget
        DESCRIPTION: * Live Stream widget
        DESCRIPTION: * Favorites widget
        EXPECTED: 
        """
        pass
