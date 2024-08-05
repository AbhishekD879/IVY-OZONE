import { of, throwError } from 'rxjs';
import { RacingEdpListComponent } from './racing-edp-list.component';
import { EDP_MARKETS } from './racing.edp.mock';

describe('RacingEdpListComponent', () => {
  let component: RacingEdpListComponent;
  let apiClientService;
  let globalLoaderService;
  let dialogService;
  let router;
  let racingEDPService;
  let racingEDPMarkets;
  let snackBar;

  beforeEach(() => {
    racingEDPMarkets = EDP_MARKETS;
    racingEDPService = {
      findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({
        body: racingEDPMarkets
      })),
      add: jasmine.createSpy('add').and.returnValue(of({
        body: racingEDPMarkets[0]
      })),
      remove: jasmine.createSpy('remove').and.returnValue(of({})),
      postNewOrder: jasmine.createSpy('remove').and.returnValue(of({}))
    };
    apiClientService = {
      racingEdp: () => racingEDPService
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader'),
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showCustomDialog: jasmine.createSpy('showCustomDialog').and.callFake((dialogComponent, {
        width, title, yesOption, noOption, yesCallback
      }) => {
        yesCallback(racingEDPMarkets[0]);
      }),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ title, message, yesCallback }) => yesCallback())
    };
    router = {
      navigate: jasmine.createSpy('navigate'),
      url: '/racing-edp-markets/1'
    };
    snackBar = {
      open: jasmine.createSpy('open')
    } as any;
    component = new RacingEdpListComponent(apiClientService, globalLoaderService, dialogService,
      router, snackBar);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should fetch all the markets based on brand', () => {
      component.ngOnInit();
      expect(component.racingEDPMarkets).not.toBe(null);
      expect(component.isLoading).toBe(false);
    });
    it('should not fetch markets if the service throws error', () => {
      racingEDPService.findAllByBrand = jasmine.createSpy().and.returnValue(throwError({error: '401'}));
      component.ngOnInit();
      expect(component.racingEDPMarkets.length).toBe(0);
      expect(component.isLoading).toBe(false);
    });
  });

  it('should remove racing edp market', () => {
    const mockMarket = racingEDPMarkets[2] as any;
    component.racingEDPMarkets = EDP_MARKETS;
    const length = component.racingEDPMarkets.length;
    component.removeRacingEdpMarket(mockMarket);
    expect(component.racingEDPMarkets.length).toBe(length - 1);
  });

  describe('#createRacingEdpMarket', () => {
    it('should create markets if service returns proper response', () => {
      component.racingEDPMarkets = EDP_MARKETS;
      const length = component.racingEDPMarkets.length;
      component.createRacingEdpMarket();
      expect(router.navigate).toHaveBeenCalled();
      expect(component.racingEDPMarkets.length).toBe(length + 1);
    });
    it('should not add any market if the service returns error', () => {
      racingEDPService.add = jasmine.createSpy().and.returnValue(throwError({error: '401'}));
      component.createRacingEdpMarket();
      expect(router.navigate).not.toHaveBeenCalled();
      expect(component.racingEDPMarkets.length).not.toBe(length + 1);
    });
  });

  it('#reorderHandler should save new coupon order', () => {
    const newOrder = { order: ['123'], id: '321' };
    component.reorderHandler(newOrder);
    expect(snackBar.open).toHaveBeenCalledWith(
      `New Racing Edp Markets Order Saved!!`,
      'OK!',
      {
        duration: 3000,
      }
    );
  });
});
