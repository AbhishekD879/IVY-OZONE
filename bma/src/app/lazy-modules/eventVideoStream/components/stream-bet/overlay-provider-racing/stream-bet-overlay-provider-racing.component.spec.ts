import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { StreamBetOverlayProviderRacingComponent } from './stream-bet-overlay-provider-racing.component';
import {
    Subject
} from 'rxjs';

describe('StreamBetOverlayProviderRacingComponent', () => {
  let component: StreamBetOverlayProviderRacingComponent;
  let quickbetService;
  let userService;
  let eventVideoStreamProviderService;
  let storageService;
  let gtmService;
  let pubSubService;
  const eventEntity = {
    siteChannels: 'M, S, ',
    liveStreamAvailable: true,
    markets: [
      {
        marketStatusCode: 'A',
        id: '27',
        siteChannels: "P,Q,C,I,M,",
        isMarketBetInRun: 'true',
        isDisplayed: 'true'
      },
      {
        marketStatusCode: 'A',
        id: '28',
        siteChannels: "P,Q,C,I,M,",
        isMarketBetInRun: 'true',
        isDisplayed: 'true'
      }
    ]
  } as any;

  beforeEach(() => {
    quickbetService = {
        quickBetOnOverlayCloseSubj: new Subject<string>()
    };
    userService = {
        sportBalanceWithSymbol: 10,
        sportBalance: '10'
    };
    eventVideoStreamProviderService = {
        isStreamAndBet: true
    };
    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    pubSubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    } as any;
    component = new StreamBetOverlayProviderRacingComponent(quickbetService, userService, eventVideoStreamProviderService,storageService, gtmService, pubSubService);    
  });

  it('StreamBetOverlayProviderRacingComponent: should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('StreamBetOverlayProviderRacingComponent: ngOnInit with quickbet close scenario', () => {
    component.eventEntity = eventEntity as any;    
    component.ngOnInit();
    component['quickbetService'].quickBetOnOverlayCloseSubj.next('close qb panel');
    expect(component.showQuickBet).toEqual(false); 
    expect(component.showReceipt).toEqual(false);   
    expect(component.allMarkets).toEqual(component.eventEntity.markets);  
  });

  it('StreamBetOverlayProviderRacingComponent: ngOnInit with quickbet receipt scenario', () => {
    component.eventEntity = eventEntity as any;    
    component.ngOnInit();
    component['quickbetService'].quickBetOnOverlayCloseSubj.next('qb receipt');
    expect(component.showQuickBet).toEqual(true); 
    expect(component.showReceipt).toEqual(true);   
    expect(component.allMarkets).toEqual(component.eventEntity.markets);  
  });

  it('StreamBetOverlayProviderRacingComponent: handleSelectionClick', () => {
    component.eventEntity = eventEntity as any;
    component.handleSelectionClick(component.eventEntity.markets[0]);
    expect(component.selectedMarket).toEqual(component.eventEntity.markets[0]); 
    expect(component.showQuickBet).toEqual(true);   
  });

  it('StreamBetOverlayProviderRacingComponent: showHideClick with qb show', () => {
    component.eventEntity = eventEntity as any;
    component.showMarkets = true;
    component.showHideText = 'HIDE';
    component.showHideClick();
    expect(component.showHideText).toEqual('SHOW'); 
    expect(component.showMarkets).toEqual(false);   
  });

  it('StreamBetOverlayProviderRacingComponent: showHideClick with qb hide', () => {
    component.eventEntity = eventEntity as any;
    component.showMarkets = true;
    component.showHideText = 'SHOW';
    component.showHideClick();
    expect(component.showHideText).toEqual('HIDE'); 
    expect(component.showMarkets).toEqual(false);   
  });

  describe('#ngAfterViewInit', () => {
    it('call ngAfterViewInit', () => {
      component.sbOverlayLoaded.emit = jasmine.createSpy();
      component['ngAfterViewInit']();
      expect(component.sbOverlayLoaded.emit).toHaveBeenCalled();
    });
  });

  describe('#ngOnDestroy', () => {
    it('call ngOnDestroy', () => {
      const service = new StreamBetOverlayProviderRacingComponent(quickbetService, userService, eventVideoStreamProviderService,storageService, gtmService, pubSubService);    
      component.ngOnDestroy();
      expect(service['eventVideoStreamProviderService'].isStreamAndBet).toEqual(false);   
    });
  });

  it('StreamBetOverlayProviderRacingComponent: #1-ngOnInit with quickbet close scenario', () => {
    component.eventEntity = eventEntity as any;
    component.eventEntity.siteChannels = undefined;    
    component.ngOnInit();
    component['quickbetService'].quickBetOnOverlayCloseSubj.next('close qb panel');
    expect(component.showQuickBet).toEqual(false); 
    expect(component.showReceipt).toEqual(false);   
    expect(component.allMarkets).toEqual([]);  
  });

  it('StreamBetOverlayProviderRacingComponent: #2-ngOnInit with quickbet close scenario', () => {
    component.eventEntity = eventEntity as any;
    component.eventEntity.siteChannels = 'M, S, ';
    component.eventEntity.markets = null;   
    component.allMarkets = []; 
    component.ngOnInit();
    component['quickbetService'].quickBetOnOverlayCloseSubj.next('close qb panel');
    expect(component.showQuickBet).toEqual(false); 
    expect(component.showReceipt).toEqual(false);    
  });

  it('StreamBetOverlayProviderRacingComponent: #3-ngOnInit with quickbet close scenario', () => {
    
    const markets = [{
        marketStatusCode: 'A',
        id: '27',
        siteChannels: null,
        isMarketBetInRun: 'true',
        isDisplayed: true
      },
      {
        marketStatusCode: 'A',
        id: '28',
        siteChannels: null,
        isMarketBetInRun: 'true',
        isDisplayed: true
      }] as any; 
    component.eventEntity = {...eventEntity, siteChannels: 'M, S, ', markets} as any;   
    component.ngOnInit();
    component['quickbetService'].quickBetOnOverlayCloseSubj.next('close qb panel');
    expect(component.showQuickBet).toEqual(false); 
    expect(component.showReceipt).toEqual(false);   
    expect(component.allMarkets).toEqual([]);  
  });

  it('StreamBetOverlayProviderRacingComponent: #4-ngOnInit with quickbet close scenario', () => {
    component.eventEntity = eventEntity as any;
    component.eventEntity.markets = [{
        marketStatusCode: 'A',
        id: '27',
        siteChannels: "M,",
        isMarketBetInRun: 'true',
        isDisplayed: null
      },
      {
        marketStatusCode: 'A',
        id: '28',
        siteChannels: "M,",
        isMarketBetInRun: 'true',
        isDisplayed: null
      }] as any;    
    component.ngOnInit();
    component['quickbetService'].quickBetOnOverlayCloseSubj.next('close qb panel');
    expect(component.showQuickBet).toEqual(false); 
    expect(component.showReceipt).toEqual(false);   
    expect(component.allMarkets).toEqual([]);  
  });

  describe('sportBalance', () => {
    it('should return sportBalance', () => {
        expect(component.sportBalance).toEqual(10); 
    });
    it('should return sportBalance with null value', () => {
        component['userService'].sportBalanceWithSymbol = null;
        expect(component.sportBalance).toEqual(null); 
    });
    it('should refresh sportBalance and return userService', () => {
      userService.sportBalance = 'undefined';
      const result = component.sportBalance;
      expect(component.balanceRefreshed).toBe(true);
      expect(result).toBe(component.sportBalance);
    });
  });
  
});


