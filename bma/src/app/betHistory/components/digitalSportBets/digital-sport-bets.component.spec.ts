import { DigitalSportBetsComponent } from './digital-sport-bets.component';

describe('DigitalSportBetsComponent', () => {
  let component: DigitalSportBetsComponent,
    pubSubService,
    digitalSportBetsSevice,
    coreToolsService,
    userService,
    domSanitizer;

  beforeEach(() => {
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn()),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        SET_ODDS_FORMAT: 'SET_ODDS_FORMAT'
      }
    };

    digitalSportBetsSevice = {
      sendOddsToDS : jasmine.createSpy()
    };

    coreToolsService = {
      uuid : jasmine.createSpy()
    };

    userService = {
      username : 'Test User',
      oddsFormat : 'Test Odd',
      currency : 'Test Currency'
    };

    domSanitizer = {
      sanitize: jasmine.createSpy().and.returnValue('test'),
      bypassSecurityTrustHtml: () => {},
      bypassSecurityTrustStyle: () => {},
      bypassSecurityTrustScript: () => {},
      bypassSecurityTrustUrl: () => {},
      bypassSecurityTrustResourceUrl: () => {}
    };

    component = new DigitalSportBetsComponent(
      userService,
      domSanitizer,
      digitalSportBetsSevice,
      pubSubService,
      coreToolsService
    );
    component.dsTempToken = 'testToken';
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', () => {
    component.dsIframe = {} as any;
    component.ngOnInit();

    expect(coreToolsService.uuid).toHaveBeenCalled();
    expect(pubSubService.subscribe).toHaveBeenCalledWith('digitalSportBets', 'SET_ODDS_FORMAT', jasmine.any(Function));
    expect(digitalSportBetsSevice.sendOddsToDS).toHaveBeenCalledWith('testToken', jasmine.any(Object));
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();

    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('digitalSportBets');
  });
});
