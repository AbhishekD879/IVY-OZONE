import { ChannelService } from './channel.service';

describe('ChannelService', () => {
  let service: ChannelService;

  beforeEach(() => {
    service = new ChannelService();
  });

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  it('formChannel', () => {
    expect(service.formChannel('vbn', '3')).toBe('vbn0000000003');
    expect(service.formChannel('sda', 345)).toBe('sda0000000345');
  });

  describe('getLSChannelsFromArray', () => {
    const events = [{
      liveServChannels: 'sEVENT1,',
      liveServChildrenChannels: 'SEVENT1,',
      id: '3'
    }, {}, {
      liveServChannels: 'sEVENT2,',
      liveServChildrenChannels: 'SEVENT2,',
      id: 345,
      markets: [{
        liveServChannels: 'sEVMKT1,'
      }, undefined]
    }] as any;

    it('should handle falsy data', () => {
      expect(service.getLSChannelsFromArray(null)).toEqual([]);
    });

    it('should gather channels from event and children levels', () => {
      expect(service.getLSChannelsFromArray(events)).toEqual(['sEVENT1', 'SEVENT1', 'sEVENT2', 'SEVENT2']);
    });

    it(`should gather channels from event level`, () => {
      expect(service.getLSChannelsFromArray(events, false)).toEqual(['sEVENT1', 'sEVENT2']);
    });

    it(`should gather channels from event level and with subscribeForScores`, () => {
      expect(service.getLSChannelsFromArray(events, false, true))
        .toEqual(['sEVENT1', 'sSCBRD0000000003', 'sEVENT2', 'sSCBRD0000000345']);
    });
  });

  describe('getLSChannels', () => {
    const event = {
      liveServChannels: 'sEVENT1,',
      liveServChildrenChannels: 'SEVENT1,',
      id: 345,
      markets: [{
        liveServChannels: 'sEVMKT1,'
      }, undefined]
    } as any;

    it('should handle falsy data', () => {
      expect(service.getLSChannels(null)).toEqual([]);
    });

    it(`should gather channels from event and children levels`, () => {
      expect(service.getLSChannels(event)).toEqual(['sEVENT1', 'SEVENT1']);
    });

    it(`should gather channels from event level`, () => {
      expect(service.getLSChannels(event, false)).toEqual(['sEVENT1']);
    });

    it(`should gather channels from event level and with subscribeForScores`, () => {
      expect(service.getLSChannels(event, false, true)).toEqual(['sEVENT1', 'sSCBRD0000000345']);
    });

    it(`should not subscribeForScores if no event id`, () => {
      delete event.id;
      expect(service.getLSChannels(event, false, true)).toEqual(['sEVENT1']);
    });

    it(`should not add if typeof Channels is Not string`, () => {
      event.liveServChannels = event.liveServChildrenChannels = 123;

      expect(service.getLSChannels(event)).toEqual([]);
    });
  });

  describe('getLSChannelsForCoupons', () => {
    const events = [{
      liveServChannels: 'sEVENT1,',
      liveServChildrenChannels: 'SEVENT1,',
      id: '3'
    }, {}, {
      liveServChannels: 'sEVENT2,',
      liveServChildrenChannels: 'SEVENT2,',
      id: 345,
      markets: [{
        liveServChannels: 'sEVMKT1,',
        liveServChildrenChannels: 'SEVMKT1'
      }, undefined]
    }] as any;

    it(`should gather needed channels for Coupons`, () => {
      expect(service.getLSChannelsForCoupons(events)).toEqual(['sEVENT1', 'sEVENT2', 'sEVMKT1', 'SEVMKT1']);
    });
  });

  describe('getEventsChildsLiveChannels', () => {
    it('should handle falsy data', () => {
      expect(service.getEventsChildsLiveChannels(null)).toEqual([]);
    });

    it('should gather needed only channels from event levels if markets not available', () => {
      const events = [{ liveServChannels: 'sEVENT1,' }, {}, { liveServChannels: 'sEVENT2,' }, null] as any;

      expect(service.getEventsChildsLiveChannels(events)).toEqual(['sEVENT1', 'sEVENT2']);
    });

    it('should gather needed only channels from event levels and markets if outcomes not available', () => {
      const events = [{
        liveServChannels: 'sEVENT1,'
      }, {}, {
        liveServChannels: 'sEVENT2,',
        markets: [{
          liveServChannels: 'sEVMKT1,'
        }, undefined]
      }] as any;

      expect(service.getEventsChildsLiveChannels(events)).toEqual(['sEVENT1', 'sEVENT2', 'sEVMKT1']);
    });

    it('should gather all needed channels from event, markets and outcomes', () => {
      const events = [{
        liveServChannels: 'sEVENT1,'
      }, {}, {
        liveServChannels: 'sEVENT2,',
        markets: [{
          liveServChannels: 'sEVMKT1,'
        }]
      }, {
        liveServChannels: 'sEVENT3,',
        markets: [{
          liveServChannels: 'sEVMKT2,',
          outcomes: [null, {
            liveServChannels: 'sSELCN1,'
          }, {}]
        }]
      }] as any;

      expect(service.getEventsChildsLiveChannels(events)).toEqual(['sEVENT1', 'sEVENT2', 'sEVMKT1',
        'sEVENT3', 'sEVMKT2', 'sSELCN1']);
    });
  });
});
