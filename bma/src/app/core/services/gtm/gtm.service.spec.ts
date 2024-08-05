import { GtmService } from './gtm.service';
import * as _ from 'underscore';

describe('GtmService', () => {
  let service;
  let user;
  let device;
  let storage;
  let pubsub;
  let windowRef;
  let sessionStorage;
  const betTrackingData = [
    {
      GTMObject: {
        betData: {
          dimension94: 1
        }
      },
      outcomeId: ['2132112']
    }
  ];
  beforeEach(() => {
    user = {};

    device = {
      deliveryPlatform: 'deliveryPlatform',
      isMobile: true
    };

    storage = {
      get: jasmine.createSpy()
    };

    pubsub = {
      subscribe: jasmine.createSpy(),
      API: {
        SET_PLAYER_INFO: 'SET_PLAYER_INFO'
      }
    };

    windowRef = {
      nativeWindow: {
        gcData: {}
      }
    };

    sessionStorage = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get').and.returnValue(betTrackingData)
    }
    service = new GtmService(user, device, storage, pubsub, windowRef, sessionStorage);
  });

  it('should subscribe on pubsub events', () => {
    expect(pubsub.subscribe).toHaveBeenCalledTimes(2);
  });

  it('init', () => {
    const gcData = {
      brand: 'Coral',
      userInterfaceName: 'Oxygen',
      signUpDeliveryPlatform: 'deliveryPlatform',
      userInterface: 'userInterface'
    };
    service['getUserInterface'] = jasmine.createSpy().and.returnValue('userInterface');
    service['extendBmaData'] = jasmine.createSpy();
    service.init();

    expect(service['extendBmaData']).toHaveBeenCalled();
    expect(service['getUserInterface']).toHaveBeenCalled();
    //expect(service.windowRef.nativeWindow.gcData).toEqual(gcData);
  });

  describe('#isConvertibleUser', () => {
    it('should return false when username is true and username from storage is true', () => {
      service.storage.get = jasmine.createSpy().and.returnValue(true);
      service.user.username = true;
      const actualResult = service['isConvertibleUser']();

      expect(actualResult).toEqual(false);
    });

    it('should return true when username is false and username from storage is false', () => {
      service.storage.get = jasmine.createSpy().and.returnValue(false);
      service.user.username = false;
      const actualResult = service['isConvertibleUser']();

      expect(actualResult).toEqual(true);
    });

    it('should return false when username is false and username from storage is true', () => {
      service.storage.get = jasmine.createSpy().and.returnValue(true);
      service.user.username = false;
      const actualResult = service['isConvertibleUser']();

      expect(actualResult).toEqual(false);
    });

    it('should return false when username is true and username from storage is false', () => {
      service.storage.get = jasmine.createSpy().and.returnValue(false);
      service.user.username = true;
      const actualResult = service['isConvertibleUser']();

      expect(actualResult).toEqual(false);
    });
  });

  describe('#getUserType', () => {
    it('getUserType: Logged in Customer', () => {
      service.user.username = true;
      const actualResult = service['getUserType']();

      expect(actualResult).toEqual('Logged in Customer');
    });

    it('getUserType: Browsing Customer', () => {
      service.user.username = false;
      service.storage.get = jasmine.createSpy().and.returnValue(true);
      const actualResult = service['getUserType']();

      expect(actualResult).toEqual('Browsing Customer');
    });

    it('getUserType: Visitor', () => {
      service.user.username = false;
      service.storage.get = jasmine.createSpy().and.returnValue(false);
      const actualResult = service['getUserType']();

      expect(actualResult).toEqual('Visitor');
    });
  });

  describe('#getUserInterface', () => {
    it('getUserInterface: HTML5', () => {
      service.device.deliveryPlatform = 'HTML5';
      const actualResult = service['getUserInterface']();

      expect(actualResult).toEqual('HTML5');
    });

    it('getUserInterface: Wrapped App', () => {
      service.device.deliveryPlatform = 'Wrapped App';
      const actualResult = service['getUserInterface']();

      expect(actualResult).toEqual('Wrapped App');
    });
  });

  it('getUserIds', () => {
    const userIds = {
      player_id: service.user.playerCode = '01',
      profile_id: service.user.profileId = '01'
    };
    const actualResult = service['getUserIds']();

    expect(actualResult).toEqual(userIds);
  });

  it('formatErrorMessage', () => {
    expect(service.formatErrorMessage(' __string__ ')).toEqual('string');
  });

  it('signUpClick', () => {
    const signUpTrackEvent = {
      event: 'trackEvent',
      eventCategory: 'registration',
      eventAction: 'click',
      eventLabel: 'join now'
    };
    service.device.isMobile = true;
    service.push = jasmine.createSpy();
    service.signUpClick();

    expect(service.push).toHaveBeenCalledWith(signUpTrackEvent.event, signUpTrackEvent);
  });

  it('pushLogoutInfo', () => {
    service['getUserIds'] = jasmine.createSpy().and.returnValue({
      player_id: '01',
      profile_id: '01'
    });
    service['platform'] = { 'signup-delivery-platform': 'deliveryPlatform' };
    service['extendBmaData'] = jasmine.createSpy();
    service.push = jasmine.createSpy();
    service.pushLogoutInfo();
    const gtmData = _.extend({ success: 'true' }, service['getUserIds'](), service['platform']);

    expect(service['extendBmaData']).toHaveBeenCalled();
    expect(service.push).toHaveBeenCalledWith('logout', gtmData);
  });

  it('pushBetPlacementErrorInfo', () => {
    const data = { success: 'true' };
    service['platform'] = { 'signup-delivery-platform': 'deliveryPlatform' };
    service.push = jasmine.createSpy();
    service.pushBetPlacementErrorInfo(data);

    expect(service.push).toHaveBeenCalledWith('bet_placement_error', data);
  });

  it('push', () => {
    windowRef.nativeWindow.dataLayer = [];
    service.push('event1', { eventLabel: 'click' });
    expect(windowRef.nativeWindow.dataLayer).toEqual([{ event: 'event1', eventLabel: 'click' }]);
  });

  it('push (gtm not loaded)', () => {
    windowRef.nativeWindow.dataLayer = undefined;
    service.push('event1', { eventLabel: 'click' });
    expect(service.cachedEvents).toEqual([{ event: 'event1', eventLabel: 'click' }]);
  });

  it('pushCachedEvents', () => {
    windowRef.nativeWindow.dataLayer = [];
    service.cachedEvents = [{ event: 'event1', eventLabel: 'click' }];

    service.pushCachedEvents();

    expect(windowRef.nativeWindow.dataLayer).toEqual([{ event: 'event1', eventLabel: 'click' }]);
    expect(service.cachedEvents).toEqual([]);
  });

  it('should call getSBTrackingData', () => {
    const returnData = service.getSBTrackingData();
    expect(returnData).not.toBeNull();
  });

  it('should call getSBTrackingData with empty data', () => {
    sessionStorage.get.and.returnValue(null);
    const returnData = service.getSBTrackingData();
    expect(returnData).toEqual([]);
  });

  describe('setSBTrackingData', () => {

    it('should return false if no GTMObject in tracking data', () => {
      const gtmData = {};
      const returnValue = service.setSBTrackingData(gtmData);
      expect(returnValue).toBe(false);
      expect(sessionStorage.set).not.toHaveBeenCalled();
    })
    it('should return false if no betDatain GTMObject', () => {
      const gtmData = {GTMObject:{}};
      const returnValue = service.setSBTrackingData(gtmData);
      expect(returnValue).toBe(false);
      expect(sessionStorage.set).not.toHaveBeenCalled();
    });
    it('should set gtm data', () => {
      const gtmData = {GTMObject:{betData:{dimension94:1}}, outcomeId: ['2132112']};
      service.setSBTrackingData(gtmData);
      expect(sessionStorage.set).toHaveBeenCalledWith(service.sbTracking, [gtmData]);
    });

    it('should push new gtm object', () => {
      const gtmData = {GTMObject:{betData:{dimension94:1}}, outcomeId: ['21435245']};
      const expectedObj = [...betTrackingData, gtmData];
      service.setSBTrackingData(gtmData);
      expect(sessionStorage.set).toHaveBeenCalledWith(service.sbTracking, expectedObj);
    });

    it('should move to else condition', () => {
      service['getSBTrackingData'] = jasmine.createSpy('getSBTrackingData').and.returnValue([]);
      const gtmData = {GTMObject:{betData:{dimension94:1}}, outcomeId: ['2132112']};
      service.setSBTrackingData(gtmData);
      expect(sessionStorage.set).toHaveBeenCalledWith(service.sbTracking, [gtmData]);
    });
  });

  describe('removeSBTrackingItem', () => {
    it('should remove item from array', () => {
      const trackingData = {GTMObject:{betData:{dimension94:1}}, outcomeId: ['2132112']};
      service['getSBTrackingData'] = jasmine.createSpy('getSBTrackingData').and.returnValue([trackingData]);
      service.removeSBTrackingItem(trackingData);
      expect(sessionStorage.set).toHaveBeenCalledWith(service.sbTracking, []);
    })
  })
});
