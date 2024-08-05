import { UkToteLiveUpdatesService } from '@core/services/ukTote/uktote-live-update.service';

describe('UkToteLiveUpdatesService', () => {
  let service: UkToteLiveUpdatesService,
    channelService,
    command;

  beforeEach(() => {
    channelService = {
      formChannel: jasmine.createSpy('formChannel').and.callFake((type: string, id: number | string) => `${ type }${ id }`)
    };
    command = {
      register: jasmine.createSpy('register'),
      API: {
        UK_TOTE_UPDATE_EVENT_WITH_LIVEUPDATE: 'UK_TOTE_UPDATE_EVENT_WITH_LIVEUPDATE'
      }
    };

    service = new UkToteLiveUpdatesService(channelService, command);
  });

  describe('constructor', () => {
    it('should register update event with live update', () => {
      expect(service['channelName']).toEqual({ event: 'sEVENT', market: 'sEVMKT', selection: 'sSELCN' });
      expect(command.register).toHaveBeenCalledWith(command.API.UK_TOTE_UPDATE_EVENT_WITH_LIVEUPDATE, jasmine.any(Function));
    });

    it('should call callback of registered update', () => {
      let cb: any;

      command.register.and.callFake((api: string, callback: any) => cb = callback);

      service = new UkToteLiveUpdatesService(channelService, command);

      service.updateEventWithLiveUpdate = jasmine.createSpy('updateEventWithLiveUpdate');

      cb && cb({}, {}).then((d: any) => {
        expect(d).toBeUndefined();
      });

      expect(service.updateEventWithLiveUpdate).toHaveBeenCalledWith({} as any, {} as any);
    });
  });

  it('updateEventStatus should update event status with received live update', () => {
    const event = {} as any,
      liveUpdate = {
        payload: {
          status: 'eventStatusCode'
        }
      } as any;

    service.updateEventStatus(event, liveUpdate);

    expect(event.eventStatusCode).toEqual('eventStatusCode');
  });

  it('updateMarketStatus should update market status with received live update', () => {
    const event = {
        markets: [{
          linkedMarketId: '1'
        }]
      } as any,
      liveUpdate = {
        id: 1,
        payload: {
          status: 'marketStatusCode'
        }
      } as any;

    service.updateMarketStatus(event, liveUpdate);

    expect(event.markets[0].marketStatusCode).toEqual('marketStatusCode');
  });

  describe('updateOutcomeStatus', () => {
    const event = {
        markets: [{
          linkedMarketId: 0,
          outcomes: [{
            linkedOutcomeId: 0
          }]
        }]
      } as any,
      liveUpdate = {
        id: '1',
        payload: {
          ev_mkt_id: '1',
          status: 'outcomeStatusCode'
        }
      } as any;

    it('should return if no market to update is found', () => {
      service.updateOutcomeStatus(event, liveUpdate);

      expect(event.markets[0].outcomes[0].outcomeStatusCode).toBeUndefined();
    });

    it('should return if no outcome to update is found', () => {
      event.markets[0].linkedMarketId = '1';

      service.updateOutcomeStatus(event, liveUpdate);

      expect(event.markets[0].outcomes[0].outcomeStatusCode).toBeUndefined();
    });

    it('should update outcome status with received live update', () => {
      const event = {
        markets: [{
          linkedMarketId: 0,
          outcomes: [{
            linkedOutcomeId: 0,
            outcomeStatusCode: 'outcomeStatusCode'
          }]
        }]
      } as any,
      liveUpdate = {
        id: '1',
        payload: {
          ev_mkt_id: '1',
          status: 'outcomeStatusCode'
        }
      } as any;
      event.markets[0].outcomes[0].linkedOutcomeId = '1';

      service.updateOutcomeStatus(event, liveUpdate);

      expect(event.markets[0].outcomes[0].outcomeStatusCode).toEqual('outcomeStatusCode');
    });
  });

  describe('updateEventWithLiveUpdate', () => {
    const event = {} as any,
      liveUpdate = {} as any;

    beforeEach(() => {
      service.updateEventStatus = jasmine.createSpy('updateEventStatus');
      service.updateMarketStatus = jasmine.createSpy('updateMarketStatus');
      service.updateOutcomeStatus = jasmine.createSpy('updateOutcomeStatus');
    });

    it('should return if type is wrong', () => {
      service.updateEventWithLiveUpdate(event, liveUpdate);

      expect(service.updateEventStatus).not.toHaveBeenCalled();
      expect(service.updateMarketStatus).not.toHaveBeenCalled();
    });

    it('should update event status', () => {
      liveUpdate.type = 'sEVENT';

      service.updateEventWithLiveUpdate(event, liveUpdate);
      expect(service.updateEventStatus).toHaveBeenCalledWith(event, liveUpdate);
    });

    it('should update market status', () => {
      liveUpdate.type = 'sEVMKT';

      service.updateEventWithLiveUpdate(event, liveUpdate);
      expect(service.updateMarketStatus).toHaveBeenCalledWith(event, liveUpdate);
    });

    it('should update outcome status', () => {
      liveUpdate.type = 'sSELCN';

      service.updateEventWithLiveUpdate(event, liveUpdate);
      expect(service.updateOutcomeStatus).toHaveBeenCalledWith(event, liveUpdate);
    });
  });

  describe('getAllChannels', () => {
    beforeEach(() => {
      spyOn(service, 'getEventChannels' as any).and.callThrough();
      spyOn(service, 'getMarketChannels' as any).and.callThrough();
      spyOn(service, 'getOutcomeChannels' as any).and.callThrough();
    });

    it('should return if no data provided', () => {
      expect(service.getAllChannels({} as any)).toEqual([]);
      expect(service['getEventChannels']).not.toHaveBeenCalled();
      expect(service['getMarketChannels']).not.toHaveBeenCalled();
      expect(service['getOutcomeChannels']).not.toHaveBeenCalled();
    });

    it('should get all channels for provided ids of events', () => {
      expect(service.getAllChannels({ event: [1, 2] } as any)).toEqual(['sEVENT1', 'sEVENT2']);
      expect(service['getEventChannels']).toHaveBeenCalledWith([1, 2]);
    });

    it('should get all channels for provided ids of markets', () => {
      expect(service.getAllChannels({ market: ['1', '2'] } as any)).toEqual(['sEVMKT1', 'sEVMKT2']);
      expect(service['getMarketChannels']).toHaveBeenCalledWith(['1', '2']);
    });

    it('should get all channels for provided ids of outcomes', () => {
      expect(service.getAllChannels({ outcome: ['1', '2'] } as any)).toEqual(['sSELCN1', 'sSELCN2']);
      expect(service['getOutcomeChannels']).toHaveBeenCalledWith(['1', '2']);
    });
  });

  it('getChannels should form channels for subscription', () => {
    expect(service['getChannels']([1, '2'] as any, 'typo')).toEqual(['typo1', 'typo2']);
    expect(channelService.formChannel).toHaveBeenCalledTimes(2);
    expect(channelService.formChannel).toHaveBeenCalledWith('typo', 1);
    expect(channelService.formChannel).toHaveBeenCalledWith('typo', '2');
  });

  describe('Channels', () => {
    beforeEach(() => {
      spyOn(service, 'getChannels' as any).and.callThrough();
    });

    it('getEventChannels should get event channels ids', () => {
      expect(service['getEventChannels']([1])).toEqual(['sEVENT1']);
      expect(service['getChannels']).toHaveBeenCalledWith([1], 'sEVENT');
    });

    it('getMarketChannels should get market channels ids', () => {
      expect(service['getMarketChannels'](['2'])).toEqual(['sEVMKT2']);
      expect(service['getChannels']).toHaveBeenCalledWith(['2'], 'sEVMKT');
    });

    it('getOutcomeChannels should get outcome channels ids', () => {
      expect(service['getOutcomeChannels'](['3'])).toEqual(['sSELCN3']);
      expect(service['getChannels']).toHaveBeenCalledWith(['3'], 'sSELCN');
    });
  });
});
