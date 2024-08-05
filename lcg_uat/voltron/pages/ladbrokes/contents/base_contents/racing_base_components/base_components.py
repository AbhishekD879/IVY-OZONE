from voltron.pages.shared.contents.base_contents.racing_base_components.base_components import Event, Meeting


class LadbrokesEvent(Event):

    @property
    def is_resulted(self):
        return self.has_icon() and self.icon.is_displayed()


class LadbrokesMeeting(Meeting):
    _list_item_type = LadbrokesEvent
