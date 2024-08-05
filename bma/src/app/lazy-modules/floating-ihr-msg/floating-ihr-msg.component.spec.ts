import { of } from 'rxjs';
import { FloatingIhrMsgComponent } from './floating-ihr-msg.component';
import environment from '@environment/oxygenEnvConfig';
import { SimpleChanges } from '@angular/core';

describe('FloatingIhrMsgComponent', () => {
    let component: FloatingIhrMsgComponent;
    let cmsService,
        pubSubService,
        locale,
        gtmService;

    beforeEach(() => {
        locale = {
            getString: jasmine.createSpy().and.returnValue('Ladbrokes')
        };
        pubSubService = {
            publish: jasmine.createSpy('publish'),
            subscribe: jasmine.createSpy().and.callFake((a, b, cb) => cb && cb()),
            unsubscribe: jasmine.createSpy('unsubscribe'),
            API: {
            EXTRA_PLACE_RACE_OFF: 'EXTRA_PLACE_RACE_OFF',
            SUSPEND_IHR_EVENT_OR_MRKT: 'SUSPEND_IHR_EVENT_OR_MRKT'
            }
        };
        cmsService = {
            getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({}))
        };
        gtmService = {
          push: jasmine.createSpy('push')
        };
        component = new FloatingIhrMsgComponent(cmsService, pubSubService, locale, gtmService);
        component.racingInMeeting = {} as any;
        component.eventId = 0;
        component.eventEntity = {} as any;
        });

    describe('FloatingIhrMsgComponent', () => {
        it('should subscribe to getSystemConfig', () => {
            environment.brand = 'bma';
            component.racingInMeeting = [{
              id: 555,
              name: 'Leg event',
              markets: [],
              categoryCode: 'HORSE_RACING',
              isFinished: 'false',
              drilldownTagNames: 'EVFLAG_IHR'
            } as any];
            cmsService.getSystemConfig.and.returnValue(of({ HorseRacingBIR: {floatingMsgEnabled: 'text for testing', marketsEnabled: ['win or each Way']}}));
            spyOn(component, 'checkToShowFloatingMsg').and.returnValue();
            component.ngOnInit();
            expect(component.floatingMsgText).toBe('text for testing');
        });
        it('cms config as null', () => {
          environment.brand = 'bma';
            component.racingInMeeting = [{
              id: 555,
              name: 'Leg event',
              markets: [],
              categoryCode: 'HORSE_RACING',
              isFinished: 'false',
              drilldownTagNames: 'EVFLAG_IHR'
            } as any];
          cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of(null));
          spyOn(component, 'checkToShowFloatingMsg').and.returnValue();
          component.ngOnInit();
          expect(component['BIRMarketsEnabled']).toBeFalsy();
        });
        it('HorseRacingBIR as null', () => {
          environment.brand = 'bma';
            component.racingInMeeting = [{
              id: 555,
              name: 'Leg event',
              markets: [],
              categoryCode: 'HORSE_RACING',
              isFinished: 'false',
              drilldownTagNames: 'EVFLAG_IHR'
            } as any];
          cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of({HorseRacingBIR: null}));
          spyOn(component, 'checkToShowFloatingMsg').and.returnValue();
          component.ngOnInit();
          expect(component['BIRMarketsEnabled']).toBeFalsy();
        });
        it('EXTRA_PLACE_RACE_OFF subscription', () => {
            component.racingInMeeting = [{
              id: 555,
              name: 'Leg event',
              markets: [],
              categoryCode: 'HORSE_RACING',
              isFinished: 'false',
              drilldownTagNames: 'EVFLAG_IHR'
            } as any];
            component.eventId = 555;
            cmsService.getSystemConfig.and.returnValue(of({ HorseRacingBIR: {floatingMsgEnabled: 'text for testing', marketsEnabled: ['win or each Way']}}));
            component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
              if (ch === pubSubService.API.EXTRA_PLACE_RACE_OFF) {
                fn('555');
                expect(component.showFloatingInplayMsg).toBe(true);
              }
            });
            spyOn(component, 'checkToShowFloatingMsg').and.returnValue();
            component.ngOnInit();
            
          });
      
          it('SUSPEND_IHR_EVENT_OR_MRKT subscription, with showFloatingInplayMsg to be false', () => {
            component.racingInMeeting = [{
              id: 555,
              name: 'Leg event',
              markets: [{marketStatusCode: 'S', name: 'Win or Each Way'}],
              categoryCode: 'HORSE_RACING',
              isFinished: 'false',
              drilldownTagNames: 'EVFLAG_IHR'
            } as any];
            component.eventId = 555;
            component.isInplay = true;
            component['isBirMarketEnabled'] = jasmine.createSpy().and.returnValue(true);
            cmsService.getSystemConfig.and.returnValue(of({ HorseRacingBIR: {floatingMsgEnabled: 'text for testing', marketsEnabled: ['win or each Way']}}));
            component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
              if (ch === pubSubService.API.SUSPEND_IHR_EVENT_OR_MRKT ) {
                fn('555', {eventStatusCode: 'S', marketStatusCode: 'S', originalName: 'Win or Each Way'});
                expect(component.showFloatingInplayMsg).toBe(false);
              }
            });
            spyOn(component, 'checkToShowFloatingMsg').and.returnValue();
            component.ngOnInit();
          });

          it('SUSPEND_IHR_EVENT_OR_MRKT subscription, with showFloatingInplayMsg to be false - eventStatusCode as active', () => {
            component.racingInMeeting = [{
              id: 555,
              name: 'Leg event',
              markets: [],
              categoryCode: 'HORSE_RACING',
              isFinished: 'false',
              drilldownTagNames: 'EVFLAG_IHR'
            } as any];
            component.eventId = 555;
            component.isInplay = true;
            cmsService.getSystemConfig.and.returnValue(of({ HorseRacingBIR: {floatingMsgEnabled: 'text for testing', marketsEnabled: ['win or each Way']}}));
            component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
              if (ch === pubSubService.API.SUSPEND_IHR_EVENT_OR_MRKT ) {
                fn('555', {eventStatusCode: 'A', marketStatusCode: 'S', originalName: 'Win or Each Way'});
                expect(component.showFloatingInplayMsg).toBe(false);
              }
            });
            spyOn(component, 'checkToShowFloatingMsg').and.returnValue();
            component.ngOnInit();
          });

          it('SUSPEND_IHR_EVENT_OR_MRKT subscription, with showFloatingInplayMsg to be true', () => {
            component.racingInMeeting = [{
              id: 555,
              name: 'Leg event',
              markets: [],
              categoryCode: 'HORSE_RACING',
              isFinished: 'false',
              drilldownTagNames: 'EVFLAG_IHR'
            } as any];
            component.eventId = 555;
            component.isInplay = true;
            cmsService.getSystemConfig.and.returnValue(of({ HorseRacingBIR: {floatingMsgEnabled: 'text for testing', marketsEnabled: ['win or each Way']}}));
            component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
              if (ch === pubSubService.API.SUSPEND_IHR_EVENT_OR_MRKT ) {
                fn('555', {eventStatusCode: 'A', marketStatusCode: 'A', originalName: 'Win or Each Way'});
                expect(component.showFloatingInplayMsg).toBe(true);
              }
            });
            spyOn(component, 'checkToShowFloatingMsg').and.returnValue();
            component.ngOnInit();
          });

          it('should assign true to showFloatingInplayMsg', () => {
            component.eventEntity.rawIsOffCode  = 'Y';
            component.eventEntity.eventStatusCode = 'A';
            component.eventEntity.markets = [{marketStatusCode: 'S'} as any];
            component['isBirMarketEnabled'] = jasmine.createSpy().and.returnValue(false);
            component.checkToShowFloatingMsg();
            expect(component.showFloatingInplayMsg).toBe(true);
          });

          it('should assign false to showFloatingInplayMsg', () => {
            component.eventEntity.isStarted = true;
            component.eventEntity.eventStatusCode = 'S';
            component.eventEntity.markets = [{marketStatusCode: 'S'} as any];
            component['isBirMarketEnabled'] = jasmine.createSpy().and.returnValue(true);
            component.checkToShowFloatingMsg();
            expect(component.showFloatingInplayMsg).toBe(false);
          });

          it('should call checkToShowFloatingMsg on ngOnChanges', () => {
            const changes: SimpleChanges = {};
            const currentValue = [{
              id: 555,
              name: 'Leg event',
              markets: [],
              categoryCode: 'HORSE_RACING',
              isFinished: 'false',
              drilldownTagNames: 'EVFLAG_IHR'
            } as any];
            const previousValue = [{
              id: 111,
              name: 'Leg event',
              markets: [],
              categoryCode: 'HORSE_RACING',
              isFinished: 'false',
              drilldownTagNames: 'EVFLAG_IHR'
            } as any];
            component.racingInMeeting = currentValue;
            component.eventId = 555;
            changes.racingInMeeting = {currentValue: currentValue, previousValue: previousValue, isFirstChange: () => true, firstChange: true};
            const checkToShowFloatingMsgSpy = spyOn(component, 'checkToShowFloatingMsg').and.returnValue();
            component.floatingMsgText = 'floating message text';
            component.ngOnChanges(changes);
            expect(checkToShowFloatingMsgSpy).toHaveBeenCalled();
          });

          it('unsubscribe to be called in ngOnDestroy', () => {
            component.ngOnDestroy();
            expect(pubSubService.unsubscribe).toHaveBeenCalled();
          });
    });
  describe('#closeFloatingInplayMsg', () => {
    it('should assign showFloatingInplayMsg as false', () => {
      component.closeFloatingInplayMsg();
      expect(component.showFloatingInplayMsg).toBeFalse();
      expect(component.closeFloatingMsg).toBeFalse();
    });
    it('should push gtm object', () => {
      component.eventEntity = {
        id: 555,
        typeID: 1,
        categoryID: "21"
      } as any;
      component.closeFloatingInplayMsg();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventAction: "race card",
        eventCategory: "horse racing",
        eventLabel: "close - in-play betting",
        categoryID: component.eventEntity.categoryId,
        typeID: component.eventEntity.typeId,
        eventID: component.eventEntity.id,
      });
    });
    it('should not push gtm object', () => {
      component.eventEntity = undefined;
      component.closeFloatingInplayMsg();
      expect(gtmService.push).not.toHaveBeenCalled();
    });
  });
  describe('isBirMarketEnabled', () => {
    it('BIRMarketsEnabled', () => {
      component['BIRMarketsEnabled'] = ['Win or Each Way'];
      expect(component['isBirMarketEnabled']('Win or Each Way')).toBeTruthy();
    });
    it('isBirMarketEnabled with null input', () => {
      component['BIRMarketsEnabled'] = ['Win or Each Way'];
      expect(component['isBirMarketEnabled']()).toBeFalsy();
    });
    it('isBirMarketEnabled with BIRMarketsEnabled as null', () => {
      component['BIRMarketsEnabled'] = null;
      expect(component['isBirMarketEnabled']()).toBeFalsy();
    });
  });
});

