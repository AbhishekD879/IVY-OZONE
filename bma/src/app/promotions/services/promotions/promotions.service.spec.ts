import { of, of as observableOf, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { PromotionsService } from './promotions.service';
import environment from '@environment/oxygenEnvConfig';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { PromotionDialogComponent } from '@promotions/components/promotionDialog/promotion-dialog.component';
import { ICheckStatusResponse } from '@promotions/models/response.model';
import { mockedPromotions } from '@app/promotions/services/promotions/promotions.mock';
const { sitecorePromotions, promotionsArray } = mockedPromotions;

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
        return observableOf({ promotion: 'test' });
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
      isOnline: jasmine.createSpy('isOnline').and.returnValue(true),
      channel: {
        channelRef: {
          id: '2313'
        }
      }
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
      vanillaApiService
    );
  }

  describe('', () => {
    beforeEach(() => {
      createService();
    });

    it('changeBtnLabel', () => {
      service.changeBtnLabel('test', btnElement);
      expect(btnElement.querySelector).toHaveBeenCalledTimes(2);
      expect(res.textContent).toEqual('test');

      expect(domToolsService.removeClass).toHaveBeenCalledTimes(1);
      expect(domToolsService.removeClass).toHaveBeenCalledWith(jasmine.anything(), 'btn-spinner');

      expect(domToolsService.addClass).toHaveBeenCalledTimes(1);
      expect(domToolsService.addClass).toHaveBeenCalledWith(jasmine.anything(), 'checked');
    });

    it('checkStatus', () => {
      service.checkStatus('5adghjs2').subscribe();
      expect(http.get).toHaveBeenCalledTimes(1);
      expect(http.get).toHaveBeenCalledWith(`${environment.OPT_IN_ENDPOINT}/api/trigger/5adghjs2`, {
        observe: 'response',
        headers: { user: 'oxygenUser', token: 'qwerty' }
      });
      expect(awsService.addAction).toHaveBeenCalledWith('GetPromoOptInSuccess', { result: {}, triggerId: '5adghjs2' });
    });

    it('checkStatus - error condition', () => {
      const error = { error: 'http error' };
      http.get = jasmine.createSpy('get').and.returnValue(throwError(error));
      service.checkStatus('5adghjs2').subscribe(() => { }, () => { });
      expect(http.get).toHaveBeenCalledTimes(1);
      expect(http.get).toHaveBeenCalledWith(`${environment.OPT_IN_ENDPOINT}/api/trigger/5adghjs2`, {
        observe: 'response',
        headers: { user: 'oxygenUser', token: 'qwerty' }
      });
      expect(awsService.addAction).toHaveBeenCalledWith('GetPromoOptInError',
        { error, triggerId: '5adghjs2' });
    });

    it('checkStatus - sholud invoke commandSevice if Auth error and re-invoke checkOptInStatus', fakeAsync(() => {
      const errorResponse = {
        fired: true,
        id: '123',
        timestamp: '123',
        error: { code: 401 }
      } as ICheckStatusResponse;

      commandService.executeAsync.and.returnValue(Promise.resolve());
      service['checkOptInStatus'] = jasmine.createSpy().and.returnValue(observableOf(errorResponse));

      service.checkStatus('5adghjs2').subscribe(() => { }, () => {
        commandService.executeAsync().then(() => {
          expect(commandService.executeAsync).toHaveBeenCalledWith(commandService.API.BPP_AUTH_SEQUENCE);
          expect(service['checkOptInStatus']).toHaveBeenCalledTimes(2);
        });
      });
      tick();
    }));

    describe('storeId', () => {
      it('should send UpdatePromoOptInSuccess action to AwsService on success', () => {
        service.storeId('5adghjs2').subscribe();
        expect(http.put).toHaveBeenCalledTimes(1);
        expect(http.put).toHaveBeenCalledWith(
          `${environment.OPT_IN_ENDPOINT}/api/trigger/`, {
          trigger_id: '5adghjs2'
        }, {
          headers: { user: 'oxygenUser', token: 'qwerty' }
        }
        );
        expect(awsService.addAction).toHaveBeenCalledWith('UpdatePromoOptInSuccess',
          { result: { body: {} }, triggerId: '5adghjs2' });
      });

      it('should send UpdatePromoOptInError action to AwsService on error', () => {
        const error = { error: 'http error' };
        http.put = jasmine.createSpy('put').and.returnValue(throwError(error));
        service.storeId('5adghjs2').subscribe(() => {
        }, () => {
        });
        expect(http.put).toHaveBeenCalledTimes(1);
        expect(http.put).toHaveBeenCalledWith(
          `${environment.OPT_IN_ENDPOINT}/api/trigger/`, {
          trigger_id: '5adghjs2'
        }, {
          headers: { user: 'oxygenUser', token: 'qwerty' }
        }
        );
        expect(awsService.addAction).toHaveBeenCalledWith('UpdatePromoOptInError', { error, triggerId: '5adghjs2' });
      });

      it('should throw error in case of generic error', fakeAsync(() => {
        const errorResponse = {
          fired: true,
          id: '123',
          timestamp: '123',
          error: {
            code: 503
          }
        } as ICheckStatusResponse;


        commandService.executeAsync.and.returnValue(Promise.resolve());
        service['storeOptInId'] = jasmine.createSpy().and.returnValue(observableOf(errorResponse));
        service.storeId('5adghjs2').subscribe(() => {
        }, (err: ICheckStatusResponse) => {
          expect(err.error.code).toEqual(503);
        });
        tick();
      }));

      it('should re-trigger auth and repeat calling storeOptInId', fakeAsync(() => {
        const errorResponse = {
          fired: true,
          id: '123',
          timestamp: '123',
          error: {
            code: 401
          }
        } as ICheckStatusResponse;

        commandService.executeAsync.and.returnValue(Promise.resolve());
        service['storeOptInId'] = jasmine.createSpy().and.returnValue(observableOf(errorResponse));
        service.storeId('5adghjs2').subscribe(() => { }, () => {
          commandService.executeAsync().then(() => {
            expect(commandService.executeAsync).toHaveBeenCalledWith(commandService.API.BPP_AUTH_SEQUENCE);
            expect(service['storeOptInId']).toHaveBeenCalled();
          });
        });
        tick();
      }));
    });

    it('isAuthError should return true on code 401', () => {
      const response = {
        fired: true,
        id: '123',
        timestamp: '123',
        error: { code: 401 }
      };
      service['isAuthError'](response);
      expect(service['isAuthError']).toBeTruthy();
    });

    it('isUserLoggedIn', () => {
      expect(service.isUserLoggedIn()).toBeTruthy();
    });

    it('enableOptInButton', () => {
      service.enableOptInButton(btnElement, () => { });
      expect(btnElement.querySelector).toHaveBeenCalledTimes(1);
      expect(domToolsService.removeClass).toHaveBeenCalledTimes(2);

      expect(rendererService.renderer.listen).toHaveBeenCalledWith(btnElement, 'click', jasmine.anything());
    });

    it('disableOptInButton', () => {
      service.disableOptInButton(btnElement, [() => { }]);
      expect(btnElement.querySelector).toHaveBeenCalledTimes(1);
      expect(domToolsService.addClass).toHaveBeenCalledTimes(2);
    });

    describe('@decorateLinkAndTrust', () => {
      it('should decorate internal link', () => {
        const html = '<p><a href="sport/football/matches/today"></a></p>';
        casinoLinkService.decorateCasinoLinkInHtml.and.returnValue(html);
        service.decorateLinkAndTrust(html);
        expect(domSanitizer.bypassSecurityTrustHtml).toHaveBeenCalledWith('<p><a data-routerlink="sport/football/matches/today"></a></p>');
      });

      it('should not decorate external link', () => {
        const html = '<p><a href="https://regex101.com/"></a></p>';
        casinoLinkService.decorateCasinoLinkInHtml.and.returnValue(html);
        service.decorateLinkAndTrust(html);
        expect(domSanitizer.bypassSecurityTrustHtml).toHaveBeenCalledWith('<p><a href="https://regex101.com/"></a></p>');
      });
    });

    it('promotionsGroupedData', fakeAsync(() => {
      bppService.send.and.returnValue(of({ response: { model: {} } }));
      service.promotionsGroupedData().subscribe();
      tick();
      expect(cmsService.getGroupedPromotions).toHaveBeenCalledTimes(1);
    }));

    it('isGroupBySectionsEnabled', fakeAsync(() => {
      service.isGroupBySectionsEnabled().subscribe();
      tick();
      expect(cmsService.getSystemConfig).toHaveBeenCalledTimes(1);
    }));

    describe('filterByOfferId', () => {
      it('should filterByOfferId(openBetId, offer)', () => {
        service['offers'] = [{ freebetOfferId: '300' }] as any[];
        const promotions = [{ openBetId: '300' }, { openBetId: '310' }, {}, { openBetId: '300' }];

        expect(service.filterByOfferId(<any>promotions).length).toEqual(3);
      });

      it('should filterByOfferId(not logged in, offer)', () => {
        const promotions = [{ openBetId: '300' }, {}, {}];
        userService.username = null;

        expect(service.filterByOfferId(<any>promotions).length).toEqual(2);
      });
    });

    it('should register command PROMOTIONS_SHOW_OVERLAY', () => {
      expect(commandService.register).toHaveBeenCalledWith('PROMOTIONS_SHOW_OVERLAY', jasmine.any(Function));
    });

    describe('should call isEmptyPromotionValue method', () => {
      const bannerLink = {
        attributes: { target: '_blank' },
        text: 'sadfdsf',
        url: 'https://test.sports.coral.co.uk/promotions/all'
      };
      const tcLink = {
        attributes: { target: '_blank' },
        text: 'sadfdsf',
        url: 'https://test.sports.coral.co.uk/promotions/all'
      };
      it('tcLink undefined', () => {
        const tclinkundefined = undefined;
        const hrefProp = 'href';
        expect(service.isEmptyPromotionValue(bannerLink, tclinkundefined, hrefProp)).toEqual(bannerLink.url);
      });
      it('tcLink and bannersLink undefined', () => {
        const tclinkundefined = undefined;
        const bannersLink = undefined;
        const hrefProp = 'href';
        expect(service.isEmptyPromotionValue(bannersLink, tclinkundefined, hrefProp)).toEqual('');
      });
      it('tcLink defined', () => {
        const hrefProp = 'href';
        expect(service.isEmptyPromotionValue(bannerLink, tcLink, hrefProp)).toEqual(tcLink.url);
      });
      it('target link undefined', () => {
        const targetundefined = undefined;
        const targProp = 'target';
        expect(service.isEmptyPromotionValue(bannerLink, targetundefined, targProp)).toEqual(bannerLink.attributes.target);
      });
      it('target link and bannerlink undefined', () => {
        const targetundefined = undefined;
        const bannersLink = undefined;
        const targProp = 'target';
        expect(service.isEmptyPromotionValue(bannersLink, targetundefined, targProp)).toEqual('');
      });
      it('target link defined', () => {
        const targProp = 'target';
        expect(service.isEmptyPromotionValue(bannerLink, tcLink, targProp)).toEqual(tcLink.attributes.target);
      });
      it('tc link and target link both undefined', () => {
        const targetProp = 'abcd';
        const bannerLinkund = undefined;
        const tcLinkund = undefined;
        expect(service.isEmptyPromotionValue(bannerLinkund, tcLinkund, targetProp)).toEqual(undefined);
      });
    });

    describe('openPromotionDialog', () => {
      it('should call dialogService.openDialog', () => {
        spyOn(service, 'getSpPromotionData').and.returnValue(of([{ marketLevelFlag: 'FLAG'}] as any));
        const args = null;
        service.openPromotionDialog('FLAG');
        expect(dialogService.openDialog).toHaveBeenCalledWith(DialogService.API.promotionDialog, PromotionDialogComponent, true, {
          flag: 'FLAG',
          getSpPromotionData: jasmine.any(Function),
          openPromotionOverlay: jasmine.any(Function),
          onBeforeClose: jasmine.any(Function)
        });

        expect(windowRefService.document.body.classList.remove).toHaveBeenCalled();
      });

      it('should call with eventLevelFlag', () => {
        spyOn(service, 'getSpPromotionData').and.returnValue(of([{  eventLevelFlag: 'FLAG'}] as any));
        const args = null;
        service.openPromotionDialog('FLAG');
        expect(dialogService.openDialog).toHaveBeenCalledWith(DialogService.API.promotionDialog, PromotionDialogComponent, true, {
          flag: 'FLAG',
          getSpPromotionData: jasmine.any(Function),
          openPromotionOverlay: jasmine.any(Function),
          onBeforeClose: jasmine.any(Function)
        });
        
        expect(service.getSpPromotionData).toHaveBeenCalledWith(false);
      });

      it('should call openPromotionOverlay', () => {
        spyOn(service, 'getSpPromotionData').and.returnValue(of([{  eventLevelFlag: 'FLAG'}] as any));
        spyOn(service, 'openPromotionOverlay').and.returnValue('FLAG' as any);
        const args = null;
        service.openPromotionDialog('FLAG');
        expect(dialogService.openDialog).toHaveBeenCalledWith(DialogService.API.promotionDialog, PromotionDialogComponent, true, {
          flag: 'FLAG',
          getSpPromotionData: jasmine.any(Function),
          openPromotionOverlay: jasmine.any(Function),
          onBeforeClose: jasmine.any(Function)
        });

        expect(service.openPromotionOverlay).toHaveBeenCalledWith('FLAG');
      });

      it('openPromotionDialog offline', () => {
        device.isOnline.and.returnValue(false);
        service.openPromotionDialog('FLAG');
        expect(infoDialog.openConnectionLostPopup).toHaveBeenCalled();
      });

      it('should bot call windowRefService', () => {
        spyOn(service, 'getSpPromotionData').and.returnValue(of([{ marketLevelFlag: '' }] as any));

        service.openPromotionDialog('FLAG');

        expect(dialogService.openDialog).not.toHaveBeenCalled();

        expect(windowRefService.document.body.classList.remove).not.toHaveBeenCalled();
      });

      it('should not call dialogService.openDialog', () => {
        spyOn(service, 'getSpPromotionData');

        service.openPromotionDialog('');

        expect(service.getSpPromotionData).not.toHaveBeenCalled();
      });
    });

    describe('getSpPromotionData', () => {

      it('should call _filterPromotionsByVipLevel', () => {
        spyOn<any>(service, '_filterPromotionsByVipLevel');

        service['spPromotionData'] = { light: 'light', dark: 'dark' };
        service.getSpPromotionData();
        expect(service['_filterPromotionsByVipLevel']).toHaveBeenCalledWith('light' as any);
      });
      it('should call _filterPromotionsByVipLevel with all', () => {
        spyOn<any>(service, '_filterPromotionsByVipLevel');

        service['spPromotionData'] = { light: 'light', all: 'all' };
        service.getSpPromotionData(false);
        expect(service['_filterPromotionsByVipLevel']).toHaveBeenCalledWith('all' as any);
      });

      it('should call _filterPromotionsByVipLevel', () => {

        spyOn<any>(service, '_filterPromotionsByVipLevel');
        const promotions = {
          promotions: {
            marketLevelFlag: 'marketLevelFlag',
            eventLevelFlag: 'eventLevelFlag',
            useDirectFileUrl: true,
            directFileUrl: 'directFileUrl',
            overlayBetNowUrl: 'overlayBetNowUrl',
            flagName: 'flagName',
            iconId: 'iconId'
          }
        };

        cmsService.getSignpostingPromotionsLight = jasmine.createSpy('getSignpostingPromotionsLight').and.callFake((p1) => {
          return observableOf(promotions);
        });


        service['spPromotionData'] = {};
        service.getSpPromotionData(true).subscribe();
        expect(service['_filterPromotionsByVipLevel']).toHaveBeenCalled();
      });

      it('should accept marketName condition', () => {

        spyOn<any>(service, '_filterPromotionsByVipLevel');
        const promotions = {
          promotions: [{
            marketLevelFlag: 'two-up',
            eventLevelFlag: 'two-up',
            useDirectFileUrl: true,
            directFileUrl: 'directFileUrl',
            overlayBetNowUrl: 'overlayBetNowUrl',
            marketName: 'Match Result',
            flagName: 'tw-up',
            iconId: '#two-up'
          }]
        };

        cmsService.getSignpostingPromotionsLight = jasmine.createSpy('getSignpostingPromotionsLight').and.callFake((p1) => {
          return observableOf(promotions);
        });


        service['spPromotionData'] = {};
        service.getSpPromotionData().subscribe();
        expect(service['_filterPromotionsByVipLevel']).toHaveBeenCalled();
      });

      it('cms service should call getAllPromotions', () => {

        spyOn<any>(service, '_filterPromotionsByVipLevel');
        const promotions = {
          promotions: {
            marketLevelFlag: 'marketLevelFlag',
            eventLevelFlag: 'eventLevelFlag',
            useDirectFileUrl: true,
            directFileUrl: 'directFileUrl',
            overlayBetNowUrl: 'overlayBetNowUrl',
            flagName: 'flagName',
            iconId: 'iconId'
          }
        };

        cmsService.getAllPromotions = jasmine.createSpy('getAllPromotions').and.returnValue(observableOf(promotions));

        service['spPromotionData'] = {};
        service.getSpPromotionData(false).subscribe();
        expect(service['_filterPromotionsByVipLevel']).toHaveBeenCalled();
        expect(cmsService['getAllPromotions']).toHaveBeenCalled();

      });


      it('should call _filterPromotionsByVipLevel', () => {

        spyOn<any>(service, '_filterPromotionsByVipLevel');
        const promotions = {
          promotions: [{
            marketLevelFlag: '',
            eventLevelFlag: '',
            useDirectFileUrl: true,
            directFileUrl: 'directFileUrl',
            marketName: 'Match Result',
            overlayBetNowUrl: 'overlayBetNowUrl',
            flagName: 'two-up',
            iconId: 'two-up',
            isSignpostingPromotion: true
          }]
        };

        cmsService.getAllPromotions = jasmine.createSpy('getSignpostingPromotionsLight').and.callFake((p1) => {
          return observableOf(promotions);
        });

        service['spPromotionData'] = { light: 'light', dark: 'dark' };
        service.getSpPromotionData(false).subscribe();
        expect(service['_filterPromotionsByVipLevel']).toHaveBeenCalled();
      });

    });
    describe('openPromotionOverlay', () => {

      it('should not have been called getSpPromotionData', () => {
        spyOn(service, 'getSpPromotionData');

        service.openPromotionOverlay('');
        expect(service['getSpPromotionData']).not.toHaveBeenCalled();
      });

      it('dialogService should have been called', () => {
        const promotion = [{
          marketLevelFlag: 'marketLevelFlag',
          eventLevelFlag: 'eventLevelFlag',
          useDirectFileUrl: true,
          directFileUrl: 'directFileUrl',
          overlayBetNowUrl: 'overlayBetNowUrl',
          flagName: 'flagName',
          iconId: 'iconId'
        }, {
          marketLevelFlag: 'marketLevelFlag',
          eventLevelFlag: 'eventLevelFlag',
          useDirectFileUrl: true,
          directFileUrl: 'directFileUrl',
          overlayBetNowUrl: 'overlayBetNowUrl',
          flagName: 'flagName',
          iconId: 'iconId'
        }];
        service['getSpPromotionData'] = jasmine.createSpy().and.callFake(() => {
          return observableOf(promotion);
        });
        service['decorateLinkAndTrust'] = jasmine.createSpy('decorateLinkAndTrust').and.callFake((url: string) => url);
        dialogService['openDialog'] = jasmine.createSpy('openDialog').and.callFake((...arg) => {
          arg[3].decorateLinkAndTrust && arg[3].decorateLinkAndTrust('some/link');
          arg[3].getSpPromotionData && arg[3].getSpPromotionData(false);
        });

        service.openPromotionOverlay('marketLevelFlag');
        expect(dialogService['openDialog']).toHaveBeenCalled();
        expect(service['getSpPromotionData']).toHaveBeenCalled();
        expect(service['getSpPromotionData']).toHaveBeenCalledWith(false);
        expect(service['decorateLinkAndTrust']).toHaveBeenCalledWith('some/link');
      });

      it('dialogService should not have been called', () => {
        const promotion = [{
          marketLevelFlag: 'test',
          eventLevelFlag: 'test',
          useDirectFileUrl: true,
          directFileUrl: 'directFileUrl',
          overlayBetNowUrl: 'overlayBetNowUrl',
          flagName: 'flagName',
          iconId: 'iconId'
        }, {
          marketLevelFlag: 'test',
          eventLevelFlag: 'test',
          useDirectFileUrl: true,
          directFileUrl: 'directFileUrl',
          overlayBetNowUrl: 'overlayBetNowUrl',
          flagName: 'flagName',
          iconId: 'iconId'
        }];
        service['getSpPromotionData'] = jasmine.createSpy().and.callFake(() => {
          return observableOf(promotion);
        });
        service.openPromotionOverlay('marketLevelFlag');
        expect(service['getSpPromotionData']).toHaveBeenCalled();
        expect(dialogService['openDialog']).not.toHaveBeenCalled();
      });

    });

    describe('_filterPromotionsByVipLevel', () => {

      it('_filterPromotionsByVipLevel should not have been called', () => {
        const promotions = [{
          marketLevelFlag: 'marketLevelFlag',
          eventLevelFlag: 'eventLevelFlag',
          useDirectFileUrl: true,
          directFileUrl: 'directFileUrl',
          overlayBetNowUrl: 'overlayBetNowUrl',
          flagName: 'flagName',
          iconId: 'iconId'
        }];
        service['_filterPromotionsByVipLevel'](promotions as any);
        expect(existNewUserService['filterExistNewUserItems']).toHaveBeenCalledWith(promotions, false);
      });

    });

    describe('promotionsRetailData', () => {
      it('cmsService getRetailPromotions should have been called', () => {

        service['promotionsRetailData']();

        expect(cmsService.getRetailPromotions).toHaveBeenCalled();
      });
    });

    describe('getSiteCoreBanners', () => {
      it('getSiteCoreBanners should have been called', () => {
        const sitecorePromotion = [{
          type: 'segmentDefault',
          teasers: [{
            title: 'Test',
            subTitle: 'QA',
            itemId: '{abc}'
          }]
        }];
        vanillaApiService.get.and.returnValue(sitecorePromotion);
        const response = service['getPromotionsFromSiteCore']();
        expect(response[0].type).toEqual(sitecorePromotion[0].type);
      });
    });

    describe('promotionData', () => {

      it('cmsService getAllPromotions should have been called', () => {
        const promotions = [{
          marketLevelFlag: 'marketLevelFlag',
          eventLevelFlag: 'eventLevelFlag',
          useDirectFileUrl: true,
          directFileUrl: 'directFileUrl',
          overlayBetNowUrl: 'overlayBetNowUrl',
          flagName: 'flagName',
          iconId: 'iconId'
        }, {
          marketLevelFlag: 'marketLevelFlag',
          eventLevelFlag: 'eventLevelFlag',
          useDirectFileUrl: true,
          directFileUrl: 'directFileUrl',
          overlayBetNowUrl: 'overlayBetNowUrl',
          flagName: 'flagName',
          iconId: 'iconId'
        }];

        cmsService.getAllPromotions = jasmine.createSpy('getAllPromotions').and.returnValue(observableOf(promotions));

        service['promotionData']('tests').subscribe();

        expect(cmsService.getAllPromotions).toHaveBeenCalled();
      });
    });

    describe('preparePromotions', () => {
      it(' should have been called', () => {
        const promotions = [{
          marketLevelFlag: 'marketLevelFlag',
          eventLevelFlag: 'eventLevelFlag',
          useDirectFileUrl: false,
          directFileUrl: 'directFileUrl',
          overlayBetNowUrl: 'overlayBetNowUrl',
          flagName: 'flagName',
          iconId: 'iconId',
          uriMedium: ''
        }, {
          marketLevelFlag: 'marketLevelFlag',
          eventLevelFlag: 'eventLevelFlag',
          useDirectFileUrl: true,
          directFileUrl: 'directFileUrl',
          overlayBetNowUrl: 'overlayBetNowUrl',
          flagName: 'flagName',
          iconId: 'iconId',
          uriMedium: 'directFileUrl'
        }];

        existNewUserService.filterExistNewUserItems = jasmine.createSpy('getAllPromotions').and.returnValue(promotions);
        service['preparePromotions'](promotions as any, sitecorePromotions as any);

        expect(promotions[0].uriMedium).toEqual('');
        expect(promotions[1].uriMedium).toEqual('directFileUrl');
        expect(filtersService.filterLink).toHaveBeenCalledTimes(2);
      });

      it('using direct file url when sitecorePromotions length is zero', () => {
        existNewUserService.filterExistNewUserItems = jasmine.createSpy('getAllPromotions').and.returnValue(promotionsArray);
        service['preparePromotions'](promotionsArray as any, []);

        expect(promotionsArray[0].uriMedium).toEqual('');
        expect(promotionsArray[1].uriMedium).toEqual('directFileUrl');
        expect(filtersService.filterLink).toHaveBeenCalledTimes(2);
      });
    });

    describe('sendGTM', () => {
      it('should set gtm', () => {
        const promotion = {
          title: 'title'
        } as any;
        const data = {
          eventCategory: 'promotions',
          vipLevel: '',
          eventAction: 'link click',
          eventLabel: 'title',
          promoAction: '/link'
        };
        const info = {
          target: {
            classList: 'class',
            text: 'text',
            dataset: {
              routerlink: '/link'
            }
          }
        };
        service.sendGTM(promotion, info, true);
        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', data);
      });

      it('should push object with Link', () => {
        const isInternalButton = true;
        const promotion = {
          title: 'title'
        } as any;
        const info = {
          target: {
            classList: 'class',
            text: 'text',
            dataset: {
              routerlink: 'link'
            }
          }
        };
        const data = {
          eventCategory: 'promotions',
          vipLevel: '',
          eventAction: 'link click',
          eventLabel: 'title',
          promoAction: !isInternalButton || info.target.classList === 'btn' ? info.target.text : info.target.dataset.routerlink
        };
        service.sendGTM(promotion, info, isInternalButton);
        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', data);
        expect(data.promoAction).toEqual('link');
      });

      it('should push object with Text', () => {
        const isInternalButton = false;
        const promotion = {
          title: 'title'
        } as any;
        const info = {
          target: {
            classList: 'btn',
            text: 'text',
            dataset: {
              routerlink: 'link'
            }
          }
        };
        const data = {
          eventCategory: 'promotions',
          vipLevel: '',
          eventAction: 'cta click',
          eventLabel: 'title',
          promoAction: !isInternalButton || info.target.classList === 'btn' ? info.target.text : info.target.dataset.routerlink
        };
        service.sendGTM(promotion, info, isInternalButton);
        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', data);
        expect(data.promoAction).toEqual('text');
      });

      it('should set to gtm trackBogDialog()', () => {
        const data = {
          eventCategory: 'promotions',
          eventMarket: 'MKTFLAG_BOG',
          eventAction: 'Best Odds Guaranteed',
          eventLabel: 'ok'
        };
        service.trackBogDialog('MKTFLAG_BOG', 'ok');
        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', data);
      });
    });

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
            { categoryId: ['2'] },
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
    describe('#trackSignPosting', () => {
      it('should push gtm object with iconFlag if marketflag not avialable', () => {
        service.trackSignPosting('Bet in Inplay', 'EVFLAG_IHR', null);
        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
          eventCategory: 'promotions',
          eventAction: 'Bet in Inplay',
          eventLabel: 'ok',
          eventMarket: 'EVFLAG_IHR'
        });
      });
      it('should push gtm object with marketflag if marketflag avialable', () => {
        service.trackSignPosting('Extra place race off', 'EVFLAG_EPR', 'EVFLAG_EPRO');
        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
          eventCategory: 'promotions',
          eventAction: 'Extra place race off',
          eventLabel: 'ok',
          eventMarket: 'EVFLAG_EPRO'
        });
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

  it('should call openPromotionOverlay when called PROMOTIONS_SHOW_OVERLAY', () => {
    const promotionsServiceSpy = spyOn<any>(PromotionsService.prototype, 'openPromotionOverlay');
    commandService.register.and.callFake((command, fn) => { fn(flag); });
    createService();
    expect(promotionsServiceSpy).toHaveBeenCalledWith(flag);
  });

});



