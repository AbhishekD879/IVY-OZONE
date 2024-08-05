import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C1785201_Verify_Football_Match_time_updates_in_Extra_Time(Common):
    """
    TR_ID: C1785201
    NAME: Verify Football Match time updates in Extra Time
    DESCRIPTION: This test case verifies Football match time Extra Time updated
    DESCRIPTION: NOTE:
    DESCRIPTION: - Use https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Amelco+Systems in order to create BIP event and change match time.
    PRECONDITIONS: 1) In order to see match Extra Time time Football event should be BIP event
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: CLOCK
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: offset - match time in seconds on periodCode= 'EXTRA_TIME_FIRST_HALF/EXTRA_TIME_HALF_TIME/EXTRA_TIME_SECOND_HALF' level
    PRECONDITIONS: 3) BIP events with primary markets are configured through Amelco
    PRECONDITIONS: 4) Featured tab is configured in CMS with corresponding Football BIP event(s)
    PRECONDITIONS: 5) App is loaded & Featured tab is opened
    """
    keep_browser_open = True

    def test_001_find_bip_football_event_from_preconditions(self):
        """
        DESCRIPTION: Find BIP Football event (from Preconditions)
        EXPECTED: BIP Football event is available
        """
        pass

    def test_002__in_amelco_inplay__commentary_feed_select_first_halfsecond_half_from_the_drop_down_in_app_verify_clock_updates_for_corresponding_bip_football_event(self):
        """
        DESCRIPTION: * In Amelco (Inplay > Commentary feed): Select First Half/Second Half from the drop down
        DESCRIPTION: * In app: Verify clock updates for corresponding BIP Football event
        EXPECTED: * Time is running in real time
        EXPECTED: * Match Time corresponds to an attribute **offset **on periodCode= "FIRST_HALF/SECOND_HALF" level
        """
        pass

    def test_003__in_amelco_inplay__commentary_feed_select_extra_time_first_half_from_the_drop_down_in_app_refresh_the_page__verify_clock_updates_for_corresponding_bip_football_event(self):
        """
        DESCRIPTION: * In Amelco (Inplay > Commentary feed): Select Extra-Time First Half from the drop down
        DESCRIPTION: * In app: Refresh the page & verify clock updates for corresponding BIP Football event
        EXPECTED: * Same event with the next active and available Primary Market appears after refresh (e.g. Extra-Time Result (market template: |Extra-Time Result|)
        EXPECTED: * Time is updated according to an attribute **offset **on periodCode= "EXTRA_TIME_FIRST_HALF" level
        """
        pass

    def test_004__in_amelco_inplay_inplay__commentary_feed_select_extra_time_half_time_from_the_drop_down_in_app_verify_clock_updates_for_corresponding_bip_football_event(self):
        """
        DESCRIPTION: * In Amelco (Inplay): (Inplay > Commentary feed): Select Extra-Time Half Time from the drop down
        DESCRIPTION: * In app: Verify clock updates for corresponding BIP Football event
        EXPECTED: Time is updated according to an attribute **offset **on periodCode= "EXTRA_HALF_TIME" level
        """
        pass

    def test_005__in_amelco_inplay_inplay__commentary_feed_select_extra_time_second_half_from_the_drop_down_in_app_verify_clock_updates_for_corresponding_bip_football_event(self):
        """
        DESCRIPTION: * In Amelco (Inplay): (Inplay > Commentary feed): Select Extra-Time Second Half from the drop down
        DESCRIPTION: * In app: Verify clock updates for corresponding BIP Football event
        EXPECTED: Time is updated according to an attribute **offset **on periodCode= "EXTRA_TIME_SECOND_HALF" level
        """
        pass

    def test_006_verify_extra_time_match_time_for_a_section_in_a_collapsed_state(self):
        """
        DESCRIPTION: Verify Extra Time Match Time for a section in a collapsed state
        EXPECTED: Time is updated after expanding a section
        """
        pass

    def test_007_repeat_steps_2_7_for_home__in_play__in_play_all_sports_pages(self):
        """
        DESCRIPTION: Repeat steps 2-7 for Home > In Play & In Play All Sports pages
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2_7_for_in_play__football__football__in_play_pages(self):
        """
        DESCRIPTION: Repeat steps 2-7 for In Play > Football & Football > In Play pages
        EXPECTED: 
        """
        pass
