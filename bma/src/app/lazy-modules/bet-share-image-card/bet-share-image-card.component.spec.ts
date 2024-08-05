import { of } from "rxjs";
import { BetShareImageCardComponent } from "./bet-share-image-card.component";

describe('BetShareImageCardComponent', () => {
  let component: BetShareImageCardComponent;
  let componentFactoryResolver, dialogService, cmsService, deviceService, betShareImageCardService, betShareGTAService, windowRef;

  beforeEach(() => {
    dialogService = jasmine.createSpyObj('dialogService', ['openDialog']);
    componentFactoryResolver = jasmine.createSpyObj('componentFactoryResolver', ['resolveComponentFactory']);
    cmsService = {
      fetchBetShareConfigDetails: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        openBetShareCardStatus: 'open bets test',
        wonBetShareCardStatus: 'won bets test'
      }))
    };
    deviceService = {
      isIos: false,
      isAndroid: true,
      isWrapper: true
    };
    betShareImageCardService = {
      getOutcomeTitle: jasmine.createSpy('getSystemConfig').and.returnValue(of('test')),
      getEventStartTime: jasmine.createSpy('getSystemConfig').and.returnValue(of('test'))
    };
    betShareGTAService = {
      setGtmData : jasmine.createSpy('setGtmData')
    }
    windowRef = {
      nativeWindow: {
        NativeBridge: jasmine.createSpy('NativeBridge').and.returnValue({shareContentOnSocialMediaGroups:{}})
    }};
    component = new BetShareImageCardComponent(componentFactoryResolver, dialogService, cmsService, deviceService, betShareImageCardService, betShareGTAService,windowRef);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should call ngoninit with regullar bet and settled status', () => {
    component.sportType= 'regularBets';
    component.bet = { eventSource: { betId: '12', date: '12-11-2022', settled: 'Y', totalStatus: 'won', legType: 'E' } };
    component.ngOnInit();
    expect(component.showSettledShareIcon).toBeTruthy();
  });

  it('should call ngoninit with regullar bet and open status', () => {
    component.bet = {  eventSource: { betId: '12', date: '12-11-2022', isSettled: 'N', status: 'open'} };
    component.ngOnInit();
    expect(component.showSettledShareIcon).toBeFalse();
  });

  it('should call ngoninit with pools bet and settled status', () => {
    component.bet = { betId: '12', date: '12-11-2022', isSettled: 'Y', status: 'lost' };
    component.ngOnInit();
    expect(component.showSettledShareIcon).toBeTruthy();
  });

  it('should call ngoninit with lotto bet and open status', () => {
    component.bet = { betId: '12', date: '12-11-2022', settled: 'N', totalStatus: 'open' };
    component.ngOnInit();
    expect(component.showSettledShareIcon).toBeFalse();
  });

  it('should call shareToMedia with totePoolBet bet and open status', () => {
    component.bet = { betId: '12', date: '12-11-2022', settled: 'N', totalStatus: 'won', orderedOutcomes: [{ runnerNumber: '1' }] };
    component.sportType = 'pools';
    component.bet.isTotePoolBetBetModel = true;
    component.shareToMedia();
    expect(component.selectionNamesData).toBeTruthy();
  });


  it('should call shareToMedia with pool bet and settled status', () => {
    component.bet = { bet:{betId: '12', date: '12-11-2022', settled: 'Y', totalStatus: 'won', orderedOutcomes: [{ runnerNumber: '1' }] }};
    component.sportType = 'pools';
    component.bet.isTotePotPoolBetBetModel = true;
    component.shareToMedia();
    expect(component.params.marketName).toBeTruthy();
  });

  it('should call shareToMedia with jackPotPool bet and isResulted true', () => {
    component.bet = { betId: '12', date: '12-11-2022', settled: 'N', totalStatus: 'won', legs: [{ isResulted: true }] };
    component.sportType = 'pools';
    component.bet.isTotePotPoolBetBetModel = false;
    component.bet.isTotePoolBetBetModel = false;
    component.shareToMedia();
    expect(component.time).toEqual(['FT']);
  });

  it('should call shareToMedia with  jackPotPool bet and isResulted false', () => {
    component.bet = { betId: '12', date: '12-11-2022', settled: 'N', totalStatus: 'won', legs: [{ isResulted: false }] };
    component.sportType = 'pools';
    component.bet.isTotePotPoolBetBetModel = false;
    component.bet.isTotePoolBetBetModel = false;
    component.shareToMedia();
    expect(component.sportType).toBe('jackPotPool');
  });

  it('should call shareToMedia with  regular bet', () => {
    component.bet = { eventSource: {  betId: '12', date: '12-11-2022', settled: 'N', totalStatus: 'won'}, location : "cashOutSection" };
    component.sportType = 'regularBets';
    component.shareToMedia();
    expect(component.time.length).toBe(0);
    expect(betShareGTAService.setGtmData).toHaveBeenCalled();
  });
});
