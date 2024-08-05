import { fakeAsync, tick } from '@angular/core/testing';

import { QuickbetRunService } from './quickbet-run.service';
import { commandApi } from '@app/core/services/communication/command/command-api.constant';

describe('QuickbetRunService', () => {

  let commandService;
  let service;
  let quickbetService;
  let quickbetNotificationService;
  let quickbetShowQuickBetHandler;
  let quickbetRestoreHandler;
  let quickbetShowErrorHandler;
  let quickbetClearErrorHandler;

  beforeEach(() => {
    commandService = {
      register: jasmine.createSpy('register').and.callFake((name, handler) => {
        if (name === commandApi.QUICKBET_RESTORE) {
          quickbetRestoreHandler = handler;
        } else if (name === commandApi.QUICKBET_SHOW_ERROR) {
          quickbetShowErrorHandler = handler;
        } else if (name === commandApi.QUICKBET_CLEAR_ERROR) {
          quickbetClearErrorHandler = handler;
        } else if(name === commandApi.SHOW_QUICKBET) {
          quickbetShowQuickBetHandler = handler;
        }
      }),
      executeAsync: jasmine.createSpy().and.returnValue(Promise.resolve([{}, {}])),
      API: commandApi
    };

    quickbetService = {
      restoreSelection: jasmine.createSpy('restoreSelection'),
      showQuickbet: jasmine.createSpy('showQuickbet')
    };
    
    quickbetNotificationService = {
      saveErrorMessage: jasmine.createSpy('saveErrorMessage'),
      clear: jasmine.createSpy('clear')
    };

    service = new QuickbetRunService(commandService, quickbetService, quickbetNotificationService);
  });

  it('Should register Quickbet API', () => {
    service.init();
    expect(commandService.register).toHaveBeenCalledWith(commandApi.SHOW_QUICKBET, jasmine.any(Function));
    expect(commandService.register).toHaveBeenCalledWith(commandApi.QUICKBET_RESTORE, jasmine.any(Function));
    expect(commandService.register).toHaveBeenCalledWith(commandApi.QUICKBET_SHOW_ERROR, jasmine.any(Function));
    expect(commandService.register).toHaveBeenCalledWith(commandApi.QUICKBET_CLEAR_ERROR, jasmine.any(Function));
  });

  describe('@init', () => {
    let successHandler,
      errorHandler;

    beforeEach(() => {
      successHandler = jasmine.createSpy('successHandler');
      errorHandler = jasmine.createSpy('errorHandler');
    });

    it('Should handle showQuickBetSelection', fakeAsync(() => {
      service.init();

      const actualResult = quickbetShowQuickBetHandler();
      actualResult.then(successHandler, errorHandler);
      tick();

      expect(successHandler).toHaveBeenCalled();
      expect(quickbetService.showQuickbet).toHaveBeenCalled();
    }));

    it('Should handle restoreSelection', fakeAsync(() => {
      service.init();

      const actualResult = quickbetRestoreHandler();
      actualResult.then(successHandler, errorHandler);
      tick();

      expect(successHandler).toHaveBeenCalled();
      expect(quickbetService.restoreSelection).toHaveBeenCalled();
    }));

    it('Should handle quickbet show error', fakeAsync(() => {
      service.init();

      const actualResult = quickbetShowErrorHandler();
      actualResult.then(successHandler, errorHandler);
      tick();

      expect(successHandler).toHaveBeenCalled();
      expect(quickbetNotificationService.saveErrorMessage).toHaveBeenCalled();
    }));

    it('Should handle quickbet clear error', fakeAsync(() => {
      service.init();

      const actualResult = quickbetClearErrorHandler();
      actualResult.then(successHandler, errorHandler);
      tick();

      expect(successHandler).toHaveBeenCalled();
      expect(quickbetNotificationService.clear).toHaveBeenCalled();
    }));
  });
});
