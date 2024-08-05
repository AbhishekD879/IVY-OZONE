import { of, of as observableOf } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { PromotionsService } from './promotions.service';
import { mockedPromotions } from '@app/promotions/services/promotions/promotions.mock';
const {sitecorePromotions, promotionsArray } = mockedPromotions;

describe('PromotionsService', () => {
  let service: PromotionsService;

  let http;
  let domSanitizer;
  let userService;
  let existNewUserService;
  let cmsService;
  let dialogService;
  let gtmService;
  let casinoLinkService;
  let filtersService;
  let domToolsService;
  let rendererService;
  let bppService;
  let commandService;
  let windowRefService;
  let device;
  let infoDialog;
  let awsService;
  let vanillaApiService;
  let localeService;

  let btnElement;
  const res = {
    textContent: ''
  };
  const flag = 'EVFLAG_DYW';

  beforeEach(() => {
    btnElement = {
      querySelector: jasmine.createSpy().and.returnValue(res)
    };

    http = {
      get: jasmine.createSpy().and.returnValue(observableOf({
        body: {}
      })),
      put: jasmine.createSpy().and.returnValue(observableOf({
        body: {}
      }))
    };
    domSanitizer = {
      bypassSecurityTrustHtml: jasmine.createSpy()
    };
    userService = {
      username: 'oxygenUser',
      bppToken: 'qwerty'
    };
    existNewUserService = {
      filterExistNewUserItems: jasmine.createSpy('filterExistNewUserItems')
    };
    cmsService = {
      getGroupedPromotions: jasmine.createSpy('getGroupedPromotions').and.returnValue(observableOf({
        promotionsBySection: [{
          promotions: [{}]
        }]
      })),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        Promotions: {}
      })),
      getRetailPromotions: jasmine.createSpy('getRetailPromotions'),
      getSignpostingPromotionsLight: jasmine.createSpy('getSignpostingPromotionsLight').and.callFake((p1) => {
        return observableOf({promotion: 'test'});
      }),
      getAllPromotions: jasmine.createSpy('getAllPromotions').and.returnValue(of([]))
    };
    dialogService = {
      openDialog: jasmine.createSpy('openDialog').and.callFake((...arg) => {
        arg[3].onBeforeClose && arg[3].onBeforeClose();
        arg[3].openPromotionOverlay && arg[3].openPromotionOverlay(arg[0]);
        arg[3].getSpPromotionData && arg[3].getSpPromotionData(false);
      })
    };
    gtmService = {
      push: jasmine.createSpy()
    };
    casinoLinkService = {
      decorateCasinoLinkInHtml: jasmine.createSpy()
    };
    filtersService = {
      filterLink: jasmine.createSpy('filterLink')
    };
    domToolsService = {
      removeClass: jasmine.createSpy(),
      addClass: jasmine.createSpy(),
    };
    rendererService = {
      renderer: {
        listen: jasmine.createSpy()
      }
    };
    bppService = {
      send: jasmine.createSpy('send').and.returnValue(of({}))
    };
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve({})),
      register: jasmine.createSpy('register'),
      API: {
        PROMOTIONS_SHOW_OVERLAY: 'PROMOTIONS_SHOW_OVERLAY',
        BPP_AUTH_SEQUENCE: 'BPP_AUTH_SEQUENCE'
      }
    };
    windowRefService = {
      document: {
        body: {
          classList: {
            remove: jasmine.createSpy('remove')
          }
        }
      }
    };
    device = {
      isOnline: jasmine.createSpy('isOnline').and.returnValue(true)
    };
    infoDialog = {
      openConnectionLostPopup: jasmine.createSpy('openConnectionLostPopup')
    };
    awsService = {
      addAction: jasmine.createSpy('addAction')
    };
    vanillaApiService = {
      get: jasmine.createSpy('get')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('test')
    };
  });

  function createService() {
    service = new PromotionsService(
      http,
      domSanitizer,
      userService,
      existNewUserService,
      cmsService,
      dialogService,
      gtmService,
      casinoLinkService,
      filtersService,
      domToolsService,
      rendererService,
      bppService,
      commandService,
      windowRefService,
      device,
      infoDialog,
      awsService,
      vanillaApiService,
      localeService
    );
  }

  describe('', () => {
    beforeEach(() => {
      createService();
    });


    it('promotionsGroupedData', fakeAsync(() => {
      bppService.send.and.returnValue(of({ response: { model: {} } }));
      service.promotionsGroupedData().subscribe();
      tick();
      expect(cmsService.getGroupedPromotions).toHaveBeenCalledTimes(1);
    }));

    describe('promotionsDigitalData', () => {
      beforeEach(() => {
        service['doRequest'] = jasmine.createSpy('doRequest').and.returnValue(of(null));
        service['getPromotions'] = jasmine.createSpy('getPromotions').and.returnValue(null);
      });

      it('no promotions', fakeAsync(() => {
        service['promotionsDigitalData']().subscribe((result) => {
          expect(result).toBeNull();
        });
        tick();
      }));

      it('should filter promotions', fakeAsync(() => {
        (service['getPromotions'] as any).and.returnValue({
          promotions: [
            { categoryId: '10' },
            { categoryId: ['1'] },
            { categoryId: ['1000'] },
            {}
          ]
        });
        service['promotionsDigitalData']().subscribe((result: any) => {
          expect(result.promotions.length).toBe(3);
        });
        tick();
      }));
    });

    describe('getPromotions', () => {
      it('should set offers and return promotions', () => {
        const result: any[] = [
          { response: { model: { freebetOffer: [] } } },
          [{}]
        ];
        expect(service['getPromotions'](result)).toBe(result[1]);
        expect(service['offers']).toBe(result[0].response.model.freebetOffer);
      });

      it('should only return promotions', () => {
        const result: any[] = [[{}]];
        expect(service['getPromotions'](result)).toBe(result[0]);
        expect(service['offers']).toEqual([]);
      });
    });

    describe('doRequest', () => {
      it('should get accountOffers and grouped promotions', () => {
        userService.username = 'dev';
        service['doRequest']();
        expect(bppService.send).toHaveBeenCalledTimes(1);
        expect(cmsService.getGroupedPromotions).toHaveBeenCalledTimes(1);
      });

      it('should get all promotions', () => {
        userService.username = '';
        service['doRequest'](false);
        expect(cmsService.getAllPromotions).toHaveBeenCalledTimes(1);
      });
    });
  });
});
