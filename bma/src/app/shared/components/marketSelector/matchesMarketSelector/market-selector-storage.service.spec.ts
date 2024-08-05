import { tick, fakeAsync } from '@angular/core/testing';
import { MarketSelectorStorageService } from './market-selector-storage.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { Subscription, of } from 'rxjs';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { ISystemConfig } from '@core/services/cms/models';

describe('MarketSelectorStorageService', () => {
    let marketSelectorStorageService: MarketSelectorStorageService;
    let router;
    let route;
    let routingState;
    let routerEventsCb;
    let marketSelectorService;
    let navEvent;
    let cmsService;
    let storage;

    beforeEach(() => {
        navEvent = new NavigationEnd(0 , 'test', 'test1');
        marketSelectorService = {
            restoreSelectedOption: jasmine.createSpy('restoreSelectedOption').and.returnValue(''),
            addCleanUpListener: jasmine.createSpy('addCleanUpListener'),
            getPathName: jasmine.createSpy('getPathName')
          };
          route = {
            events: {
              subscribe: jasmine.createSpy('subscribe').and.returnValue(new Subscription()),
              unsubscribe: jasmine.createSpy('unsubscribe')
            },
            navigateByUrl: jasmine.createSpy(),
            snapshot: jasmine.createSpy().and.returnValue('Main Market')
          };
          router = {
            events: {
              subscribe: jasmine.createSpy('subscribeSpy').and.callFake(cb => {
                routerEventsCb = cb;
                return {
                  unsubscribe: jasmine.createSpy('unsubscribe')
                };
              })
            }
          };
          routingState = {
            getPreviousUrl: jasmine.createSpy('getPreviousUrl'),
            getPathName: jasmine.createSpy('getPathName'),
            getRouteParam: jasmine.createSpy('getRouteParam')
          };
          const sysConfig: ISystemConfig = {
            MarketSwitcher: {
              cricket: true
            }
          };
          cmsService = {
            getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of(sysConfig))
          };
          storage = {
            get: (key: string)=>{
              return { 'football': {selectedOption : 'MockOption'}};
             },
             set: (key: string, value: any)=>{
              return true;
             },
             remove: (key: string)=>{
              return key;
             }
          };
          marketSelectorStorageService = new MarketSelectorStorageService(
            storage,
            router as Router,
            route as ActivatedRoute,
            routingState as RoutingState,
            cmsService
        );
    });
    describe('constructor()', () => {
        it('Should call constructor', () => {
          marketSelectorStorageService['sportNameByParam'] = 'football';
          marketSelectorStorageService.sportNameFlag = true;
          marketSelectorStorageService.sportsList = ['AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts', 
          'AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts']
          routingState.getPreviousUrl.and.returnValue('/sport/'+ marketSelectorStorageService['sportNameByParam']+'/');
          routingState.getRouteParam.and.returnValue('football');
          routingState.getPathName.and.returnValue('today');
          expect(marketSelectorStorageService).toBeTruthy();
        });
        it('Should call constructor getRouteParam is empty', () => {
          marketSelectorStorageService['sportNameByParam'] = 'football';
          marketSelectorStorageService.sportNameFlag = true;
          marketSelectorStorageService.sportsList = ['AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts', 
          'AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts']
          routingState.getPreviousUrl.and.returnValue('/sport/'+ marketSelectorStorageService['sportNameByParam']+'/');
          routingState.getRouteParam.and.returnValue(null);
          routingState.getPathName.and.returnValue('today');
          const res = marketSelectorStorageService['isValidFootballLocation']();
          expect(res).toBeFalsy();
        });

        it('Should call sport param', () => {
          marketSelectorStorageService['sportNameByParam'] = 'football';
          marketSelectorStorageService.sportNameFlag = true;
          marketSelectorStorageService.sportsList = ['AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts', 
          'AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts']
          routingState.getPreviousUrl.and.returnValue('/sport/'+ marketSelectorStorageService['sportNameByParam']+'/');
          routingState.getRouteParam.and.returnValue('sport');
          routingState.getPathName.and.returnValue('today');
          const res = marketSelectorStorageService['isValidFootballLocation']();
          expect(res).toBeFalsy();
        });
    });

    describe('isValidFootballLocation()', () => {
        it('Should be sportNameFlag false value', () => {
          cmsService.getSystemConfig.and.returnValue(of(undefined));
          marketSelectorStorageService['isValidFootballLocation']();
          expect(marketSelectorStorageService.sportNameFlag).toBeFalsy();
      });

      it('Should enter 1st if block with event/football in previousUrl', () => {
          marketSelectorStorageService.sportNameFlag = true;
          marketSelectorStorageService.sportsList = ['AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 
          'volleyball', 'baseball', 'darts', 'AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts'];
          routingState.getPreviousUrl.and.returnValue('/event/'+ marketSelectorStorageService['sportNameByParam']);
          routingState.getPathName.and.returnValue('live');
          expect(marketSelectorStorageService['isValidFootballLocation']()).toBeTruthy();
      });

      it('Should enter 2nd if block with event/football in previousUrl', () => {
          marketSelectorStorageService['sportNameByParam'] = 'football';
          marketSelectorStorageService.sportNameFlag = true;
          marketSelectorStorageService.sportsList = ['AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts', 
          'AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts']
          routingState.getPreviousUrl.and.returnValue('/sport/'+ marketSelectorStorageService['sportNameByParam']+'/');
          routingState.getRouteParam.and.returnValue('football');
          routingState.getPathName.and.returnValue('today');
          const res = marketSelectorStorageService['isValidFootballLocation']();
          expect(res).toBeFalsy();
      });

      it('Should enter 2nd if else condition one previousUrl', () => {
        marketSelectorStorageService['sportNameByParam'] = 'ABCD';
        marketSelectorStorageService.sportNameFlag = true;
        marketSelectorStorageService.sportsList = ['AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts', 
        'AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts']
        routingState.getPreviousUrl.and.returnValue('/sport/'+ marketSelectorStorageService['sportNameByParam']+'/');
        routingState.getRouteParam.and.returnValue('football');
        routingState.getPathName.and.returnValue('today');
        const res = marketSelectorStorageService['isValidFootballLocation']();
        expect(res).toBeTruthy();
        marketSelectorStorageService['sportNameByParam'] = 'rugbyunion';
        routingState.getPreviousUrl.and.returnValue('/abcd/'+ marketSelectorStorageService['sportNameByParam']+'/');
        expect(res).toBeTruthy();
        marketSelectorStorageService['sportNameByParam'] = 'rugbyunion';
        routingState.getPathName.and.returnValue('abcd');
        expect(res).toBeTruthy();
      });

      it('Should enter 3rd if condition', () => {
        marketSelectorStorageService['sportNameByParam'] = 'ABCD';
        marketSelectorStorageService.sportNameFlag = true;
        marketSelectorStorageService.sportsList = ['AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts', 
        'AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts']
        routingState.getPreviousUrl.and.returnValue('/sport/'+ marketSelectorStorageService['sportNameByParam']+'/');
        routingState.getRouteParam.and.returnValue('football');
        routingState.getPathName.and.returnValue('today');
        const res = marketSelectorStorageService['isValidFootballLocation']();
        expect(res).toBeTruthy();
        marketSelectorStorageService['sportNameByParam'] = 'xyz';
        routingState.getPreviousUrl.and.returnValue('/abcd/'+ marketSelectorStorageService['sportNameByParam']+'/');
        routingState.getPathName.and.returnValue('pqrs');
        expect(res).toBeTruthy();
      });

      it('Should enter 3rd if else condition return true', () => {
        marketSelectorStorageService['sportNameByParam'] = 'ABCD';
        marketSelectorStorageService.sportNameFlag = true;
        marketSelectorStorageService.sportsList = ['AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts', 
        'AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts']
        routingState.getPreviousUrl.and.returnValue('/sport/'+ marketSelectorStorageService['sportNameByParam']+'/');
        routingState.getRouteParam.and.returnValue('today');
        const res = marketSelectorStorageService['isValidFootballLocation']();
        expect(res).toBeTruthy();
      });

      it('Should enter 3rd if else condition return false', () => {
        marketSelectorStorageService['sportNameByParam'] = 'ABCD';
        marketSelectorStorageService.sportNameFlag = true;
        marketSelectorStorageService.sportsList = ['AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts', 
        'AllSports', 'rugbyunion', 'football', 'snooker', 'icehockey', 'golf', 'basketball', 'rugbyleague', 'cricket', 'americanfootball', 'boxing', 'volleyball', 'baseball', 'darts']
        routingState.getPreviousUrl.and.returnValue('/sport/'+ marketSelectorStorageService['sportNameByParam']+'/');
        routingState.getPathName.and.returnValue('');
        routingState.getRouteParam.and.returnValue('');
        const res = marketSelectorStorageService['isValidFootballLocation']();
        expect(res).toBeFalsy();
      });

      it('Should enter 3rd if block with getRouteParam', () => {
        marketSelectorStorageService['sportNameByParam'] = 'ABCD';
        marketSelectorStorageService.sportNameFlag = true;
        routingState.getPreviousUrl.and.returnValue('DUMMY');
        routingState.getPathName.and.returnValue('');
        routingState.getRouteParam.and.returnValue('football');
        expect(marketSelectorStorageService['isValidFootballLocation']()).toBeFalsy();
      });

      it('Should enter 3rd ifs else block with getRouteParam and return false', () => {
        marketSelectorStorageService['sportNameByParam'] = 'ABCD';
        marketSelectorStorageService.sportNameFlag = true;
        routingState.getPreviousUrl.and.returnValue('DUMMY');
        routingState.getPathName.and.returnValue('');
        routingState.getRouteParam.and.returnValue('');
        expect(marketSelectorStorageService['isValidFootballLocation']()).toBeFalsy();
      });

      it('Should enter 3rd ifs else block with getRouteParam and return true', () => {
        marketSelectorStorageService['sportNameByParam'] = 'ABCD';
        marketSelectorStorageService.sportNameFlag = true;
        routingState.getPreviousUrl.and.returnValue('DUMMY');
        routingState.getPathName.and.returnValue('');
        routingState.getRouteParam.and.returnValue('today');
        expect(marketSelectorStorageService['isValidFootballLocation']()).toBeTruthy();
      });
  });

    describe('storeSelectedOption()', () => {
        it('Should call the storeSelectedOption function', () => {
            marketSelectorStorageService['storeSelectedOption']('Golf', 'optionValue');
        });
    });

    describe('removeCleanUpListener()', () => {
        it('Should call the removeCleanUpListener function, isListenForClean is true', () => {
            marketSelectorStorageService['isListenForClean'] = true;
            const mockSubscription = jasmine.createSpyObj('removeRouteChangeListener',
          {unsubscribe: jasmine.createSpy()});
          marketSelectorStorageService['removeRouteChangeListener'] = mockSubscription;
            marketSelectorStorageService['removeCleanUpListener']();
            expect(mockSubscription.unsubscribe).toHaveBeenCalled();
        });

        it('Should call the removeCleanUpListener function, isListenForClean is false', () => {
            marketSelectorStorageService['isListenForClean'] = false;
            const mockSubscription = jasmine.createSpyObj('removeRouteChangeListener',
          {unsubscribe: jasmine.createSpy()});
          marketSelectorStorageService['removeRouteChangeListener'] = mockSubscription;
            marketSelectorStorageService['removeCleanUpListener']();
            expect(mockSubscription.unsubscribe).not.toHaveBeenCalled();
        });
    });

    describe('addCleanUpListener()', () => {
        it('Should Not call the addCleanUpListener function', () => {
            marketSelectorStorageService['isListenForClean'] = true;
            marketSelectorStorageService['addCleanUpListener']();
            expect(marketSelectorStorageService['isListenForClean']).toBeTruthy();
        });

        it('Should enter 1st if() block', fakeAsync(() => {
            marketSelectorStorageService['isListenForClean'] = false;
            marketSelectorStorageService['checkRouteForCleanUpData'] = jasmine.createSpy('checkRouteForCleanUpData');
            marketSelectorStorageService['addCleanUpListener']();
            tick();
            routerEventsCb(navEvent);
            expect(marketSelectorStorageService['isListenForClean']).toBeTruthy();
            expect( marketSelectorStorageService['checkRouteForCleanUpData']).toHaveBeenCalled();
        }));

        it('Should enter 1st if() block and Not enter 2nd if()', fakeAsync(() => {
            marketSelectorStorageService['isListenForClean'] = false;
            marketSelectorStorageService['checkRouteForCleanUpData'] = jasmine.createSpy('checkRouteForCleanUpData');
            marketSelectorStorageService['addCleanUpListener']();
            tick();
            routerEventsCb();
            expect(marketSelectorStorageService['isListenForClean']).toBeTruthy();
            expect( marketSelectorStorageService['checkRouteForCleanUpData']).not.toHaveBeenCalled();
        }));
    });

    describe('checkRouteForCleanUpData()', () => {
        it('should Not enter its if() block', () => {
            marketSelectorStorageService['isValidFootballLocation'] = jasmine.createSpy('isValidFootballLocation').and.returnValue(true);
            marketSelectorStorageService['edpCall'] = jasmine.createSpy('edpCall').and.returnValue(true);
            marketSelectorStorageService['cleanUpStoredData'] = jasmine.createSpy('cleanUpStoredData');
            marketSelectorStorageService['removeCleanUpListener'] = jasmine.createSpy('removeCleanUpListener');
            marketSelectorStorageService['checkRouteForCleanUpData']();
            expect( marketSelectorStorageService['cleanUpStoredData']).not.toHaveBeenCalled();
        });

        it('should enter its if() block', () => {
            marketSelectorStorageService['isValidFootballLocation'] = jasmine.createSpy('isValidFootballLocation').and.returnValue(false);
            marketSelectorStorageService['edpCall'] = jasmine.createSpy('edpCall').and.returnValue(false);
            marketSelectorStorageService['cleanUpStoredData'] = jasmine.createSpy('cleanUpStoredData');
            marketSelectorStorageService['removeCleanUpListener'] = jasmine.createSpy('removeCleanUpListener');
            marketSelectorStorageService['checkRouteForCleanUpData']();
            expect( marketSelectorStorageService['cleanUpStoredData']).toHaveBeenCalled();
            expect( marketSelectorStorageService['removeCleanUpListener']).toHaveBeenCalled();
        });
    });

    describe('cleanUpStoredData()', () => {
        it('should delete selectorStoredData', () => {
            marketSelectorStorageService.selectorStoredData = { 'football': {selectedOption : 'MockOption'}};
            expect(marketSelectorStorageService['storage']['get']('hasKey')).toEqual({ 'football': {selectedOption : 'MockOption'}});
        });
    });

    describe('restoreSelectedOption()', () => {
        it('should return selectedOption data', () => {
            marketSelectorStorageService.selectorStoredData = { 'football': {selectedOption : 'MockOption'}};
            expect(marketSelectorStorageService.restoreSelectedOption('football')).toBe('MockOption');
        });

        it('should return empty string as data', () => {
            marketSelectorStorageService.selectorStoredData = { 'football': {selectedOption : 'MockOption'}};
            expect(marketSelectorStorageService.restoreSelectedOption('baseball')).toBe('');
        });
    });

    describe('storeSelectedOption()', () => {
        it('should call addCleanUpListener()', () => {
            marketSelectorStorageService['addCleanUpListener'] = jasmine.createSpy('addCleanUpListener');
            marketSelectorStorageService.selectorStoredData = { 'baseball': {selectedOption : ''}};
            marketSelectorStorageService.storeSelectedOption('football', 'MockOption');
            expect(marketSelectorStorageService.selectorStoredData['football'].selectedOption).toBe('MockOption');
            expect(marketSelectorStorageService['addCleanUpListener']).toHaveBeenCalled();
        });
    });
});