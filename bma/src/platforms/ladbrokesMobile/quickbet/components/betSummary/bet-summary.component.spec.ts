import { LadbrokesBetSummaryComponent } from '@ladbrokesMobile/quickbet/components/betSummary/bet-summary.component';

describe('#LadbrokesBetSummaryComponent', () => {
   let component;
   let user, currencyPipe, bppProviderService, germanSupportService, pubsub;

  beforeEach(() => {
    user = {
      currencySymbol: 'currencySymbol'
    };
    currencyPipe = {
      transform: jasmine.createSpy('transformCurrency')
    };
    bppProviderService = {
      quickBet: jasmine.createSpy('quickBet')
    };
    germanSupportService = {
      isGermanUser: jasmine.createSpy('isGermanUser').and.returnValue(true)
    };

    pubsub = {
      API: {
        SESSION_LOGIN: 'SESSION_LOGIN',
        SESSION_LOGOUT: 'SESSION_LOGOUT'
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((p1, p2, cb) => cb(true)),
      unsubscribe: jasmine.createSpy('unsubscribe'),
    };

    component = new LadbrokesBetSummaryComponent(
      user,
      currencyPipe,
      bppProviderService,
      germanSupportService,
      pubsub
    );
  });

  it('should create LadbrokesBetSummaryComponent instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should set isGermanUser', () => {
    component.ngOnInit();
    expect(pubsub.subscribe).toHaveBeenCalledWith('QuickbetSummary', [pubsub.API.SESSION_LOGIN, pubsub.API.SESSION_LOGOUT],
      jasmine.any(Function));
    expect(component.isGermanUser).toBeTruthy();
  });

  it('#ngOnDestroy should unsubscribe from pubsub', () => {
    component.ngOnDestroy();
    expect(pubsub.unsubscribe).toHaveBeenCalledWith('QuickbetSummary');
  });

  describe('#quickdepositClass', () => {
    it('should set class for specific deposit background color', () => {
      component.isQuickdeposit = true;
      expect(component.quickdepositClass).toEqual('quickdeposit-info-spot');
    });

    it('should NOT set class for specific deposit background color', () => {
      component.isQuickdeposit = false;
      expect(component.quickdepositClass).toEqual('');
    });
  });
});
