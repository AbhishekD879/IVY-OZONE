import { RemoteBetslipService } from './remote-betslip.service';
import environment from '@environment/oxygenEnvConfig';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { remoteBetslipConstant } from '@core/services/remoteBetslip/remote-betslip.constant';
import { Subject, of as observableOf, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

describe('RemoteBetslipService', () => {
  let service: RemoteBetslipService;
  let WSConnector;
  let sessionStorage;
  let time;
  let command;
  let pubsub;
  let gtmTrackingService;
  let connection;
  let handlers;
  let cmsService;
  let pubSubService;
  let windowRef;
  let timeoutHandler;
  let fanzoneStorageService;
  let userService;
  beforeEach(() => {
    handlers = {};
    connection = {
      updateOptions: jasmine.createSpy(),
      connect: jasmine.createSpy(),
      disconnect: jasmine.createSpy(),
      removeOption: jasmine.createSpy(),
      addAnyMessagesHandler: jasmine.createSpy().and.callFake(handler => {
        handlers['addAnyMessagesHandler'] = handler;
      }),
      emit: jasmine.createSpy().and.returnValue(new Subject())
    };
    WSConnector = {
      create: jasmine.createSpy().and.returnValue(connection)
    };
    sessionStorage = {
      get: jasmine.createSpy('get').and.returnValue({
        date: new Date('10/11/50')
      }),
      remove: jasmine.createSpy('remove'),
      set: jasmine.createSpy('set')
    };
    time = {
      daysDifference: jasmine.createSpy().and.returnValue(0.5)
    };
    command = {};
    pubsub = {
      API: pubSubApi,
      publish: jasmine.createSpy()
    };
    gtmTrackingService = {
      getTracking: jasmine.createSpy('getTracking'),
      restoreTracking: jasmine.createSpy('restoreTracking')
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({ BalanceUpdate: {}}))
    };

    pubSubService = {
      publish: jasmine.createSpy(),
      API: {
        IMPLICIT_BALANCE_REFRESH: 'IMPLICIT_BALANCE_REFRESH'
      }
    };

    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake((callback) => {
          timeoutHandler = callback;
        }),
        clearTimeout: jasmine.createSpy('clearTimeout')
      }
    };

    fanzoneStorageService = {
      get: jasmine.createSpy('get')
    };

    userService = {
      status: jasmine.createSpy('status').and.returnValue(true)
    };
    service = new RemoteBetslipService(
      WSConnector,
      sessionStorage,
      time,
      command,
      pubsub,
      gtmTrackingService,
      cmsService,
      pubSubService,
      windowRef,
      fanzoneStorageService,
      userService
    );
  });

  it('constructor', () => {
    expect(service).toBeDefined();
    expect(RemoteBetslipService.STORAGE_KEY).toBe('RemoteBS');
    expect(RemoteBetslipService.UPDATE_CHANNELS).toEqual(['sEVENT', 'sEVMKT', 'sSELCN']);
    expect(WSConnector.create).toHaveBeenCalledWith(environment.REMOTEBETSLIPMS, jasmine.any(Object), 'quickbet-ms');
    expect(connection.addAnyMessagesHandler).toHaveBeenCalled();
  });

  it('should get configs', () => {
    expect(service.configs).toBe(remoteBetslipConstant);
  });

  describe('Restore', () => {
    it('should get session data', () => {
      spyOn(service as any, 'getSessionData').and.returnValue({});
      service.restoreSession();

      expect(service['getSessionData']).toHaveBeenCalled();
    });

    it('should restore session', () => {
      service.restoreSession();

      expect(gtmTrackingService.restoreTracking).toHaveBeenCalled();
      expect(connection.updateOptions).toHaveBeenCalled();
      expect(connection.connect).toHaveBeenCalled();
    });

    it('should clear session', () => {
      time.daysDifference = jasmine.createSpy().and.returnValue(2);
      service.restoreSession();

      expect(sessionStorage.remove).toHaveBeenCalledWith('RemoteBS');
      expect(gtmTrackingService.restoreTracking).not.toHaveBeenCalled();
      expect(connection.updateOptions).not.toHaveBeenCalled();
      expect(connection.connect).toHaveBeenCalled();
    });
  });

  describe('StoreSession', () => {
    it('should get and add bet tracking', () => {
      gtmTrackingService.getTracking.and.returnValue({});
      service['storeSession']();

      expect(gtmTrackingService.getTracking).toHaveBeenCalled();
      expect(sessionStorage.set).toHaveBeenCalled();

      const storageData = sessionStorage.set.calls.argsFor(0)[1];
      expect(storageData.hasOwnProperty('betTrace')).toBe(true);
    });

    it('should get but not add bet tracking if empty', () => {
      service['storeSession']();

      expect(gtmTrackingService.getTracking).toHaveBeenCalled();
      expect(sessionStorage.set).toHaveBeenCalled();

      const storageData = sessionStorage.set.calls.argsFor(0)[1];
      expect(storageData.hasOwnProperty('betTrace')).toBe(false);
    });

    it('should update session storage data', () => {
      sessionStorage.get = jasmine.createSpy('get').and.returnValue({
        test_1: 1,
        test_2: 2
      });

      service['storeSession']();

      expect(sessionStorage.set).toHaveBeenCalledWith(
        RemoteBetslipService.STORAGE_KEY,
        jasmine.objectContaining({
        selectionData: {
          test_1: 1,
          test_2: 2
        }
      }));
    });

    it('should not update data',  () => {
      sessionStorage.get = jasmine.createSpy('get').and.returnValue(null);
      service['sessionId'] = '1';

      service['storeSession']();

      expect(sessionStorage.set).toHaveBeenCalledWith(
        RemoteBetslipService.STORAGE_KEY,
        {
          id: '1',
          date: jasmine.any(Number)
        }
      );
    });
  });

  it('should remove selection', () => {
    service.removeSelection();
    expect(connection.emit).toHaveBeenCalled();
  });

  it('should connect', () => {
    service.connect();
    expect(connection.connect).toHaveBeenCalled();
  });

  it('should disconnect', () => {
    service.disconnect();
    expect(connection.disconnect).toHaveBeenCalled();
  });

  it('should call global handler', () => {
    handlers.addAnyMessagesHandler('sSELCN');
    expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.QUICKBET_SELECTION_UPDATE, [ 'sSELCN', undefined ]);
  });
  it('should init session', () => {
    service['updateOptions'] = jasmine.createSpy();
    const id = 'zxsdwe';
    service['onSessionInitHandler']({id});
    expect(service['sessionId']).toEqual(id);
    expect(connection['updateOptions']).toHaveBeenCalled();
  });
  it('onErrorHandler', () => {
    service['clearSession'] = jasmine.createSpy();
    connection.connect.and.returnValue(observableOf());
    service['onErrorHandler']({});
    expect(connection.disconnect).toHaveBeenCalled();
    expect(connection.connect).toHaveBeenCalled();
  });
  it('should clear session', () => {
    service['clearSession'] = jasmine.createSpy();
    service['onSessionClearHandler']();
    expect(service['clearSession']).toHaveBeenCalled();
  });
  describe('addSelection', () => {
    it('should add selection', () => {
      const outcome = {
        outcomeIds: [1, 2, 3],
        selectionType: 'multiple'
      };

      expect(service.addSelection(outcome) instanceof Subject).toBe(true);
    });
    it('should publish events of  add selection', fakeAsync(() => {
      const outcome = {
        outcomeIds: [1, 2, 3],
        selectionType: 'multiple'
      };
      const config = {add:{change:'41003'}};
      const response = { error: 500 };
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');
      fanzoneStorageService.get = jasmine.createSpy('fanzoneStorageService.get').and.returnValue({teamId: '4dsgumo7d4zupm2ugsvm4zm4d'});
      

      service.addSelection(outcome, config)
        .subscribe(successHandler, errorHandler);
      tick();

      expect(successHandler).not.toHaveBeenCalled();
    }));
    it('should handle error of add selection', fakeAsync(() => {
      const outcome = {
        outcomeIds: [1, 2, 3],
        selectionType: 'multiple'
      };
      const response = { error: 500 };
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');
      fanzoneStorageService.get = jasmine.createSpy('fanzoneStorageService.get').and.returnValue(null);

      connection.emit.and.returnValue(throwError(response));

      service.addSelection(outcome)
        .subscribe(successHandler, errorHandler);
      tick();

      expect(successHandler).not.toHaveBeenCalled();
      expect(errorHandler).toHaveBeenCalled();

      service.addSelection(outcome);
      tick();

      expect(errorHandler).toHaveBeenCalledTimes(1);
    }));

    it('should handle success message as add selection response and store session', fakeAsync(() => {
      const outcome = {
        outcomeIds: [1, 2, 3],
        selectionType: 'multiple'
      };
      const response = { data: {} };
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');

      connection.emit.and.returnValue(observableOf());
      fanzoneStorageService.get = jasmine.createSpy('fanzoneStorageService.get').and.returnValue({idResignedUser: true});
      service.addSelection(outcome).subscribe(successHandler, errorHandler);
      service['anyMessageHandler']('31001', response);
      tick();

      expect(successHandler).toHaveBeenCalledWith(response);
      expect(errorHandler).not.toHaveBeenCalled();
      expect(gtmTrackingService.getTracking).toHaveBeenCalled();
      expect(sessionStorage.set).toHaveBeenCalledWith('RemoteBS', jasmine.objectContaining({
        id: null,
        date: jasmine.any(Number)
      }));

      service.addSelection(outcome);
      tick();

      expect(successHandler).toHaveBeenCalledTimes(1);
    }));

    it('should handle success message as add selection response and not store session as its stream n bet', fakeAsync(() => {
      const outcome = {
        outcomeIds: [1, 2, 3],
        selectionType: 'multiple',
        isStreamBet: true
      };
      const response = { data: {} };
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');

      connection.emit.and.returnValue(observableOf());
      fanzoneStorageService.get = jasmine.createSpy('fanzoneStorageService.get').and.returnValue({idResignedUser: true});
      service.addSelection(outcome).subscribe(successHandler, errorHandler);
      service['anyMessageHandler']('31001', response);
      tick();

      expect(successHandler).toHaveBeenCalledWith(response);
      expect(errorHandler).not.toHaveBeenCalled();
      expect(gtmTrackingService.getTracking).not.toHaveBeenCalled();
      expect(sessionStorage.set).not.toHaveBeenCalled();

      service.addSelection(outcome);
      tick();

      expect(successHandler).toHaveBeenCalledTimes(1);
    }));

    it('should Not handle timeout error when response from MS was received', fakeAsync(() => {
      service.timeoutId = 123;
      const outcome = {
        outcomeIds: [1, 2, 3],
        selectionType: 'multiple',
        fanzoneTeamId: '4dsgumo7d4zupm2ugsvm4zm4d'
      };
      const response = { data: {} };
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');

      connection.emit.and.returnValue(observableOf());

      service.addSelection(outcome).subscribe(successHandler, errorHandler);
      service['anyMessageHandler']('31001', response);
      tick();

      expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalledWith(123);
      expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalledTimes(2);
      expect(successHandler).toHaveBeenCalledWith(response);
      expect(errorHandler).not.toHaveBeenCalled();
      expect(sessionStorage.remove).not.toHaveBeenCalled();

      service.addSelection(outcome);
      tick();

      expect(successHandler).toHaveBeenCalledTimes(1);
    }));

    it('should handle timeout error when response from MS was not received', fakeAsync(() => {
      service.timeoutId = 123;
      const outcome = {
        outcomeIds: [1, 2, 3],
        selectionType: 'multiple'
      };
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');

      connection.emit.and.returnValue(observableOf());

      service.addSelection(outcome).subscribe(successHandler, errorHandler);
      tick();

      expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalledWith(123);
      expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalledTimes(1);
      expect(successHandler).not.toHaveBeenCalled();
      expect(errorHandler).not.toHaveBeenCalled();
      expect(sessionStorage.remove).not.toHaveBeenCalled();

      timeoutHandler();
      tick();

      expect(sessionStorage.remove).toHaveBeenCalled();
      expect(service['connection'].removeOption).toHaveBeenCalledWith('query');
      expect(service['connection'].disconnect).toHaveBeenCalled();
    }));

    it('should handle timeout error', fakeAsync(() => {
      const outcome = { outcomeIds: [1, 2, 3], selectionType: 'multiple' };
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');
      service.timeoutId = 123;
      connection.emit.and.returnValue(observableOf());

      service.addSelection(outcome).subscribe(successHandler, errorHandler);
      timeoutHandler();
      tick();

      expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalledWith(123);
      expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalledTimes(2);
      expect(successHandler).not.toHaveBeenCalled();
      expect(errorHandler).toHaveBeenCalledWith({ error: 'timeout' });
    }));
  });

  describe('placeBet', () => {
    const bet = {
      currency: 'USD',
      price: '100',
      stake: '1/2',
      token: 'dsdsadf12312',
      winType: 'jackpot',
      clientUserAgent: 'S|W|I0000000'
    };
    const nremoteBetslipConstant=remoteBetslipConstant as any;

    it('should return instance of Subject', () => {
      expect(service.placeBet(bet,nremoteBetslipConstant.sgl) instanceof Subject).toBe(true);
    });

    it('should handle error after place bet emit', fakeAsync(() => {
      const response = { error: 500 };
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');

      connection.emit.and.returnValue(throwError(response));

      service.placeBet(bet,nremoteBetslipConstant.sgl)
        .subscribe(successHandler, errorHandler);
      tick();

      expect(successHandler).not.toHaveBeenCalled();
      expect(errorHandler).toHaveBeenCalled();

      service.placeBet(bet,nremoteBetslipConstant.sgl);
      tick();

      expect(errorHandler).toHaveBeenCalledTimes(1);
    }));

    it('should handle error message as place bet response', fakeAsync(() => {
      const response = { error: 500 };
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');

      connection.emit.and.returnValue(observableOf());

      service.placeBet(bet,nremoteBetslipConstant.sgl).subscribe(successHandler, errorHandler);
      service['anyMessageHandler']('31012', response);
      tick();

      expect(successHandler).not.toHaveBeenCalled();
      expect(errorHandler).toHaveBeenCalledWith(response);

      service.placeBet(bet,nremoteBetslipConstant.sgl);
      tick();

      expect(errorHandler).toHaveBeenCalledTimes(1);
    }));

    it('should handle overask message after place bet response', fakeAsync(() => {
      const response = { data: { status: 'readBet' } };
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');

      connection.emit.and.returnValue(observableOf());

      service.placeBet(bet,nremoteBetslipConstant.sgl).subscribe(successHandler, errorHandler);
      service['anyMessageHandler']('30031', response);
      tick();

      expect(successHandler).not.toHaveBeenCalled();
      expect(errorHandler).toHaveBeenCalledWith({ data: { error: { description: 'overask', code: 'OVERASK' } } });
      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.REMOTE_BETSLIP_OVERASK_TRIGGERED, response);

      service.placeBet(bet,nremoteBetslipConstant.sgl);
      tick();

      expect(errorHandler).toHaveBeenCalledTimes(1);
    }));

    it('should handle success message as place bet response', fakeAsync(() => {
      const response = { data: {} };
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');
      service['implicitBalanceRefresh'] = jasmine.createSpy();

      connection.emit.and.returnValue(observableOf());

      service.placeBet(bet,).subscribe(successHandler, errorHandler);
      service['anyMessageHandler']('30012', response);
      tick();

      expect(successHandler).toHaveBeenCalledWith(response);
      expect(errorHandler).not.toHaveBeenCalled();

      service.placeBet(bet,nremoteBetslipConstant.sgl);
      tick();

      expect(successHandler).toHaveBeenCalledTimes(1);
      expect(service['implicitBalanceRefresh']).toHaveBeenCalledWith(true);
    }));

    describe('should handle bir and success messages,', () => {
      let response, successHandler;

      beforeEach(() => {
        response = {
          data: {
            receipt: [{}],
          }
        };
        successHandler = jasmine.createSpy('successHandler');
        service['addIsBirFlagToReceipt'] = jasmine.createSpy('addIsBirFlagToReceipt').and.returnValue(response);
        service['implicitBalanceRefresh'] = jasmine.createSpy('implicitBalanceRefresh');
        connection.emit.and.returnValue(observableOf());

        service.placeBet(bet,nremoteBetslipConstant.sgl).subscribe(successHandler);
      });

      it('OpenBetBir is exist', fakeAsync(() => {
        const birResponse =  { provider: 'OpenBetBir' };

        service['anyMessageHandler']('30013', birResponse);
        service['anyMessageHandler']('30012', response);
        tick();

        expect(service['addIsBirFlagToReceipt']).toHaveBeenCalledWith(response, false);
        expect(successHandler).toHaveBeenCalled();
      }));

      it('is not equal OpenBetBir', fakeAsync(() => {
        const birResponse =  { provider: 'OpenBet' };

        service['anyMessageHandler']('30013', birResponse);
        service['anyMessageHandler']('30012', response);
        tick();

        expect(service['addIsBirFlagToReceipt']).toHaveBeenCalledWith(response, false);
        expect(successHandler).toHaveBeenCalled();
      }));
    });
  });

  describe('implicitBalanceRefresh', () => {
    it('should not call balance refresh if no system config BalanceUpdate', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({ test: 'No balance' }));
      service['implicitBalanceRefresh'](true);

      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should not call balance refresh if success and no system config BalanceUpdate RemoteBetslipSuccess', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({ BalanceUpdate: {} }));
      service['implicitBalanceRefresh'](true);

      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should call balance refresh if success and RemoteBetslipSuccess config', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({ BalanceUpdate: { RemoteBetslipSuccess: true } }));
      service['implicitBalanceRefresh'](true);

      expect(pubSubService.publish).toHaveBeenCalledWith('IMPLICIT_BALANCE_REFRESH');
    });

    it('should not call balance refresh if error and no system config RemoteBetslipError', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({ BalanceUpdate: {} }));
      service['implicitBalanceRefresh'](false);

      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should call balance refresh if error and RemoteBetslipError config', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({ BalanceUpdate: { RemoteBetslipError: true } }));
      service['implicitBalanceRefresh'](false);

      expect(pubSubService.publish).toHaveBeenCalledWith('IMPLICIT_BALANCE_REFRESH');
    });
  });

  describe('getErrorHandler', () => {
    it('should call balance update if updateBalance field is passed', () => {
      service['implicitBalanceRefresh'] = jasmine.createSpy();
      service['getErrorHandler'](new Subject(), true)();
      expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalledTimes(1);
      expect(service['implicitBalanceRefresh']).toHaveBeenCalledWith(false);
    });

    it('should not call balance update if updateBalance field is missed', () => {
      service['implicitBalanceRefresh'] = jasmine.createSpy();
      service['getErrorHandler'](new Subject())();
      expect(service['implicitBalanceRefresh']).not.toHaveBeenCalledWith(false);
    });
  });

  it('overAskHandler should call balance update', () => {
    service['implicitBalanceRefresh'] = jasmine.createSpy();
    service['overAskHandler'](new Subject())();
    expect(service['implicitBalanceRefresh']).toHaveBeenCalledWith(false);
  });

  it('should clear session', () => {
    service['clearSession']();
    expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalledTimes(1);
    expect(sessionStorage.remove).toHaveBeenCalledWith('RemoteBS');
  });

  it('addIsBirFlagToReceipt should return value which contains a receipt with isBir property', () => {
    const value = {
      data: { receipt: [{}] }
    };

    expect(service['addIsBirFlagToReceipt'](value, true).data.receipt[0]).toEqual({ isBir: true });
  });

  it('getConfig if LuckyDip Available', () => {
    const config = {
      luckyDipPlaceBet: {},
      placeBet: {}
    };
    sessionStorage.get = jasmine.createSpy('get').and.returnValue('LuckyDip');

 
    service['getConfig'](config);
    expect(service['getConfig'](config)).toEqual({});
  });

  it('getConfig if LuckyDip not Available', () => {
    const config = {
      luckyDipPlaceBet: {},
      placeBet: {}
    };
    sessionStorage.get = jasmine.createSpy('get').and.returnValue(null);

 
    service['getConfig'](config);
    expect(service['getConfig'](config)).toEqual({});
  });

});
