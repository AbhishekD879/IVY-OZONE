import { of as observableOf, Subject } from 'rxjs';
import * as _ from 'underscore';

import { BetslipLiveUpdateService } from './betslip-live-update.service';
import { IBetInfo } from '@betslip/services/bet/bet.model';
import { Bet } from '@betslip/services/bet/bet';
import { ILeg } from '@betslip/services/models/bet.model';
import { IPayload } from '@core/models/live-serve-update.model';
import { ILiveUpdateResponseMessage } from '@betslip/services/betslipLiveUpdate/betslip-live-update.model';

describe('BetslipLiveUpdateService', () => {
  let service;
  let liveServConnectionService;
  let pubSubService;
  let betslipService;
  let betslipDataService;
  let fakeConnection;

  const mockCallbacks = {
    '1': {
      channels: ['sEVENT1'],
      handler: jasmine.createSpy('handler1')
    },
    '2': null,
    '3': {
      channels: ['sEVENT2'],
      handler: jasmine.createSpy('handler2')
    }
  };

  beforeEach(() => {
    fakeConnection = {
      connected: true,
      id: 10
    };
    liveServConnectionService = {
      connect: jasmine.createSpy('connect').and.returnValue(observableOf(fakeConnection)),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      onDisconnect: jasmine.createSpy('onDisconnect'),
      isDisconnected: jasmine.createSpy('isDisconnected')
    };
    pubSubService = {
      subscribe: jasmine.createSpy('pubSubSubscribe'),
      unsubscribe: jasmine.createSpy(),
      publish: jasmine.createSpy('publish'),
      API: {
        EACHWAY_FLAG_UPDATED: 'EACHWAY_FLAG_UPDATED'
      }
    };
    betslipService = {
      updateSelection: jasmine.createSpy('updateSelection'),
      updateSelectionLiveUpdateHistory: jasmine.createSpy('updateSelectionLiveUpdateHistory'),
      updateLegsWithPriceChange: jasmine.createSpy('updateLegsWithPriceChange'),
      setLiveUpdateHistory: jasmine.createSpy('setLiveUpdateHistory')
    };
    betslipDataService = {
      bets: []
    };

    service = new BetslipLiveUpdateService(
      liveServConnectionService,
      pubSubService,
      betslipService,
      betslipDataService
    );
  });

  it('constructor', () => {
    service.subscribeForToteBets = jasmine.createSpy();
    service.unsubscribe = jasmine.createSpy();
    expect(pubSubService.subscribe).toHaveBeenCalledWith('betslipLiveUpdateService',
      pubSubService.API.BETSLIP_LIVEUPDATE_SUBSCRIBE_FOR_TOTE_BETS, jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith('betslipLiveUpdateService',
      pubSubService.API.BETSLIP_LIVEUPDATE_UNSUBSCRIBE, jasmine.any(Function));
  });

  it('should return priceUpdate subject', () => {
    const priceUpdate = new Subject<any>();
    service['priceUpdate'] = priceUpdate;
    expect(service.getPriceUpdate() as Subject<object>).toBe(priceUpdate);
  });

  describe('isConnectionValid', () => {
    it('should return falsy value if not valid connection passed', () => {
      expect(service.isConnectionValid(null)).toBeFalsy();
      expect(service.isConnectionValid({})).toBeFalsy();
    });

    it('should return falsy value if passed connection is the same as current one', () => {
      const mockConnection = {
        connected: true,
        id: 111
      };
      service.connection = mockConnection;

      expect(service.isConnectionValid(mockConnection)).toBeFalsy();
    });

    it('should return truthy value if current connection does not exist and passed one is valid', () => {
      const mockConnection = {
        connected: true
      };

      expect(service.isConnectionValid(mockConnection)).toBeTruthy();
    });

    it('should return truthy value if current connection does not exist and passed one is valid', () => {
      const mockConnection = {
        connected: true,
        id: 2
      };
      service.connection = { id: 1 };

      expect(service.isConnectionValid(mockConnection)).toBeTruthy();
    });
  });

  describe('updateConnection', () => {
    it('should not update connection if not valid connection passed', () => {
      service.updateConnection(null);
      expect(service.connection).toBeNull();

      service.updateConnection(false);
      expect(service.connection).toBeNull();
    });

    it('should update connection if current connection does not exist and passed one is valid', () => {
      const mockConnection = {
        connected: true
      };

      service.updateConnection(mockConnection);

      expect(service.connection).toEqual(mockConnection);
      expect(liveServConnectionService.onDisconnect).toHaveBeenCalledWith(service.disconnectHandler);
    });

    it('should update connection if current connection does not exist and passed one is valid', () => {
      const mockConnection = {
        connected: true,
        id: 2
      };
      service.connection = { id: 1 };

      service.updateConnection(mockConnection);

      expect(service.connection).toEqual(mockConnection);
    });
  });

  describe('clearAllSubs', () => {
    it('should not call unsubscribe method if no callbacks stored', () => {
      service.clearAllSubs();

      expect(liveServConnectionService.unsubscribe).not.toHaveBeenCalled();
    });

    it('should unsubscribe for each valid stored callback', () => {
      service.callbacks = mockCallbacks;
      service.clearAllSubs();

      expect(liveServConnectionService.unsubscribe).toHaveBeenCalledTimes(2);
      expect(liveServConnectionService.unsubscribe).toHaveBeenCalledWith(mockCallbacks['1'].channels, mockCallbacks['1'].handler);
      expect(liveServConnectionService.unsubscribe).toHaveBeenCalledWith(mockCallbacks['3'].channels, mockCallbacks['3'].handler);
      expect(service.callbacks).toEqual({});
    });
  });

  describe('reconnect', () => {
    it('should update all subscriptions on callbacks and store new connection', () => {
      service.callbacks = mockCallbacks;
      service.reconnect();

      expect(liveServConnectionService.unsubscribe).toHaveBeenCalledTimes(2);
      expect(liveServConnectionService.subscribe).toHaveBeenCalledTimes(2);
      expect(service.connection).toEqual(fakeConnection);
      expect(service.callbacks['1']).toEqual(mockCallbacks['1']);
    });

    it('should reinit after reconnect', () => {
      pubSubService.subscribe.and.callFake((p1, p2, cb) => cb());
      service.reconnect();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('betslipLiveUpdateServiceReinit');
    });
  });

  describe('setDisconnectHandler', () => {
    it('should set onDisconnect LS handler with properly bound context', () => {
      liveServConnectionService.onDisconnect.and.callFake(cb => cb());
      liveServConnectionService.isDisconnected.and.returnValue(true);
      spyOn(service, 'reconnect');
      service['setDisconnectHandler']();

      expect(liveServConnectionService.onDisconnect).toHaveBeenCalledWith(service['disconnectHandler']);
      expect(liveServConnectionService.isDisconnected).toHaveBeenCalled();
      expect(service.reconnect).toHaveBeenCalled();
    });
  });

  describe('disconnectHandler', () => {
    it('should not call reconnect if not disconnected error passed', () => {
      liveServConnectionService.isDisconnected.and.returnValue(false);
      service.disconnectHandler('some error');

      expect(liveServConnectionService.connect).not.toHaveBeenCalled();
    });

    it('should call reconnect if disconnected error passed', () => {
      spyOn(service, 'reconnect').and.callThrough();
      liveServConnectionService.isDisconnected = jasmine.createSpy('isDisconnected').and.returnValue(true);
      service.connection = { id: 1 };
      service.disconnectHandler('transport close');

      expect(service.reconnect).toHaveBeenCalled();

      expect(service.connection).toEqual(fakeConnection);
      expect(liveServConnectionService.unsubscribe).not.toHaveBeenCalled();
      expect(liveServConnectionService.subscribe).not.toHaveBeenCalled();
    });
  });

  describe('handleSubscribe', () => {
    it('should not add callback to stored map if passed bet does not have outcomeId', () => {
      const sglBet = { isSP: false };
      const channels = [];
      const handler = () => {};

      service.handleSubscribe(sglBet as IBetInfo, channels, handler);

      expect(Object.keys(service.callbacks).length).toEqual(0);
    });

    it('should add callback to stored map if passed bet has outcomeId', () => {
      const sglBet = { outcomeId: '123' };
      const channels = [];
      const handler = () => {};

      service.handleSubscribe(sglBet as IBetInfo, channels, handler);

      expect(service.callbacks['123']).toEqual({ channels, handler });
    });
  });

  describe('clearOutdatedSubs', () => {
    it('should clear all stored callbacks if no singles passed', () => {
      service.callbacks = mockCallbacks;

      service.clearOutdatedSubs([]);

      expect(liveServConnectionService.unsubscribe).toHaveBeenCalledTimes(2);
      expect(service.callbacks).toEqual({});
    });

    it('should not clear any callbacks if no callbacks were stored', () => {
      const singles = [{ outcomeId: '1' }] as IBetInfo[];

      service.clearOutdatedSubs(singles);

      expect(liveServConnectionService.unsubscribe).not.toHaveBeenCalled();
    });

    it('should clear needed callbacks for passed singles', () => {
      const singles = [{ outcomeId: '1' }, { outcomeId: '4' }] as IBetInfo[];

      service.callbacks = _.extend({}, mockCallbacks);
      service.clearOutdatedSubs(singles);

      expect(liveServConnectionService.unsubscribe).toHaveBeenCalledTimes(1);
      expect(liveServConnectionService.unsubscribe).toHaveBeenCalledWith(mockCallbacks['3'].channels, mockCallbacks['3'].handler);
      expect(service.callbacks['3']).toEqual(undefined);
    });
  });

  describe('getSingles', () => {
    it('should return filtered bets by singles outcome id', () => {
      const betInfos = [{ outcomeId: '22' }, { outcomeId: '33' }];
      const bets = [{
        uid: '1',
        info: () => {
          return { };
        }
      }, {
        uid: '2',
        info: () => {
          return betInfos[1];
        }
      }, {
        uid: '3',
        info: () => {
          return { outcomeId: undefined };
        }
      }, {
        uid: '4',
        info: () => {
          return betInfos[0];
        }
      }] as Bet[];
      const result = service.getSingles(bets);

      expect(result.length).toEqual(2);
      expect(result).toEqual([betInfos[1], betInfos[0]]);
    });
  });

  describe('getSelectionIndexes', () => {
    it('should return empty list if no bets in betslipDataService', () => {
      betslipDataService.bets = [];

      expect(service.getSelectionIndexes(1)).toEqual([]);
    });

    it('should filter selection indexes', () => {
      const betInfos = [{
        outcomeId: '1',
        type: 'SGL',
        eventIds: [{
          documentId: '339'
        }] as ILeg[]
      }, {
        outcomeId: '2',
        type: 'DBL',
        eventIds: [{
          documentId: '333'
        }] as ILeg[]
      }, {
        outcomeId: '3',
        type: 'SGL',
        eventIds: [{
          documentId: '333'
        }] as ILeg[]
      }];

      betslipDataService.bets = [{
        uid: '1',
        info: () => {
          return betInfos[0] as IBetInfo;
        }
      }, {
        uid: '2',
        info: () => {
          return betInfos[1] as IBetInfo;
        }
      }, {
        uid: '3',
        info: () => {
          return betInfos[2] as IBetInfo;
        }
      }] as Bet[];
      const channelID = '333';

      expect(service.getSelectionIndexes(channelID)).toEqual([2]);
    });
  });

  describe('handleUpdateMsg', () => {
    it('should not execute betslipService methods if no bets stored', () => {
      const update = {
        type: 'MESSAGE',
        channel: {
          id: 111,
          name: 'test',
          type: 'sEVMKT'
        },
        event: { id: 1 },
        message: {
          ev_id: '111',
          raw_hcap: '3.5',
          lp_den: '1'
        } as IPayload,
        subChannel: {
          id: 11111,
          name: 'test',
          type: 'sEVMKT'
        }
      } as ILiveUpdateResponseMessage;
      const bet = {Bet:{params:{}}} as IBetInfo;

      betslipDataService.bets = [];
      service['isPriceChanged'] = jasmine.createSpy().and.returnValue(true);

      service.handleUpdateMsg(update, bet);

      expect(service['isPriceChanged']).not.toHaveBeenCalled();
      expect(betslipService.updateSelection).not.toHaveBeenCalled();
      expect(betslipService.updateLegsWithPriceChange).not.toHaveBeenCalled();
    });

    it('should handle update "sSELCN" type', () => {
      const channelId = '111';
      const update = {
        type: 'MESSAGE',
        channel: {
          id: +channelId,
          name: 'test',
          type: 'sSELCN'
        },
        event: { id: 1 },
        message: {
          ev_id: '111',
          raw_hcap: '3.5',
          lp_den: '1'
        } as IPayload,
        subChannel: {
          id: 11111,
          name: 'test',
          type: 'sSELCN'
        }
      } as ILiveUpdateResponseMessage;
      const betInfos = [{
        outcomeId: '1',
        type: 'SGL',
        Bet: {
          price: {
            type: 'NOTDIVIDEND'
          }
        } as Bet,
        eventIds: [{
          documentId: channelId
        }] as ILeg[]
      }];
      const bet = {} as IBetInfo;

      betslipDataService.bets = [{
        uid: '1',
        info: () => {
          return betInfos[0] as IBetInfo;
        }
      }] as Bet[];
      service.handleUpdateMsg(update, bet);

      expect(betslipService.updateSelection).toHaveBeenCalledTimes(1);
      expect(betslipService.updateSelection).toHaveBeenCalledWith(0, update.message, 'outcome');
      expect(betslipService.updateLegsWithPriceChange).not.toHaveBeenCalled();
    });

    it('should handle update "sMHCAP" type', () => {
      const channelId = '111';
      const update = {
        type: 'MESSAGE',
        channel: {
          id: +channelId,
          name: 'test',
          type: 'sSELCN'
        },
        event: { id: 1 },
        message: {
          ev_id: '111',
          raw_hcap: undefined,
          lp_den: ''
        } as IPayload,
        subChannel: {
          id: 11111,
          name: 'test',
          type: 'sSELCN'
        }
      } as ILiveUpdateResponseMessage;
      const betInfos = [{
        outcomeId: '1',
        type: 'SGL',
        Bet: {
          price: {
            type: 'NOTDIVIDEND'
          }
        } as Bet,
        eventIds: [{
          documentId: channelId
        }] as ILeg[]
      }];
      const bet = {} as IBetInfo;

      betslipDataService.bets = [{
        uid: '1',
        info: () => {
          return betInfos[0] as IBetInfo;
        }
      }] as Bet[];
      service.handleUpdateMsg(update, bet);

      expect(betslipService.updateSelection).toHaveBeenCalledTimes(1);
      expect(betslipService.updateSelection).toHaveBeenCalledWith(0, update.message, 'outcome');
      expect(betslipService.updateLegsWithPriceChange).not.toHaveBeenCalled();
    });

    it('should handle update "sPRICE" type', () => {
      const channelId = '111';
      const update = {
        type: 'MESSAGE',
        channel: {
          id: +channelId,
          name: 'test',
          type: 'sSELCN'
        },
        event: { id: 1 },
        message: {
          ev_id: '111',
          raw_hcap: undefined,
          lp_den: '2'
        } as IPayload,
        subChannel: {
          id: 11111,
          name: 'test',
          type: 'sSELCN'
        }
      } as ILiveUpdateResponseMessage;
      const betInfos = [{
        outcomeId: '1',
        type: 'SGL',
        Bet: {
          price: {
            type: 'NOTDIVIDEND'
          }
        } as Bet,
        eventIds: [{
          documentId: channelId
        }] as ILeg[]
      }];

      betslipDataService.bets = [{
        uid: '1',
        info: () => {
          return betInfos[0] as IBetInfo;
        }
      }] as Bet[];
      const bet =  {
        price: {
          priceNum: 3,
          priceDen: 7
        }
      } as IBetInfo;
      service['emitPriceUpdate'] = jasmine.createSpy();
      service['isPriceChanged'] = jasmine.createSpy().and.returnValue(true);
      service.handleUpdateMsg(update, bet);

      expect(betslipService.updateSelection).toHaveBeenCalledTimes(1);
      expect(betslipService.updateSelection).toHaveBeenCalledWith(0, update.message, 'outcome');
      expect(betslipService.updateLegsWithPriceChange).toHaveBeenCalledWith(update.message, update.channel.id);
      expect(service['emitPriceUpdate']).toHaveBeenCalledWith(update);
      expect(service['isPriceChanged']).toHaveBeenCalledWith(update, bet);
    });

    it('emitPriceUpdate should not emit new value', () => {
      const update = {};
      service['priceUpdate'] = {
        next: jasmine.createSpy(),
        observers: []
      };
      service['emitPriceUpdate'](update);
      expect(service['priceUpdate'].next).not.toHaveBeenCalled();
    });

    it('emitPriceUpdate should emit new value', () => {
      const update = {};
      service['priceUpdate'] = {
        next: jasmine.createSpy(),
        observers: [{}]
      };
      service['emitPriceUpdate'](update);
      expect(service['priceUpdate'].next).toHaveBeenCalledWith(update);
    });
    it('should publish the update if iseachWayFlagUpdated is true', () => {
      const update = {
        type: 'MESSAGE',
        channel: {
          id: 11,
          name: 'test',
          type: 'sSELCN'
        },
        event: { id: 1 },
        message: {
          ev_id: '111',
          raw_hcap: undefined,
          lp_den: '',
          ew_avail: 'N'
        } as IPayload,
        subChannel: {
          id: 11111,
          name: 'test',
          type: 'sEVMKT'
        }
      } as ILiveUpdateResponseMessage;
      const betinfo = {
        Bet: {
          params: {
            eachWayAvailable: 'Y'
          }
        }
      };
      service['eachWayFlagUpdated'] = jasmine.createSpy('eachWayFlagUpdated').and.returnValue(true);
      service['handleUpdateMsg'](update, betinfo);
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.EACHWAY_FLAG_UPDATED, [update.message, betinfo]);
    });
    it('should not publish the update if iseachWayFlagUpdated is false', () => {
      const update = {
        type: 'MESSAGE',
        channel: {
          id: 11,
          name: 'test',
          type: 'sSELCN'
        },
        event: { id: 1 },
        message: {
          ev_id: '111',
          raw_hcap: undefined,
          lp_den: '',
          ew_avail: 'N'
        } as IPayload,
        subChannel: {
          id: 11111,
          name: 'test',
          type: 'sEVMKT'
        }
      } as ILiveUpdateResponseMessage;
      const betinfo = {
        Bet: {
          params: {
            eachWayAvailable: 'N'
          }
        }
      };
      service['eachWayFlagUpdated'] = jasmine.createSpy('eachWayFlagUpdated').and.returnValue(false);
      service['handleUpdateMsg'](update, betinfo);
      expect(pubSubService.publish).not.toHaveBeenCalledWith(pubSubService.API.EACHWAY_FLAG_UPDATED, [update.message.ew_avail, betinfo]);
    });
  });

  describe('getChannels', () => {
    it('should parse live serv channels', () => {
      const betSlipItem = {
        liveServChannels: {
          marketliveServChannels: ['1', '2'],
          eventliveServChannels: ['3', '4'],
          outcomeliveServChannels: ['5']
        }
      };
      const result = service.getChannels(betSlipItem as IBetInfo);

      expect(result).toEqual(['1', '2', '3', '4', '5']);
    });
  });

  describe('subscribe', () => {
    it('should not create connection if no singles are passed in the bets', () => {
      const betSlipData = [{
        uid: '1',
        info: () => {
          return { };
        }
      }, {
        uid: '3',
        info: () => {
          return { outcomeId: undefined };
        }
      }] as Bet[];
      const result = service.subscribe(betSlipData);

      expect(liveServConnectionService.connect).not.toHaveBeenCalled();
      expect(result).toEqual(betSlipData);
      expect(service.connection).toBeNull();
      expect(service.callbacks).toEqual({});
    });

    it('should store new connection and subscribe for singles updates', () => {
      const betInfos = [{
        outcomeId: '11',
        liveServChannels: {
          marketliveServChannels: ['1'],
          eventliveServChannels: ['2'],
          outcomeliveServChannels: ['3']
        }
      }, {
        outcomeId: '22',
        liveServChannels: {
          marketliveServChannels: ['4'],
          eventliveServChannels: ['5'],
          outcomeliveServChannels: ['6']
        }
      }];
      const betSlipData = [{
        uid: '1',
        info: () => {
          return { };
        }
      }, {
        uid: '2',
        info: () => {
          return betInfos[0];
        }
      }, {
        uid: '3',
        info: () => {
          return { outcomeId: undefined };
        }
      }, {
        uid: '4',
        info: () => {
          return betInfos[1];
        }
      }] as Bet[];

      service.callbacks[betInfos[1].outcomeId] = { channels: [] };
      service.subscribe(betSlipData);

      expect(liveServConnectionService.connect).toHaveBeenCalled();
      expect(service.connection).toEqual(fakeConnection);
      expect(liveServConnectionService.subscribe).toHaveBeenCalledWith(['1', '2', '3'], jasmine.any(Function));
    });

    it('should handle new update message', () => {
      const channelId = '111';
      const update = {
        type: 'MESSAGE',
        channel: {
          id: +channelId,
          name: 'test',
          type: 'sSELCN'
        },
        event: { id: 1 },
        message: {
          ev_id: '111',
          raw_hcap: undefined,
          lp_den: '2'
        } as IPayload,
        subChannel: {
          id: 11111,
          name: 'test',
          type: 'sSELCN'
        }
      } as ILiveUpdateResponseMessage;
      const betInfos = [{
        outcomeId: '1',
        type: 'SGL',
        Bet: {
          price: {
            type: 'NOTDIVIDEND'
          }
        } as Bet,
        eventIds: [{
          documentId: channelId
        }] as ILeg[],
        liveServChannels: {
          marketliveServChannels: ['1'],
          eventliveServChannels: ['2'],
          outcomeliveServChannels: ['3']
        }
      }];
      const betSlipData = [{
        uid: '2',
        info: () => {
          return betInfos[0];
        }
      }] as Bet[];
      const bet =  {
        price: {
          priceNum: 3,
          priceDen: 7
        }
      } as IBetInfo;
      let storedHandler = (args) => {};

      betslipDataService.bets = betSlipData;
      service['getSingles'] = jasmine.createSpy().and.returnValue([bet]);

      liveServConnectionService.subscribe.and.callFake((channel, handlerFn) => {
        storedHandler = handlerFn;
      });
      service.subscribe(betSlipData);

      storedHandler({ type: 'TEST' });
      storedHandler(update);

      expect(betslipService.updateSelection).toHaveBeenCalledWith(0, update.message, 'outcome');
      expect(betslipService.updateLegsWithPriceChange).toHaveBeenCalledWith(update.message, update.channel.id);
    });

    it('should handle SUBSCRIBE message', () => {
      liveServConnectionService.subscribe.and.callFake((p1, cb) => {
        cb({ type: 'SUBSCRIBED' });
      });

      service.subscribe([{
        info: () => ({ outcomeId: '777' })
      }]);

      expect(service.callbacks['777']).toBeDefined();
    });

    it('should handle subscription confirmation message only once', () => {
      const outcomeId = '777';

      liveServConnectionService.subscribe.and.callFake((p1, cb) => {
        cb({ type: 'SUBSCRIBED' });
      });

      service.subscribe([{
        info: () => ({ outcomeId })
      }]);
      service.subscribe([{
        info: () => ({ outcomeId })
      }]);

      expect(service.callbacks[outcomeId]).toBeDefined();
      expect(liveServConnectionService.subscribe).toHaveBeenCalledTimes(1);
    });
  });

  describe('unsubscribe', () => {
    it('should call unsubscribe of liveServConnectionService', () => {
      const channels = ['sEVENT1', 'sPRICE2'];

      service.unsubscribe(channels);

      expect(liveServConnectionService.unsubscribe).toHaveBeenCalledWith(channels, jasmine.any(Function));
    });
  });

  describe('subscribeForToteBets', () => {
    it('should subscribe for updates and store new connection', () => {
      const channels = ['sEVENT1', 'sPRICE11'];
      const updateHandler = jasmine.createSpy('updateHandler');

      service.subscribeForToteBets(channels, updateHandler);

      expect(liveServConnectionService.connect).toHaveBeenCalled();
      expect(liveServConnectionService.subscribe).toHaveBeenCalledWith(channels, jasmine.any(Function));
      expect(service.connection).toEqual(fakeConnection);
    });

    it('should call updateHandler on connection subscribe', () => {
      const channels = ['sEVENT1', 'sPRICE11'];
      const updateHandler = jasmine.createSpy('updateHandler');
      let storedHandler = (args) => {};

      liveServConnectionService.subscribe.and.callFake((channel, handlerFn) => {
        storedHandler = handlerFn;
      });

      service.subscribeForToteBets(channels, updateHandler);

      storedHandler({ type: 'UPDATE' });
      expect(updateHandler).not.toHaveBeenCalled();

      const updateMessage = { type: 'MESSAGE' };
      storedHandler(updateMessage);
      expect(updateHandler).toHaveBeenCalledWith(updateMessage);
    });
  });

  it('handleUpdateMsg sprice', () => {
    service.getSelectionIndexes = jasmine.createSpy().and.returnValue([1, 2, '3']);
    const update = {
      message: {
        lp_den: '10'
      },
      channel: {
        type: 'sPRICE',
        id: '123'
      }
    };
    const bet =  {
      price: {
        priceNum: 3,
        priceDen: 7
      }
    } as IBetInfo;
    service['isPriceChanged'] = jasmine.createSpy().and.returnValue(true);
    service['handleUpdateMsg'](update, bet);

    expect(betslipService.updateSelection).toHaveBeenCalledTimes(2);
    expect(betslipService.updateLegsWithPriceChange).toHaveBeenCalledWith(update.message, update.channel.id);
    expect(service['isPriceChanged']).toHaveBeenCalledWith(update, bet);
  });

  it('handleUpdateMsg no price changes', () => {
    service.getSelectionIndexes = jasmine.createSpy().and.returnValue([1, 2, '3']);
    let update = {
      message: {
        raw_hcap: '10'
      },
      channel: {
        type: 'sPRICE',
        id: '123'
      },
      subChannel: {}
    };
    const bet = {Bet:{params:{}}} as IBetInfo;
    service['handleUpdateMsg'](update, bet);

    expect(betslipService.updateLegsWithPriceChange).not.toHaveBeenCalled();

    service.getSelectionIndexes = jasmine.createSpy().and.returnValue([1, 2, '3']);
    update = {
      message: {
        raw_hcap: '10'
      },
      channel: {
        type: 'sPRICE',
        id: '123'
      },
      subChannel: {
        type: 'sEVMKT'
      }
    };
    service['handleUpdateMsg'](update, bet);

    expect(betslipService.updateLegsWithPriceChange).not.toHaveBeenCalled();
  });

  it('getSelectionIndexes', () => {
    betslipDataService.bets = [
      {
        info: () => {
          return {
            eventIds: ['2', '1'],
            type: 'SGL',
            Bet: {
              price: {
                type: 'TEST'
              }
            }
          };
        }
      },
      {
        info: () => {
          return {
            eventIds: ['3', '2', '1'],
            type: 'SGL',
            Bet: {
              price: {
                type: 'DIVIDENT'
              }
            }
          };
        }
      },
      {
        info: () => {
          return {
            eventIds: ['2', '1'],
            type: 'DBL'
          };
        }
      },
      {
        info: () => {
          return {
            eventIds: ['1', '3', '2', '1'],
            type: 'DBL'
          };
        }
      }
    ];

    expect(service['getSelectionIndexes'](1)).toEqual([0, 1]);
  });

  it('getChannels', () => {
    expect(service['getChannels']({ liveServChannels: [[1, 2, 3], [4, 5, 6]] })).toEqual([1, 2, 3, 4, 5, 6]);
  });

  describe('isPriceChanged', () => {
    it('should return true when lp_num was changed', () => {
      const msg = {
        type: 'MESSAGE',
        channel: {
          id: 123,
          name: 'test',
          type: 'sSELCN'
        },
        event: { id: 1 },
        message: {
          ev_id: '111',
          raw_hcap: undefined,
          lp_den: '2',
          lp_num: '8'
        } as IPayload,
        subChannel: {
          id: 11111,
          name: 'test',
          type: 'sSELCN'
        }
      } as ILiveUpdateResponseMessage;
      const bet =  {
        price: {
          priceNum: 7,
          priceDen: 2
        }
      } as IBetInfo;
      expect(service['isPriceChanged'](msg, bet)).toBeTruthy();
    });

    it('should return true when lp_den was changed', () => {
      const msg = {
        type: 'MESSAGE',
        channel: {
          id: 123,
          name: 'test',
          type: 'sSELCN'
        },
        event: { id: 1 },
        message: {
          ev_id: '111',
          raw_hcap: undefined,
          lp_den: '5',
          lp_num: '8'
        } as IPayload,
        subChannel: {
          id: 11111,
          name: 'test',
          type: 'sSELCN'
        }
      } as ILiveUpdateResponseMessage;
      const bet =  {
        price: {
          priceNum: 8,
          priceDen: 3
        }
      } as IBetInfo;
      expect(service['isPriceChanged'](msg, bet)).toBeTruthy();
    });

    it('should return false', () => {
      const msg = {
        type: 'MESSAGE',
        channel: {
          id: 123,
          name: 'test',
          type: 'sSELCN'
        },
        event: { id: 1 },
        message: {
          ev_id: '111',
          raw_hcap: undefined,
          lp_den: '5',
          lp_num: '8'
        } as IPayload,
        subChannel: {
          id: 11111,
          name: 'test',
          type: 'sSELCN'
        }
      } as ILiveUpdateResponseMessage;
      const bet =  {
        price: {
          priceNum: 8,
          priceDen: 5
        }
      } as IBetInfo;
      expect(service['isPriceChanged'](msg, bet)).toBeFalsy();
    });

    it('should return false when no prices', () => {
      const msg = {
        type: 'MESSAGE',
        channel: {
          id: 123,
          name: 'test',
          type: 'sSELCN'
        },
        event: { id: 1 },
        message: {
          ev_id: '111',
          raw_hcap: undefined,
          lp_den: '5',
          lp_num: '8'
        } as IPayload,
        subChannel: {
          id: 11111,
          name: 'test',
          type: 'sSELCN'
        }
      } as ILiveUpdateResponseMessage;
      const bet =  {
        price: {}
      } as IBetInfo;
      expect(service['isPriceChanged'](msg, bet)).toBeFalsy();
    });
  });
  describe('#isEachWayFlagUpdated', () => {
    it('should return true if both the update and Bet.params.eachWayAvailable are not equal', () => {
      const betinfo = {
        Bet: {
          params: {
            eachWayAvailable: 'Y'
          }
        }
      }
      expect(service['isEachWayFlagUpdated']('N', betinfo)).toBeTruthy();
    });
    it('should return false if both the update and Bet.params.eachWayAvailable are equal', () => {
      const betinfo = {
        Bet: {
          params: {
            eachWayAvailable: 'Y'
          }
        }
      }
      expect(service['isEachWayFlagUpdated']('Y', betinfo)).toBeFalsy();
    });
  });
});
