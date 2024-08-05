import { of, throwError } from 'rxjs';
import { EditRacingEdpMarketComponent } from './edit-racing-edp-market.component';
import { EDP_MARKETS } from '../racing-edp-list/racing.edp.mock';
import { RacingEdpMarket } from '@app/client/private/models/racing.edpmarket.model';

describe('EditRacingEdpMarketComponent', () => {
  let component: EditRacingEdpMarketComponent;
  let activatedRoute;
  let globalLoaderService;
  let apiClientService;
  let router;
  let dialogService;
  let racingEDPMarketsService;

  beforeEach(() => {
    racingEDPMarketsService = {
      edit: jasmine.createSpy('edit').and.returnValue(of({
        body: EDP_MARKETS[1]
      })),
      remove: jasmine.createSpy('remove').and.returnValue(of({})),
      getById: jasmine.createSpy('getById').and.returnValue(of({
        body: EDP_MARKETS[0]
      }))
    };
    activatedRoute = {
      params: of({
        id: 'abc123'
      })
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    apiClientService = {
      racingEdp: () => racingEDPMarketsService,
      publicApi: jasmine.createSpy('publicApi').and.returnValue({
        getSystemConfigByBrand: jasmine.createSpy('getSystemConfigByBrand').and.returnValue(of({ body: { HorseRacingBIR: { marketsEnabled: ['ABC'] } } }))
      })
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog')
    };
    component = new EditRacingEdpMarketComponent(activatedRoute, globalLoaderService,
      apiClientService, router, dialogService);
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should fetch details by id', () => {
      component.racingEDPMarket = {name:'ABC'} as RacingEdpMarket;
      component.ngOnInit();
      expect(component.racingEDPMarket).not.toBeNull();
      expect(component.isLoading).toBeFalse();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
    it('should not fetch details, if the service throws error', () => {
      racingEDPMarketsService.getById = jasmine.createSpy('getById').and.returnValue(throwError({error: '401'}));
      component.ngOnInit();
      expect(component.racingEDPMarket).toBeUndefined();
      expect(component.isLoading).toBeFalse();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
    it('should call getBirEnabledMarkets',()=>{
      spyOn(component as any,'getBirEnabledMarkets');
      component.racingEDPMarket = {name:'ABC'} as RacingEdpMarket;
      component.ngOnInit();
      expect(component['getBirEnabledMarkets']).toHaveBeenCalled();
    });
  });

  it('should remove racing edp market and navigate back to list page', () => {
    component.racingEDPMarket = {
      id: 'abc123',
      name:'ABC'
    } as any;
    component.removeRacingEdpMarket();
    expect(router.navigate).toHaveBeenCalled();
  });

  it('should save changes', () => {
    component.saveChanges();
    expect(dialogService.showNotificationDialog).toHaveBeenCalled();
  });

  it('should revert changes', () => {
    component.revertChanges();
    expect(component.racingEDPMarket).not.toBeNull();
    expect(component.isLoading).toBeFalse();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  describe('#actionsHandler', () => {
    it('should remove racing edp market', () => {
      const event = 'remove';
      component.racingEDPMarket = {
        id: 'abc123'
      } as any;
      component.actionsHandler(event);
      expect(racingEDPMarketsService.remove).toHaveBeenCalled();
    });
    it('should save racing edp market', () => {
      const event = 'save';
      component.actionsHandler(event);
      expect(racingEDPMarketsService.edit).toHaveBeenCalled();
    });
    it('should revert racing edp market', () => {
      const event = 'revert';
      component.actionsHandler(event);
      expect(racingEDPMarketsService.getById).toHaveBeenCalled();
    });
    it('should set default condition', () => {
      spyOn(console, 'error');
      const event = 'racdom';
      component.actionsHandler(event);
      expect(component.racingEDPMarket).toBeUndefined();
    });
  });

  describe('#isValidForm', () => {
    it('should return true if form is valid', () => {
      const racingEDPMarket = {
        name: 'Win'
      } as any;
      const response = component.isValidForm(racingEDPMarket);
      expect(response).toBeTrue();
    });
    it('should return false if form is not valid', () => {
      const racingEDPMarket = {
        name: ''
      } as any;
      const response = component.isValidForm(racingEDPMarket);
      expect(response).toBeFalse();
    });
  });
  describe('#getBirEnabledMarkets', () => {
    it('should return system-config data and assign to birEnabledMarkets', () => {
      spyOn(component as any, 'isBirEnabledMarket');
      component.racingEDPMarket = { name: "ABC" } as RacingEdpMarket;
      component['getBirEnabledMarkets']();
      expect(apiClientService.publicApi).toHaveBeenCalled();
      expect(apiClientService.publicApi().getSystemConfigByBrand).toHaveBeenCalled();
      expect(component['birEnabledMarkets']).toEqual(['ABC']);
      expect(component['isBirEnabledMarket']).toHaveBeenCalledWith('ABC');
    });
    it('should assign isBirMarketFlag to true if isBirEnabledMarket return true', () => {
      spyOn(component as any, 'isBirEnabledMarket').and.returnValue(true);
      component.racingEDPMarket = { name: "ABC" } as RacingEdpMarket;
      component['getBirEnabledMarkets']();
      expect(component.isBirMarketFlag).toBeTrue();
    });
    it('should assign isBirMarketFlag to true if isBirEnabledMarket return false', () => {
      spyOn(component as any, 'isBirEnabledMarket').and.returnValue(false);
      component.racingEDPMarket = { name: "ABCD" } as RacingEdpMarket;
      component['getBirEnabledMarkets']();
      expect(component.isBirMarketFlag).toBeFalse();
    });
  });
  describe('isBirEnabledMarket', () => {
    it('should return true id the array includes the marketname', () => {
      component['birEnabledMarkets'] = ['ABC'];
      expect(component['isBirEnabledMarket']('ABC')).toBeTruthy();
    });
    it('should return true id the array includes the marketname', () => {
      component['birEnabledMarkets'] = ['ABC'];
      expect(component['isBirEnabledMarket']('ABCD')).toBeFalsy();
    });
  });
});
