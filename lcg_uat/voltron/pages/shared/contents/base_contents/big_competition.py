from selenium.common.exceptions import NoSuchElementException
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.contents.base_contents.sport_base import SportPageBase


class BigCompetitionPageBase(SportPageBase):
    _tab_content = 'xpath=.//big-competition'

    @property
    def tab_content(self):
        return TabContent(selector=self._tab_content, bypass_exceptions=(NoSuchElementException,))
