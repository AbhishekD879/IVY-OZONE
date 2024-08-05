from voltron.pages.shared.contents.sports_tab_contents.competitions_tab_content import CompetitionsAccordionList, \
    CompetitionsTabContent


class LadbrokesCompetitionsAccordionList(CompetitionsAccordionList):
    _item = 'xpath=.//*[@data-crlat="accordionComp"]'


class LadbrokesCompetitionsTabContent(CompetitionsTabContent):

    @property
    def competitions_categories(self):
        return LadbrokesCompetitionsAccordionList(selector=self._competitions_categories_locator)

    @property
    def all_competitions_categories(self):
        return LadbrokesCompetitionsAccordionList(selector=self._all_competitions_categories_locator)
