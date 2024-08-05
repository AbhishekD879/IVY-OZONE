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
class Test_C2601333_Updating_labels_name_for_card_in_Specials_carousel(Common):
    """
    TR_ID: C2601333
    NAME: Updating label's name for card in Specials carousel
    DESCRIPTION: This test case verifies labels' name displaying on card in Specials carousel
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - How to link selections to event: https://confluence.egalacoral.com/display/SPI/How+to+link+selections+to+event
    PRECONDITIONS: - You should have a linked selection to <Race> event
    PRECONDITIONS: - "Racing Specials Carousel" should be enabled in CMS > System Configuration > Structure
    PRECONDITIONS: - You should have specified name for cards labels in CMS > System Configuration > Structure > 'Races Specials Carousel' section > "label" field
    PRECONDITIONS: - You should be on a <Race> EDP that has linked selections
    PRECONDITIONS: **From OX 107:**
    PRECONDITIONS: **The full request to check Enhanced Multiples data:**
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/227?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.typeName:equals:|Enhanced%20Multiples|&simpleFilter=event.suspendAtTime:greaterThan:2020-08-28T11:32:30.000Z&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_verify_cards_labels_name_displaying_in_specials_carousel(self):
        """
        DESCRIPTION: Verify card's label's name displaying in Specials carousel
        EXPECTED: Card's label's name in Specials carousel is the same as configured in CMS
        """
        pass

    def test_002___in_cms__system_configuration__structure__racing_specials_carousel_section__label_field_set_some_short_name_1_character_for_example_and_save_changes__refresh_the_page_in_application_and_verify_label_on_card_in_specials_carousel(self):
        """
        DESCRIPTION: - In CMS > System Configuration > Structure > 'Racing Specials Carousel' section > "label" field set some short name (1 character for example) and save changes
        DESCRIPTION: - Refresh the page in application and verify label on card in Specials carousel
        EXPECTED: - Card's label's name in Specials carousel is the same as configured in CMS
        EXPECTED: - Label is as long as it is needed for label's name
        """
        pass

    def test_003___in_cms__system_configuration__structure__racing_specials_carousel_section__label_field_set_some_long_name_over_40_characters_for_example_and_save_changes__refresh_the_page_in_application_and_verify_label_on_card_in_specials_carousel(self):
        """
        DESCRIPTION: - In CMS > System Configuration > Structure > 'Racing Specials Carousel' section > "label" field set some long name (over 40 characters for example) and save changes
        DESCRIPTION: - Refresh the page in application and verify label on card in Specials carousel
        EXPECTED: - Card's label's name in Specials carousel is the same as configured in CMS
        EXPECTED: - Card's label's name is displayed as long as it doesn't overlap the outcome button and is truncated with the ellipsis
        EXPECTED: - Label is as long as it is needed for label's name
        EXPECTED: - Cards are not merged and displayed as normal
        """
        pass

    def test_004___in_cms__system_configuration__structure__races_specials_carousel_section__label_field_remove_all_text_and_save_changes__refresh_the_page_in_application_and_verify_cards_labels_names_in_specials_carousel(self):
        """
        DESCRIPTION: - In CMS > System Configuration > Structure > 'Races Specials Carousel' section > "label" field remove all text and save changes
        DESCRIPTION: - Refresh the page in application and verify cards' labels names in Specials carousel
        EXPECTED: - Card's label's name in Specials carousel is set to the default name taken from CMS > System Configuration > Config > Racing Specials Carousel section > "label" field
        EXPECTED: - Label is as long as it is needed for label's name
        """
        pass
