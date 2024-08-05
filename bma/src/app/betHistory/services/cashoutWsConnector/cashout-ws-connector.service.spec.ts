import { CashoutWsConnectorService } from '@app/betHistory/services/cashoutWsConnector/cashout-ws-connector.service';
import { WsConnectorService } from '@core/services/wsConnector/ws-connector.service';
import { UserService } from '@core/services/user/user.service';
import { CashOutLiveServeUpdatesService } from '@app/betHistory/services/cashOutLiveServeUpdatesService/cashOutLiveServeUpdatesService';
import { CommandService } from '@core/services/communication/command/command.service';
import { Observable, of, Subject, throwError } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import { IBetDetail } from '@bpp/services/bppProviders/bpp-providers.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { TimeService } from '@app/core/services/time/time.service';

class MockWsConnector {
  state$ = new Subject();
  connect = jasmine.createSpy('connect');
  disconnect = jasmine.createSpy('disconnect');
  addAnyMessagesHandler = jasmine.createSpy('addAnyMessagesHandler').and.callFake((fn: Function) => { this.handler = fn; });

  private handler: Function;

  emit(event: string, data: any) {
    this.handler(event, data);
  }
}

const unauthorizedErrorMessage = { error: { code: 'UNAUTHORIZED_ACCESS' } };
const unknownServiceErrorMessage = { error: { code: 'UNKNOWN_SERVICE_ERROR' } };

