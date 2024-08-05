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
class Test_C884419_Verify_Double_Your_winnings_Promo_Icon_on_Football_event_level(Common):
    """
    TR_ID: C884419
    NAME: Verify "Double Your winnings" Promo Icon on Football event level
    DESCRIPTION: This test case verifies "Double Your winnings" Promo Icon on Football odds cards.
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-34455 Promo/Signposting: Pop-up: Customer no longer sees pop-ups appear as a Footer Banner] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-34455
    PRECONDITIONS: * There has to be a Football event with "Double Your winnings" promotion available in next places:
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
    PRECONDITIONS: * Make sure that there are promotion created in CMS and linked to active signposting promotions  (Event Flags)
    PRECONDITIONS: **NOTE:** Information about promotions, available for the event, is received in **<drilldownTagNames>** attribute in SiteServer response for the event
    PRECONDITIONS: Parameters:
    PRECONDITIONS: * **EVFLAG_DYW** - Double Your Winnings
    PRECONDITIONS: Link to response on TST2 endpoints:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForEvent/yyyyyyy?translationLang=en
    PRECONDITIONS: WHERE
    PRECONDITIONS: x.xx is the current version of SiteServer
    PRECONDITIONS: yyyyyyy is the OpenBet event ID
    """
    keep_browser_open = True

    def test_001_find_the_event_with_double_your_winnings_promotion_on_the_homepage(self):
        """
        DESCRIPTION: Find the event with **Double Your Winnings** promotion on the Homepage
        EXPECTED: Corresponding promo icon is shown on the event odds card (placed before 'x more>' link)
        """
        pass

    def test_002_verify_that_the_icon_is_displayed_properly_in_case_there_are_more_icons_on_the_event_odds_card_favourite_icon_live_icon_event_start_time_or_match_clock_for_football_events_watch_or_watch_live_label_for_events_with_live_stream_available(self):
        """
        DESCRIPTION: Verify that the icon is displayed properly in case there are more icons on the event odds card:
        DESCRIPTION: * 'Favourite' icon
        DESCRIPTION: * "LIVE" icon
        DESCRIPTION: * Event start time OR Match clock (for Football events)
        DESCRIPTION: * 'Watch' OR "Watch Live" label (for events with Live stream available)
        EXPECTED: Double Your Winnings icon is displayed after all listed icons in the same row (on the left of the odds card)
        """
        pass

    def test_003_tap_on_the_double_your_winnings_icon(self):
        """
        DESCRIPTION: Tap on the 'Double Your Winnings' icon
        EXPECTED: Promo pop-up is displayed after tapping the icon
        """
        pass

    def test_004_repeat_steps_1_3_in_the_places_listed_in_preconditions_homepage___featured_tab_homepage___in_play_tab_homepage___live_stream_tab_homepage___coupons_tab_football___in_play_in_play_page___all_sports_football_accordion_in_play_page___football_football___matches_football___coupons_tab_football___competitions_tab_favorites_page_in_play_widget_live_stream_widget_favorites_widget(self):
        """
        DESCRIPTION: Repeat steps 1-3 in the places listed in preconditions:
        DESCRIPTION: * Homepage -> Featured tab
        DESCRIPTION: * Homepage -> In Play tab
        DESCRIPTION: * Homepage -> Live Stream tab
        DESCRIPTION: * Homepage -> Coupons tab
        DESCRIPTION: * Football -> In Play
        DESCRIPTION: * In Play page -> All Sports (Football accordion)
        DESCRIPTION: * In Play page -> Football
        DESCRIPTION: * Football -> Matches
        DESCRIPTION: * Football -> Coupons tab
        DESCRIPTION: * Football -> Competitions tab
        DESCRIPTION: * Favorites page
        DESCRIPTION: * In Play widget
        DESCRIPTION: * Live Stream widget
        DESCRIPTION: * Favorites widget
        EXPECTED: 
        """
        pass
