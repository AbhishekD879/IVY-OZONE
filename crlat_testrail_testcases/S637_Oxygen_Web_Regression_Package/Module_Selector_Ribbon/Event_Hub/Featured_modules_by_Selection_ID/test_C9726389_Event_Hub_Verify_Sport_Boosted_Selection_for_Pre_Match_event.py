import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C9726389_Event_Hub_Verify_Sport_Boosted_Selection_for_Pre_Match_event(Common):
    """
    TR_ID: C9726389
    NAME: Event Hub: Verify <Sport> Boosted Selection for Pre-Match event
    DESCRIPTION: This test case verifies Modules configured in CMS for <Sport> where Module consists of one selection retrieved by 'Selection ID'.
    PRECONDITIONS: 1) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 2) To retrieve an information about event outcomes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?translationLang=LL
    PRECONDITIONS: *   *ZZZZ - an **'event id'***
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 4) Featured Events module by Selection Id with ID of Pre Match event
    PRECONDITIONS: 5) User is on Homepage > Event hub
    """
    keep_browser_open = True

    def test_001_verify_selection_name(self):
        """
        DESCRIPTION: Verify 'Selection Name'
        EXPECTED: * 'Selection Name' within module corresponds to <name> attribute from SS response OR to <name> set in CMS if name was overridden
        EXPECTED: * Name of a long selection is wrapped into a few lines without cutting the text
        """
        pass

    def test_002_verify_event_start_time_within_created_module(self):
        """
        DESCRIPTION: Verify 'Event Start time' within created Module
        EXPECTED: *   'Event Start time' corresponds to '**startTime**' attribute
        EXPECTED: *   For events that occur Today date format is **HH:MM, Today**
        EXPECTED: *   For events that occur Tomorrow date format is **HH:MM, DD MMM** (e.g. 14:00 or 05:00, 24 Nov or 02 Nov)
        """
        pass

    def test_003_verify_favourites_icon(self):
        """
        DESCRIPTION: Verify 'Favourites' icon
        EXPECTED: 'Favourites' icon is displayed only for Football events within Module section
        EXPECTED: NOTE: 'Favourites' functionality is turned off for Ladbrokes by Default
        """
        pass

    def test_004_verify_watch_live_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and label
        EXPECTED: 'Watch Live' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: EVFLAG_AVA
        EXPECTED: EVFLAG_IVM
        EXPECTED: EVFLAG_PVM
        EXPECTED: EVFLAG_RVA
        EXPECTED: EVFLAG_RPM
        EXPECTED: EVFLAG_GVM
        """
        pass

    def test_005_verify_priceodds_button_within_created_module(self):
        """
        DESCRIPTION: Verify 'Price/Odds' button within created Module
        EXPECTED: 'Price/Odds' button is shown with correct price which corresponds to **'priceNum/priceDen'** in fractional format (**'priceDec'** in decimal format) attributes values in SS response
        """
        pass

    def test_006_clicktapanywhere_on_event_card_except_for_price_buttons_within_verified_module(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event card (except for price buttons) within verified module
        EXPECTED: Event Details page is opened
        """
        pass
