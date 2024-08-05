import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C58595722_Verify_restrictions_and_their_lifting_for_inactive_users_which_try_to_view_a_stream_end_to_end(Common):
    """
    TR_ID: C58595722
    NAME: Verify restrictions and their lifting for inactive users which try to view a stream (end-to-end)
    DESCRIPTION: This test case verifies change in validation behaviour in accordance to appropriate front-end changes, when new users try to view a stream, before and after they make their first deposit.
    DESCRIPTION: Applies to <Race> events
    PRECONDITIONS: Mapping guide for test environments:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    PRECONDITIONS: In order to run this case, 2 events should be configured within the TI with following settings taken into account:
    PRECONDITIONS: SiteServer event should be configured to support Perform streaming (**'typeFlagCodes'**='PVA' or 'RVA', AND, **'drilldownTagNames'**='EVFLAG_PVM' or 'EVFLAG_RVA' flags should be set) and should be mapped to Perform stream events #1 and #2
    PRECONDITIONS: Event #1 should have the following attributes:
    PRECONDITIONS: isStarted = "false" (5 minutes or more should be left till the event start)
    PRECONDITIONS: isMarketBetInRun = "true"
    PRECONDITIONS: Ukraine should be whitelisted by Perform
    PRECONDITIONS: Event #2 should have the following attributes:
    PRECONDITIONS: isStarted = "false" (20 minutes or more should be left till the event start)
    PRECONDITIONS: isMarketBetInRun = "true"
    PRECONDITIONS: Ukraine should be whitelisted by Perform
    PRECONDITIONS: **(!)** SPORT RULES should be applied to a mapped through TI event for **Ladbrokes** brand.
    PRECONDITIONS: ![](index.php?/attachments/get/103507411)
    PRECONDITIONS: Perform iFrame is disabled in CMS:
    PRECONDITIONS: -> System configuration -> Structure -> performGroup -> CSBIframeEnabled (false/unchecked)
    PRECONDITIONS: -> System configuration -> Structure -> performGroup -> CSBIframeSportIds (false/unchecked)
    PRECONDITIONS: A fresh(new -> without credit card and previous bet placement) user is registered within Oxygen app.
    PRECONDITIONS: User is logged into the Oxygen app.
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_racing_event_1_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of <Racing> event #1 which satisfies Preconditions
        EXPECTED: Event details page is opened
        EXPECTED: **Coral:**
        EXPECTED: * Desktop:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050952) button is shown below the event name line
        EXPECTED: * Mobile or Tablet Responsive:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050954) button is shown when scoreboard is absent.
        EXPECTED: **Ladbrokes:**
        EXPECTED: * Desktop:
        EXPECTED: 'Watch' ![](index.php?/attachments/get/3050953) (Ladbrokes) button is shown below the event name line
        EXPECTED: * Mobile or Tablet Responsive:
        EXPECTED: 'Watch' ![](index.php?/attachments/get/3050955) (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_002_mobile_or_tablet_responsivedesktoptapclick_on_watchlive_stream_button(self):
        """
        DESCRIPTION: **Mobile** or Tablet Responsive/Desktop**
        DESCRIPTION: Tap/click on 'Watch'/'Live Stream' button
        EXPECTED: **Coral:**
        EXPECTED: [Mobile/Tablet Responsive & Desktop view]
        EXPECTED: Warning message (popup for mobile) is shown with a following text : "This stream has not yet started. Please try again soon".
        EXPECTED: **Ladbrokes:**
        EXPECTED: [Mobile or Tablet Responsive]
        EXPECTED: Pop up opens with message "This stream has not yet started. Please try again soon".
        EXPECTED: Timer countdown is shown below the text.
        EXPECTED: There is an ability to close pop-up with a 'OK' button
        EXPECTED: ![](index.php?/attachments/get/101002537)
        EXPECTED: [Desktop]
        EXPECTED: Warning message is shown with a following text : "This stream has not yet started. Please try again soon".
        EXPECTED: ![](index.php?/attachments/get/101002538)
        EXPECTED: ===
        EXPECTED: **User is not able to watch the stream.**
        """
        pass

    def test_003_wait_till_2_or_less_minutes_left_before_event_start_time_and_repeat_step_2(self):
        """
        DESCRIPTION: Wait till 2 or less minutes left before event Start Time and repeat step '2'
        EXPECTED: [Mobile/Tablet Responsive & Desktop view]
        EXPECTED: **Coral:**
        EXPECTED: Warning message (popup for mobile)is shown with a following text : "In order to watch the race you must have a funded account or have placed a bet in the last 24 hours"
        EXPECTED: **Ladbrokes:**
        EXPECTED: [Mobile or Tablet Responsive]
        EXPECTED: Pop-up is shown with a following text "In order to watch the race you must have a funded account or have placed a bet in the last 24 hours"
        EXPECTED: Timer countdown is shown below the text.
        EXPECTED: There is an ability to close pop-up with a 'No, Thanks' button
        EXPECTED: ![](index.php?/attachments/get/100978322)
        EXPECTED: [Desktop]
        EXPECTED: Warning message is shown with a following text : "In order to watch the race you must have a funded account or have placed a bet in the last 24 hours"
        EXPECTED: ![](index.php?/attachments/get/100978327)
        EXPECTED: ===
        EXPECTED: **User is not able to watch the stream.**
        """
        pass

    def test_004_wait_for_the_event_start_time_to_comeevent_to_become_live_refresh_the_page_and_repeat_step_2(self):
        """
        DESCRIPTION: Wait for the event start time to come(event to become live), refresh the page and repeat step '2'
        EXPECTED: Expected results match ER of step **2**
        EXPECTED: * Request to OptIn MS is sent to indentify stream provider
        EXPECTED: * The next code/response info is received from Optin MS:
        EXPECTED: {
        EXPECTED: "code": 1405,
        EXPECTED: "description": "Error on passing qualification",
        EXPECTED: "details": {
        EXPECTED: "failureCode": "4105",
        EXPECTED: "failureKey": "account.videoNoBetPlaced",
        EXPECTED: "failureReason": "Bet not placed in the level of the hierarchy",
        EXPECTED: "failureDebug": "account.videoNoBetPlaced Customer is not qualified. Customer needs to Play an 1P bet or make deposit"
        EXPECTED: }
        EXPECTED: }
        """
        pass

    def test_005_in_oxygen_app_add_a_new_credit_card_to_your_user_account_and_make_a_first_deposit_through_itwithout_bet_placementcoral_user_menu___banking___depositladbrokes_user_menu___depositor_banking___deposit(self):
        """
        DESCRIPTION: In Oxygen app, add a new credit card to your user account and make a first deposit through it(without bet placement).
        DESCRIPTION: **Coral:** User Menu -> Banking -> Deposit
        DESCRIPTION: **Ladbrokes:** User Menu -> 'Deposit'(or 'Banking' -> 'Deposit')
        EXPECTED: User Balance is successfully updated and is not 0
        """
        pass

    def test_006_open_event_details_page_of_racing_event_2_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of <Racing> event #2 which satisfies Preconditions
        EXPECTED: Expected results match ER of step **1**
        """
        pass

    def test_007_wait_till_2_or_less_minutes_left_before_event_start_time_and_repeat_step_2(self):
        """
        DESCRIPTION: Wait till 2 or less minutes left before event Start Time and repeat step '2'
        EXPECTED: Stream is launched
        EXPECTED: Request to OptIn MS is sent to indetify stream provider
        EXPECTED: listingUrl attribute is received from OptIn MS to consume streaming
        EXPECTED: The next provider info is received from Optin MS:
        EXPECTED: {
        EXPECTED: priorityProviderCode: "PERFORM"
        EXPECTED: priorityProviderName: "Perform"
        EXPECTED: }
        """
        pass

    def test_008_wait_for_the_event_start_time_to_comeevent_to_become_live_refresh_the_page_and_repeat_step_2(self):
        """
        DESCRIPTION: Wait for the event start time to come(event to become live), refresh the page and repeat step '2'
        EXPECTED: Expected results match those from step '7'
        """
        pass
