import { AccaNotificationComponent } from './acca-notification.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { of } from 'rxjs';

describe('AccaNotificationComponent', () => {
  let component: AccaNotificationComponent;

  let
    nativeBridgeService,
    user,
    fracToDec,
    domTools,
    pubsub,
    deviceService,
    GTM,
    windowRef,
    localeService,
    cmsService,
    changeDetectorRef,
    filterService;

  const querySelectorMock = {
    dispatchEvent: jasmine.createSpy('dispatchEvent'),
    top: 20,
    scrollIntoView: jasmine.createSpy('scrollIntoView'),

  };

  const betData = {
    potentialPayout: 2,
    price: '2'
  };

  beforeEach(() => {
    nativeBridgeService = {
      accaNotificationChanged: jasmine.createSpy('accaNotificationChanged')
    };
    user = {
      oddsFormat: 'frac'
    };
    filterService = {
      getTeamName: jasmine.createSpy('getTeamName'),
      filterPlayerName: jasmine.createSpy('filterPlayerName')
    };
    fracToDec = {
      decToFrac: jasmine.createSpy('decToFrac').and.returnValue('1/2'),
      getDecimal: jasmine.createSpy('getDecimal').and.returnValues('1.5', '1.75', '2.125'),
      roundTwoFraction: jasmine.createSpy('roundTwoFraction').and.returnValue('123.12'),
      getAccumulatorPrice: jasmine.createSpy('getAccumulatorPrice').and.returnValue('0.5/1')
    };
    domTools = {
      getOffset: jasmine.createSpy().and.returnValue({
        top: 20
      }),
      closest: jasmine.createSpy()
    };
    pubsub = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publishSync: jasmine.createSpy('publishSync'),
      subscribe: jasmine.createSpy('subscribe')
    };
    deviceService = {};
    GTM = {
      push: jasmine.createSpy()
    };
    windowRef = {
      document: {
        querySelector: jasmine.createSpy('querySelector').and.returnValue({
          scrollTop: 5,
          scrollHeight: 100499,
          offsetWidth: 345
        })
      },
      nativeWindow: {
        document: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue(querySelectorMock),
          documentElement: {
            clientHeight: 100500
          },
        },
        getComputedStyle: jasmine.createSpy().and.returnValue({paddingLeft: '15'}),
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn())
      }
    };

    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('')
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig')
    };

    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };

    component = new AccaNotificationComponent(
      nativeBridgeService,
      user,
      fracToDec,
      domTools,
      pubsub,
      deviceService,
      GTM,
      windowRef,
      localeService,
      cmsService,
      changeDetectorRef,
      filterService
      );
    });

  it('constructor', () => {
    expect(component).toBeDefined();
    expect(component.minPayout).toBe(1.00099);
    expect(component.animationDuration).toBe(2000);
  });

  describe('onInit', () => {

    beforeEach(() => {
      spyOn(component, 'getCmsConfig');
      spyOn(component, 'subscribeToBsUpdate');
      spyOn(component, 'updateAccaData');
      pubsub.subscribe.and.callFake((a, b, cb) => {
        cb && cb(true);
      });
    });

    it('should make pubSub subscribtions on acca change (ACCA_NOTIFICATION_CHANGED)', () => {
      component.ngOnInit();

      expect(pubsub.subscribe).toHaveBeenCalledWith('bma-accaBar', 'ACCA_NOTIFICATION_CHANGED', jasmine.any(Function));
      expect(component.updateAccaData).toHaveBeenCalled();
    });

    it('should subscribe on timeline displaying change (TIMELINE_SHOWN)', () => {
      component.ngOnInit();

      expect(pubsub.subscribe).toHaveBeenCalledWith('bma-accaBar', 'TIMELINE_SHOWN', jasmine.any(Function));
      expect(component.timelineShown).toBeTruthy();
    });

    it('should subscribe on network indicator displaying change (NW_INDICATOR_DISPLAY)', () => {
      component.ngOnInit();

      expect(pubsub.subscribe).toHaveBeenCalledWith('bma-accaBar', 'NW_INDICATOR_DISPLAY', jasmine.any(Function));
      expect(component.timelineShown).toBeTruthy();
    });

    it('should call subscribeToBsUpdate and getCmsConfig', () => {
      component.ngOnInit();

      expect(component.getCmsConfig).toHaveBeenCalled();
      expect(component.subscribeToBsUpdate).toHaveBeenCalled();
    });
  });

  describe('ngOnDestroy', () => {

    it('should unsubscribe', () => {
      component.ngOnDestroy();

      expect(pubsub.unsubscribe).toHaveBeenCalled();
    });
  });

  describe('updateAccaData', () => {

    it('should get acca name', () => {
      component.updateAccaData({translatedType: 'foo'});

      expect(localeService.getString).toHaveBeenCalledWith('bs.foo');
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should round payout', () => {
      component.updateAccaData({translatedType: 'foo', potentialPayout: 123.12345});

      expect(fracToDec.roundTwoFraction).toHaveBeenCalledWith(123.12345);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should not round payout without data', () => {
      component.updateAccaData({});

      expect(fracToDec.roundTwoFraction).not.toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should not even get acca type if no data', () => {
      component.updateAccaData(null);

      expect(localeService.getString).not.toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should set bet as valid if payout greater than min', () => {
      expect(component.isBetValid).toBe(false);

      component.updateAccaData({translatedType: 'foo', potentialPayout: 2});

      expect(component.isBetValid).toBe(true);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should set bet as not valid if payout less than min', () => {
      expect(component.isBetValid).toBe(false);

      component.updateAccaData({translatedType: 'foo', potentialPayout: 1});

      expect(component.isBetValid).toBe(false);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should set bet as not valid if payout not a number', () => {
      expect(component.isBetValid).toBe(false);

      component.updateAccaData({translatedType: 'foo', potentialPayout: '123'} as any);

      expect(component.isBetValid).toBe(false);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should notify bridge without data (bet not valid)', () => {
      component.updateAccaData({});

      expect(nativeBridgeService.accaNotificationChanged).toHaveBeenCalledWith();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should notify bridge with data (bet is valid)', () => {
      component.updateAccaData({translatedType: 'DBL', potentialPayout: 3});

      expect(nativeBridgeService.accaNotificationChanged).toHaveBeenCalledWith({
        title: 'DBL',
        price: jasmine.any(String)
      });
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should use decimal value for price', () => {
      user.oddsFormat = 'dec';
      component.updateAccaData({translatedType: 'DBL', potentialPayout: 3});

      expect(component.price).toBe('123.12');
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should use fractional value for price', () => {
      component.updateAccaData({translatedType: 'DBL', potentialPayout: 123.123});

      expect(fracToDec.decToFrac).toHaveBeenCalledWith(123.123, true);
      expect(fracToDec.getAccumulatorPrice).toHaveBeenCalledWith('1/2');
      expect(component.price).toBe('0.5/1');
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should not calculate and finish animation if not enabled', () => {
      expect(component['isAnimationEnabled']).not.toBeDefined();

      component.updateAccaData({});

      expect(windowRef.nativeWindow.setTimeout).not.toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should not calculate and finish animation if not yet started', () => {
      expect(component['animationStart']).not.toBeDefined();
      component['isAnimationEnabled'] = true;

      component.updateAccaData({});

      expect(windowRef.nativeWindow.setTimeout).not.toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should calculate and finish animation if ready', () => {
      component['animationStart'] = 123;
      component['isAnimationEnabled'] = true;
      component.isLoadingAnimationActive = true;

      component.updateAccaData({});

      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), jasmine.any(Number));
      expect(component.isLoadingAnimationActive).toBe(false);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalledTimes(2);
    });

    it('should calculate remaining animation time', () => {
      component['animationStart'] = 123;
      component['isAnimationEnabled'] = true;
      spyOn(Date, 'now').and.returnValue(500);

      component.updateAccaData({});

      expect(windowRef.nativeWindow.setTimeout.calls.argsFor(0)[1]).toBe(1623);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalledTimes(2);
    });
  });

  describe('getCmsConfig', () => {

    beforeEach(() => {
      expect(component['isRecalculationEnabled']).not.toBeDefined();
      expect(component['isAnimationEnabled']).not.toBeDefined();
    });

    it('should set props (all enabled)', () => {
      cmsService.getSystemConfig.and.returnValue(of({accaQuickRecalculation: {enabled: true, allowLoadingAnimation: true}}));
      component.getCmsConfig();

      expect(component['isRecalculationEnabled']).toBe(true);
      expect(component['isAnimationEnabled']).toBe(true);
    });

    it('should set props (all disabled)', () => {
      cmsService.getSystemConfig.and.returnValue(of({accaQuickRecalculation: {enabled: false, allowLoadingAnimation: false}}));
      component.getCmsConfig();

      expect(component['isRecalculationEnabled']).toBe(false);
      expect(component['isAnimationEnabled']).toBe(false);
    });

    it('should set props (not set)', () => {
      cmsService.getSystemConfig.and.returnValue(of({}));
      component.getCmsConfig();

      expect(component['isRecalculationEnabled']).toBe(false);
      expect(component['isAnimationEnabled']).toBe(false);
    });

    it('should set props (only animation fallback)', () => {
      cmsService.getSystemConfig.and.returnValue(of({accaQuickRecalculation: {enabled: false, allowLoadingAnimation: true}}));
      component.getCmsConfig();

      expect(component['isRecalculationEnabled']).toBe(false);
      expect(component['isAnimationEnabled']).toBe(true);
    });
  });

  describe('subscribeToBsUpdate', () => {
    let calculateAccaDataSpy;

    beforeEach(() => {
      calculateAccaDataSpy = spyOn(component, 'calculateAccaData');
      pubsub.subscribe.and.callFake((a, method, cb) => {
        if (cb && method === pubSubApi.BETSLIP_SELECTIONS_UPDATE) {
          cb(betData);
        }
      });
    });

    it('should subscribe to bs updates', () => {
      component.subscribeToBsUpdate();

      expect(pubsub.subscribe.calls.argsFor(0)[1]).toBe(pubSubApi.BETSLIP_SELECTIONS_UPDATE);
      expect(changeDetectorRef.markForCheck).not.toHaveBeenCalled();
    });

    it('should recalculate data', () => {
      component['isRecalculationEnabled'] = true;
      component.subscribeToBsUpdate();

      expect(calculateAccaDataSpy).toHaveBeenCalledWith([betData]);
      expect(changeDetectorRef.markForCheck).not.toHaveBeenCalled();
    });

    it('should use fallback animation', () => {
      expect(component['animationStart']).not.toBeDefined();

      component.isBetValid = true;
      component.isLoadingAnimationActive = false;
      component['isRecalculationEnabled'] = false;
      component['isAnimationEnabled'] = true;
      component.subscribeToBsUpdate();

      expect(component['isLoadingAnimationActive']).toBe(true);
      expect(component['animationStart']).toBeDefined();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should not start fallback animation (not yet displayed)', () => {
      expect(component['animationStart']).not.toBeDefined();

      component.isBetValid = false;
      component.isLoadingAnimationActive = false;
      component['isRecalculationEnabled'] = false;
      component['isAnimationEnabled'] = true;
      component.subscribeToBsUpdate();

      expect(component['isLoadingAnimationActive']).toBe(false);
      expect(component['animationStart']).not.toBeDefined();
      expect(changeDetectorRef.markForCheck).not.toHaveBeenCalled();
    });

    it('should not start fallback animation again (already in progress)', () => {
      component.isBetValid = true;
      component.isLoadingAnimationActive = true;
      component['animationStart'] = 12345;
      component['isRecalculationEnabled'] = false;
      component['isAnimationEnabled'] = true;
      component.subscribeToBsUpdate();

      expect(component['isLoadingAnimationActive']).toBe(true);
      expect(component['animationStart']).toBe(12345);
      expect(changeDetectorRef.markForCheck).not.toHaveBeenCalled();
    });
  });

  describe('#focusOnMultiple', () => {
    it('should focus input', fakeAsync(() => {
      component.focusOnMultiple();
      tick(1000);
      expect(GTM.push).toHaveBeenCalledWith('trackEvent', {
        eventAction: 'click ',
        eventLabel: 'odds notification banner'
      });
      expect(querySelectorMock.dispatchEvent).toHaveBeenCalled();
      expect(pubsub.publishSync).toHaveBeenCalledWith('show-slide-out-betslip', true);
    }));
  });

  it('scrollToFn', () => {
    spyOn(component, 'getCmsConfig');
    spyOn(component, 'subscribeToBsUpdate');
    windowRef.nativeWindow.document.querySelector = jasmine.createSpy().and.returnValue({
      ...querySelectorMock,
      scrollHeight: 100505
    });
    const firstMultiple={scrollIntoView:jasmine.createSpy('scrollIntoView')}
    component.ngOnInit();
    component['scrollToFn'](100501,firstMultiple);

    expect(component.homeBody.scrollTop).toEqual(0);
  });

  describe('getAccaTypeByCount', () => {

    it('fallback - should return empty string if acca impossible', () => {
      expect(component.getAccaTypeByCount(0)).toBe('');
      expect(component.getAccaTypeByCount(1)).toBe('');
      expect(component.getAccaTypeByCount(undefined)).toBe('');
    });

    it('DBL', () => {
      expect(component.getAccaTypeByCount(2)).toBe('DBL');
    });

    it('TBL', () => {
      expect(component.getAccaTypeByCount(3)).toBe('TBL');
    });

    it('acca 4-9', () => {
      expect(component.getAccaTypeByCount(4)).toBe('ACC4');
      expect(component.getAccaTypeByCount(9)).toBe('ACC9');
    });

    it('acca 10-15', () => {
      expect(component.getAccaTypeByCount(10)).toBe('AC10');
      expect(component.getAccaTypeByCount(15)).toBe('AC15');
    });
  });

  describe('#filterPlayerName', () => {

    it('should filter player name, home case', () => {
      component.filterPlayerName("home", "ind vs pak");
      expect(filterService.getTeamName).toHaveBeenCalled();
    });

    it('should filter player name, away case', () => {
      component.filterPlayerName("away", "ind vs pak");
      expect(filterService.getTeamName).toHaveBeenCalled();
    });

    it('should filter player name, draw case', () => {
      component.filterPlayerName("draw", "ind vs pak");
      expect(filterService.getTeamName).not.toHaveBeenCalled();
    });

  });

  describe('#getDivWidth', () => {
    
    const selectionNames = ['Szymon Twardowski', 'Vaclav Hruska Jr'];
    it('if element acca is not null and selection names not null', () => {
      component.getDivWidth(selectionNames);

      windowRef.nativeWindow.document.querySelector = jasmine.createSpy().and.returnValue({
        offsetWidth: 345
      });
      expect(component.getDivWidth(selectionNames)).toBe("Szymon Twardowski, Vaclav Hruska Jr");
    });

    it('if selection names more than div width', () => {
      const selectionNames = ['Szymon Twardowski', 'Vaclav Hruska Jr', 'Jakarta BIN O2C Women'];
      component.getDivWidth(selectionNames);
      windowRef.nativeWindow.document.querySelector = jasmine.createSpy().and.returnValue({
        offsetWidth: 345
      });
      expect(component.getDivWidth(selectionNames)).toBe("Szymon Twardowski, Vaclav Hruska Jr, (+1)");
    });

    it('if selection names not more than div width', () => {
      const selectionNames = ['Shanxi Zhongyu', 'J. Maio/L. Palermo'];
      component.getDivWidth(selectionNames);
      windowRef.nativeWindow.document.querySelector = jasmine.createSpy().and.returnValue({
        offsetWidth: 345
      });
      expect(component.getDivWidth(selectionNames)).toBe("Shanxi Zhongyu, J. Maio/L. Palermo");
    });

    it('if the first selection name is too lengthy', () => {
      const selectionNames = ['Test selection to test add selections to Accabar is too lenghty', 'J. Maio/L. Palermo'];
      component.getDivWidth(selectionNames);
      windowRef.nativeWindow.document.querySelector = jasmine.createSpy().and.returnValue({
        offsetWidth: 345
      });
      expect(component.getDivWidth(selectionNames)).toBe("Test selection to test add selections to Accabar i...(+1)");
    });

  });

  describe('calculateAccaData', () => {

    beforeEach(() => {
      spyOn(component, 'getAccaTypeByCount').and.returnValue('ACC');
    });

    beforeEach(() => {
      spyOn(component, 'filterPlayerName').and.returnValue('Jamaicwwwwwwwwwwww');
    });

    it('fallback - should emit empty object (no selections)', () => {
      component.calculateAccaData([]);

      expect(pubsub.publishSync).toHaveBeenCalledWith('ACCA_NOTIFICATION_CHANGED', {});
    });

    it('fallback - should emit empty object (only one selection)', () => {
      component.calculateAccaData([{}] as any);

      expect(pubsub.publishSync).toHaveBeenCalledWith('ACCA_NOTIFICATION_CHANGED', {});
      expect(component.getAccaTypeByCount).not.toHaveBeenCalled();
    });

    it('should not build acca if more than one selection of same event', () => {
      
      component.calculateAccaData([{
        eventId: 111,
        price: { priceNum: 1, priceDen: 2},
        outcomes: [ {
          "details":{
            "info" : {
              "event" : 'abc v def'
            }
          },
          "name": "home"
        }],
      }, {
        eventId: 111,
        price: { priceNum: 3, priceDen: 4},
        outcomes: [ {
          "details":{
            "info" : {
              "event" : 'India v Pak'
            }
          },
          "name": "draw"
        }],
      }, {
        eventId: 222,
        price: { priceNum: 9, priceDen: 8},
        outcomes: [ {
          "details":{
            "info" : {
              "event" : 'munic v Jamaic'
            }
          },
          "name": "away"
        }],
      }] as any);

      expect(fracToDec.getDecimal).toHaveBeenCalledTimes(3);
      const calls0 = fracToDec.getDecimal.calls.argsFor(0);
      expect(calls0).toEqual([1, 2, 16]);
      const calls1 = fracToDec.getDecimal.calls.argsFor(1);
      expect(calls1).toEqual([3, 4, 16]);
      const calls2 = fracToDec.getDecimal.calls.argsFor(2);
      expect(calls2).toEqual([9, 8, 16]);

      expect(component.getAccaTypeByCount).not.toHaveBeenCalled();
      expect(pubsub.publishSync).toHaveBeenCalledWith('ACCA_NOTIFICATION_CHANGED', {});
    });

    it('should not build acca if at least one selection is special', () => {
      component.calculateAccaData([{
        eventId: 111,
        price: { priceNum: 1, priceDen: 2},
        outcomes: [ {
          "details":{
            "info" : {
              "event" : 'abc v def'
            }
          },
          "name": "home"
        }],
      }, {
        eventId: 222,
        price: { priceNum: 3, priceDen: 4},
        outcomes: [ {
          "details":{
            "info" : {
              "event" : 'India v Pak'
            }
          },
          "name": "draw"
        }],
      }, {
        eventId: 333,
        price: { priceNum: 9, priceDen: 8},
        isSpecial: true,
        outcomes: [ {
          "details":{
            "info" : {
              "event" : 'munic v Jamaic'
            }
          },
          "name": "away"
        }],
      }] as any);

      expect(fracToDec.getDecimal).toHaveBeenCalledTimes(3);

      expect(component.getAccaTypeByCount).not.toHaveBeenCalled();
      expect(pubsub.publishSync).toHaveBeenCalledWith('ACCA_NOTIFICATION_CHANGED', {});
    });

    it('should build TBL acca bar', () => {
      component.calculateAccaData([{
        eventId: 111,
        price: { priceNum: 1, priceDen: 2},
        eventName: 'abcqqqqqqqqqqqqqqqqqqqqqqqq v defuuuuuuuuuuuuuuuuuu',
        outcomes: [ {
          "details":{
            "info" : {
              "event" : 'abcqqqqqqqqqqqqqqqqqqqqqqqq v defuuuuuuuuuuuuuuuuuu'
            }
          },
          "name": "home"
        }],
      }, {
        eventId: 222,
        price: { priceNum: 3, priceDen: 4},
        eventName: 'Indiadsssssssssss v Paksssssssssssssssssss',
        outcomes: [ {
          "details":{
            "info" : {
              "event" : 'Indiadsssssssssss v Paksssssssssssssssssss'
            }
          },
          "name": "draw"
        }],
      }, {
        eventId: 333,
        price: { priceNum: 9, priceDen: 8},
        eventName: 'municyyyyyyyyy v Jamaicwwwwwwwwwwww',
        outcomes: [ {
          "details":{
            "info" : {
              "event" : 'municyyyyyyyyy v Jamaicwwwwwwwwwwww'
            }
          },
          "name": "away"
        }],
      }] as any);

      expect(fracToDec.getDecimal).toHaveBeenCalledTimes(3);

      expect(component.getAccaTypeByCount).toHaveBeenCalledWith(3);
      expect(component.filterPlayerName).toHaveBeenCalledTimes(3);
      expect(pubsub.publishSync).toHaveBeenCalledWith('ACCA_NOTIFICATION_CHANGED', {
        translatedType: 'ACC',
        potentialPayout: 5.578125
      });
    });


    it('should call else if eventName property does not exist', () => {
      component.calculateAccaData([{
        eventId: 111,
        price: { priceNum: 1, priceDen: 2},
        outcomes: [ {
          "details":{
            "info" : {
              "event" : 'abcqqqqqqqqqqqqqqqqqqqqqqqq v defuuuuuuuuuuuuuuuuuu'
            }
          },
          "name": "home"
        }]
      }, {
        eventId: 222,
        price: { priceNum: 3, priceDen: 4},
        outcomes: [ {
          "details":{
            "info" : {
              "event" : 'Indiadsssssssssss v Paksssssssssssssssssss'
            }
          },
          "name": "draw"
        }]
      }, {
        eventId: 333,
        price: { priceNum: 9, priceDen: 8},
        outcomes: [ {
          "details":{
            "info" : {
              "event" : 'municyyyyyyyyy v Jamaicwwwwwwwwwwww'
            }
          },
          "name": "away"
        }]
      }] as any);

      expect(component.filterPlayerName).toHaveBeenCalled();

    });

  });
});
