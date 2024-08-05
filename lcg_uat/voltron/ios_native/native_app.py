from abc import ABCMeta

from voltron.utils import mixins
from voltron.ios_native.shared.components.ios_native_home_page import NativeHomePage


class NativeApp(mixins.LoggingMixin, metaclass=ABCMeta):

    @property
    def home_page(self):
        return NativeHomePage()
