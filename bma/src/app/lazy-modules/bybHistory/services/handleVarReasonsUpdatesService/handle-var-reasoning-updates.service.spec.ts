import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { IMatchCommentaryStatsUpdate } from '../../models/scoreboards-stats-update.model';
import { HandleVarReasoningUpdatesService } from './handle-var-reasoning-updates.service';
import { IMatchCmtryData } from '@app/betHistory/models/bet-history.model';
import { ISocketIO } from '@app/core/services/liveServ/live-serv-connection.model';

describe('HandleVarReasoningUpdatesService', () => {
  let service: HandleVarReasoningUpdatesService;
  let liveServConnectionService;
  let pubSubService;
  beforeEach(() => {
    liveServConnectionService = {
      connect: jasmine.createSpy().and.returnValue({
        subscribe: jasmine.createSpy('subscribe').and.callFake(cb => cb())
      }),
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      onDisconnect: jasmine.createSpy(),
      isDisconnected: jasmine.createSpy('isDisconnected'),
      subscribeToMatchCommentary: jasmine.createSpy('subscribeToMatchCommentary'),
      unsubscribeFromMatchCommentary: jasmine.createSpy('unsubscribeFromMatchCommentary'),
      sendRequestForLastMatchFact:jasmine.createSpy('sendRequestForLastMatchFact'),
      removeAllEventListner: jasmine.createSpy('sendRequestForLastMatchFact')
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      API: pubSubApi
    };
    service = new HandleVarReasoningUpdatesService(
      liveServConnectionService,
      pubSubService
    );
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
  describe('#subscribeForMatchCmtryUpdates', () => {
    it('should call liveServConnectionService.connect', () => {
      service.subscribeForMatchCmtryUpdates('12345');
      expect(service['callbacks']).toEqual({ handler: jasmine.any(Function) });
      expect(liveServConnectionService.connect).toHaveBeenCalled();
      expect(service['channels'].length).toEqual(1);
      expect(liveServConnectionService.subscribeToMatchCommentary).toHaveBeenCalledWith('sFACTS12345', jasmine.any(Function));
    });
    it('should call updatesVarHandler when update for event id exists', () => {
      service['channels'] = ['12345'];
      service.subscribeForMatchCmtryUpdates('12345');
      expect(liveServConnectionService.connect).toHaveBeenCalled();
      expect(liveServConnectionService.subscribeToMatchCommentary).toHaveBeenCalledWith('sFACTS12345', jasmine.any(Function));
    });
    it('should call updatesVarHandler when update for event id exists', () => {
      service['channels'] = ['12345'];
      const matchCmtryDataUpdate = {
        incident: { eventId: '12345', feed: 'OPTA', type: { code: 602, description: 'test matchfact' }, context: { reasonId: 101, playerName: 'A', teamName: 'B' } }
      } as IMatchCommentaryStatsUpdate;
      spyOn(service as any,'matchCommentryUpdateHandler')
      service.subscribeForMatchCmtryUpdates('12345');
      service['callbacks'].handler(matchCmtryDataUpdate);
      expect(service['matchCommentryUpdateHandler']).toHaveBeenCalledWith(matchCmtryDataUpdate);
      expect(liveServConnectionService.connect).toHaveBeenCalled();
      expect(liveServConnectionService.subscribeToMatchCommentary).toHaveBeenCalledWith('sFACTS12345', jasmine.any(Function));
    });
  });
  describe('#updatesVarHandler', () => {
    it('should publish data if we get if reason-id is available in Var-config', () => {
      const updateObj = { incident: { eventId: '12345', type: { code: 601 }, context: { reasonId: 101, playerName: 'A', teamName: 'B' } } } as IMatchCommentaryStatsUpdate;
      service['matchCommentryUpdateHandler'](updateObj);
      expect(service['varIconData']).toEqual({ svgId: 'Var_Goal', description: 'Goal' });
      expect(service['matchCmtryDataUpdate']).toEqual({ matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } } as any);
      expect(pubSubService.publish).toHaveBeenCalledWith('UPDATE_MATCHCOMMENTARY_DATA', { matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } } as any);
    });
    it('should not publish data if we get if reason-id is not available in Var-config', () => {
      const updateObj = { incident: { eventId: '12345', type: { code: 601 }, context: { reasonId: 101, playerName: 'A', teamName: 'B' } } } as IMatchCommentaryStatsUpdate;
      service['matchCommentryUpdateHandler'](updateObj);
      expect(service['varIconData']).toEqual({ svgId: 'Var_Goal', description: 'Goal' });
      expect(service['matchCmtryDataUpdate']).toEqual({ matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } } as any);
      expect(pubSubService.publish).not.toHaveBeenCalledWith('UPDATE_VAR_DATA', service['matchCmtryDataUpdate']);
    });
    it('should not publish data if we get data is null', () => {
      const updateObj = null
      service['matchCommentryUpdateHandler'](updateObj);
      expect(service['varIconData']).not.toEqual({ svgId: 'Var_Goal', description: 'Goal' });
      expect(service['matchCmtryDataUpdate']).not.toEqual({ matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } } as any);
      expect(pubSubService.publish).not.toHaveBeenCalledWith('UPDATE_VAR_DATA', service['matchCmtryDataUpdate']);
    });
    it('should not publish data if we get incident is null', () => {
      const updateObj = { incident: null } as IMatchCommentaryStatsUpdate;
      service['matchCommentryUpdateHandler'](updateObj);
      expect(service['varIconData']).not.toEqual({ svgId: 'Var_Goal', description: 'Goal' });
      expect(service['matchCmtryDataUpdate']).not.toEqual({ matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } } as any);
      expect(pubSubService.publish).not.toHaveBeenCalledWith('UPDATE_VAR_DATA', service['matchCmtryDataUpdate']);
    });
    it('should not publish data if we get type is null', () => {
      const updateObj = { incident: { type: null } } as IMatchCommentaryStatsUpdate;
      service['matchCommentryUpdateHandler'](updateObj);
      expect(service['varIconData']).not.toEqual({ svgId: 'Var_Goal', description: 'Goal' });
      expect(service['matchCmtryDataUpdate']).not.toEqual({ matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } } as any);
      expect(pubSubService.publish).not.toHaveBeenCalledWith('UPDATE_VAR_DATA', service['matchCmtryDataUpdate']);
    });
    it('should not publish data if we get context is null', () => {
      const updateObj = { incident: { eventId: '12345', type: { code: 601 }, context: null } } as IMatchCommentaryStatsUpdate;
      service['matchCommentryUpdateHandler'](updateObj);
      expect(service['varIconData']).not.toEqual({ svgId: 'Var_Goal', description: 'Goal' });
      expect(service['matchCmtryDataUpdate']).not.toEqual({ matchCmtryEventId: '12345', teamName: 'B', playerName: 'A', varIconData: { svgId: 'Var_Goal', description: 'Goal' } } as any);
      expect(pubSubService.publish).not.toHaveBeenCalledWith('UPDATE_VAR_DATA', service['matchCmtryDataUpdate']);
    });
    it('should publish OPTA data if reason-id is available and code not equal to 601 in Var-config', () => {
      const updateObj = { incident: { eventId: '12345', feed: 'OPTA', type: { code: 602, description: 'test matchfact' }, context: { reasonId: 101, playerName: 'A', teamName: 'B' } } } as IMatchCommentaryStatsUpdate;
      spyOn<any>(service, 'getMatchFactData').and.callThrough();
      service['matchCommentryUpdateHandler'](updateObj);
      expect(service['matchCmtryDataUpdate']).toEqual({ matchCmtryEventId: '12345', feed: 'OPTA', matchfact: 'test matchfact', teamName: 'B', playerName: 'A', varIconData: null } as any);
      expect(pubSubService.publish).toHaveBeenCalledWith('UPDATE_MATCHCOMMENTARY_DATA', service['matchCmtryDataUpdate']);
    });
    it('should publish data if reason-id is available in Var-config', () => {
      const updateObj = { incident: { eventId: '12345', feed: 'AMELCO', type: { code: 602, description: 'test matchfact' }, context: { reasonId: 101, playerName: 'A', teamName: 'B' } } } as IMatchCommentaryStatsUpdate;
      spyOn<any>(service, 'getMatchFactData').and.callThrough();
      service['matchCommentryUpdateHandler'](updateObj);
      expect(service['matchCmtryDataUpdate']).toEqual({ matchCmtryEventId: '12345', feed: 'AMELCO', matchfact: 'test matchfact', teamName: 'B', varIconData: null } as any);
      expect(pubSubService.publish).toHaveBeenCalledWith('UPDATE_MATCHCOMMENTARY_DATA', service['matchCmtryDataUpdate']);
    });
    it('should not publish data if feed is undefined', () => {
      const updateObj = { incident: { eventId: '12345', type: { code: 602, description: 'test matchfact' }, context: { reasonId: 101, playerName: 'A', teamName: 'B' } } } as IMatchCommentaryStatsUpdate;
      spyOn<any>(service, 'getMatchFactData').and.callThrough();
      service['matchCommentryUpdateHandler'](updateObj);
      expect(service['matchCmtryDataUpdate']).not.toEqual({ matchCmtryEventId: '12345', feed: 'AMELCO', matchfact: 'test matchfact', teamName: 'B', varIconData: null } as any);
      expect(pubSubService.publish).not.toHaveBeenCalledWith('UPDATE_MATCHCOMMENTARY_DATA', service['matchCmtryDataUpdate']);
    });
    it('should not publish data if feed is undefined', () => {
      const updateObj = null;
      spyOn<any>(service, 'getMatchFactData').and.callThrough();
      service['matchCommentryUpdateHandler'](updateObj);
      expect(service['matchCmtryDataUpdate']).not.toEqual({ matchCmtryEventId: '12345', feed: 'AMELCO', matchfact: 'test matchfact', teamName: 'B', varIconData: null } as any);
      expect(pubSubService.publish).not.toHaveBeenCalledWith('UPDATE_MATCHCOMMENTARY_DATA', service['matchCmtryDataUpdate']);
    });
    it('should not publish  data if incident is undefined', () => {
      const updateObj = { incident: null } as IMatchCommentaryStatsUpdate;
      spyOn<any>(service, 'getMatchFactData').and.callThrough();
      service['matchCommentryUpdateHandler'](updateObj);
      expect(service['matchCmtryDataUpdate']).not.toEqual({ matchCmtryEventId: '12345', feed: 'AMELCO', matchfact: 'test matchfact', teamName: 'B', varIconData: null } as any);
      expect(pubSubService.publish).not.toHaveBeenCalledWith('UPDATE_MATCHCOMMENTARY_DATA', service['matchCmtryDataUpdate']);
    });
  });
  describe('#reconnect', () => {

    it('reconnect', () => {
      const handler = () => { };
      service['callbacks'] = { handler };
      service['channels'] = ['123'];
      service.unsubscribeForMatchCmtryUpdates = jasmine.createSpy('unsubscribeForMatchCmtryUpdates');
      service['updateConnection'] = jasmine.createSpy('updateConnection');

      service.reconnect();

      expect(liveServConnectionService.connect).toHaveBeenCalled();
      expect(liveServConnectionService.subscribeToMatchCommentary).toHaveBeenCalled();
      expect(service.unsubscribeForMatchCmtryUpdates).toHaveBeenCalled();
      expect(service['updateConnection']).toHaveBeenCalled();
    });
  });
  describe('unsubscribeForMatchCmtryUpdates', () => {
    it('should call unsubscribeFromMatchCommentary from live-serve', () => {
      const handler = () => { };
      service['callbacks'] = { handler };
      service['channels'] = ['123'];
      service.unsubscribeForMatchCmtryUpdates('123');
      expect(liveServConnectionService.unsubscribeFromMatchCommentary).toHaveBeenCalledWith('sFACTS123', service['callbacks']['handler'])
    });
  });

  describe('updateConnection', () => {
    beforeEach(() => {
      service['isConnectionValid'] = jasmine.createSpy().and.returnValue(true);
      service['setDisconnectHandler'] = jasmine.createSpy();
    });

    it('should call setDisconnectHandler', () => {
      const connection: any = {};

      service['updateConnection'](connection);

      expect(service['isConnectionValid']).toHaveBeenCalledWith(connection);
      expect(service['setDisconnectHandler']).toHaveBeenCalled();
    });

    it('should not call setDisconnectHandler', () => {
      (service['isConnectionValid'] as jasmine.Spy).and.returnValue(false);
      const connection: any = {};

      service['updateConnection'](connection);

      expect(service['isConnectionValid']).toHaveBeenCalledWith(connection);
      expect(service['setDisconnectHandler']).not.toHaveBeenCalled();
    });
  });
  describe('#isConnectionValid', () => {
    it('isConnectionValid', () => {
      expect(service['isConnectionValid'](null)).toBeFalsy();

      service['connection'] = null;
      expect(service['isConnectionValid']({ connected: true } as any)).toBeTruthy();

      service['connection'] = { id: 1 } as any;
      expect(service['isConnectionValid']({ connected: true, id: 2 } as any)).toBeTruthy();

      service['connection'] = { id: 1 } as any;
      expect(service['isConnectionValid']({ connected: true, id: 1 } as any)).toBeFalsy();
    });
  });

  describe('setDisconnectHandler', () => {
    it('should set onDisconnect LS handler with properly bound context', () => {
      service['setDisconnectHandler']();

      expect(liveServConnectionService.onDisconnect).toHaveBeenCalledWith(service['disconnectHandler']);
    });
  });

  describe('disconnectHandler', () => {
    it('should disconnect on disconnection message', () => {
      service['reconnect'] = jasmine.createSpy();
      liveServConnectionService.isDisconnected = jasmine.createSpy('isDisconnected').and.returnValue(true);
      service['disconnectHandler']('transport error');
      expect(service['reconnect']).toHaveBeenCalled();
    });
    it('should`t disconnect on not disconnection message', () => {
      service['reconnect'] = jasmine.createSpy();
      liveServConnectionService.isDisconnected = jasmine.createSpy('isDisconnected').and.returnValue(false);
      service['disconnectHandler']('transport open');
      expect(service['reconnect']).not.toHaveBeenCalled();
    });
  });

  describe('#getMatchFactData ', () => {
    it('should return opta match fact info and teamName and playerName as Null if related to match-time', () => {
      const matchCmtryDataUpdate = {
        incident: { eventId: '12345', feed: 'OPTA', type: { code: 2, description: 'STOP_FIRST_HALF' }, context: { reasonId: 101, playerName: 'A', teamName: 'B' } }
      } as IMatchCommentaryStatsUpdate;
      expect(service['getMatchFactData'](matchCmtryDataUpdate)).toEqual({
        feed: 'OPTA',
        matchCmtryEventId: '12345',
        varIconData: null,
        matchfact: 'Half Time',
        teamName: null,
        playerName: null,
      } as IMatchCmtryData);
    });
    it('should return opta match fact info', () => {
      const matchCmtryDataUpdate = {
        incident: { eventId: '12345', feed: 'OPTA', type: { code: 602, description: 'test matchfact' }, context: { reasonId: 101, playerName: 'A', teamName: 'B' } }
      } as IMatchCommentaryStatsUpdate;
      expect(service['getMatchFactData'](matchCmtryDataUpdate)).toEqual({
        feed: 'OPTA',
        matchCmtryEventId: '12345',
        varIconData: null,
        matchfact: 'test matchfact',
        teamName: 'B',
        playerName: 'A',
      } as IMatchCmtryData);
    });
    it('should return opta match fact info', () => {
      const matchCmtryDataUpdate = {
        incident: { eventId: '12345', feed: 'OPTA', type: { code: 602, description: 'test matchfact' }, context: null }
      } as IMatchCommentaryStatsUpdate;
      expect(service['getMatchFactData'](matchCmtryDataUpdate)).toEqual({
        feed: 'OPTA',
        matchCmtryEventId: '12345',
        varIconData: null,
        matchfact: 'test matchfact',
        teamName: undefined,
        playerName: undefined,
      } as IMatchCmtryData);
    });
    it('should call getAddtionalFactData if code exists in unique-template', () => {
      const matchCmtryDataUpdate = {
        incident: { eventId: '12345', feed: 'OPTA', type: { code: 215, description: 'test matchfact' }, context: { playerName: 'B', teamName: 'A', playerOffName: 'India', playerOnName: 'B' } }
      } as IMatchCommentaryStatsUpdate;
      spyOn(service as any, 'getAddtionalFactData').and.callThrough();
      expect(service['getMatchFactData'](matchCmtryDataUpdate)).toEqual({
        feed: 'OPTA',
        matchCmtryEventId: '12345',
        varIconData: null,
        matchfact: 'SUBSTITUTION',
        teamName: 'A',
        playerName: null,
        playerOffName: 'India',
        playerOnName: 'B'
      } as IMatchCmtryData);
    });
    it('should return Amelco match fact info', () => {
      const matchCmtryDataUpdate = {
        incident: { eventId: '12345', feed: 'AMELCO', type: { code: 602, description: 'test matchfact' }, context: { reasonId: 101, playerName: 'A', teamName: 'B' } }
      } as IMatchCommentaryStatsUpdate;
      expect(service['getMatchFactData'](matchCmtryDataUpdate)).toEqual({
        feed: 'AMELCO',
        matchCmtryEventId: '12345',
        varIconData: null,
        matchfact: 'test matchfact',
        teamName: 'B'
      } as any);
    });
    it('should return altered match fact info', () => {
      const matchCmtryDataUpdate = {
        incident: { eventId: '12345', feed: 'AMELCO', type: { code: 207, description: 'FREE_KICK_AWARDED' }, context: { reasonId: 101, playerName: 'A', teamName: 'B' } }
      } as IMatchCommentaryStatsUpdate;
      expect(service['getMatchFactData'](matchCmtryDataUpdate)).toEqual({
        feed: 'AMELCO',
        matchCmtryEventId: '12345',
        varIconData: null,
        matchfact: 'FREE KICK',
        teamName: 'B'
      } as any);
    });
  });
  describe('#getAddtionalFactData', () => {
    it('should assign clock data', () => {
      const matchCmtryDataUpdate = {
        incident: { clock: '50:00', eventId: '12345', feed: 'OPTA', type: { code: 103, description: 'Injury' }, context: { playerName: 'B', teamName: 'A' } }
      } as IMatchCommentaryStatsUpdate;
      const Update = service['getAddtionalFactData'](matchCmtryDataUpdate);
      expect(Update).toEqual({ clock: '50:00', matchfact: 'Injury' });
    });
    it('should assign minitues data', () => {
      const matchCmtryDataUpdate = {
        incident: { clock: '50:00', eventId: '12345', feed: 'OPTA', type: { code: 102, description: 'INJURY_TIME' }, context: { playerName: 'B', teamName: 'A', minutes: '4' } }
      } as IMatchCommentaryStatsUpdate;
      const Update = service['getAddtionalFactData'](matchCmtryDataUpdate);
      expect(Update).toEqual({ playerName:null,teamName:null,minutes: '4', matchfact: 'INJURY_TIME' });
    });
    it('should not assign minitues data', () => {
      const matchCmtryDataUpdate = {
        incident: { clock: '50:00', eventId: '12345', feed: 'OPTA', type: { code: 102, description: 'INJURY_TIME' }, context: null }
      } as IMatchCommentaryStatsUpdate;
      const Update = service['getAddtionalFactData'](matchCmtryDataUpdate);
      expect(Update).toEqual({ matchfact: 'INJURY_TIME' });
    });
    it('should assign playerName as null if opta feed and code is 200', () => {
      const matchCmtryDataUpdate = {
        incident: { clock: '50:00', eventId: '12345', feed: 'OPTA', type: { code: 200, description: 'Kick off' }, context: { playerName: 'B', teamName: 'A', minutes: '4' } }
      } as IMatchCommentaryStatsUpdate;
      const Update = service['getAddtionalFactData'](matchCmtryDataUpdate);
      expect(Update).toEqual({ playerName: null, matchfact: 'Kick off' });
    });
    it('should assign TeamName as null if Amelco feed and code is 200', () => {
      const matchCmtryDataUpdate = {
        incident: { clock: '50:00', eventId: '12345', feed: 'AMELCO', type: { code: 200, description: 'Kick off' }, context: { teamName: 'A', minutes: '4' } }
      } as IMatchCommentaryStatsUpdate;
      const Update = service['getAddtionalFactData'](matchCmtryDataUpdate);
      expect(Update).toEqual({ matchfact: 'Kick off', teamName: null });
    });
    it('should not assign playeroffName and playerOnName data', () => {
      const matchCmtryDataUpdate = {
        incident: { clock: '50:00', eventId: '12345', feed: 'OPTA', type: { code: 215, description: 'SUBSTITUTION' }, context: null }
      } as IMatchCommentaryStatsUpdate;
      const Update = service['getAddtionalFactData'](matchCmtryDataUpdate);
      expect(Update).toEqual({ matchfact: 'SUBSTITUTION' });
    });
  });
  describe('#sendRequestForLastMatchFact', () => {
    it('should call liveServConnectionService.sendRequestForLastMatchFact', () => {
      const channels = ['mFACTS1234', 'mFACTS12345'];
      service.sendRequestForLastMatchFact(channels);
      expect(liveServConnectionService.sendRequestForLastMatchFact).toHaveBeenCalledWith(channels, jasmine.any(Function));
    });
    it('should call liveServConnectionService.sendRequestForLastMatchFact with pubsub', () => {
      const channels = ['mFACTS1234', 'mFACTS12345'];
      const connection = { connected: true } as ISocketIO
      pubSubService.subscribe.and.callFake((p1, p2, cb) => cb(connection));
      service.sendRequestForLastMatchFact(channels);
      expect(pubSubService.subscribe).toHaveBeenCalled();
      expect(liveServConnectionService.sendRequestForLastMatchFact).toHaveBeenCalledWith(channels, jasmine.any(Function));
    });
    it('should call liveServConnectionService.sendRequestForLastMatchFact updatesHandlers', () => {
      const channels = ['mFACTS1234', 'mFACTS12345'];
      const matchCmtryDataUpdate = {
        incident: { eventId: '12345', feed: 'OPTA', type: { code: 602, description: 'test matchfact' }, context: { reasonId: 101, playerName: 'A', teamName: 'B' } }
      } as IMatchCommentaryStatsUpdate;
      spyOn(service as any, 'matchCommentryUpdateHandler');
      service.sendRequestForLastMatchFact(channels);
      service['lastCodeCallBacks'].handler(matchCmtryDataUpdate);
      expect(service['matchCommentryUpdateHandler']).toHaveBeenCalledWith(matchCmtryDataUpdate);
    });
  });
  describe('removeHandlers', () => {
    it('liveServConnectionService.removeHandlers to have been called', () => {
      const channels = ['mFACTS123'];
      service.removeHandlers(channels);
      expect(liveServConnectionService.removeAllEventListner).toHaveBeenCalledWith([channels[0]]);
    });
  });
});
