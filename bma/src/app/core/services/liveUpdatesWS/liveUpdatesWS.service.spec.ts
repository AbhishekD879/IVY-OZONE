import { Subject } from 'rxjs';

import { LiveUpdatesWSService } from './liveUpdatesWS.service';

describe('LiveUpdatesWSService', () => {
  let service: LiveUpdatesWSService;
  let pubSubService;
  let liveServConnectionService;

  beforeEach(() => {
    pubSubService = {
      __cbMap: {},
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy().and.callFake((name, channel, cb) => pubSubService.__cbMap[channel] = cb),
      API: {
        LIVE_SERVE_MS_UPDATE: 'LIVE_SERVE_MS_UPDATE'
      }
    };
    liveServConnectionService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      connect: jasmine.createSpy('connect'),
      onDisconnect: jasmine.createSpy('onDisconnect'),
      isDisconnected: jasmine.createSpy('isDisconnected')
    };

    service = new LiveUpdatesWSService(
      pubSubService,
      liveServConnectionService
    );
  });

  describe('constructor', () => {
    it('basic test', () => {
      expect(service).toBeTruthy();
    });
  });

  describe('subscribe', () => {
    let channels, result, expectedKey;

    beforeEach(() => {
      channels = ['1', '2', '3'];
      service['subscribeMapQueue'] = { 'sport-matches': ['5', '6'] };
      service['unsubscribeMapQueue'] = { id2: ['3', '4'] };
      spyOn(Date, 'now').and.returnValue(1234567);
      spyOn(service as any, 'fetchSubscriptions');
    });

    describe('should add channels array to subscription queue and fetch LS subscriptions', () => {
      it('(by module name)', () => {
        expectedKey = 'sport-matches';
        result = service.subscribe(channels, 'sport-matches');
        expect(service['subscribeMapQueue']).toEqual({ 'sport-matches': ['1', '2', '3']  });
      });
      it('(by channel ids)', () => {
        expectedKey = '1,2,3-1234567';
        result = service.subscribe(channels);
        expect(Date.now).toHaveBeenCalled();
        expect(service['subscribeMapQueue']).toEqual({ 'sport-matches': ['5', '6'], '1,2,3-1234567': ['1', '2', '3'] });
      });
      afterEach(() => {
        expect(result).toEqual(expectedKey);
        expect(service['unsubscribeMapQueue']).toEqual({ id2: ['3', '4'] });
        expect(service['fetchSubscriptions']).toHaveBeenCalled();
      });
    });
  });

  describe('unsubscribe', () => {
    beforeEach(() => {
      service['subscribersMap'] = { id2: ['5', '6'] };
      service['unsubscribeMapQueue'] = { id2: ['7'], id3: ['8'] };
      service['subscribeMapQueue'] = { id1: ['1', '2'], id2: ['3', '4'] };
      spyOn(service as any, 'fetchSubscriptions');
    });

    describe('if channels id is present in current subscriptions', () => {
      beforeEach(() => {
        service.unsubscribe('id1');
      });
      it('should only remove channels array from subscription queue', () => {
        expect(service['unsubscribeMapQueue']).toEqual({ id2: ['7'], id3: ['8'] });
        expect(service['subscribeMapQueue']).toEqual({ id2: ['3', '4'] });
      });
      it('should not fetch LS subscription', () => {
        expect(service['fetchSubscriptions']).not.toHaveBeenCalled();
      });
    });

    describe('if channels id is present in current subscriptions', () => {
      beforeEach(() => {
        service.unsubscribe('id2');
      });
      it('should remove channels array from subscription queue', () => {
        expect(service['subscribeMapQueue']).toEqual({ id1: ['1', '2'] });
      });
      it('should add channels array to unsubscription queue', () => {
        expect(service['unsubscribeMapQueue']).toEqual({ id2: ['5', '6'], id3: ['8'] });
      });
      it('should fetch LS subscription', () => {
        expect(service['fetchSubscriptions']).toHaveBeenCalled();
      });
    });

    afterEach(() => {
      expect(service['subscribersMap']).toEqual({ id2: ['5', '6'] });
    });
  });

  describe('fetchSubscriptions', () => {
    let connection$;
    const connection = Symbol('connection');
    beforeEach(() => {
      connection$ = new Subject();
      liveServConnectionService.connect.and.returnValue(connection$);
      spyOn(service as any, 'connectHandler').and.callThrough();
      spyOn(service as any, 'updateSubscriptions');
      service['fetchSubscriptions']();
    });

    it('should connect to LS', () => {
      expect(liveServConnectionService.connect).toHaveBeenCalled();
    });
    it('should call connectHandler with proper context when connection is resolved', () => {
      connection$.next(connection);
      expect(service['connectHandler']).toHaveBeenCalled();
      expect(service['updateSubscriptions']).toHaveBeenCalled();
      expect(liveServConnectionService.onDisconnect).toHaveBeenCalledWith(service['disconnectHandler']);
    });
  });

  describe('connectHandler', () => {
    let callback;
    beforeEach(() => {
      callback = () => {};
      spyOn(service as any, 'updateSubscriptions');
      liveServConnectionService.onDisconnect.and.callFake(fn => callback = fn);
      service['connectHandler']();
    });

    it('should call updateSubscriptions method and add LS onDisconnect handler', () => {
      expect(service['updateSubscriptions']).toHaveBeenCalled();
      expect(liveServConnectionService.onDisconnect).toHaveBeenCalledWith(service['disconnectHandler']);
    });
    it('should add LS onDisconnect handler with proper context', () => {
      liveServConnectionService.isDisconnected.and.returnValue(false);
      spyOn(service as any, 'fetchSubscriptions');
      callback('error');
      expect(liveServConnectionService.isDisconnected).toHaveBeenCalledWith('error');
    });
  });


  describe('updateSubscriptions should process queues and clear them', () => {
    beforeEach(() => {
      service['subscribersMap'] = { id1: ['11', '12'], id3: ['31', '32'] };
      service['unsubscribeMapQueue'] = { id1: ['11u', '12u'], id2: ['21u', '22u'] };
      service['subscribeMapQueue'] = { id2: ['23s', '24s'], id3: ['31s', '32s'] };
      spyOn(service as any, 'getChannelsList').and.callThrough();
    });
    describe('when both subscription/unsubscription queues are not empty', () => {
      beforeEach(() => {
        service['updateSubscriptions']();
      });
      it('should get channels lists for unsubscribe and subscribe queue', () => {
        expect((service as any).getChannelsList.calls.allArgs()).toEqual([
          [{ id1: ['11u', '12u'], id2: ['21u', '22u'] }],
          [{ id2: ['23s', '24s'], id3: ['31s', '32s'] }]
        ]);
      });

      it('should call liveServConnectionService unsubscribe before subscribe', () => {
        expect(liveServConnectionService.unsubscribe).toHaveBeenCalledWith(['11u', '12u', '21u', '22u'], service['liveServeUpdateHandler']);
        expect(liveServConnectionService.unsubscribe).toHaveBeenCalledBefore(liveServConnectionService.subscribe);
        expect(liveServConnectionService.subscribe).toHaveBeenCalledWith(['23s', '24s', '31s', '32s'], service['liveServeUpdateHandler']);
      });

      it('should update subscribers map according to queues', () => {
        expect((service as any).subscribersMap).toEqual({ id2: ['23s', '24s'], id3: ['31s', '32s'] });
      });
    });

    describe('when only unsubscription queue is not empty', () => {
      beforeEach(() => {
        service['subscribeMapQueue'] = {};
        service['updateSubscriptions']();
      });
      it('should get channels lists for unsubscribe and subscribe queue', () => {
        expect((service as any).getChannelsList.calls.allArgs()).toEqual([
          [{ id1: ['11u', '12u'], id2: ['21u', '22u'] }],
          [{}]
        ]);
      });

      it('should call only liveServConnectionService unsubscribe', () => {
        expect(liveServConnectionService.unsubscribe).toHaveBeenCalledWith(['11u', '12u', '21u', '22u'], service['liveServeUpdateHandler']);
        expect(liveServConnectionService.subscribe).not.toHaveBeenCalled();
      });

      it('should update subscribers map according to queues', () => {
        expect((service as any).subscribersMap).toEqual({ id3: ['31', '32'] });
      });
    });

    describe('when only subscription queue is not empty', () => {
      beforeEach(() => {
        service['unsubscribeMapQueue'] = {};
        service['updateSubscriptions']();
      });
      it('should get channels lists for unsubscribe and subscribe queue', () => {
        expect((service as any).getChannelsList.calls.allArgs()).toEqual([
          [{}],
          [{ id2: ['23s', '24s'], id3: ['31s', '32s'] }]
        ]);
      });

      it('should call only liveServConnectionService subscribe', () => {
        expect(liveServConnectionService.unsubscribe).not.toHaveBeenCalled();
        expect(liveServConnectionService.subscribe).toHaveBeenCalledWith(['23s', '24s', '31s', '32s'], service['liveServeUpdateHandler']);
      });

      it('should update subscribers map according to queues', () => {
        expect((service as any).subscribersMap).toEqual({ id1: ['11', '12'], id2: ['23s', '24s'], id3: ['31s', '32s'] });
      });
    });
    describe('when both subscription/unsubscription queues are empty', () => {
      beforeEach(() => {
        service['unsubscribeMapQueue'] = {};
        service['subscribeMapQueue'] = {};
        service['updateSubscriptions']();
      });
      it('should get channels lists for unsubscribe and subscribe queue', () => {
        expect((service as any).getChannelsList.calls.allArgs()).toEqual([ [{}], [{}] ]);
      });

      it('should not call liveServConnectionService methods', () => {
        expect(liveServConnectionService.unsubscribe).not.toHaveBeenCalled();
        expect(liveServConnectionService.subscribe).not.toHaveBeenCalled();
      });

      it('should leave subscribers map untouched', () => {
        expect((service as any).subscribersMap).toEqual({ id1: ['11', '12'], id3: ['31', '32'] });
      });
    });
    afterEach(() => {
      expect((service as any).unsubscribeMapQueue).toEqual({});
      expect((service as any).subscribeMapQueue).toEqual({});
    });
  });

  it('getChannelsList should get all array items from array map', () => {
    const map = { id1: ['1', '2'], id2: ['3', '4'] };
    expect(service['getChannelsList'](map)).toEqual(['1', '2', '3', '4']);
  });

  it('liveServeUpdateHandler', () => {
    const update: any = {
      type: 'MESSAGE',
      channel: { name: 'channel1' },
      message: 'txt',
      event: { id: '1' },
      subChannel: { id: '2', type: 'type' }
    };

    service['liveServeUpdateHandler'](update);

    expect(pubSubService.publish).toHaveBeenCalledWith(
      'LIVE_SERVE_MS_UPDATE', [{
        channel: 'channel1',
        channel_number: update.event.id,
        payload: update.message,
        subject_number: update.subChannel.id,
        subject_type: update.subChannel.type
      }]
    );
  });

  describe('disconnectHandler', () => {
    beforeEach(() => {
      service['subscribersMap'] = { id1: ['1', '2'] };
      service['unsubscribeMapQueue'] = {};
      service['subscribeMapQueue'] = {};
      spyOn(service as any, 'fetchSubscriptions');
    });

    it('should do nothing if error is not related to connection loss', () => {
      liveServConnectionService.isDisconnected.and.returnValue(false);
      service['disconnectHandler']('error');
      expect(service['fetchSubscriptions']).not.toHaveBeenCalled();
      expect(service['unsubscribeMapQueue']).toEqual({});
      expect(service['subscribeMapQueue']).toEqual({});
    });
    it('should update both queues with current subscribers and call fetchSubscription on connection loss error', () => {
      liveServConnectionService.isDisconnected.and.returnValue(true);
      service['disconnectHandler']('error');
      expect(service['fetchSubscriptions']).toHaveBeenCalled();
      expect(service['unsubscribeMapQueue']).toEqual({ id1: ['1', '2'] });
      expect(service['subscribeMapQueue']).toEqual({ id1: ['1', '2'] });
    });
    afterEach(() => {
      expect(liveServConnectionService.isDisconnected).toHaveBeenCalledWith('error');
      expect(service['subscribersMap']).toEqual({ id1: ['1', '2'] });
    });
  });
});
