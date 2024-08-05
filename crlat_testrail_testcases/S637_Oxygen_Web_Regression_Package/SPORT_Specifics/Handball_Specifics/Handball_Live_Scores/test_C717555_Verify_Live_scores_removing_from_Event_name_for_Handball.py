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
class Test_C717555_Verify_Live_scores_removing_from_Event_name_for_Handball(Common):
    """
    TR_ID: C717555
    NAME: Verify Live scores removing from Event name for Handball
    DESCRIPTION: This test case verifies BIP scores in Event Name are replaced to ''v'' for Handball events on Front End
    PRECONDITIONS: 1. In order to get events with Scorers use the link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. EN, Ukr)
    PRECONDITIONS: 2. OB tool: https://confluence.egalacoral.com/display/MOB/Open+Bet+Systems
    PRECONDITIONS: 3. Go to OB and create Handball live event with name:
    PRECONDITIONS: |Team A Name| ScoreA-ScoreB |Team B Name|
    PRECONDITIONS: (e.g. |Saint Raphael| 25-18 |Selestat|(BG)|
    """
    keep_browser_open = True

    def test_001_heck_event_name_displaying_on_page_in_play_pagetabwidget__all_sports_filter_and_handball_sports_filter(self):
        """
        DESCRIPTION: Сheck event name displaying on page:
        DESCRIPTION: * In Play page/tab/widget ( all sports filter and handball sports filter)
        EXPECTED: Event name should be:
        EXPECTED: Saint Raphael v Selestat (BG)
        EXPECTED: ''25-18'' should be replaced on ''v''
        """
        pass

    def test_002__live_stream_pagewidget__if_live_stream_is_available_for_event(self):
        """
        DESCRIPTION: * Live Stream page/widget ( if live stream is available for event)
        EXPECTED: Event name should be:
        EXPECTED: Saint Raphael v Selestat (BG)
        EXPECTED: ''25-18'' should be replaced on ''v''
        """
        pass

    def test_003__betslip_sliderwidget_adding_via_deep_link_too(self):
        """
        DESCRIPTION: * Betslip slider/widget (adding via deep link too)
        EXPECTED: Event name should be:
        EXPECTED: Saint Raphael v Selestat (BG)
        EXPECTED: ''25-18'' should be replaced on ''v''
        """
        pass

    def test_004__cash_out(self):
        """
        DESCRIPTION: * Cash Out
        EXPECTED: Event name should be:
        EXPECTED: Saint Raphael v Selestat (BG)
        EXPECTED: ''25-18'' should be replaced on ''v''
        """
        pass

    def test_005__bet_historyopen_bets(self):
        """
        DESCRIPTION: * Bet History/Open bets
        EXPECTED: Event name should be:
        EXPECTED: Saint Raphael v Selestat (BG)
        EXPECTED: ''25-18'' should be replaced on ''v''
        """
        pass

    def test_006__featured__created_by_type_id(self):
        """
        DESCRIPTION: * Featured ( created by type id)
        EXPECTED: Event name should be:
        EXPECTED: Saint Raphael v Selestat (BG)
        EXPECTED: ''25-18'' should be replaced on ''v''
        """
        pass
