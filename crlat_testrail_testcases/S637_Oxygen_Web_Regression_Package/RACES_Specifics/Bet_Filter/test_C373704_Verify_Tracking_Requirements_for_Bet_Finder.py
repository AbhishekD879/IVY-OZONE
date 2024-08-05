import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C373704_Verify_Tracking_Requirements_for_Bet_Finder(Common):
    """
    TR_ID: C373704
    NAME: Verify Tracking Requirements for Bet Finder
    DESCRIPTION: This test case verifies Tracking Requirements for Bet Finder
    DESCRIPTION: JIRA ticket:
    DESCRIPTION: HMN-2460 Tracking Requirements for Bet Finder
    DESCRIPTION: HMN-2833 Web: Amend Bet Finder
    PRECONDITIONS: Use
    PRECONDITIONS: Connect app:
    PRECONDITIONS: https://connect-app-tst1.coral.co.uk/#/horseracing
    PRECONDITIONS: https://connect-app-tst1.coral.co.uk/#/bet-finder
    PRECONDITIONS: for testing in desktop browser
    PRECONDITIONS: Sportsbook/Coral:
    PRECONDITIONS: https://connect-invictus.coral.co.uk/#/horseracing
    PRECONDITIONS: https://connect-invictus.coral.co.uk/#/bet-finder/
    PRECONDITIONS: Extra resources:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Web+documentation
    PRECONDITIONS: Bet Finder (GA tracking)
    """
    keep_browser_open = True

    def test_001_load_httpsconnect_app_tst1coralcoukhorseracing(self):
        """
        DESCRIPTION: Load https://connect-app-tst1.coral.co.uk/#/horseracing
        EXPECTED: Horse Racing page is loaded.
        """
        pass

    def test_002_tap_bet_filter_link_on_the_breadcrumbopen_browser_console_f12___network___request_collectv___headers(self):
        """
        DESCRIPTION: Tap 'Bet Filter' link on the breadcrumb.
        DESCRIPTION: Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        EXPECTED: Check values of following parameters:
        EXPECTED: dl:https://connect-app-tst1.coral.co.uk/
        EXPECTED: dp:/bet-finder
        """
        pass

    def test_003_verify_odds_selection_select_some_odds_value1_open_browser_console_f12___network___request_collectv___headers2_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify Odds selection. Select <SOME odds VALUE>.
        DESCRIPTION: 1. Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: 2. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: 1. Check values of following parameters:
        EXPECTED: ec:bet finder
        EXPECTED: ea:odds
        EXPECTED: el:select - <SOME odds VALUE>
        EXPECTED: 2. Verify
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"odds"
        EXPECTED: eventCategory:"bet finder"
        EXPECTED: eventLabel:"select <SOME odds VALUE>" (e.g. "select - 4/1 - 15/2")
        """
        pass

    def test_004_verify_odds_de_selection_unselect_some_odds_value1_open_browser_console_f12___network___request_collectv___headers2_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify Odds DE-selection. Unselect <SOME odds VALUE>.
        DESCRIPTION: 1. Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: 2. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: 1. Check values of following parameters:
        EXPECTED: ec:bet finder
        EXPECTED: ea:odds
        EXPECTED: el:deselect - <SOME odds VALUE>
        EXPECTED: 2. Verify
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"odds"
        EXPECTED: eventCategory:"bet finder"
        EXPECTED: eventLabel:"deselect <SOME odds VALUE>" (e.g. "deselect - 4/1 - 15/2")
        """
        pass

    def test_005_verify_form_selection_select_some_form_value1_open_browser_console_f12___network___request_collectv___headers2_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify Form selection. Select <SOME form VALUE>.
        DESCRIPTION: 1. Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: 2. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: 1. Check values of following parameters:
        EXPECTED: ec:bet finder
        EXPECTED: ea:form
        EXPECTED: el:select - <SOME form VALUE>
        EXPECTED: 2. Verify
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"form"
        EXPECTED: eventCategory:"bet finder"
        EXPECTED: eventLabel:"select <SOME form VALUE>" (e.g. "select - course winner")
        """
        pass

    def test_006_verify_form_deselection_unselect_some_form_value1_open_browser_console_f12___network___request_collectv___headers2_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify Form DEselection. Unselect <SOME form VALUE>.
        DESCRIPTION: 1. Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: 2. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: 1. Check values of following parameters:
        EXPECTED: ec:bet finder
        EXPECTED: ea:form
        EXPECTED: el:deselect - <SOME form VALUE>
        EXPECTED: 2. Verify
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"form"
        EXPECTED: eventCategory:"bet finder"
        EXPECTED: eventLabel:"deselect <SOME form VALUE>" (e.g. "deselect - course winner")
        """
        pass

    def test_007_verify_going_ground_type_selection_select_going_ground_type1_open_browser_console_f12___network___request_collectv___headers2_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify Going (Ground type) selection. Select Going (Ground type).
        DESCRIPTION: 1. Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: 2. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: 1. Check values of following parameters:
        EXPECTED: ec:bet finder
        EXPECTED: ea:going (ground type)
        EXPECTED: el:select - proven
        EXPECTED: 2. Verify
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"going (ground type)"
        EXPECTED: eventCategory:"bet finder"
        EXPECTED: eventLabel:"select - proven"
        """
        pass

    def test_008_verify_going_ground_type_deselection_unselect_going_ground_type1_open_browser_console_f12___network___request_collectv___headers2_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify Going (Ground type) DEselection. Unselect Going (Ground type).
        DESCRIPTION: 1. Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: 2. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: 1. Check values of following parameters:
        EXPECTED: ec:bet finder
        EXPECTED: ea:going (ground type)
        EXPECTED: el:deselect - proven
        EXPECTED: 2. Verify
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"going (ground type)"
        EXPECTED: eventCategory:"bet finder"
        EXPECTED: eventLabel:"deselect - proven"
        """
        pass

    def test_009_verify_supercomputer_filters_tracking_on_selection_select_some_supercomputer_value1_open_browser_console_f12___network___request_collectv___headers2_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify Supercomputer filters tracking on selection. Select <SOME supercomputer VALUE>.
        DESCRIPTION: 1. Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: 2. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: 1. Check values of following parameters:
        EXPECTED: ec:bet finder
        EXPECTED: ea:supercomputer filters
        EXPECTED: el:select - <SOME supercomputer VALUE>
        EXPECTED: NOTE:
        EXPECTED: If another Supercomputer value is chosen, then we again get only SELECT. (No deselect - select)
        EXPECTED: 2. Verify
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"supercomputer filters"
        EXPECTED: eventCategory:"bet finder"
        EXPECTED: eventLabel:"select - <SOME supercomputer VALUE>"
        """
        pass

    def test_010_verify_supercomputer_filters_tracking_on_deselection_deselect_some_supercomputer_value1_open_browser_console_f12___network___request_collectv___headers2_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify Supercomputer filters tracking on Deselection. Deselect <SOME supercomputer VALUE>.
        DESCRIPTION: 1. Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: 2. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: 1. Check values of following parameters:
        EXPECTED: ec:bet finder
        EXPECTED: ea:supercomputer filters
        EXPECTED: el:deselect - <SOME supercomputer VALUE>
        EXPECTED: 2. Verify
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"supercomputer filters"
        EXPECTED: eventCategory:"bet finder"
        EXPECTED: eventLabel:"deselect - <SOME supercomputer VALUE>"
        """
        pass

    def test_011_verify_star_rating_set__stars1_open_browser_console_f12___network___request_collectv___headers2_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify Star Rating. Set <# stars>.
        DESCRIPTION: 1. Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: 2. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: 1. Check values of following parameters:
        EXPECTED: ec:bet finder
        EXPECTED: ea:star rating
        EXPECTED: el:<# starts> (e.g. 3 stars)
        EXPECTED: 2. Verify
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"star rating"
        EXPECTED: eventCategory:"bet finder"
        EXPECTED: eventLabel:"# starts"
        """
        pass

    def test_012_verify_star_rating_unsetting_unset_some_stars_rating1_open_browser_console_f12___network___request_collectv___headers2_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify Star Rating unsetting. Unset <SOME STARS RATING>.
        DESCRIPTION: 1. Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: 2. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: 1. Check values of following parameters:
        EXPECTED: ec:bet finder
        EXPECTED: ea:star rating
        EXPECTED: el:0 stars
        EXPECTED: 2. Verify
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"star rating"
        EXPECTED: eventCategory:"bet finder"
        EXPECTED: eventLabel:"0 starts"
        """
        pass

    def test_013_verify_meetings_select_some_meeting1_open_browser_console_f12___network___request_collectv___headers2_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify Meetings. Select <SOME MEETING>.
        DESCRIPTION: 1. Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: 2. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: 1. Check values of following parameters:
        EXPECTED: ec:bet finder
        EXPECTED: ea:meetings
        EXPECTED: el:<SOME MEETING>
        EXPECTED: 2. Verify
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"meeting"
        EXPECTED: eventCategory:"bet finder"
        EXPECTED: eventLabel:"<SOME MEETING>"
        """
        pass

    def test_014_verify_reset_button_tracking_tap_reset1_open_browser_console_f12___network___request_collectv___headers2_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify RESET button tracking. Tap RESET
        DESCRIPTION: 1. Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: 2. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: 1. Check values of following parameters:
        EXPECTED: ec:bet finder
        EXPECTED: ea:reset
        EXPECTED: 2. Verify
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"reset"
        EXPECTED: eventCategory:"bet finder"
        EXPECTED: eventLabel:""
        """
        pass

    def test_015_verify_find_bets_button_tracking_tap_find_bets1_open_browser_console_f12___network___request_collectv___headers2_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_but_one_object3_open_browser_console_f12___console___enter_datalayer_in_console____expand_last_object(self):
        """
        DESCRIPTION: Verify Find Bets button tracking. Tap Find Bets.
        DESCRIPTION: 1. Open browser console (F12) -> Network -> request 'collect?v' -> Headers
        DESCRIPTION: 2. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last but one Object
        DESCRIPTION: 3. Open browser console (F12) -> Console -> enter 'dataLayer' in Console --> expand last Object
        EXPECTED: 1. Two 'collect?v' requests are sent out.
        EXPECTED: a) values of following parameters:
        EXPECTED: ec:bet finder
        EXPECTED: ea:find bets
        EXPECTED: el: <#> selections found
        EXPECTED: b) Redirection to another screen
        EXPECTED: dl:https://connect-app-tst1.coral.co.uk/
        EXPECTED: dp:/bet-finder/results
        EXPECTED: 2. Verify
        EXPECTED: betFinderForm:""
        EXPECTED: betFinderGoing:""
        EXPECTED: betFinderMeetings:"All Meetings"
        EXPECTED: betFinderOdds:""
        EXPECTED: betFinderSearch:""
        EXPECTED: betFinderStarRating:"1 star"
        EXPECTED: betFinderSupercomputer:""
        EXPECTED: event:"trackEvent"
        EXPECTED: eventAction:"find bets"
        EXPECTED: eventCategory:"bet finder"
        EXPECTED: eventLabel:"# selections found"
        EXPECTED: 3. Verify
        EXPECTED: event:"content-view"
        EXPECTED: screen_name:"/bet-finder/results"
        """
        pass

    def test_016_load_httpsconnect_invictuscoralcoukhorseracingrepeat_steps_1_17_for_oxygen_connect_invictuscoralcouk(self):
        """
        DESCRIPTION: Load https://connect-invictus.coral.co.uk/#/horseracing
        DESCRIPTION: Repeat steps #1-17 for [Oxygen] Connect-invictus.coral.co.uk
        EXPECTED: Note:
        EXPECTED: * Browser Console -> Network -> request 'collect?v' -> Headers might be missing in connect-invictus, but should be present in the higher environments
        EXPECTED: * Browser Console (F12) -> Console -> enter 'dataLayer should work fine
        """
        pass

    def test_017_ensure_it_is_possible_to_differentiate_between_sportsbook_app_and_connect_app_usage(self):
        """
        DESCRIPTION: Ensure it is possible to differentiate between Sportsbook app and Connect app usage
        EXPECTED: Verify GMT is different in the collect?v requests
        EXPECTED: gtm=GTM-PRJ7P4 (connect)
        EXPECTED: gtm=GTM-KW37JJ9 (oxygen)
        """
        pass
