import { SessionService } from './session.service';
import { commandApi } from '@app/core/services/communication/command/command-api.constant';
import { fakeAsync, tick } from '@angular/core/testing';

describe('VanSessionService', () => {
  let service: SessionService;
  let userService;
  let command;
  let errorHandler;
  let whenProxySessionHandler;

  beforeEach(() => {
    userService = {
      getProxyAuth: jasmine.createSpy('getProxyAuth').and.returnValue(Promise.resolve()),
      getOpenApiAuth: jasmine.createSpy('getOpenApiAuth').and.returnValue(Promise.resolve()),
      sessionToken: 'sessionToken'
    };
    command = {
      register: jasmine.createSpy().and.callFake((p1, handler) => {
        whenProxySessionHandler = handler;
      }),
      API: commandApi
    };

    errorHandler = jasmine.createSpy('errorHandler');
    service = new SessionService(userService, command);
  });

  describe('constructor', () => {
    it('Test if command is registered', () => {
      expect(command.register).toHaveBeenCalled();
    });
    it('Test if command is registered', fakeAsync(() => {
      service.whenProxySession = jasmine.createSpy().and.returnValue(Promise.reject('error'));
      const actualResult = whenProxySessionHandler();
      actualResult.catch(errorHandler);
      tick();
      expect(service.whenProxySession).toHaveBeenCalled();
    }));
  });

  describe('whenSession', () => {
    it('getOpenApiAuth is called', () => {
      service.whenSession();
      expect(userService.getOpenApiAuth).toHaveBeenCalled();
    });
  });

  describe('whenProxySession', () => {

    it('whenSession if sessionToken', () => {
      service.whenProxySession();
      expect(userService.getProxyAuth).toHaveBeenCalled();
    });

    it('whenSession if no sessionToken', () => {
      userService.sessionToken = null;
      service.whenProxySession().catch(() => { });
      expect(userService.getProxyAuth).not.toHaveBeenCalled();
    });
  });

  it('whenUserSession', fakeAsync(() => {
    service.whenUserSession().subscribe();
    tick();
    expect(userService.getProxyAuth).toHaveBeenCalledTimes(1);
  }));
});
