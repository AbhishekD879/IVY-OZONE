import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29431_Your_Enhanced_Markets_tab_section_for_Eligible_User(Common):
    """
    TR_ID: C29431
    NAME: 'Your Enhanced Markets' tab/section for Eligible User
    DESCRIPTION: This test case verifies 'Your Enhanced Markets' tab/section for the user which is eligible for private market offers.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1.  Open Invictus app and log in
    PRECONDITIONS: 2. **accountFreebets?freebetTokenType=ACCESS** request is used in order to get a private market for particular user after a page refresh or navigating to Homepage from any other page and **user** request is used to get private market after login(open Dev tools -> Network ->XHR tab) (!!! AFTER BMA-49190 we get this data from https://bpp-{env}/Proxy/accountFreebets?channel=MI&returnOffers=Y request
    PRECONDITIONS: 3.  User should be eligible for one or more private enhanced market offers with more than 3 selections
    PRECONDITIONS: 4.  Private market offers should be active (not expired)
    PRECONDITIONS: 5.  Odds format is Fractional
    PRECONDITIONS: 6.  To view event information on SS use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?includeRestricted=true&translationLang=LL
    PRECONDITIONS: *   XXX - event ID (can be get from response - in Console XHR tab or from UAT)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: For setting private markets use the link:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/How+to+Setup+and+Use+Private+Markets?preview=/36604227/36604228/HowToSetupAndUsePrivateMarkets%20.pdf
    PRECONDITIONS: Place a bet on the configured event by any user with sufficient funds for bet placement and then verify Private Markets on the Homepage. Private Markets will be shown for all users which placed a bet on the configured event.
    """
    keep_browser_open = True

    def test_001_load_oxygen_and_login_with_the_user_with_private_markets_available(self):
        """
        DESCRIPTION: Load Oxygen and login with the user with private markets available
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_your_enhancedmarkets_tabsection(self):
        """
        DESCRIPTION: Navigate to 'Your Enhanced Markets' tab/section
        EXPECTED: *   All eligible private markets and associated selections are shown
        EXPECTED: *   All private market accordions expanded by default
        """
        pass

    def test_003_collapseexpand_private_market_accordions(self):
        """
        DESCRIPTION: Collapse/expand private market accordions
        EXPECTED: It is possible to collapse/expand private market accordions
        """
        pass

    def test_004_verifyprivate_market_imagegraphics(self):
        """
        DESCRIPTION: Verify private market image/graphics
        EXPECTED: Private market image/graphics is shown beside each private market line
        """
        pass

    def test_005_verifyname_of_the_private_market(self):
        """
        DESCRIPTION: Verify name of the private market
        EXPECTED: Name of each private market corresponds to **<name>** attribute on market level (e.g. name="Asian Handicap Half-Time Betting")
        """
        pass

    def test_006_verify_market_with_cash_out_label_on_market_section_coral_onlybma_45633(self):
        """
        DESCRIPTION: Verify Market with 'CASH OUT' label on market section (Coral Only!BMA-45633)
        EXPECTED: 'CASH OUT' label is shown next to market name ONLY for markets  with **cashoutAvail="Y" **attribute on Market level
        EXPECTED: (Coral Only! BMA-45633)
        """
        pass

    def test_007_verify_selections_within_the_private_market(self):
        """
        DESCRIPTION: Verify selections within the private market
        EXPECTED: *  First 3 selections and their respective prices are displayed in the market section
        EXPECTED: *  Selections Names and Price/Odds values are correct
        EXPECTED: * 'Show All' button is displayed below
        """
        pass

    def test_008_verify_show_all_button(self):
        """
        DESCRIPTION: Verify 'Show All' button
        EXPECTED: *   'Show All' button is displayed if there are more than 3 selections for a given private market
        EXPECTED: *   All available selection are shown after tapping on 'Show All' button
        EXPECTED: *   'Show All' button is changed to 'Show Less'
        EXPECTED: *   On tapping 'Show Less' button selection list is collapsed back to showing 3 selections
        EXPECTED: *   'Show Less' button is changed to 'Show All' after collapsing
        """
        pass

    def test_009_verify_terms_and_conditions_link(self):
        """
        DESCRIPTION: Verify 'Terms and Conditions' link
        EXPECTED: Link is displayed under the last of available market section
        """
        pass
