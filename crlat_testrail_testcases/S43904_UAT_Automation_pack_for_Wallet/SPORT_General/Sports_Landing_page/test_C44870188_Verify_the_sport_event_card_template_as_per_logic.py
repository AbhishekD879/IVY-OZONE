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
class Test_C44870188_Verify_the_sport_event_card_template_as_per_logic(Common):
    """
    TR_ID: C44870188
    NAME: Verify the sport event card template  as per logic
    DESCRIPTION: 
    PRECONDITIONS: User is logged in
    PRECONDITIONS: Verify the template for football
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_sport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on the Sports Menu Ribbon
        EXPECTED: <Sport> Landing Page is opened
        EXPECTED: 'Home Draw Away' Price Odds Template Type is shown
        """
        pass

    def test_003_tap_anywhere_on_event_section(self):
        """
        DESCRIPTION: Tap anywhere on Event section
        EXPECTED: Event Details Page is opened
        """
        pass

    def test_004_verify_below_data_for_event_in_the_edp_team_names_odds_market_name_event_eg_chelsea_v_arsenal__verify_collapseexpand_accordion_and__navigation_to_event_details_page_score_and_time_as_per_logic_below_show_score_and_time_if_available_else_show_score_and_live_if_time_is_not_available__and_event_has_started_show_live_only_if_score_and_time_is_not_available_and_event_has_started_display_watch_live_icon__if_available_verify_navigation_arrow_for_surface_bets_if_available(self):
        """
        DESCRIPTION: Verify below data for event in the EDP
        DESCRIPTION: -Team names
        DESCRIPTION: -Odds
        DESCRIPTION: -Market name
        DESCRIPTION: -Event (e.g Chelsea v Arsenal)
        DESCRIPTION: --Verify Collapse/Expand accordion and  Navigation to Event Details Page
        DESCRIPTION: -Score and time as per logic below:
        DESCRIPTION: -Show score and time if available, else
        DESCRIPTION: -Show score and Live if time is not available  and event has started
        DESCRIPTION: -Show Live only, if score and time is not available; and event has started
        DESCRIPTION: -Display 'Watch Live' Icon  if available
        DESCRIPTION: -Verify Navigation arrow for surface bets if available
        EXPECTED: All the data should be displayed correctly
        """
        pass
