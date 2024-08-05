import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.streaming
@vtest
class Test_C29276_Watching_a_Stream_with_incorrect_configuration(Common):
    """
    TR_ID: C29276
    NAME: Watching a Stream with incorrect configuration
    DESCRIPTION: User is trying to watch a Stream when CMS configuration for that specific stream provider is incorrect.
    DESCRIPTION: Applies to <Race> events
    PRECONDITIONS: 1. SiteServer event should be configured to support RPGTV/Perform streaming (**'typeFlagCodes'**='RPG , ... ' AND **'drilldownTagNames'**='EVFLAG_RPM' flags should be set) and should be mapped to RPGTV/Perform stream event
    PRECONDITIONS: 2. Event should have the following attributes:
    PRECONDITIONS: *   isStarted = "true", but stream has not run for more than 1 minute after the 'start time'
    PRECONDITIONS: *   isMarketBetInRun = "true"
    PRECONDITIONS: 3. User is logged in and placed a minimum sum of £1 on one or many Selections within tested event
    PRECONDITIONS: 4. Ukraine should be whitelisted by Perform
    PRECONDITIONS: 5. Change CMS configurations for Perform stream to incorrect values here: CMS -> System Configuration -> Structure -> 'performGroup'( **After OX103:** CMS -> Secrets -> 'performGroup')
    PRECONDITIONS: **Postconditions**
    PRECONDITIONS: All configurations should be set to DEFAULT again:
    PRECONDITIONS: For Coral:
    PRECONDITIONS: *   **desktopPartnerId** = 905
    PRECONDITIONS: *   **desktopUserId** = test
    PRECONDITIONS: *   **mobilePartnerId** = 2864
    PRECONDITIONS: *   **mobileUserId** = test
    PRECONDITIONS: *   **desktopSeed** = 3GVJr687Z2KSTu2r3J7D
    PRECONDITIONS: *   **mobileSeed** = 2fhghg46565kjlkill56
    PRECONDITIONS: For Ladbrokes:
    PRECONDITIONS: *   **desktopPartnerId** = 30
    PRECONDITIONS: *   **desktopUserId** = test
    PRECONDITIONS: *   **mobilePartnerId** = 4004
    PRECONDITIONS: *   **mobileUserId** = test
    PRECONDITIONS: *   **desktopSeed** = l4ddi35shWWEEhgsm9937jdh
    PRECONDITIONS: *   **mobileSeed** =bwuKoP47Km56pPoka
    """
    keep_browser_open = True

    def test_001_open_event_details_page_of_any_race_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Race> event which satisfies Preconditions
        EXPECTED: * Desktop:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050952) (Coral) / 'Watch' ![](index.php?/attachments/get/3050953) (Ladbrokes) button is shown below the event name line
        EXPECTED: * Mobile/Tablet:
        EXPECTED: 'Live Stream' ![](index.php?/attachments/get/3050954) (Coral) / 'Watch' ![](index.php?/attachments/get/3050955) (Ladbrokes) button is shown when scoreboard is absent.
        """
        pass

    def test_002_all_devicestapclick_on_watchlive_stream_button(self):
        """
        DESCRIPTION: **All Devices**
        DESCRIPTION: Tap/click on 'Watch'/'Live Stream' button
        EXPECTED: * [ **Coral** desktop / **Ladbrokes** desktop]: Message is displayed: "The Stream for this event is currently not available."
        EXPECTED: * [ **Ladbrokes** and **Coral** tablet/mobile]: Pop up opens with message "The Stream for this event is currently not available."
        EXPECTED: * User is not able to watch the stream
        EXPECTED: * Application has not crashed
        """
        pass
