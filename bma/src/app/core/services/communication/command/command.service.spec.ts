import { CommandService } from './command.service';
import { commandApi } from './command-api.constant';
import { fakeAsync, tick } from '@angular/core/testing';

describe('CommandService', () => {
  let service: CommandService;

  beforeEach(() => {
    service = new CommandService();
  });

  it('isPromise', () => {
    expect(CommandService.isPromise({})).toBeFalsy();
    expect(CommandService.isPromise({ then: jasmine.createSpy() })).toBeTruthy();
  });

  it('getter for ERROR', () => {
    expect(CommandService.ERROR).toEqual({
      ASYNC_COMMAND_MISSED: 'Not existed asynchronous command: ',
      SYNC_COMMAND_MISSED: 'Not existed synchronous command: ',
      COMMAND_NOT_FOUND: 'Not found command to delete: ',
      NOT_PROMISE_RESULT: 'Promise should be returned in command: ',
      PROMISE_RESULT: 'Not a Promise should be returned in command: ',
      COMMAND_OVERRIDE: 'Should no override existed command: '
    });
  });

  it('API', () => {
    expect(service.API).toEqual(commandApi);
  });

  describe('unregister', () => {
    it('service command should not change', () => {
      spyOn(console, 'error');
      service['commands'] = {
        registered: 'registered'
      };

      service.unregister('unregister');
      expect(service['commands']).toEqual( service['commands']);
    });

    it('should delete unregistered', () => {
      service['commands'] = {
        unregistered: 'unregistered',
        registered: 'registered'
      };

      spyOn(console, 'error');
      service.unregister('unregistered');
      expect(service['commands']).toEqual({registered: 'registered'});
    });
  });

  describe('execute', () => {
    it(' should return null', () => {
      spyOn(console, 'error');
      const result = service.execute(service.API.BETSLIP_READY, [ 1, 2, 3 ]);
      expect(result).toEqual(null);
    });
    it(' should return null', () => {
      spyOn(console, 'error');
      const result = service.execute(service.API.BETSLIP_READY);
      expect(result).toEqual(null);
    });
    it(' execute should return null', () => {
      service['commands'] = {
        unregistered: jasmine.createSpy().and.callFake(() => {
          return {then: true};
        }),
        registered: 'registered'
      };
      spyOn(console, 'error');
      const result = service.execute('unregistered', [ 1, 2, 3 ]);
      expect(result).toEqual(null);
    });
  });

  describe('executeAsync', () => {
    it('should return then: true', fakeAsync(() => {
        service['commands'] = {
          unregistered: jasmine.createSpy().and.callFake(() => {
            return {then: true};
          }),
          registered: 'registered'
        };
      const lazyloadStub = jasmine.createSpy().and.returnValue(Promise.resolve());
      service.register(service.API.LAZY_LOAD, lazyloadStub);

      const res = service.executeAsync('unregistered', [ 1, 2, 3 ], { res: 'yes' });
      tick();

      res.then((result) => {
        expect(result).toEqual({ then: true });
      });
    }));

    it('should return then: promise reject', fakeAsync(() => {
        service['commands'] = {
          unregistered: jasmine.createSpy().and.callFake(() => {
            return {res: 'yes'};
          }),
          registered: 'registered'
        };
      const lazyloadStub = jasmine.createSpy().and.returnValue(Promise.resolve());
      service.register(service.API.LAZY_LOAD, lazyloadStub);

      service.executeAsync('unregistered', [ 1, 2, 3 ], { res: 'yes' }).then(res => {})
        .catch((error) => {
        expect(error).toEqual('Promise should be returned in command: unregistered');
      });
      tick();
    }));

    it('should return then: promise reject', fakeAsync(() => {
        service['commands'] = {
          unregistered: jasmine.createSpy().and.callFake(() => {
            return {res: 'yes'};
          }),
          registered: 'registered'
        };
      const lazyloadStub = jasmine.createSpy().and.returnValue(Promise.resolve());
      service.register(service.API.LAZY_LOAD, lazyloadStub);

      service.executeAsync('execute' ).then(res => {})
        .catch((error) => {
        expect(error).toEqual('Not existed asynchronous command: execute');
      });
      tick();
    }));
  });

  describe('register, execute, executeAsync', () => {
    it('register', () => {
      const callback = jasmine.createSpy().and.returnValue(() => {});
      service.register(service.API.BETSLIP_READY, callback);
      expect(service['commands'][service.API.BETSLIP_READY]).toBeDefined();
    });

    it('should return ', () => {
      service['commands'] = {
        unregistered: 'unregistered',
        registered: 'registered'
      };
      const callback = jasmine.createSpy().and.returnValue(() => {});

      service.register('unregistered', callback);
      expect(service['commands']).toEqual(service['commands']);
    });

    it('register, execute', () => {
      const callback = jasmine.createSpy().and.returnValue(() => {});
      service.register(service.API.BETSLIP_READY, callback);
      service.execute(service.API.BETSLIP_READY, [ 1, 2, 3 ], { res: 'yes' });
      expect(callback).toHaveBeenCalledTimes(1);
      expect(callback).toHaveBeenCalledWith(1, 2, 3);
    });

    it('not registered, but executed', () => {
      const res = service.execute(service.API.BETSLIP_READY, [ 1, 2, 3 ], { res: 'yes' });
      expect(res).toEqual({ res: 'yes' });
    });

    it('register, executeAsync', fakeAsync(() => {
      const lazyloadStub = jasmine.createSpy().and.returnValue(Promise.resolve());
      service.register(service.API.LAZY_LOAD, lazyloadStub);

      const callback = jasmine.createSpy().and.returnValue(Promise.resolve());
      service.register(service.API.BETSLIP_READY, callback);

      const res = service.executeAsync(service.API.BETSLIP_READY, [ 1, 2, 3 ], { res: 'yes' });
      expect(res.then).toBeDefined();

      expect(lazyloadStub).toHaveBeenCalledTimes(1);
      expect(lazyloadStub).toHaveBeenCalledWith(service.API.BETSLIP_READY);
      tick();

      expect(callback).toHaveBeenCalledTimes(1);
      expect(callback).toHaveBeenCalledWith(1, 2, 3);
    }));

    it('not registered, executeAsync', fakeAsync(() => {
      const lazyloadStub = jasmine.createSpy().and.returnValue(Promise.resolve());
      service.register(service.API.LAZY_LOAD, lazyloadStub);

      const res = service.executeAsync(service.API.BETSLIP_READY, [ 1, 2, 3 ], { res: 'yes' });
      expect(res.then).toBeDefined();

      expect(lazyloadStub).toHaveBeenCalledTimes(1);
      expect(lazyloadStub).toHaveBeenCalledWith(service.API.BETSLIP_READY);
      tick();

      res.then((result) => {
        expect(result).toEqual({ res: 'yes' });
      });
    }));
  });
});