describe('CashoutWsConnectorService', () => {
  let service: CashoutWsConnectorService;
  let wsConnectorService: Partial<WsConnectorService>;
  let userService: Partial<UserService>;
  let cashOutLiveServeUpdatesService: Partial<CashOutLiveServeUpdatesService>;
  let commandService: Partial<CommandService>;
  let awsService: Partial<AWSFirehoseService>;
  let timeService: Partial<TimeService>;

  beforeEach(() => {
    wsConnectorService = {
      create: jasmine.createSpy('create').and.returnValue(new MockWsConnector()),
    };

    userService = {
      bppToken: 'abc123',
    };

    awsService = {
      addAction: jasmine.createSpy('addAction'),
    };

    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('2019-04-26 00:00:00')
    } as any;
    
    cashOutLiveServeUpdatesService = {
      updateBetDetails: jasmine.createSpy(),
      applyCashoutValueUpdate: jasmine.createSpy(),
      updatePayoutDetails: jasmine.createSpy(),
      updateEventDetail:jasmine.createSpy(),
      update2UpSelection:jasmine.createSpy()
    };

    service = new CashoutWsConnectorService(
      wsConnectorService as WsConnectorService,
      userService as UserService,
      cashOutLiveServeUpdatesService as CashOutLiveServeUpdatesService,
      commandService as CommandService,
      awsService as AWSFirehoseService,
      timeService as TimeService
    );

    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue([]),
      API: { BPP_AUTH_SEQUENCE: '' }
    };
  });

  afterAll(() => {
    service = null;
  });

  describe('trackConnectionState', () => {
    it('should call trackConnection for newrelic call', () => {
      const state = 'cashoutUpdates->error->test';
      service['trackConnectionState'](state,{ data: { error: 'test' }});
      expect(awsService.addAction).toHaveBeenCalled();
    });
  });

  describe('constructor', () => {
    it('should init default values', () => {
      expect(service).toBeTruthy();
      expect(service['CASHOUT_MS_ENDPOINT']).toEqual(environment.CASHOUT_MS);
      expect(service['moduleName']).toBe('cashout');
      expect(service['subscribers']).toBe(0);
      expect(service['unknownErrorReconnectAttempts']).toBe(3);
    });
  });

  describe('streamBetDetails', () => {
    const observable = Symbol('observable') as any;
    beforeEach(() => {
      (service as any).betDetails$ = { asObservable: jasmine.createSpy('asObservable').and.returnValue(observable) };
      spyOn(service as any, 'reconnect').and.callThrough();
    });

    it('should return connection observable', () => {
      expect(service.streamBetDetails()).toEqual(observable);
    });

    it('should increment subscribers amount', () => {
      expect((service as any).subscribers).toEqual(0);
      service.streamBetDetails();
      expect((service as any).subscribers).toEqual(1);
    });

    it('should reconnect the CashoutWS', () => {
      service.streamBetDetails();
      expect((service as any).reconnect).toHaveBeenCalled();
    });
  });

  describe('nextPageCashoutDataEventHandler', () => {
    it('#nextPageCashoutDataEventHandler to trigger pageScrollCallBack', () => {
      service['pageScrollCallBack'] = () => {"test"};
      service['nextPageCashoutDataEventHandler']({paging: {
        token: "pagingtoken"
      }});
      expect(service['pageScrollCallBack']).toEqual(jasmine.any(Function));
    });
    it('#nextPageCashoutDataEventHandler not to trigger pageScrollCallBack', () => {
      service['pageScrollCallBack'] = new Function();
      
      const spy = spyOn(service as any, 'pageScrollCallBack');
      service['pageScrollCallBack'] = null;
      service['nextPageCashoutDataEventHandler']({paging: {
        token: "pagingtoken"
      }});
      expect(spy).not.toHaveBeenCalled();
    });
    it('#nextPageCashoutDataEventHandler to trigger pageScrollCallBack', () => {
      service['nextPageCashoutDataEventHandler']({});
      expect(service['trackUpdatesError']).toEqual(jasmine.anything());
    });
  });
  describe('getFormattedDateObject', () => {
    beforeEach(() => {
      spyOn(service as any, 'getDateObject').and.callThrough();
    });
    it('#getFormattedDateObject should return dates object', () => {
      expect(service.getFormattedDateObject()).toEqual({startDate: {value: new Date('2019-04-26T00:00:00')}, endDate: {value: new Date('2019-04-26T00:00:00')}});
    });
  })

  describe('updateBet', () => {
    it('should emit updateBet WS message', () => {
      (service as any).connection = { emit: jasmine.createSpy('emit') };
      service.updateBet({ betId: '1234' } as any);
      expect((service as any).connection.emit).toHaveBeenCalledWith('updateBet', { betId: '1234', updateType: 'cashedOut' });
    });
  });

  describe('dateChangeBet', () => {
    it('should emit dateChangeBet WS message', () => {
      (service as any).connection = { emit: jasmine.createSpy('emit') };
      service.dateChangeBet({value: new Date('2021-10-22')}, {value: new Date('2021-10-25')} as any);//TBU
      expect((service as any).connection.emit).toHaveBeenCalledWith('initialBets', {
        detailLevel: 'DETAILED',
        pagingBlockSize: '20',
        token: userService.bppToken,
        fromDate: '2019-04-26 00:00:00',
        toDate: '2019-04-26 00:00:00',
        group: 'BET',
        settled: 'N'
      });
    });
    it('dateChangeBet picking default dateObject', () => {
      (service as any).connection = { emit: jasmine.createSpy('emit') };
      service.dateChangeBet();//TBU
      expect((service as any).connection.emit).toHaveBeenCalledWith('initialBets', {
        detailLevel: 'DETAILED',
        pagingBlockSize: '20',
        token: userService.bppToken,
        fromDate: '2019-04-26 00:00:00',//TBU
        toDate: '2019-04-26 00:00:00',//TBU
        group: 'BET',
        settled: 'N'
      });
    });
  });

  describe('nextCashoutBet', () => {
    it('should emit nextCashoutBet WS message', () => {
      (service as any).connection = { emit: jasmine.createSpy('emit') };
      service.pagingToken = 'test';
      service.nextCashoutBet();
      expect((service as any).connection.emit).toHaveBeenCalledWith('nextBets', {
        detailLevel: 'DETAILED', 
        blockSize: '20', 
        pagingToken: 'test',
        token: userService.bppToken
      });
    });
    it('should not emit nextCashoutBet WS message', () => {
      service['connection'] = {
        emit: jasmine.createSpy('emit')
      } as any;
      service.nextCashoutBet();
      expect(service['connection'].emit).not.toHaveBeenCalled();
    });
  });

  describe('closeStream', () => {
    describe('if only one subscriber', () => {
      beforeEach(() => service['subscribers'] = 1);

      it('should close connection', () => {
        const spy = spyOn(service as any, 'closeConnection');
        service.closeStream();
        expect(spy).toHaveBeenCalled();
      });

      it('should decrease subscribers count', () => {
        service.closeStream();
        expect(service['subscribers']).toBe(0);
      });
    });

    describe('if more than one subscriber', () => {
      beforeEach(() => service['subscribers'] = 4);
      it('should not call close connection', () => {
        const spy = spyOn(service as any, 'closeConnection');
        service.closeStream();
        expect(spy).not.toHaveBeenCalled();
      });

      it('should decrease subscribers count', () => {
        service.closeStream();
        expect(service['subscribers']).toBe(3);
      });
    });

    describe('if no subscribers', () => {
      beforeEach(() => service['subscribers'] = 0);
      it('should not call close connection', () => {
        const spy = spyOn(service as any, 'closeConnection');
        service.closeStream();
        expect(spy).not.toHaveBeenCalled();
      });
    });

    it('should handle state change without handler', () => {
      expect(function() {
        service['handleConnectionStateChange']('disconnect');
      }).not.toThrow();
    });
  });

  describe('event handlers', () => {
    let returnedBetDetails$: Observable<IBetDetail[]>;
    beforeEach(() => {
      returnedBetDetails$ = service.streamBetDetails();
    });

    describe('handle socket messages', () => {
      describe('initial', () => {
        it('should emit betDetails$ when correct initial data received', (done) => {
          const bets = [1, 2, 3] as any;

          returnedBetDetails$.subscribe((data) => {
            expect(data).toEqual(bets);
            done();
          });

          // emit event
          service['connection'].emit('initial', { bets, paging: {token: '1'} });
        });
        it('should complete betDetails$ when correct initial data received', (done) => {
          const bets = [1, 2, 3] as any;

          returnedBetDetails$.subscribe(
            null,
            null,
            () => {
              expect(true).toBeTruthy();
              done();
            });

          // emit event
          service['connection'].emit('initial', { bets, paging: {token: '1'} });
        });
        it('should log to AWS if incorrect data received', () => {
          service['connection'].emit('initial', { error: 'test' });
          expect(awsService.addAction).toHaveBeenCalledWith(
            'cashoutUpdates->error->initial',
            { data: { error: 'test' } }
          );
        });
        it('should handle UNAUTHORIZED_ACCESS error', () => {
          const spy = spyOn(service as any, 'handleUnauthorisedError').and.returnValue(of([]));

          service['connection'].emit('initial', unauthorizedErrorMessage);
          expect(spy).toHaveBeenCalled();
        });
        it('should throw betDetails error if failed UNAUTHORIZED_ACCESS error handler', (done) => {
          spyOn(service as any, 'handleUnauthorisedError').and.returnValue(throwError('failed'));
          service['connection'].emit('initial', unauthorizedErrorMessage);

          returnedBetDetails$.subscribe(
            null,
            () => {
              expect(true).toBeTruthy();
              done();
            });
        });
        it('should reconnect if UNKNOWN_SERVICE_ERROR and service has reconnection attempts', () => {
          const spy = spyOn(service as any, 'reconnect');
          service['unknownErrorReconnectAttempts'] = 3;
          service['connection'].emit('initial', unknownServiceErrorMessage);
          expect(spy).toHaveBeenCalled();
          expect(service['unknownErrorReconnectAttempts']).toBe(2);
        });
        it('should not reconnect it UNKNOWN_SERVICE_ERROR and no reconnection attempts', () => {
          const spy = spyOn(service as any, 'reconnect');
          service['unknownErrorReconnectAttempts'] = 0;
          service['connection'].emit('initial', unknownServiceErrorMessage);
          expect(spy).not.toHaveBeenCalled();
        });
        it('should close connection and throw betDetails error if unknown error', (done) => {
          service['connection'].emit('initial', { error: 'test'});

          returnedBetDetails$.subscribe(
            null,
            () => {
              expect(service['connection']).toBeFalsy();
              done();
            });
        });
      });
      describe('betUpdate', () => {
        it('should call cashOutLiveServeUpdatesService.updateBetDetails if valid data', () => {
          // emit event
          service['connection'].emit('betUpdate', { bet: { } });
          expect(cashOutLiveServeUpdatesService.updateBetDetails).toHaveBeenCalled();
        });
        it('should log an error if invalid data', () => {
          const spy = spyOn(service as any, 'trackUpdatesError');
          // emit event
          service['connection'].emit('betUpdate', { noBet: { } });
          expect(spy).toHaveBeenCalledWith('betUpdate', { noBet: { } });
        });
        it('should handle UNAUTHORIZED_ACCESS', () => {
          const spy  = spyOn(service as any, 'handleUnauthorisedError').and.callThrough();
          service['connection'].emit('betUpdate', unauthorizedErrorMessage);
          expect(spy).toHaveBeenCalled();
        });
      });
      describe('cashoutUpdate', () => {
        it('should call cashOutLiveServeUpdatesService.applyCashoutValueUpdate if valid data', () => {
          // emit event
          service['connection'].emit('cashoutUpdate', { cashoutData: { } });
          expect(cashOutLiveServeUpdatesService.applyCashoutValueUpdate).toHaveBeenCalled();
        });
        it('should log an error if invalid data', () => {
          const spy = spyOn(service as any, 'trackUpdatesError');
          // emit event
          service['connection'].emit('cashoutUpdate', { notValid: { } });
          expect(spy).toHaveBeenCalledWith('cashoutUpdate', { notValid: { } });
        });
      });
      describe('payoutUpdate', () => {
        it('should call cashOutLiveServeUpdatesService.updatePayoutDetails if valid data', () => {
          // emit event
          service['connection'].emit('payoutUpdate', [{ returns: 0.09, betNo:'12334'}]);
          expect(cashOutLiveServeUpdatesService.updatePayoutDetails).toHaveBeenCalled();
        });
        it('should log an error if invalid data', () => {
          const spy = spyOn(service as any, 'trackUpdatesError');
          // emit event
          service['connection'].emit('payoutUpdate', { notValid: { } });
          expect(spy).toHaveBeenCalledWith('payoutUpdate', { notValid: { } });
        });
      });
      describe('evetUpdate', () => {
        it('should call cashOutLiveServeUpdatesService.eventUpdateEventHandler if valid data', () => {
          // emit event
          service['handleMessage']('eventUpdate', {
            "event": {
              "eventId": "240801945",
              "VOD": true
            }
          });
          expect(cashOutLiveServeUpdatesService.updateEventDetail).toHaveBeenCalled();
        });
        it('should log an error if invalid data', () => {
          const spy = spyOn(service as any, 'trackUpdatesError');
          // emit event
          service['handleMessage']('eventUpdate', { notValid: {} });
          expect(spy).toHaveBeenCalledWith('eventUpdate', { notValid: {} });
        });
      });
      describe('twoUpUpdate', () => {
        it('should call cashOutLiveServeUpdatesService.twoUpUpdateEventHandler if valid data', () => {
          // emit event
          service['handleMessage']('twoUpUpdate', {
            twoUp: {
              selectionId: 240801945,
              betIds:[22222,222221],
              twoUpSettled:true
            }
          });
          expect(cashOutLiveServeUpdatesService.update2UpSelection).toHaveBeenCalled();
        });
        it('should log an error if invalid data', () => {
          const spy = spyOn(service as any, 'trackUpdatesError');
          // emit event
          service['handleMessage']('twoUpUpdate', { notValid: {} });
          expect(spy).toHaveBeenCalledWith('twoUpUpdate', { notValid: {} });
        });
      });
      it('should trackConnectionState', () => {
        service['trackConnectionState']('connected');
        expect(awsService.addAction).toHaveBeenCalled();
      });
    });
  });

});
