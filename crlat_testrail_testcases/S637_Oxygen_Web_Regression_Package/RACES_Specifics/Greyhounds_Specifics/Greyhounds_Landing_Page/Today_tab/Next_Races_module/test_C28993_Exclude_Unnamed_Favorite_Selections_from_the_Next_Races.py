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
class Test_C28993_Exclude_Unnamed_Favorite_Selections_from_the_Next_Races(Common):
    """
    TR_ID: C28993
    NAME: Exclude Unnamed Favorite Selections from the 'Next Races'
    DESCRIPTION: This test case verifies that 'Unnamed Favorite' and 'Unnamed 2nd Favorite' selection shouldn't be displayed in th 'Next Races' module.
    DESCRIPTION: Jira ticket: BMA-10828 All devices - Next 4 Races
    PRECONDITIONS: To retrieve data from the Site Server use the following:
    PRECONDITIONS: 1) To get Class IDs use a link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:19&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Greyhound category id =19
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To get a list of all "Events" for the classes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?translationLang=LL
    PRECONDITIONS: Notice,
    PRECONDITIONS: *YYYY is a comma separated list of Class ID's e.g. 97 or 97, 98.*
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) To retrieve an information about event outcomes, silks info etc. use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZZ?racingForm=outcome&translationLang=LL
    PRECONDITIONS: where,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *ZZZZZZ is an **'event id'** which is taken from the link in step 2.*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - **'name'** on outcome level to see an outcome name
    """
    keep_browser_open = True

    def test_001_on_site_server_find_an_eventwich_has_unnamed_selections_in_the_site_server_response(self):
        """
        DESCRIPTION: On Site Server find an event wich has 'unnamed' selections in the Site Server response
        EXPECTED: 1.  'Unnamed Favorite' selection corresponds to the **'name' **attribute
        EXPECTED: 2.  'Unnamed 2nd Favorite' selection corresponds to the **'name' **attribute
        """
        pass

    def test_002_load_invictis_application(self):
        """
        DESCRIPTION: Load Invictis application
        EXPECTED: 
        """
        pass

    def test_003_from_the_sports_menu_ribbon_on_homepage_tap_greyhounds_icon(self):
        """
        DESCRIPTION: From the sports menu ribbon on homepage tap 'Greyhounds' icon
        EXPECTED: 'Greyhounds' landing page is opened
        """
        pass

    def test_004_find_an_event_in_the_next_races_module_wich_have_unnamed_selections(self):
        """
        DESCRIPTION: Find an event in the 'Next Races' module wich have 'unnamed' selections
        EXPECTED: Event is shown
        """
        pass

    def test_005_verify_selections_in_the_next_races_module(self):
        """
        DESCRIPTION: Verify selections in the 'Next Races' module
        EXPECTED: 1.  'Unnamed Favorite' and 'Unnamed 2nd Favorite' won't appear in the list of selection on the 'Next Races' module
        EXPECTED: 2.  'Unnamed' selections are excluded by **'name'** attribute
        """
        pass

    def test_006_change_quantity_of_selections_via_cms(self):
        """
        DESCRIPTION: *\***|Change quantity of selections via CMS\***|*
        EXPECTED: *\***|This functionality will be implemented in future\***|*
        """
        pass

    def test_007_look_at_the_selections_in_the_next_races_module(self):
        """
        DESCRIPTION: Look at the selections in the 'Next Races' module
        EXPECTED: 'Unnamed' selections are not displayed in the 'Next Races' module
        """
        pass
