from voltron.ios_native.shared.components.ios_native_base import IOSNativeBase


class NativeHomePage(IOSNativeBase):
    _home_button = 'id=home'
    _logo = 'id=logo'
    _login_button = 'id=LOGIN / JOIN'
    _racing_card_item = 'xpath=//*[@name="Coral"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeCollectionView/XCUIElementTypeCell[2]/XCUIElementTypeOther/XCUIElementTypeOther'
    # 'xpath=//*[@name="Ladbrokes"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[3]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeOther[2]'

    @property
    def home_button(self):
        return IOSNativeBase(selector=self._home_button)

    @property
    def login_button(self):
        return IOSNativeBase(selector=self._login_button)

    @property
    def logo(self):
        return IOSNativeBase(selector=self._logo)
