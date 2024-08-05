import { CasinoMyBetsFiveasideBetHeaderComponent } from "./casino-mybets-fiveaside-bet-header.component";


describe('CasinoMyBetsFiveasideBetHeaderComponent', () => {
  let component: CasinoMyBetsFiveasideBetHeaderComponent;
  let router,
  rulesEntryService,
  casinoMyBetsIntegratedService;

  beforeEach(() => {
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl').and.returnValue(Promise.resolve('success')),
      navigate: jasmine.createSpy('navigate')
    };
    rulesEntryService = {
      trackGTMEvent: jasmine.createSpy('trackGTMEvent')
    };
    casinoMyBetsIntegratedService = {
      confirmationPopUpClick: jasmine.createSpy('confirmationPopUpClick'),
      goToSportsCTABtnClick: jasmine.createSpy('goToSportsCTABtnClick')
    };
    component = new CasinoMyBetsFiveasideBetHeaderComponent(router, rulesEntryService, casinoMyBetsIntegratedService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  xit('#onWidgetClick should trigger and navigate', () => {
    component.bet = {
      event: ['123456'],
      id: '2379097305',
      source: 'f',
      contestId: '60eb075772149d6475386619',
      leg: [{ part: [{ outcome: [{}] }] }]
    };
    component.onWidgetClick();
    expect(router.navigateByUrl).toHaveBeenCalled();
  });

  it('should navigate To Five A Side pitch view, isMyBetsInCasino is true and showLeavingCasinoDialog is false', () => {
    component.bet = {
      event: ['123456'],
      id: '2379097305',
      source: 'f',
      contestId: '60eb075772149d6475386619',
      leg: [{ part: [{ outcome: [{}] }] }]
    };
    component.isMyBetsInCasino = true;
    component.showLeavingCasinoDialog = false;
    component.onWidgetClick();
    expect(component['casinoMyBetsIntegratedService'].goToSportsCTABtnClick).toHaveBeenCalled();  
  });

  it('should navigate To Five A Side pitch view, isMyBetsInCasino is false and showLeavingCasinoDialog is false', () => {
    component.bet = {
      event: ['123456'],
      id: '2379097305',
      source: 'f',
      contestId: '60eb075772149d6475386619',
      leg: [{ part: [{ outcome: [{}] }] }]
    };
    component.isMyBetsInCasino = false;
    component.showLeavingCasinoDialog = false;
    component.onWidgetClick();
    expect(component['casinoMyBetsIntegratedService'].goToSportsCTABtnClick).not.toHaveBeenCalled();  
  });

  it('confirmationDialogClick, with event data', () => {
    const event = {
      output: 'userAction',
      value: {
        checkboxValue: true, 
        btnClicked: 'no thanks'
      }
    };
    component.bet = {
      event: ['123456'],
      id: '2379097305',
      source: 'f',
      contestId: '60eb075772149d6475386619',
      leg: [{ part: [{ outcome: [{}] }] }]
    };
    component.confirmationDialogClick(event);
    expect(component['casinoMyBetsIntegratedService'].confirmationPopUpClick).toHaveBeenCalled();  
  });
});
