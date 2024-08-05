import { of } from 'rxjs';
import { FirstBetEntryPointComponent } from './first-bet-entry-point.component';

describe('FirstBetEntryPointComponent', () => {
  let component: FirstBetEntryPointComponent;
  let pubSubService,sessionStorageService,firstBetGAService,user,cdr,windowRefService;
  let device, cmsService;

  beforeEach(() => {
    pubSubService = {
        publish: jasmine.createSpy(),
        subscribe: jasmine.createSpy('subscribe').and.callFake((subscriber, method, handler) => {
         handler && handler()
        }),
        API: {
          FIRST_BET: 'FIRST_BET'
        }
      };
    firstBetGAService = {
        setGtmData: jasmine.createSpy('setGtmData'),
    };
    sessionStorageService = {
        set: jasmine.createSpy('set'), 
        get: jasmine.createSpy('get').and.callFake(n => {if(n === 'firstBetTutorial'){return {firstBetAvailable: true, user: 'test12'}} 
        else if(n === 'firstBetTutorialAvailable'){return false}}),
        remove: jasmine.createSpy('remove')
    };
    user = {
              'username':'test',
              'sportBalance': 10,
               'lastBet': 25/11/2022
          };
    cdr = {
        detectChanges: jasmine.createSpy('detectChanges')
    };
    windowRefService={
    document : {
      getElementById: jasmine.createSpy().and.returnValue({classList: {
        add: jasmine.createSpy('add'),
        remove: jasmine.createSpy('remove')
      }}),

    }};
    device = {
      requestPlatform: 'mobile'
    }
    cmsService = {
      getFirstBetDetails: jasmine.createSpy().and.returnValue(of({body:{isEnable: false, imageUrl: 'test', months: 1, 'displayTo': new Date(new Date().setMonth(new Date().getMonth() - 1)),
        'displayFrom': new Date(new Date().setMonth(new Date().getMonth() - 1)),
        expiryDateEnabled: true}}))
    }
    component = new FirstBetEntryPointComponent(
        pubSubService,sessionStorageService,firstBetGAService,device,user,cdr,cmsService,windowRefService
    );

  });

  it('should create component instance', () => {
    component.firstBetPlacementDetails={
        brand:'bma'
    
    } as any;
    user.status=true;
    component.ngOnInit();
    expect(component).toBeTruthy();
  });

  it('should create component instance brand ladbrokes', () => {
    component.firstBetPlacementDetails={
        brand:'ladbrokes'
    
    } as any;
    user.status=true;
    component.ngOnInit();
    expect(component).toBeTruthy();
  });

  it('should retuen userstatus false', () => {
    user={
      'username':'test',
      'sportBalance': 10,
       'lastBet': new Date(new Date().setMonth(new Date().getMonth() - 2))
    } as any;
    user.status = false;
    component.ngOnInit();
    expect(component).toBeTruthy();
  });

  it('clicked undo', () => {
    component.firstBetPlacementDetails={
        brand:'ladbrokes'
    
    } as any;
    component.openUndo();
    expect(component.isCloseTutorial).toBeTruthy();
  });

  it('clicked dismiss', () => {
    component.firstBetPlacementDetails={
        brand:'ladbrokes',
        button:{rightButtonDesc:'test desc'}
    
    } as any;
    component.dismiss(true);
    expect(component.isCloseTutorial).toBeFalse();
  });

  it('should return expiry false', () => {
    user.status = true;
    cmsService.getFirstBetDetails.and.returnValue(of({body:{isEnable: false, imageUrl: 'test', months: 1, 'displayTo': new Date(new Date().setMonth(new Date().getMonth() + 1)),
    'displayFrom': new Date(new Date().setMonth(new Date().getMonth() - 1)),
    expiryDateEnabled: true}}))
    sessionStorageService.get.and.returnValue(false)
    component.ngOnInit();
    expect(component).toBeTruthy();
  });

  it('should return lastBet null', () => {
    user.lastBet = null;
    user.status = true;
    cmsService.getFirstBetDetails.and.returnValue(of({body:{isEnable: true, imageUrl: 'test', months: 1, 'displayTo': new Date(new Date().setMonth(new Date().getMonth() + 1)),
    'displayFrom': new Date(new Date().setMonth(new Date().getMonth() - 1)),
    expiryDateEnabled: false}}))
    sessionStorageService.get.and.returnValue(false)
    component.ngOnInit();
    expect(component).toBeTruthy();
  });

  it('clicked Start Tutorial', () => {
    component.firstBetPlacementDetails={
        brand:'ladbrokes',
        homePage:{button:'test'}
    
    } as any;
    pubSubService.publish('FirstBetEntryPointComponent', pubSubService.API.FIRST_BET_PLACEMENT_TUTORIAL);
    component.onStartTutorial();
    expect(component.isFirstBetAvailable).toBeFalse();
  });

  it('close tutorial', () => {
    component.firstBetPlacementDetails={
        brand:'ladbrokes',
        button: {  leftButtonDesc:'testdesc'}
    
    } as any;
    component.closeUndo();
    expect(component.isCloseTutorial).toBeFalse();
  });


});
