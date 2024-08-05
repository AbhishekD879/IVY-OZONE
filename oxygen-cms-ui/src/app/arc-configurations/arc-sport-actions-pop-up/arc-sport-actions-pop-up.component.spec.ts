import { ArcSportActionsPopUpComponent } from '@app/arc-configurations/arc-sport-actions-pop-up/arc-sport-actions-pop-up.component';

describe('ArcSportActionsPopUpComponent', () => {
  let component: ArcSportActionsPopUpComponent;
  let mockArray, mockSports, dataDisabled, dataEnabled;
  beforeEach(() => {
    mockArray = [
      { action: 'Homepage & landing pages', messagingContent: 'home data', gcLink: "https://qa3.sports.ladbrokes.com/", enabled: true },
      { action: 'Betslip', messagingContent: '', gcLink: "https://qa3.sports.ladbrokes.com/", enabled: false },
      { action: 'Betreceipt', messagingContent: '', gcLink: "https://qa3.sports.ladbrokes.com/", enabled: false },
      { action: 'My Bets', messagingContent: '', gcLink: "https://qa3.sports.ladbrokes.com/", enabled: false },
      { action: 'Quick bet removal', messagingContent: '', gcLink: "https://qa3.sports.ladbrokes.com/", enabled: true },
      { action: 'Gaming cross sell removal', messagingContent: '', gcLink: "https://qa3.sports.ladbrokes.com/", enabled: false }
    ],
      mockSports = [
        { action: 'Homepage & landing pages', messagingContent: 'home data', gcLink: "https://qa3.sports.ladbrokes.com/", enabled: true },
        { action: 'Quick bet removal', messagingContent: '', gcLink: '', enabled: true }
      ];
    dataDisabled = { action: 'My Bets', messagingContent: '', gcLink: '', enabled: false };
    dataEnabled = { action: 'Quick bet removal', messagingContent: '', gcLink: '', enabled: true };
    component = new ArcSportActionsPopUpComponent(mockSports);
  });
  it('should create', () => {
    expect(component).toBeTruthy();
  });
  describe('ngOnInit', () => {
    it('general calls', () => {
      component.data.sports = mockSports;
      component.ngOnInit();
      expect(component.data.sportsArray).toEqual(mockArray);
      expect(component.addData).toEqual(mockSports);
    });
  });
  describe('addSport', () => {
    it('when sport action is enabled', () => {
      component.addData = [{ action: 'Homepage & landing pages', messagingContent: 'home data', gcLink: 'https://qa3.sports.ladbrokes.com/', enabled: true }];
      component.addSport(dataEnabled);
      expect(component.addData).toEqual(mockSports);
    });
    it('when sport action is disabled', () => {
      component.addData = mockSports;
      component.addSport(dataDisabled);
      expect(component.addData).toEqual(mockSports);
    });
  });
});