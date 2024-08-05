import { FlagSourceService } from './flag-source.service';
describe('FlagSourceService', () => {
  let service: FlagSourceService;
  let windowRefService;
  beforeEach(() => {
    windowRefService = {
      nativeWindow: {
        ldkeys: '123',
        setTimeout: jasmine.createSpy().and.callFake((callback: Function) => {
          callback();
        })
      }
    };
  });
  describe('FlagSourceService', () => {
    beforeEach(() => {
      service = new FlagSourceService(windowRefService);
    });

    it('constructor', () => {
      expect(service).toBeTruthy();
    });

    it('onAppInit', () => {
      const spyOnNext = spyOn(service, 'getServerFlags');
      service.onAppInit();
      expect(spyOnNext).toHaveBeenCalled();
    });
      

    it('getServerFlags when flags are unavailable', () => {
      windowRefService.nativeWindow.ldkeys = '123';
      service.getServerFlags();
      console.log('getserverflags',service.flagStore);
      expect(service.flagStore).toEqual('123');
    });

    it('updateFlagstore', () => {
      service.updateFlagstore('showQuickLinks');
      service.flagUpdate.subscribe((val: any) => {
        expect(val).toEqual('showQuickLinks');
       }
      )
    });
  });
})

