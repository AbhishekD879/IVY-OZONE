import { Subject } from "rxjs";
import { EzNavVanillaService } from "./eznav-vanilla.service";


describe('EzNavVanillaService', () => {
  let service: EzNavVanillaService;
  let windowRef,
  renderer,
  device,
  userService,
  route,
  gtmService,
  storageService;

  beforeEach(() => {
    route = renderer = windowRef = device = userService = gtmService = storageService = {} as any;
    windowRef = {
      document: {
          getElementsByClassName: jasmine.createSpy('querySelector').and.returnValue({
              parentNode: {}
          } as any)
      },
      nativeWindow: {
        top: {
          location: {
            replace: jasmine.createSpy('replace')
          }
        }
      }
    };
    renderer = {
      renderer: {
          addClass: jasmine.createSpy('addClass')
      }
    };
    storageService = {
      set: jasmine.createSpy('storageService.set'),
      get: jasmine.createSpy('storageService.get')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    route.queryParams = new Subject();

    service = new EzNavVanillaService(windowRef, renderer, device, userService, route, gtmService, storageService);
    });

    describe('#casinoMyBetsVanillaInit', () => {  
      it('vanilla init with iframe as true', () => {
        const element = { } as any;
        spyOn(service, 'isDeviceBrowserValidForCasino').and.returnValue(true);
        service.casinoMyBetsVanillaInit();
        route.queryParams.next( { iFrameCasino: 'true' });
        expect(service.isMyBetsInCasino).toBe(true);
      });

      it('vanilla init with isDeviceBrowserValidForCasino as true and iframe as undefined', () => {
        const element = { } as any;
        spyOn(service, 'isDeviceBrowserValidForCasino').and.returnValue(true);
        service.casinoMyBetsVanillaInit();
        route.queryParams.next({ iFrameCasino: undefined });
        expect(service.isMyBetsInCasino).toBe(false);
      });

      it('vanilla init with isDeviceBrowserValidForCasino as false and iframe as true', () => {
        const element = { } as any;
        spyOn(service, 'isDeviceBrowserValidForCasino').and.returnValue(false);
        service.casinoMyBetsVanillaInit();
        route.queryParams.next({ iFrameCasino: 'true' });
        expect(service.isMyBetsInCasino).toBe(false);
      });
    });

    describe('#isDeviceBrowserValidForCasino', () => {  
      it('isDeviceBrowserValidForCasino with device wrapper as true and is of Ios', () => {
        device.isWrapper = true;
        device.isIos = true;
        expect(service.isDeviceBrowserValidForCasino()).toBe(false);
      });

      it('isDeviceBrowserValidForCasino with device wrapper as false and is of Ios', () => {
        device.isWrapper = false;
        device.isIos = true;
        expect(service.isDeviceBrowserValidForCasino()).toBe(true);
      });

      it('isDeviceBrowserValidForCasino with device wrapper as false and is of Android', () => {
        device.isWrapper = false;
        device.isIos = false;
        device.isAndroid = true;
        expect(service.isDeviceBrowserValidForCasino()).toBe(true);
      });
    });
});