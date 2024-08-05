import { Observable, of, ReplaySubject, throwError } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { CmsService } from './cms.service';
import environment from '@environment/oxygenEnvConfig';
import { ISvgItem, ISystemConfig, IWidget } from '@core/services/cms/models';
import { fakeAsync, tick } from '@angular/core/testing';
import { CONNECT_PROMOTION_CATEGORY_ID } from '@core/services/cms/cms.constants';
import { CLUBDATAMOCK, CLUBDATA_ACTIVEFALSEMOCK, CLUBDATA_ACTIVEFALSE_NOT_IN_RANGEMOCK, CLUBDATA_ACTIVETRUE_NOT_IN_RANGEMOCK, CLUBDATA_EQUALMOCK, EQUALSTATDATAMOCK, STATDATAMOCK, STAT_NOT_IN_RANGEMOCK } from './mockdata/cmsservice.mock';
import { FANZONEDETAILS } from '@app/core/services/fanzone/constant/fanzone.constant';

describe('@CmsService', () => { 
  const initialDataMock = {
    systemConfiguration: { systemConfiguration: {} },
    modularContent: { modularContent: {} },
    navigationPoints: [{ a: 1, b: 2 }],
    sportCategories: [{ categoryId: 1, sportName: 'category1' },
    { categoryId: 2, sportName: 'category2' },
    { categoryId: 3, sportName: 'greyhoundracing' },
    { categoryId: 4, imageTitle: 'football', svgId: '#1' }],
    svgSpriteContent: '<svg>',
    seoPages: { '1': { title: 'bet on sports', description: 'betting on sports' } },
    lotto: [],
    seoAutoPages: { '/event': { title: 'bet on event', description: 'betting on event' } },
    PredefinedStakes:{
      quick_bet:'1,2,3,4',
      global_stakes:"10,20,30,40"
    }
  } as any;

  let service: CmsService,
    pubSubService,
    cmsToolsService,
    deviceService,
    httpClient,
    coreToolsService,
    fanzoneStorageService,
    casinoLinkService,
    nativeBridgeService,
    userService,
    segmentEventManagerService,
    segmentedCMSService,
    cmsInitConfigPromise;

  beforeEach(() => {
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb: Function) => {
        if (b === pubSubApi.INITIATE_RGY_CALL) {
          cb && cb();
        }
        if (b === pubSubApi.SESSION_LOGOUT) {
          cb && cb();
        }
      }),
      API: pubSubApi
    };

    cmsToolsService = {
      processResult: jasmine.createSpy('processResult').and.returnValue([])
    };

    deviceService = {
      strictViewType: 'mobile',
      requestPlatform: 'mobile'
    };

    httpClient = {
      get: jasmine.createSpy('get').and.returnValue(of(
        {
          body: []
        }))
    };

    coreToolsService = {
      deepClone: jasmine.createSpy('deepClone')
    };

    fanzoneStorageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get')
    };

    casinoLinkService = {
      filterGamingLinkForIOSWrapper: jasmine.createSpy('filterGamingLinkForIOSWrapper')
    };

    nativeBridgeService = {
      isRemovingGamingEnabled: false
    };

    userService = {
      currencySymbol: '$',
      status: true,
      bonusSuppression: false,
      getPostLoginBonusSupValue: jasmine.createSpy('getPostLoginBonusSupValue')
    };
    segmentEventManagerService = {
      getSegmentDetails: jasmine.createSpy('getSegmentDetails'),
      chkModuleForSegmentation: jasmine.createSpy('chkModuleForSegmentation'),
    };
    segmentedCMSService = {
      getCmsInitData: jasmine.createSpy('getCmsInitData')
    };
    cmsInitConfigPromise = undefined;
    service = new CmsService(
      pubSubService,
      cmsToolsService,
      deviceService,
      httpClient,
      coreToolsService,
      fanzoneStorageService,
      casinoLinkService,
      nativeBridgeService,
      userService,
      segmentEventManagerService,
      segmentedCMSService,
      cmsInitConfigPromise
    );

    service['initialData$'] = new ReplaySubject<any>(1);
    service['initialData$'].next(initialDataMock as any);
    service['initialCmsDataPromise'] = undefined;
    service['initialRGYData$'] = new ReplaySubject<any>(1);

  });

  afterEach(() => {
    service = null;
  });

  it('should create instance', () => {
    expect(service).toBeDefined();
    expect(service instanceof CmsService).toBeTruthy();
  });

  it('should call getFSC', () => {
    service.getFSC('123').subscribe();
    expect(httpClient.get).toHaveBeenCalled();
  })

  it('should call getStaticBlock()', () => {
    service.getStaticBlock('contact-us');

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/static-block/contact-us`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getSystemConfig() once', () => {
    service['getInitialSystemConfig'] = jasmine.createSpy('getInitialSystemConfig').and
      .returnValue(of(initialDataMock.systemConfiguration));
    (<Observable<ISystemConfig>>service.getSystemConfig(true)).subscribe();

    service.systemConfiguration = initialDataMock.systemConfiguration as any;

    (<Observable<ISystemConfig>>service.getSystemConfig()).subscribe();

    expect(service['getInitialSystemConfig']).toHaveBeenCalledTimes(1);
  });

  it('should return systemConfiguration', () => {
    service['systemConfiguration'] = 'test' as any;

    service.getSystemConfig().subscribe(data => {
      expect(data as any).toEqual('test');
    });
  });

  describe('@getFeatureConfig()', () => {
    const preventCache = false;

    beforeEach(() => {
      service['getFeatureConfigByName'] = jasmine.createSpy('getFeatureConfigByName');
      service.featureConfigMap = new Map as any;
    });

    it('should call getFeatureConfigByName() ', () => {
      service.getFeatureConfig('football');
      expect(service['getFeatureConfigByName']).toHaveBeenCalledWith('football');
    });

    it('should call getFeatureConfigByName() ', () => {
      service.getFeatureConfig('football', preventCache);
      expect(service['getFeatureConfigByName']).toHaveBeenCalledWith('football');
    });

    it('should not call getFeatureConfigByName() ', () => {
      const successHandler = jasmine.createSpy('successHandler'),
        errorHandler = jasmine.createSpy('errorHandler');
      const featureConfigMock = { visible: true, showHeader: false };
      service.featureConfigMap.set('football', of(featureConfigMock));
      service.getFeatureConfig('football', preventCache).subscribe(successHandler, errorHandler);
      expect(successHandler).toHaveBeenCalledWith(featureConfigMock);
      expect(errorHandler).not.toHaveBeenCalled();
      expect(service['getFeatureConfigByName']).not.toHaveBeenCalled();
    });

    it('should call getFeatureConfigByName() method when preventCache was passed', () => {
      const successHandler = jasmine.createSpy('successHandler'),
        errorHandler = jasmine.createSpy('errorHandler');
      const featureConfigMock = { visible: true, showHeader: false };
      service.featureConfigMap.set('football', of(featureConfigMock));
      service['getFeatureConfigByName'] = jasmine.createSpy('getFeatureConfigByName').and.returnValue(of(featureConfigMock));

      service.getFeatureConfig('football', true).subscribe(successHandler, errorHandler);

      expect(successHandler).toHaveBeenCalledWith(featureConfigMock);
      expect(errorHandler).not.toHaveBeenCalled();
      expect(service['getFeatureConfigByName']).toHaveBeenCalled();
    });

    it('should not call getFeatureConfigByName() and not handle throwing error', () => {
      const successHandler = jasmine.createSpy('successHandler'),
        errorHandler = jasmine.createSpy('errorHandler');
      service.featureConfigMap.set('football', throwError('error'));

      service.getFeatureConfig('football', preventCache).subscribe(successHandler, errorHandler);

      expect(successHandler).not.toHaveBeenCalled();
      expect(errorHandler).toHaveBeenCalledWith('error');
      expect(service['getFeatureConfigByName']).not.toHaveBeenCalled();
    });

    it('should call getFeatureConfigByName() with error handling', () => {
      service['getFeatureConfigByName'] = jasmine.createSpy('getFeatureConfigByName').and.returnValue(throwError('error'));
      service.getFeatureConfig('football', preventCache, true).subscribe((data) => {
        expect(data).toEqual({});
      });

      expect(service['getFeatureConfigByName']).toHaveBeenCalledWith('football');
    });

    it('should not call getFeatureConfigByName() with error handling', () => {
      const successHandler = jasmine.createSpy('successHandler'),
        errorHandler = jasmine.createSpy('errorHandler');
      service.featureConfigMap.set('football', throwError('error'));
      service.getFeatureConfig('football', preventCache, true).subscribe(successHandler, errorHandler);

      expect(service['getFeatureConfigByName']).not.toHaveBeenCalled();
      expect(successHandler).toHaveBeenCalledWith({});
      expect(errorHandler).not.toHaveBeenCalled();
    });
  });

  describe('@getCompetitions()', () => {
    const competitions = { 'A-ZClassIDs': '', InitialClassIDs: '123' },
      competitionsFootball = { 'A-ZClassIDs': '', InitialClassIDs: '456' },
      competitionsBasketball = { 'A-ZClassIDs': '', InitialClassIDs: '789' };

    beforeEach(() => {
      service['systemConfiguration'] = {
        Competitions: competitions,
        CompetitionsFootball: competitionsFootball,
        CompetitionsBasketball: competitionsBasketball
      };
    });

    it('should return proper config for football sport', fakeAsync(() => {
      service.getCompetitions('Football')
        .subscribe(data => {
          expect(data).toEqual(competitionsFootball);
        });

      tick();
    }));

    it('should return proper config for CAPITALIZED basketball sport', fakeAsync(() => {
      service.getCompetitions('BASKETBALL')
        .subscribe(data => {
          expect(data).toEqual(competitionsBasketball);
        });

      tick();
    }));

    it('should return proper config for basketball sport', fakeAsync(() => {
      service.getCompetitions('basketball')
        .subscribe(data => {
          expect(data).toEqual(competitionsBasketball);
        });

      tick();
    }));

    it('should return fallback config', fakeAsync(() => {
      service.getCompetitions()
        .subscribe(data => {
          expect(data).toEqual(competitions);
        });

      tick();
    }));
  });

  it('should call getData()', fakeAsync(() => {
    const featureConfigMock = { visible: true, showHeader: false };
    service['getData'] = jasmine.createSpy('getData').and.returnValue(of(featureConfigMock));
    service['getFeatureConfigByName']('CompetitionsBasketball').subscribe();
    tick();

    expect(service['getData']).toHaveBeenCalledWith(`system-configurations/CompetitionsBasketball`);
  })
  );
  describe('@getToggleStatus()', () => {
    it('should return true if feature is enabled in CMS', fakeAsync(() => {
      service['systemConfiguration'] = { FeatureToggle: { PromoSignposting: true } };
      service.getToggleStatus('PromoSignposting')
        .subscribe(toggleStatus => {
          expect(toggleStatus).toBeTruthy();
        });

      tick();
    }));

    it('should return false if feature is disabled in CMS', fakeAsync(() => {
      service['systemConfiguration'] = { FeatureToggle: { PromoSignposting: false } };
      service.getToggleStatus('PromoSignposting')
        .subscribe(toggleStatus => {
          expect(toggleStatus).toBeFalsy();
        });

      tick();
    }));

    it('should return false if feature is not configured in CMS', fakeAsync(() => {
      service['systemConfiguration'] = { FeatureToggle: {} };
      service.getToggleStatus('PromoSignposting')
        .subscribe((toggleStatus) => {
          expect(toggleStatus).toBeFalsy();
        });

      tick();
    }));
  });

  it('should call getCmsCountries()', () => {
    service.getCmsCountries().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/countries-settings`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getInitialSystemConfig()', () => {
    service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
    service.getInitialSystemConfig().subscribe();

    expect(service['getCmsInitData']).toHaveBeenCalled();
  });

  it('should call triggerSystemConfigUpdate()', () => {
    service['getSystemConfig'] = jasmine.createSpy('getSystemConfig').and.returnValue(of(initialDataMock.systemConfiguration));
    service.triggerSystemConfigUpdate();

    expect(service['getSystemConfig']).toHaveBeenCalledWith(true);
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.SYSTEM_CONFIG_UPDATED, [initialDataMock.systemConfiguration]);
  });

  it('should call getRibbonModule()', () => {
    service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
    service['filterScheduleTabs'] = jasmine.createSpy('getCmsInitData').and.returnValue(initialDataMock.modularContent);
    service.getRibbonModule().subscribe((data) => {
      expect(data).toEqual({ getRibbonModule: initialDataMock.modularContent });
    });

    expect(service['getCmsInitData']).toHaveBeenCalled();
    expect(service['filterScheduleTabs']).toHaveBeenCalledWith(initialDataMock.modularContent);
  });

  it('should call getContactUs()', () => {
    service.getContactUs().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/static-block/contact-us-en-us`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getQuizPopupSetting()', () => {
    service['initialData$'] = undefined;
    service.getQuizPopupSetting().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/initial-data/mobile`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getTimelineSetting()', () => {
    service['initialData$'] = undefined;
    service.getTimelineSetting().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/initial-data/mobile`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getVirtualSports()', () => {
    service['initialData$'] = undefined;
    service.getVirtualSports().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/virtual-sports`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getVirtualSportstoPromise()', () => {
    service.getVirtualSportstoPromise().then();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/virtual-sports`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getVirtualSportAliases()', () => {
    service['initialData$'] = undefined;
    service.getVirtualSportAliases().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/initial-data/mobile`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getPrivateMarketsTermsAndConditions()', () => {
    service.getPrivateMarketsTermsAndConditions().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/static-block/private-markets-terms-and-conditions-en-us`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getFreebetsHelperText()', () => {
    service.getFreebetsHelperText().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/static-block/freebets-helper-text`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getMenuItems() once', () => {
    service['getCmsCSPInitData'] = jasmine.createSpy('getCmsCSPInitData').and.returnValue(of(initialDataMock));
    nativeBridgeService.isRemovingGamingEnabled = true;

    service['isGamingEnabled'] = jasmine.createSpy('isGamingEnabled').and.returnValue(true);
    service.getMenuItems().subscribe();

    expect(casinoLinkService.filterGamingLinkForIOSWrapper).toHaveBeenCalled();
  });

  it('should call getSports()', () => {
    service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));

    service.getSports().subscribe();

    expect(service['getCmsInitData']).toHaveBeenCalled();
    expect(cmsToolsService.processResult).toHaveBeenCalled();
  });

  it('should call getOddsBoost()', () => {
    service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
    service.getOddsBoost().subscribe((data) => {
      expect(data).toEqual({} as any);
    });

    expect(service['getCmsInitData']).toHaveBeenCalled();
  });

  it('should call getCouponSegment()', () => {
    service.getCouponSegment().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/coupon-segments`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getCouponMarketSelector()', () => {
    service.getCouponMarketSelector().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/coupon-market-selector`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getQuizPopupSettingDetails()', () => {
    service.getQuizPopupSettingDetails().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/quiz-popup-setting-details`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getTimelineTutorialDetails()', () => {
    service.getTimelineTutorialDetails().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/timeline-splash-config`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getOnboardingOverlay()', () => {
    service.getOnboardingOverlay('coupon-stats-widget').subscribe();
    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/coupon-stats-widget`,
      { observe: 'response', params: {} }
    );
  });

  it('should call extractInitialIcons()', () => {
    service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
    service.extractInitialIcons().subscribe(res => {
      expect(service['getCmsInitData']).toHaveBeenCalled();
      expect(res).toBe(initialDataMock.svgSpriteContent);
    });
  });

  describe('getItemSvg', () => {
    beforeEach(() => {
      service['getMenuItems'] = jasmine.createSpy('getMenuItems').and.returnValue(of(initialDataMock.sportCategories));
    });

    it('should call to get observable', () => {
      service.getItemSvg('football').subscribe((data: ISvgItem) => {
        expect(data).toEqual({ svgId: '#1' } as any);
      });

      expect(service['getMenuItems']).toHaveBeenCalledWith();
    });
    it('should call to get observable with id', () => {
      service.getItemSvg('football', 4).subscribe((data: ISvgItem) => {
        expect(data).toEqual({ svgId: '#1' } as any);
      });

      expect(service['getMenuItems']).toHaveBeenCalledWith();
    });
  });

  it('should call getAllPromotions()', () => {
    service.getAllPromotions().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/promotions`,
      { observe: 'response', params: {} }
    );
    expect(cmsToolsService.processResult).toHaveBeenCalled();
  });

  it('should call getRetailPromotions()', () => {
    service.getRetailPromotions().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/v2/${environment.brand}/promotions/${CONNECT_PROMOTION_CATEGORY_ID}`,
      { observe: 'response', params: {} }
    );
    expect(cmsToolsService.processResult).toHaveBeenCalled();
  });

  it('should call getGroupedPromotions()', () => {
    httpClient.get = jasmine.createSpy().and.returnValue(of({
      body: {
        promotionsBySection: [{ uriMedium: 'http://promo' }]
      }
    }));

    service.getGroupedPromotions().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/grouped-promotions`,
      { observe: 'response', params: {} }
    );
    expect(cmsToolsService.processResult).toHaveBeenCalled();
  });

  it('should call getSignpostingPromotionsLight()', () => {
    service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
    service.getSignpostingPromotionsLight().subscribe();

    expect(cmsToolsService.processResult).toHaveBeenCalled();
    expect(service['getCmsInitData']).toHaveBeenCalled();
  });

  it('should call getDesktopQuickLinks()', () => {
    service.getDesktopQuickLinks().subscribe();
    service['systemConfiguration'] = { BetPack: { enableBetPack: false } };
    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/desktop-quick-links`,
      { observe: 'response', params: {} }
    );
    expect(cmsToolsService.processResult).toHaveBeenCalled();
  });

  it('should call getFooterMenu()', () => {
    service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
    nativeBridgeService.isRemovingGamingEnabled = true;

    service['isGamingEnabled'] = jasmine.createSpy('isGamingEnabled').and.returnValue(true);
    service.getFooterMenu().subscribe();

    expect(service['isGamingEnabled']).toHaveBeenCalled();
    expect(casinoLinkService.filterGamingLinkForIOSWrapper).toHaveBeenCalled();
    expect(cmsToolsService.processResult).toHaveBeenCalled();
    expect(service['getCmsInitData']).toHaveBeenCalled();
  });

  it('should call getHeaderSubMenu()', () => {
    service['getFanzoneSportCategories'] = jasmine.createSpy('getFanzoneSportCategories');
    service.getHeaderSubMenu().subscribe();
    service['systemConfiguration'] = { BetPack: { enableBetPack: false } };
    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/header-submenu`,
      { observe: 'response', params: {} }
    );
    expect(service.getFanzoneSportCategories).toHaveBeenCalled();
    expect(cmsToolsService.processResult).toHaveBeenCalled();
  });

  it('isFanzoneConfig not disabled', () => {
    service.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of({Fanzone :{enabled: true}}))
    service.isFanzoneConfigDisabled().subscribe(res => {
      expect(res).toBe(false);
    });
  });

  it('should call getFanzoneSportCategories() when storage is empty', () => {
    service.isFanzoneConfigDisabled = jasmine.createSpy('isFanzoneConfigDisabled').and.returnValue(of(false));
    const sportCategories = [{categoryId: 160, targetUri: 'fz-football/everton/now-next'}];
    service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue({});
    service.getFanzoneSportCategories(sportCategories, FANZONEDETAILS[0]);
    expect(fanzoneStorageService.set).toHaveBeenCalled();
  });
  it('should call getFanzoneSportCategories() when storage is empty', () => {
    service.isFanzoneConfigDisabled = jasmine.createSpy('isFanzoneConfigDisabled').and.returnValue(of(false));
    const sportCategories = [{categoryId: 160, targetUri: 'fz-football/everton/now-next'}];
    service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue(undefined);
    service.getFanzoneSportCategories(sportCategories, FANZONEDETAILS[0]);
    expect(fanzoneStorageService.set).toHaveBeenCalled();
  });
  
  it('should set fanzone vacation as target uri when fanzone is disabled', () => {
    service.isFanzoneConfigDisabled = jasmine.createSpy('isFanzoneConfigDisabled').and.returnValue(of(true));
    const sportCategories = [{categoryId: 160, targetUri: 'fz-football/everton/now-next'}];
    service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue({teamName:'everton'});
    service.getFanzoneSportCategories(sportCategories, {});
    expect(sportCategories[0].targetUri).toBe('/fz-football/everton/now-next/vacation');
  });
  it('should set fanzone vacation as target uri when fanzone is disabled only once', () => {
    service.isFanzoneConfigDisabled = jasmine.createSpy('isFanzoneConfigDisabled').and.returnValue(of(true));
    const sportCategories = [{categoryId: 160, targetUri: 'fz-football/vacation'}];
    service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue({teamName:'everton'});
    service.getFanzoneSportCategories(sportCategories, {});
    expect(sportCategories[0].targetUri).toBe('fz-football/vacation');
  });

  it('isFanzoneConfig is disabled', () => {
    service.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of({Fanzone :{enabled: false}}))
    service.isFanzoneConfigDisabled().subscribe((res) => {
      expect(res).toBe(true);
    });
  });

  it('should call getFanzoneSportCategories()', () => {
    service.isFanzoneConfigDisabled = jasmine.createSpy('isFanzoneConfigDisabled').and.returnValue(of(false));
    const sportCategories = [{categoryId: 160, targetUri: 'fz-football/everton/now-next'}];
    service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue({teamName:'everton'});

    service.getFanzoneSportCategories(sportCategories, FANZONEDETAILS[0]);

    expect(fanzoneStorageService.set).toHaveBeenCalled();
  });

  it('should call getFanzoneSportCategories() in case of 21st team', () => {
    service.isFanzoneConfigDisabled = jasmine.createSpy('isFanzoneConfigDisabled').and.returnValue(of(false));
    const sportCategories = [{categoryId: 160, targetUri: 'fz-football/everton/now-next'}];
    service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue({teamName:'generic', teamId: 'FZ001'});

    service.getFanzoneSportCategories(sportCategories, FANZONEDETAILS[0]);

    expect(fanzoneStorageService.set).toHaveBeenCalled();
  });

  it('should return route name as now-next if now-next tab is enabled', () => {
    expect(service.getFanzoneRouteName(FANZONEDETAILS[0])).toBe('now-next');
  });
  
  it('should return route name as stats if now-next tab is disabled', () => {
    FANZONEDETAILS[0].fanzoneConfiguration.showNowNext = false;
    expect(service.getFanzoneRouteName(FANZONEDETAILS[0])).toBe('stats');
  });

  it('should return route name as club if now-next,stats tab are disabled', () => {
    userService.bonusSuppression = false;
    FANZONEDETAILS[0].fanzoneConfiguration.showNowNext = false;
    FANZONEDETAILS[0].fanzoneConfiguration.showStats = false;
    expect(service.getFanzoneRouteName(FANZONEDETAILS[0])).toBe('club');
  });

  it('should return route name as games if now-next,stats tab are disabled and is an rgy user', () => {
    FANZONEDETAILS[0].fanzoneConfiguration.showNowNext = false;
    FANZONEDETAILS[0].fanzoneConfiguration.showStats = false;
    FANZONEDETAILS[0].fanzoneConfiguration.showClubs = true;
    userService.bonusSuppression = true;
    expect(service.getFanzoneRouteName(FANZONEDETAILS[0])).toBe('games');
  });

  it('should return route name as games if now-next,stats ,clubs tabs are disabled', () => {
    FANZONEDETAILS[0].fanzoneConfiguration.showNowNext = false;
    FANZONEDETAILS[0].fanzoneConfiguration.showStats = false;
    FANZONEDETAILS[0].fanzoneConfiguration.showClubs = false;
    expect(service.getFanzoneRouteName(FANZONEDETAILS[0])).toBe('games');
  });

  it('should call getRetailMenu()', () => {
    service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
    service.getRetailMenu().subscribe();

    expect(cmsToolsService.processResult).toHaveBeenCalled();
    expect(service['getCmsInitData']).toHaveBeenCalled();
  });

  describe('@getOffers()', () => {
    beforeEach(() => {
      httpClient.get = jasmine.createSpy().and.returnValue(of({
        body: [{
          name: 'offer1',
          offers: []
        }, {
          name: 'offer2',
          offers: []
        }]
      }));
    });

    it('should call getOffers() for mobile', () => {
      service.getOffers('mobile').subscribe();

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/v2/${environment.brand}/offers/mobile`,
        { observe: 'response', params: {} }
      );
      expect(cmsToolsService.processResult).toHaveBeenCalled();
    });

    it('should call getOffers() for desktop', () => {
      service.getOffers('desktop').subscribe();

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/v2/${environment.brand}/offers/desktop`,
        { observe: 'response', params: {} }
      );
      expect(cmsToolsService.processResult).toHaveBeenCalled();
    });
  });

  it('should call getWidgets()', fakeAsync(() => {
    service['getData'] = jasmine.createSpy().and.returnValue(of({}));

    service['widgets'] = null;
    service.getWidgets().subscribe();
    tick();

    service['widgets'] = [{}] as any[];
    service.getWidgets().subscribe();
    tick();

    expect(service['getData']).toHaveBeenCalledTimes(1);
    expect(coreToolsService.deepClone).toHaveBeenCalledTimes(1);
  }));

  describe('@getActiveWidgets()', () => {
    it('should call getActiveWidgets() and return full list', () => {
      const sysConfig: ISystemConfig = {
        Favourites: {
          displayOnMobile: false,
          displayOnTablet: true,
          displayOnDesktop: true
        }
      };

      const widgets: IWidget[] = [
        { directiveName: 'favourites' },
        { directiveName: 'betslip' },
        { directiveName: 'testW' }
      ] as any;

      service.getWidgets = jasmine.createSpy('getWidgets').and.returnValue(of());
      service.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of(sysConfig));
      service.checkFavouritesWidget = jasmine.createSpy('checkFavouritesWidget').and.returnValue(true);

      service.getActiveWidgets().subscribe((filteredWidgets: IWidget[]) => {
        expect(service.getWidgets).toHaveBeenCalledTimes(1);
        expect(service.getSystemConfig).toHaveBeenCalledTimes(1);
        expect(service.checkFavouritesWidget).toHaveBeenCalledTimes(1);
        expect(service.checkFavouritesWidget).toHaveBeenCalledWith(sysConfig);
        expect(filteredWidgets).toEqual(widgets);
      });
    });

    it('should call getActiveWidgets() and return without favourites', () => {
      const widgets: IWidget[] = [
        { directiveName: 'favourites' },
        { directiveName: 'betslip' },
        { directiveName: 'testW' }
      ] as any;

      service.getWidgets = jasmine.createSpy('getWidgets').and.returnValue(of(widgets));
      service.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of({}));
      service.checkFavouritesWidget = jasmine.createSpy('checkFavouritesWidget').and.returnValue(false);

      service.getActiveWidgets().subscribe((filteredWidgets: IWidget[]) => {
        expect(filteredWidgets).toEqual([
          { directiveName: 'betslip' },
          { directiveName: 'testW' }
        ] as any);
      });
    });
  });

  it('should call checkFavouritesWidget() and check favourites widget state', () => {
    const sysConfig: ISystemConfig = {
      Favourites: {
        displayOnMobile: true,
        displayOnTablet: true,
        displayOnDesktop: true
      }
    };

    service['device'] = {
      strictViewType: ''
    } as any;

    expect(service.checkFavouritesWidget(sysConfig)).toBeFalsy();

    service['device'].strictViewType = 'mobile';
    expect(service.checkFavouritesWidget(sysConfig)).toBeTruthy();

    sysConfig.Favourites.displayOnMobile = false;
    expect(service.checkFavouritesWidget(sysConfig)).toBeFalsy();

    service['device'].strictViewType = 'tablet';
    expect(service.checkFavouritesWidget(sysConfig)).toBeTruthy();

    sysConfig.Favourites.displayOnTablet = false;
    expect(service.checkFavouritesWidget(sysConfig)).toBeFalsy();

    service['device'].strictViewType = 'desktop';
    expect(service.checkFavouritesWidget(sysConfig)).toBeTruthy();

    sysConfig.Favourites.displayOnDesktop = false;
    expect(service.checkFavouritesWidget(sysConfig)).toBeFalsy();

    sysConfig.Favourites = undefined;
    expect(service.checkFavouritesWidget(sysConfig)).toBeFalsy();
  });

  it('should call getSeoPage()', () => {
    const id = '1';

    service.getSeoPage(id).subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/seo-page/${id}`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getLottoBanner()', () => {
    service.getLottoBanner().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/lotto-configs`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getSportTabs', () => {
    const id = '1';

    service.getSportTabs(id);

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/sport-tabs/1`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getSportConfig()', () => {
    const id = 1;
    deviceService.requestPlatform = 'mobile';
    service['initialData$'] = undefined;

    service.getSportConfig(id).subscribe(result => {
      // eslint-disable-next-line no-console
      console.log(result);
      expect(result).toEqual([]);
    });
  });

  it('should call getSportConfigs()', () => {
    const ids = [1, 2];
    deviceService.requestPlatform = 'mobile';
    service['initialData$'] = undefined;

    service.getSportConfigs(ids).subscribe(result => {
      expect(result).toEqual([]);
    });
  });

  it('should call getFootball3DBanners()', () => {
    httpClient.get = jasmine.createSpy().and.returnValue(of({
      body: {
        bannersData: [{
          uriMedium: 'http://uriMedium'
        }, {
          uriMedium: 'http://uriMedium'
        }]
      }
    }));

    service.getFootball3DBanners().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/3d-football-banners`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getLeagues()', () => {
    service.getLeagues().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/leagues`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getMarketLinks()', () => {
    service.getMarketLinks().subscribe();

    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/market-links`,
      { observe: 'response', params: {} }
    );
  });

  describe('getNavigationPoints', () => {
    beforeEach(() => {
      userService.username = 'Test User';
      segmentedCMSService.isInitialDataAvailable = jasmine.createSpy('isInitialDataAvailable').and.returnValue(true);
      segmentEventManagerService.getOtfSegmentUserStatus = jasmine.createSpy('getOtfSegmentUserStatus').and.returnValue(true);
    });

    it('no navigationPoints', fakeAsync(() => {
      segmentedCMSService.getActiveExtraNavPoints = jasmine.createSpy('getActiveExtraNavPoints').and.returnValue(of([]));
      const navMock = initialDataMock;
      navMock.navigationPoints = undefined;
      service['initialData$'].next(navMock as any);
      service.getNavigationPoints().subscribe(result => {
        expect(result).toEqual([]);
      });
      tick();
    }));


    it('navigationPoints exists', fakeAsync(() => {
      segmentedCMSService.getActiveExtraNavPoints = jasmine.createSpy('getActiveExtraNavPoints').and.returnValue(of([]));
      spyOn(Date, 'now').and.returnValue(1588539600000);
      const navMock = initialDataMock;
      navMock.navigationPoints = [{
        validityPeriodEnd: '2020-07-26T06:00:00Z',
        validityPeriodStart: '2020-04-03T21:00:00Z'
      }, {
        validityPeriodEnd: '2020-07-26T06:00:00Z',
        validityPeriodStart: '2020-06-03T21:00:00Z'
      }, {
        validityPeriodEnd: '2020-04-26T06:00:00Z',
        validityPeriodStart: '2020-03-03T21:00:00Z'
      }];
      service['initialData$'].next(navMock as any);

      service.getNavigationPoints().subscribe(result => {
        expect(result).toEqual([{
          validityPeriodEnd: '2020-07-26T06:00:00Z',
          validityPeriodStart: '2020-04-03T21:00:00Z'
        }] as any);
      });
      tick();
    }));
    it('get ExtranavigationPoint', fakeAsync(() => {
      userService.username = 'Test User';
      segmentedCMSService.isInitialDataAvailable = jasmine.createSpy('isInitialDataAvailable').and.returnValue(true);
      segmentedCMSService.getActiveExtraNavPoints = jasmine.createSpy('getActiveExtraNavPoints').and.returnValue([{
        categoryId: [16],
        competitionId: ['123', '234'],
        homeTabs: ['/featured', '/inplay'],
        enabled: true,
        targetUri: '/sport/football',
        title: 'Football',
        description: 'werthjk',
        validityPeriodEnd: '2019-02-24T09:48:20.917Z',
        validityPeriodStart: '2018-12-24T09:48:20.917Z',
        featureTag: '12F'
      }])
      service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue({ segment: 'true' });
      spyOn(Date, 'now').and.returnValue(1588539600000);
      const navMock = initialDataMock;
      navMock.navigationPoints = [{
        validityPeriodEnd: '2020-07-26T06:00:00Z',
        validityPeriodStart: '2020-04-03T21:00:00Z'
      }, {
        validityPeriodEnd: '2020-07-26T06:00:00Z',
        validityPeriodStart: '2020-06-03T21:00:00Z'
      }, {
        validityPeriodEnd: '2020-04-26T06:00:00Z',
        validityPeriodStart: '2020-03-03T21:00:00Z'
      }];
      service['initialData$'].next(navMock as any);

      service.getNavigationPoints(['inplay'], 'homeTabs').subscribe(result => {
        expect(result).toEqual([{
          categoryId: [16],
          competitionId: ['123', '234'],
          homeTabs: ['/featured', '/inplay'],
          enabled: true,
          targetUri: '/sport/football',
          title: 'Football',
          description: 'werthjk',
          validityPeriodEnd: '2019-02-24T09:48:20.917Z',
          validityPeriodStart: '2018-12-24T09:48:20.917Z',
          featureTag: '12F'
        }] as any);
      });
      tick();
    }));

    it(' ExtranavigationPoints Undefined', fakeAsync(() => {
      userService.username = undefined;
      segmentedCMSService.getActiveExtraNavPoints = jasmine.createSpy('getActiveExtraNavPoints').and.returnValue(of([]));
      service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue({});
      const navMock = initialDataMock;
      navMock.navigationPoints = undefined;
      service['initialData$'].next(navMock as any);
      service.getNavigationPoints().subscribe(result => {
        expect(result).toEqual([]);
      });
      tick();
    }));
    it(' ExtranavigationPoints segment Undefined', fakeAsync(() => {
      userService.username = undefined;
      segmentedCMSService.getActiveExtraNavPoints = jasmine.createSpy('getActiveExtraNavPoints').and.returnValue(of([]));
      service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue({});
      const navMock = initialDataMock;
      navMock.navigationPoints = undefined;
      service['initialData$'].next(navMock as any);
      service.getNavigationPoints().subscribe(result => {
        expect(result).toEqual([]);
      });
      tick();
    }));
  });

  it('should call getCmsYourCallLeaguesConfig() once', () => {
    (<any>service.getCmsYourCallLeaguesConfig()).subscribe();

    expect(httpClient.get).toHaveBeenCalledTimes(1);
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/yc-leagues`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getYourCallStaticBlock()', () => {
    service.getYourCallStaticBlock().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/yc-static-block`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getEDPMarkets()', () => {
    service.getEDPMarkets().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/edp-markets`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getRacingEDPMarkets()', () => {
    service.getRacingEDPMarkets().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/racing-edp-markets`,
      { observe: 'response', params: {} }
    );
  });
  it('should handle error in  getRacingEDPMarkets()', () => {
    httpClient.get.and.returnValue(throwError('error'));
    service.getRacingEDPMarkets().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/racing-edp-markets`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getEDPSurfaceBets()', () => {
    const id = 1;

    service.getEDPSurfaceBets(id).subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.SURFACE_BETS_URL}/${environment.brand}/edp-surface-bets/${id}`,
      { observe: 'response', params: {} }
    );
  });
  it('should call getStatisticalContent()', () => {
    const id = '1';

    service.getStatisticalContent(id).subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/statistic-content/${id}`,
      { observe: 'response', params: {} }
    );
  });


  it('should call getTeamsColors()', () => {
    service.getTeamsColors(['team1', 'team2'], '12').subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/asset-management`,
      {
        observe: 'response', params: {
          teamNames: 'TEAM1,TEAM2', sportId: '12'
        }
      }
    );
  });

  it('should call getYourCallBybMarkets()', () => {
    service.getYourCallBybMarkets().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/byb-markets`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getOTFIosToggle()', () => {
    service.getOTFIosToggle().subscribe();
    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/one-two-free/otf-ios-app-toggle`,
      { observe: 'response', params: {} }
    );
  });

  it('should call getFiveASideFormations()', () => {
    service.getFiveASideFormations().subscribe();
    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/five-a-side-formations`,
      { observe: 'response', params: {} }
    );
  });

  describe('@getMaintenancePage()', () => {
    it('(desktop maintenance page)', () => {
      deviceService.requestPlatform = 'desktop';

      service.getMaintenancePage().subscribe();

      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/maintenance-page/desktop`,
        { observe: 'response', params: {} }
      );
    });

    it('(mobile maintenance page)', () => {
      service.getMaintenancePage().subscribe();

      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/maintenance-page/mobile`,
        { observe: 'response', params: {} }
      );
    });
  });

  describe('@getData()', () => {
    it('should call getData() with params', () => {
      const url = 'test-link',
        options = { option: 'option' };

      service['getData'](url, options);

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/${url}`,
        { observe: 'response', params: options }
      );
    });

    it('should call getData() without params', () => {
      const url = 'test-link';

      service['getData'](url);

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/${url}`,
        { observe: 'response', params: {} }
      );
    });
  });

  describe('@getSurfaceBetsData()', () => {
    it('should call getSurfaceBetsData() with params', () => {
      const url = 'edp-surface-bets/1',
        options = { option: 'option' };

      service['getSurfaceBetsData'](url, options);

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.SURFACE_BETS_URL}/${environment.brand}/${url}`,
        { observe: 'response', params: options }
      );
    });

    it('should call getSurfaceBetsData() without params', () => {
      const url = 'edp-surface-bets/1';

      service['getSurfaceBetsData'](url);

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.SURFACE_BETS_URL}/${environment.brand}/${url}`,
        { observe: 'response', params: {} }
      );
    });
  });

  describe('@getV2Data()', () => {
    it('should call getV2Data() with params', () => {
      const url = 'offers',
        options = { option: 'option' };

      service['getV2Data'](url, options);

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/v2/${environment.brand}/${url}`,
        { observe: 'response', params: options }
      );
    });

    it('should call getV2Data() without params', () => {
      const url = 'offers';

      service['getV2Data'](url);

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/v2/${environment.brand}/${url}`,
        { observe: 'response', params: {} }
      );
    });
  });

  describe('@isGamingEnabled()', () => {
    it('should call isGamingEnabled() and return true', () => {
      service.systemConfiguration = {
        GamingEnabled: {
          enabledGamingOverlay: false
        }
      } as any;

      expect(service['isGamingEnabled']()).toEqual(true);
    });

    it('should call isGamingEnabled() and return false if no GamingEnabled configuration', () => {
      service.systemConfiguration = {} as any;

      expect(service['isGamingEnabled']()).toBe(false);
    });

    it('should call isGamingEnabled() and return false if gaming enabled', () => {
      service.systemConfiguration = {
        GamingEnabled: {
          enabledGamingOverlay: true
        }
      } as any;

      expect(service['isGamingEnabled']()).toBe(false);
    });
  });

  describe('@getPromotions()', () => {
    it('should call getPromotions() without params', () => {
      service['getPromotions']().subscribe();

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/promotions`,
        { observe: 'response', params: {} }
      );
      expect(cmsToolsService.processResult).toHaveBeenCalled();
    });

    it('should call getPromotions() wit category id', () => {
      const id = '1';

      service['getPromotions'](id).subscribe();

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/promotions/${id}`,
        { observe: 'response', params: {} }
      );
      expect(cmsToolsService.processResult).toHaveBeenCalled();
    });

    it('should call getPromotions() wit category id and V2', () => {
      const id = '1';

      service['getPromotions'](id, true).subscribe();

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/v2/${environment.brand}/promotions/${id}`,
        { observe: 'response', params: {} }
      );
      expect(cmsToolsService.processResult).toHaveBeenCalled();
    });
  });

  describe('@filterScheduleTabs()', () => {
    it('should call filterScheduleTabs() without range and return the same ribbonData', () => {
      const ribbonData = [{
        devices: ['s1', 's2'],
        directiveName: 'featured',
        id: '1',
        showTabOn: 'tab',
        title: 'title',
        url: 'http://url',
        visible: true
      }],
        result = service['filterScheduleTabs'](ribbonData);

      expect(result).toEqual(ribbonData);
    });

    it('should call filterScheduleTabs() with one element, filter ribbonData and return the same ribbonData', () => {
      const ribbonData = [{
        devices: ['s1', 's2'],
        directiveName: 'featured',
        id: '1',
        showTabOn: 'tab',
        title: 'title',
        url: 'http://url',
        visible: true,
        displayFrom: new Date(new Date().setDate(new Date().getDate() - 1)).toDateString(),
        displayTo: new Date(new Date().setDate(new Date().getDate() + 1)).toDateString()
      }],
        result = service['filterScheduleTabs'](ribbonData);

      expect(result).toEqual(ribbonData);
    });

    it('should call filterScheduleTabs(), filter ribbonData when betPack is disable', () => {
      const ribbonData = [{ title: 'BetPack' } as any]
      service['systemConfiguration'] = { BetPack: { enableBetPack: false } };
      expect(service['filterScheduleTabs'](ribbonData)).toEqual([]);
    });

    it('should call filterScheduleTabs(), filter ribbonData when betPack is enable', () => {
      const ribbonData = [{ title: 'BetPack' } as any]
      service['systemConfiguration'] = { BetPack: { enableBetPack: true } };
      expect(service['filterScheduleTabs'](ribbonData)).toEqual(ribbonData);
    });

    it('should call filterScheduleTabs() with multiple elements, filter ribbonData and return the same ribbonData', () => {
      const ribbonData = [{
        devices: ['s1', 's2'],
        directiveName: 'featured',
        id: '1',
        showTabOn: 'tab',
        title: 'title',
        url: 'http://url',
        visible: true,
        displayFrom: new Date(new Date().setDate(new Date().getDate() - 1)).toDateString(),
        displayTo: new Date(new Date().setDate(new Date().getDate() + 1)).toDateString()
      }, {
        devices: ['s1', 's2'],
        directiveName: 'featured',
        id: '1',
        showTabOn: 'tab',
        title: 'title',
        url: 'http://url',
        visible: true,
        displayFrom: new Date(new Date().setDate(new Date().getDate() + 4)).toDateString(),
        displayTo: new Date(new Date().setDate(new Date().getDate() + 5)).toDateString()
      }],
        result = service['filterScheduleTabs'](ribbonData);

      expect(result).toEqual(ribbonData);
    });

    it('should call filterScheduleTabs(), filter ribbonData and return not the same ribbonData', () => {
      const ribbonData = [{
        devices: ['s1', 's2'],
        directiveName: 'eventhub',
        id: '1',
        showTabOn: 'tab',
        title: 'title',
        url: 'http://url',
        visible: true,
        displayFrom: new Date(new Date().setDate(new Date().getDate() - 1)).toDateString(),
        displayTo: new Date(new Date().setDate(new Date().getDate() + 1)).toDateString()
      }, {
        devices: ['s1', 's2'],
        directiveName: 'eventhub',
        id: '1',
        showTabOn: 'tab',
        title: 'title',
        url: 'http://url',
        visible: true,
        displayFrom: new Date(new Date().setDate(new Date().getDate() + 4)).toDateString(),
        displayTo: new Date(new Date().setDate(new Date().getDate() + 5)).toDateString()
      }],
        result = service['filterScheduleTabs'](ribbonData);

      expect(result).not.toEqual(ribbonData);
    });
  });

  it('should be in active range', () => {
    const from = new Date(new Date().setDate(new Date().getDate() - 1)).toDateString(),
      to = new Date(new Date().setDate(new Date().getDate() + 1)).toDateString(),
      result = service['isActiveRange'](from, to);

    expect(result).toBeTruthy();
  });

  it('should not be in active range', () => {
    const from = new Date(new Date().setDate(new Date().getDate())).toDateString(),
      to = new Date(new Date().setDate(new Date().getDate() + 1)).toDateString(),
      result = service['isActiveRange'](from, to);

    expect(result).toBeTruthy();
  });

  it('@parseContent: should replace params in cms static block', () => {
    const content = 'Place your 5 team accumulator or upwards on selected matches on the match betting market' +
      'and get money back as a free bet up to [[\'currency\']][[\'param1\']] if one team lets you down.';
    const params = ['20'];

    const actualResult = service.parseContent(content, params);

    expect(actualResult).toEqual('Place your 5 team accumulator or upwards on selected matches on the match betting market' +
      'and get money back as a free bet up to $20 if one team lets you down.');
  });

  it('@parseContent: should replace params in cms static block when params is string', () => {
    const content = 'Place your 5 team accumulator or upwards on selected matches on the match betting market' +
      'and get money back as a free bet up to [[\'currency\']][[\'param1\']] if one team lets you down.';
    const params = '[20]';

    const actualResult = service.parseContent(content, params);

    expect(actualResult).toEqual('Place your 5 team accumulator or upwards on selected matches on the match betting market' +
      'and get money back as a free bet up to $20 if one team lets you down.');
  });

  describe('isBogFromCms()', () => {
    it('should call isBogFromCms()', () => {
      const sysConfig: ISystemConfig = {
        BogToggle: {
          bogToggle: true
        }
      };
      service.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of(sysConfig));
      service.isBogFromCms().subscribe();

      expect(service.getSystemConfig).toHaveBeenCalledTimes(1);
    });
  });

  describe('isEDPLogsEnabled()', () => {
    it('should call isEDPLogsEnabled()', () => {
      const sysConfig: ISystemConfig = {
        EDPLogs: {
          enabled: true
        }
      };
      service.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of(sysConfig));
      service.isEDPLogsEnabled().subscribe();

      expect(service.getSystemConfig).toHaveBeenCalledTimes(1);
    });
  });

  describe('getFiveASideStaticBlocks', () => {
    it('should get five-a-side static blocks', () => {
      service.getFiveASideStaticBlocks().subscribe();
      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/5a-side-static-block`,
        { observe: 'response', params: {} }
      );
    });
  });


  describe('getStatisticalContent', () => {
    it('should call getStatisticalContent()', () => {
      const id = '1';
      service.getStatisticalContent(id).subscribe();
      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/statistic-content/${id}`,
        { observe: 'response', params: {} }
      );
    });
  });
  it('should  get STATICAL data', async () => {
    const id = '1';
    httpClient.get = jasmine.createSpy().and.returnValue(of({
      body: STATDATAMOCK
    }));
    const currentDate = new Date('2022-05-02T15:05:27Z').getTime().toString();
    spyOn(window, 'Date').and.returnValue(currentDate);

    service.getStatisticalContent(id).subscribe((data) => {
      expect(data).toEqual(EQUALSTATDATAMOCK);
    });

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/statistic-content/${id}`,
      { observe: 'response', params: {} }
    );
  });
  it('should not get STATICAL data if active is true but date is not in range', async () => {
    const id = '1';
    httpClient.get = jasmine.createSpy().and.returnValue(of({
      body: STAT_NOT_IN_RANGEMOCK
    }));

    service.getStatisticalContent(id).subscribe((data) => {
      expect(data).toEqual([]);
    });

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/statistic-content/${id}`,
      { observe: 'response', params: {} }
    );
  });
  describe('getMarketSwitcherFlagValue()', () => {
    it('should call getMarketSwitcherFlagValue()', () => {
      const sysConfig: ISystemConfig = {
        MarketSwitcher: {
          cricket: true
        }
      };
      service.getFeatureConfig = jasmine.createSpy('getFeatureConfig').and.returnValue(of(sysConfig));
      service.getMarketSwitcherFlagValue('cricket').subscribe();
      expect(service.getFeatureConfig).toHaveBeenCalledTimes(1);
    });
    it('should return true if MarketSwitcher feature is enabled in CMS', fakeAsync(() => {
      const sysConfig: ISystemConfig = { cricket: true, AllSports: true };
      service.getFeatureConfig = jasmine.createSpy('getFeatureConfig').and.returnValue(of(sysConfig));
      service.getMarketSwitcherFlagValue('cricket')
        .subscribe(marketSwitcherFlag => {
          expect(marketSwitcherFlag).toBeTruthy();
        });
      tick();
    }));
    it('should return false if MarketSwitcher feature is disabled globally in CMS', fakeAsync(() => {
      const sysConfig: ISystemConfig = { cricket: true, AllSports: false };
      service.getFeatureConfig = jasmine.createSpy('getFeatureConfig').and.returnValue(of(sysConfig));
      service.getMarketSwitcherFlagValue('cricket')
        .subscribe(marketSwitcherFlag => {
          expect(marketSwitcherFlag).toBeFalsy();
        });
      tick();
    }));
    it('should return false if MarketSwitcher feature is disabled per sport level in CMS', fakeAsync(() => {
      const sysConfig: ISystemConfig = { cricket: false, AllSports: true };
      service.getFeatureConfig = jasmine.createSpy('getFeatureConfig').and.returnValue(of(sysConfig));
      service.getMarketSwitcherFlagValue('cricket')
        .subscribe(marketSwitcherFlag => {
          expect(marketSwitcherFlag).toBeFalsy();
        });
      tick();
    }));
    it('should return false if MarketSwitcher feature is not configured in CMS', fakeAsync(() => {
      const sysConfig: ISystemConfig = {};
      service.getFeatureConfig = jasmine.createSpy('getFeatureConfig').and.returnValue(of(sysConfig));
      service.getMarketSwitcherFlagValue('cricket')
        .subscribe((marketSwitcherFlag) => {
          expect(marketSwitcherFlag).toBeFalsy();
        });
      tick();
    }));
  });

  describe('getCmsInitData', () => {
    beforeEach(() => {
      service.initialData = undefined;
      service['initialCmsDataPromise'] = undefined;
      service['initialData$'] = undefined;
      service['getData'] = jasmine.createSpy('getData').and.returnValue(of({ body: initialDataMock }));
      service['releaseSubject'] = jasmine.createSpy('releaseSubject');
    });

    it('should resolve initialCmsDataPromise if present in cmsInitConfigPromise Injected token', fakeAsync(() => {
      service['windowRef'] = { nativeWindow: {} } as any;
      service['cmsInitConfigPromise'] = Promise.resolve(initialDataMock);
      service['getCmsInitData']().subscribe();

      tick();

      expect(service['releaseSubject']).toHaveBeenCalledWith(initialDataMock);
      expect(service['getData']).not.toHaveBeenCalled();
    }));

    it('should do call if no Promise', fakeAsync(() => {
      service['windowRef'] = { nativeWindow: {} } as any;

      service['getCmsInitData']().subscribe();

      tick();

      expect(service['releaseSubject']).toHaveBeenCalledWith(initialDataMock);
      expect(service['getData']).toHaveBeenCalledWith('initial-data/mobile');
    }));

    it('should return stored data', () => {
      service['initialData$'] = new ReplaySubject<any>(1);
      service['initialData$'].next(initialDataMock);

      service['getCmsInitData']().subscribe((data) => {
        expect(data).toBe(initialDataMock);
      });
      expect(service['releaseSubject']).not.toHaveBeenCalled();
      expect(service['getData']).not.toHaveBeenCalled();
    });
  });

  it('releaseSubject', fakeAsync(() => {
    service.betpackValidInitialData = jasmine.createSpy('betpackValidInitialData');
    service.initialData = undefined;
    service.systemConfiguration = undefined;
    service['initialData$'] = new ReplaySubject<any>(1);
    service['initialData$'].subscribe((data) => {
      expect(data).toBe(initialDataMock);
    });
    service['releaseSubject'](initialDataMock);
    tick();

    expect(service['initialData$'].closed).toBe(false);
    expect(service['initialData$'].isStopped).toBe(true);
    expect(service.initialData).toBe(initialDataMock as any);
    expect(service.systemConfiguration).toBe(initialDataMock.systemConfiguration as any);
  }));

  describe('ngOnDestroy', () => {
    it('should unsubscribe ReplaySubject', () => {
      service['initialData$'] = new ReplaySubject<any>(1);

      service.ngOnDestroy();

      expect(service['initialData$'].closed).toBe(true);
      expect(service['initialData$'].isStopped).toBe(true);
    });

    it('should not unsubscribe', function () {
      service['initialData$'] = null;

      service.ngOnDestroy();

      expect(service['initialData$']).toBe(null);
    });

    it('should unsubscribe ReplaySubject initialRGYData$', () => {
      service['initialRGYData$'] = new ReplaySubject<any>(1);

      service.ngOnDestroy();

      expect(service['initialRGYData$'].closed).toBe(true);
      expect(service['initialRGYData$'].isStopped).toBe(true);
    });

    it('should not unsubscribe initialRGYData$', () => {
      service['initialRGYData$'] = null;

      service.ngOnDestroy();

      expect(service['initialRGYData$']).toBe(null);
    });
  });
  it('getSportCategoryById', fakeAsync(() => {
    service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
    cmsToolsService.processResult.and.returnValue(initialDataMock.sportCategories);

    service.getSportCategoryById('1').subscribe((result) => {
      expect(result).toEqual({ categoryId: 1, sportName: 'category1' } as any);
    });
    tick();

    expect(cmsToolsService.processResult).toHaveBeenCalledWith(initialDataMock.sportCategories);
  }));

  it('getSportCategoryByIds', fakeAsync(() => {
    service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
    cmsToolsService.processResult.and.returnValue(initialDataMock.sportCategories);

    service.getSportCategoryByIds([1]).subscribe((result) => {
      expect(result).toEqual([{ categoryId: 1, sportName: 'category1' } as any]);
    });
    tick();

    expect(cmsToolsService.processResult).toHaveBeenCalledWith(initialDataMock.sportCategories);
  }));

  it('getSportCategoryByIds', fakeAsync(() => {
    service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
    cmsToolsService.processResult.and.returnValue(initialDataMock.sportCategories);

    service.getSportCategoryByIds([5]).subscribe((result) => {
      expect(result).toEqual([]);
    });
    tick();

    expect(cmsToolsService.processResult).toHaveBeenCalledWith(initialDataMock.sportCategories);
  }));

  it('getSportCategoryById when category id null', fakeAsync(() => {
    service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
    cmsToolsService.processResult.and.returnValue(
      [{ categoryId: null, sportName: 'categorynull' },
      { categoryId: 1, sportName: 'category1' },
      { categoryId: 3, sportName: 'greyhoundracing' },
      { imageTitle: 'football', svgId: '#1' }]
    );

    service.getSportCategoryById('1').subscribe((result) => {
      expect(result).toEqual({ categoryId: 1, sportName: 'category1' } as any);
    });
    tick();

    expect(cmsToolsService.processResult).toHaveBeenCalledWith(initialDataMock.sportCategories);
  }));

  describe('getSportCategoryByName', () => {
    beforeEach(() => {
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
      cmsToolsService.processResult.and.returnValue(initialDataMock.sportCategories);
    });

    it('football', fakeAsync(() => {
      service.getSportCategoryByName('category1').subscribe(res => {
        expect(res).toEqual({ categoryId: 1, sportName: 'category1' } as any);
      });
      tick();

      expect(cmsToolsService.processResult).toHaveBeenCalledWith(initialDataMock.sportCategories);
    }));

    it('greyhound', fakeAsync(() => {
      service.getSportCategoryByName('greyhound').subscribe(res => {
        expect(res).toEqual({ categoryId: 3, sportName: 'greyhoundracing' } as any);
      });
      tick();

      expect(cmsToolsService.processResult).toHaveBeenCalledWith(initialDataMock.sportCategories);
    }));
  });

  describe('getSportCategoriesByName', () => {
    beforeEach(() => {
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
      cmsToolsService.processResult.and.returnValue(initialDataMock.sportCategories);
    });

    it('football', fakeAsync(() => {
      service.getSportCategoriesByName(['category1', 'category2']).subscribe(res => {
        expect(res).toContain({ categoryId: 1, sportName: 'category1' } as any);
        expect(res).toContain({ categoryId: 2, sportName: 'category2' } as any);
      });
      tick();

      expect(cmsToolsService.processResult).toHaveBeenCalledWith(initialDataMock.sportCategories);
    }));

    it('greyhound', fakeAsync(() => {
      service.getSportCategoriesByName(['greyhound']).subscribe(res => {
        expect(res).toContain({ categoryId: 3, sportName: 'greyhoundracing' } as any);
      });
      tick();

      expect(cmsToolsService.processResult).toHaveBeenCalledWith(initialDataMock.sportCategories);
    }));
  });
  describe('getHeaderMenu list', () => {
    it('filters if version matches and all domain matches', () => {
      const initialData = {
        systemConfiguration: {
          GamingEnabled: {
            iosVersionBlackList: ['6', '7-7.1'],
            hostMenuBlackList: ['www.ladbrokes.com', 'sport/poker']
          }
        },
        sportCategories: [{ 'targetUri': 'www.ladbrokes.com' }, { 'targetUri': 'sport/poker' }, { 'targetUri': 'www.ladbrokes123.com' }]
      };
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      deviceService.isWrapper = true;
      deviceService.isIos = true;
      const result = [{ 'targetUri': 'www.ladbrokes123.com' }];
      service.getMenuItems('6').subscribe();
      expect(cmsToolsService.processResult).toHaveBeenCalledWith(result);
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });

    it('set team name for fanzone', () => {
      const initialData = {
        systemConfiguration: {
          GamingEnabled: {
            iosVersionBlackList: ['6', '7-7.1'],
            hostMenuBlackList: ['www.ladbrokes.com', 'sport/poker']
          }
        },
        sportCategories: [{ categoryId: 160, targetUri: 'fz-football' }]
      };
      service.isFanzoneConfigDisabled = jasmine.createSpy('isFanzoneConfigDisabled').and.returnValue(of(false));
      service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue({teamName:'manchester'});
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      deviceService.isWrapper = true;
      deviceService.isIos = true;
      service.getMenuItems('6').subscribe();
      expect(cmsToolsService.processResult).toHaveBeenCalled();
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });

    it('should not set team name for fanzone for other categories', () => {
      const initialData = {
        systemConfiguration: {
          GamingEnabled: {
            iosVersionBlackList: ['6', '7-7.1'],
            hostMenuBlackList: ['www.ladbrokes.com', 'sport/poker']
          }
        },
        sportCategories: [{ categoryId: 16, targetUri: 'fz-football' }]
      };
      service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue({ teamName: 'manchester' });
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      deviceService.isWrapper = true;
      deviceService.isIos = true;
      const result = [{ categoryId: 16, targetUri: 'fz-football' }]
      service.getMenuItems('6').subscribe();
      expect(cmsToolsService.processResult).toHaveBeenCalledWith(result);
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
    it('should not set team name for fanzone for other categories based on no storage value as undefined', () => {
      const initialData = {
        systemConfiguration: {
          GamingEnabled: {
            iosVersionBlackList: ['6', '7-7.1'],
            hostMenuBlackList: ['www.ladbrokes.com', 'sport/poker']
          }
        },
        sportCategories: [{ categoryId: 160, targetUri: 'fz-football' }]
      };
      service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue(undefined);
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      deviceService.isWrapper = true;
      deviceService.isIos = true;
      const result = [{ categoryId: 160, targetUri: 'fz-football' }]
      service.getMenuItems('6').subscribe();
      expect(cmsToolsService.processResult).toHaveBeenCalledWith(result);
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
    it('should not set team name for fanzone for other categories based on no storage value as null', () => {
      const initialData = {
        systemConfiguration: {
          GamingEnabled: {
            iosVersionBlackList: ['6', '7-7.1'],
            hostMenuBlackList: ['www.ladbrokes.com', 'sport/poker']
          }
        },
        sportCategories: [{ categoryId: 160, targetUri: 'fz-football' }]
      };
      service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue(null);
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      deviceService.isWrapper = true;
      deviceService.isIos = true;
      const result = [{ categoryId: 160, targetUri: 'fz-football' }]
      service.getMenuItems('6').subscribe();
      expect(cmsToolsService.processResult).toHaveBeenCalledWith(result);
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
    it('should not set team name for fanzone for other categories based on now and next tab', () => {
      service.getFanzoneSportCategories = jasmine.createSpy('');
      const initialData = {
        systemConfiguration: {
          GamingEnabled: {
            iosVersionBlackList: ['6', '7-7.1'],
            hostMenuBlackList: ['www.ladbrokes.com', 'sport/poker']
          }
        },
        sportCategories: [{ categoryId: 160, targetUri: 'fz-football/everton/now-next' }]
      };
      service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue('everton');
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      deviceService.isWrapper = true;
      deviceService.isIos = true;
      const result = [{ categoryId: 160, targetUri: 'fz-football/everton/now-next' }]
      service.getMenuItems('6', FANZONEDETAILS[0]).subscribe();
      expect(cmsToolsService.processResult).toHaveBeenCalledWith(result);
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
    it('filters if version matches and few domain matches', () => {
      const initialData = {
        systemConfiguration: { GamingEnabled: { iosVersionBlackList: ['6', '7-7.1'], hostMenuBlackList: ['www.ladbrokes.com'] } },
        sportCategories: [{ 'targetUri': 'www.ladbrokes.com' }, { 'targetUri': 'www.coral.co.uk' }]
      };
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      deviceService.isWrapper = true;
      deviceService.isIos = true;
      const result = [{ 'targetUri': 'www.coral.co.uk' }];
      service.getMenuItems('6').subscribe();
      expect(cmsToolsService.processResult).toHaveBeenCalledWith(result);
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
    it('doesnt filters if version doesnt matches', () => {
      const initialData = { systemConfiguration: { GamingEnabled: { iosVersionBlackList: ['6-6.1', '7-7.1'] } }, sportCategories: [] };
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      deviceService.isWrapper = true;
      deviceService.isIos = true;
      service.getMenuItems('6').subscribe();
      expect(cmsToolsService.processResult).toHaveBeenCalledWith(initialData.sportCategories);
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
    it('doesnt filters if version in cms is null or empty', () => {
      const initialData = { systemConfiguration: { GamingEnabled: { iosVersionBlackList: '' } }, sportCategories: [] };
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      deviceService.isWrapper = true;
      deviceService.isIos = true;
      service.getMenuItems('6').subscribe();
      expect(cmsToolsService.processResult).toHaveBeenCalledWith(initialData.sportCategories);
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
    it('doesnt filters if device is not iOS wrapper', () => {
      const initialData = { systemConfiguration: { GamingEnabled: { iosVersionBlackList: '' } }, sportCategories: [] };
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      deviceService.isWrapper = true;
      deviceService.isIos = false;
      service.getMenuItems('6').subscribe();
      expect(cmsToolsService.processResult).toHaveBeenCalledWith(initialData.sportCategories);
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
  });
  describe('getFooterMenu list', () => {
    it('filters if version matches and all domain matches', () => {
      const initialData = {
        systemConfiguration: {
          GamingEnabled: {
            iosVersionBlackList: ['6-6.1', '7-7.1'],
            hostMenuBlackList: ['www.ladbrokes.com', 'sport/poker']
          }
        },
        footerMenu: [{ 'targetUri': 'www.ladbrokes.com' }, { 'targetUri': 'sport/poker' }, { 'targetUri': 'www.ladbrokes123.com' }]
      };
      service.appBuildVersion = '6-6.1';
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      deviceService.isWrapper = true;
      deviceService.isIos = true;
      const result = [{ 'targetUri': 'www.ladbrokes123.com' }];
      service.getFooterMenu('6-6.1').subscribe();
      expect(cmsToolsService.processResult).toHaveBeenCalledWith(result);
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
    it('filters if version matches and few domain matches', () => {
      const initialData = {
        systemConfiguration: { GamingEnabled: { iosVersionBlackList: ['6', '7-7.1'], hostMenuBlackList: ['www.ladbrokes.com'] } },
        footerMenu: [{ 'targetUri': 'www.ladbrokes.com' }, { 'targetUri': 'www.coral.co.uk' }]
      };
      service.appBuildVersion = '6';
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      deviceService.isWrapper = true;
      deviceService.isIos = true;
      const result = [{ 'targetUri': 'www.coral.co.uk' }];
      service.getFooterMenu('6').subscribe();
      expect(cmsToolsService.processResult).toHaveBeenCalledWith(result);
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
    it('doesnt filters if version doesnt matches', () => {
      const initialData = { systemConfiguration: { GamingEnabled: { iosVersionBlackList: ['6-6.1', '7-7.1'] } }, footerMenu: [] };
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      deviceService.isWrapper = true;
      deviceService.isIos = true;
      service.getFooterMenu('6').subscribe();
      expect(cmsToolsService.processResult).toHaveBeenCalledWith(initialData.footerMenu);
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
    it('doesnt filters if version in cms is null or empty', () => {
      const initialData = { systemConfiguration: { GamingEnabled: { iosVersionBlackList: '' } }, footerMenu: [] };
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      deviceService.isWrapper = true;
      deviceService.isIos = true;
      service.getFooterMenu('6').subscribe();
      expect(cmsToolsService.processResult).toHaveBeenCalledWith(initialData.footerMenu);
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
    it('doesnt filters if device is not iOS wrapper', () => {
      const initialData = { systemConfiguration: { GamingEnabled: { iosVersionBlackList: '' } }, footerMenu: [] };
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      deviceService.isWrapper = true;
      deviceService.isIos = false;
      service.getFooterMenu('6').subscribe();
      expect(cmsToolsService.processResult).toHaveBeenCalledWith(initialData.footerMenu);
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
  });
  describe('formArcData', () => {
    it('should formArcData', () => {
      const reason = '3';
      const risk = '4';
      service['getArcData'](reason, risk).subscribe();
      service.formArcData(reason, risk);
      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/arc-profile/${risk}/${reason}`,
        { observe: 'response' }
      );
    })
  });
  describe('@getArcData()', () => {
    it('should call getArcData()', () => {
      const reason = '3';
      const risk = '4';

      service['getArcData'](reason, risk);

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/arc-profile/${risk}/${reason}`,
        { observe: 'response' }
      );
    });
  });

  describe('getCmsCSPInitData', () => {
    beforeEach(() => {
      const initialData = { footerMenu: [] };
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialData));
      service.betpackValidInitialData = jasmine.createSpy('betpackValidInitialData');
    });
    it('calls getCmsInitData for desktop users', () => {
      deviceService.requestPlatform = 'desktop';
      service['getCmsCSPInitData']();
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
    it('calls getCmsInitData if no segment data', () => {
      segmentEventManagerService.getSegmentDetails = jasmine.createSpy('getSegmentDetails').and.returnValue('');
      service['getCmsCSPInitData']();
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
    it('calls getCmsInitData if user is not logged In', () => {
      userService.username = '';
      service['getCmsCSPInitData']();
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
    it('calls getCmsCSPInitData if user is logged In, mobile mode and have segment data', () => {
      segmentEventManagerService.getSegmentDetails = jasmine.createSpy('getSegmentDetails').and.returnValue('segment1');
      segmentEventManagerService.chkModuleForSegmentation = jasmine.createSpy('chkModuleForSegmentation').and.returnValue(true);
      segmentedCMSService.isInitialDataAvailable = jasmine.createSpy('isInitialDataAvailable').and.returnValue(true);
      deviceService.requestPlatform = 'mobile';
      userService.username = 'user1';
      segmentedCMSService.getCmsInitData = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
      service['getCmsCSPInitData']();
      expect(service['getCmsInitData']).not.toHaveBeenCalled();
      expect(service.systemConfiguration).toEqual(initialDataMock.systemConfiguration);
      expect(service.initialData).toEqual(initialDataMock);
    });
    it('calls getCmsCSPInitData if user is logged In, mobile mode and have segment data', () => {
      segmentEventManagerService.getSegmentDetails = jasmine.createSpy('getSegmentDetails').and.returnValue('segment1');
      segmentEventManagerService.chkModuleForSegmentation = jasmine.createSpy('chkModuleForSegmentation').and.returnValue(false);
      segmentedCMSService.getCmsInitData = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
      segmentedCMSService.isInitialDataAvailable = jasmine.createSpy('isInitialDataAvailable').and.returnValue(true);
      service['getCmsCSPInitData']();
      expect(service['getCmsInitData']).toHaveBeenCalled();
    });
    it('calls getCmsCSPInitData if user is logged In, mobile mode and have segment data', () => {
      segmentEventManagerService.getSegmentDetails = jasmine.createSpy('getSegmentDetails').and.returnValue('segment1');
      segmentEventManagerService.chkModuleForSegmentation = jasmine.createSpy('chkModuleForSegmentation').and.returnValue(true);
      segmentedCMSService.getCmsInitData = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
      segmentedCMSService.isInitialDataAvailable = jasmine.createSpy('isInitialDataAvailable').and.returnValue(false);
      service['getCmsCSPInitData']();
      expect(service['getCmsInitData']).toHaveBeenCalled();
    })
  })

  describe('getCouponLeagueLinks', () => {
    let subscribeSpy;
    beforeEach(() => {
      subscribeSpy = jasmine.createSpy('subscribeSpy');
      httpClient.get.and.returnValue(of({ body: [{ couponId: '123' }] }));
    });
    it('should call CMS api', () => {
      service.getCouponLeagueLinks('123').subscribe(subscribeSpy);
      expect(httpClient.get).toHaveBeenCalled();
      expect(subscribeSpy).toHaveBeenCalledWith([{ couponId: '123' }]);
    });
    it('should call CMS api', () => {
      service.getCouponLeagueLinks('123').subscribe(subscribeSpy);
      expect(httpClient.get).toHaveBeenCalled();
      expect(subscribeSpy).toHaveBeenCalledWith([{ couponId: '123' }]);
    });
  });
  describe('@Fanzones Service()', () => {
    it('should call getFanzone', async () => {
      service.getFanzone().subscribe();

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone`,
        { observe: 'response', params: {} }
      );
    })

    it('should call getFanzoneNewSeason', async () => {
      service.getFanzoneNewSeason().subscribe();

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone-new-season`,
        { observe: 'response', params: {} }
      );
    })

    it('should call getFanzoneComingBack', async () => {
      service.getFanzoneComingBack().subscribe();

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone-coming-back`,
        { observe: 'response', params: {} }
      );
    })

    it('should call getFanzoneClubs', async () => {
      service.getFanzoneClubs().subscribe();

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone-club`,
        { observe: 'response', params: {} }
      );
    })

    it('should  get fanzone club data', async () => {
      httpClient.get = jasmine.createSpy().and.returnValue(of({
        body: CLUBDATAMOCK
      }));
      const currentDate = new Date('2022-02-05T08:49:37.177Z').getTime().toString();
      spyOn(window, 'Date').and.returnValue(currentDate);

      service.getFanzoneClubs().subscribe((data) => {
        expect(data).toEqual(CLUBDATA_EQUALMOCK);
      });

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone-club`,
        { observe: 'response', params: {} }
      );
    })

    it('should not get fanzone club data if active is false', async () => {
      httpClient.get = jasmine.createSpy().and.returnValue(of({
        body: CLUBDATA_ACTIVEFALSEMOCK
      }));

      service.getFanzoneClubs().subscribe((data) => {
        expect(data).toEqual([]);
      });

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone-club`,
        { observe: 'response', params: {} }
      );
    })

    it('should not get fanzone club data if active is true but date is not in range', async () => {
      httpClient.get = jasmine.createSpy().and.returnValue(of({
        body: CLUBDATA_ACTIVETRUE_NOT_IN_RANGEMOCK
      }));

      service.getFanzoneClubs().subscribe((data) => {
        expect(data).toEqual([]);
      });

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone-club`,
        { observe: 'response', params: {} }
      );
    })

    it('should not get fanzone club data if active is false and date is not in range', async () => {
      httpClient.get = jasmine.createSpy().and.returnValue(of({
        body: CLUBDATA_ACTIVEFALSE_NOT_IN_RANGEMOCK
      }));

      service.getFanzoneClubs().subscribe((data) => {
        expect(data).toEqual([]);
      });

      expect(httpClient.get).toHaveBeenCalled();
      expect(httpClient.get).toHaveBeenCalledWith(
        `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone-club`,
        { observe: 'response', params: {} }
      );
    })
  });
  describe('getSeoPagesPaths', () => {
    it('should call getSeoPagePaths()', () => {
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
      service.getSeoPagesPaths().subscribe(seodata => {
        expect(service['getCmsInitData']).toHaveBeenCalled();
        expect(seodata).toBe(initialDataMock.seoPages);
      });
    });
  });

  describe('getLottoBanner', () => {
    it('should call getLottoBanner()', () => {
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
      service.getLottoBanner().subscribe(lottoBanner => {
        expect(lottoBanner).toEqual(initialDataMock.lotto);
      })
    })
  });

  describe('getAutoSeoPages', () => {
    it('should call getAutoSeoPagePaths()', () => {
      service['getCmsInitData'] = jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock));
      service.getAutoSeoPages().subscribe(Autoseodata => {
        expect(service['getCmsInitData']).toHaveBeenCalled();
        expect(Autoseodata).toBe(initialDataMock.seoAutoPages);
      });
    });
  });
  describe('betpackValidInitialData', () => {
    it('when sportCategories and FooterMenu is Spliced when BetPack is disabled', () => {
      service['systemConfiguration'] = { BetPack: { enableBetPack: false } };
      const data = { sportCategories: [{ imageTitle: 'BetPack' }], footerMenu: [{ linkTitle: 'BetPack' }] } as any
      service.betpackValidInitialData(data);
    });
    it('when sportCategories and FooterMenu is not Spliced when BetPack is disabled', () => {
      service['systemConfiguration'] = { BetPack: { enableBetPack: false } };
      service.betpackValidInitialData({ sportCategories: [{ imageTitle: '' }], footerMenu: [{ linkTitle: '' }, {}] } as any);

      service.betpackValidInitialData({} as any);
    });
    it('when sportCategories and FooterMenu is not Spliced when BetPack is enabled', () => {
      service['systemConfiguration'] = { BetPack: { enableBetPack: true } };
      const data = { sportCategories: [{ imageTitle: 'BetPack' }], footerMenu: [{ linkTitle: 'BetPack' }] } as any
      service.betpackValidInitialData(data);
    });
    it('when sportCategories and FooterMenu is not Spliced when BetPack is enabled', () => {
      service['systemConfiguration'] = { BetPack: { enableBetPack: true } };
      service.betpackValidInitialData({ sportCategories: [{ imageTitle: '' }], footerMenu: [{ linkTitle: '' }, {}] } as any);

      service.betpackValidInitialData({} as any);
    });
  });
  it('getDesktopQuickLinks', fakeAsync(() => {
    service['getData'] = jasmine.createSpy('getData').and.returnValue(of({ body: [{ title: 'BetPack' }] }));
    service['systemConfiguration'] = { BetPack: { enableBetPack: false } };
    service.getDesktopQuickLinks().subscribe();
    tick(1000);

    service['getData'] = jasmine.createSpy('getData').and.returnValue(of({ body: [{ title: 'BetPack' }] }));
    service['systemConfiguration'] = { BetPack: { enableBetPack: true } };
    service.getDesktopQuickLinks().subscribe();
    tick(1000);

    service['getData'] = jasmine.createSpy('getData').and.returnValue(of({ body: [{ title: '' }] }));
    service['systemConfiguration'] = { BetPack: { enableBetPack: true } };
    service.getDesktopQuickLinks().subscribe();
    tick(1000);

    service['getData'] = jasmine.createSpy('getData').and.returnValue(of({ body: undefined }));
    service['systemConfiguration'] = { BetPack: { enableBetPack: true } };
    service.getDesktopQuickLinks().subscribe();
    tick(1000);
  }));
  it('getHeaderSubMenu', fakeAsync(() => {
    spyOn(service, 'getFanzoneSportCategories');
    service['getData'] = jasmine.createSpy('getData').and.returnValue(of({ body: [{ linkTitle: 'BetPack' }] }));
    service['systemConfiguration'] = { BetPack: { enableBetPack: false } };
    service.getHeaderSubMenu().subscribe();
    tick(1000);

    service['getData'] = jasmine.createSpy('getData').and.returnValue(of({ body: [{ linkTitle: 'BetPack' }] }));
    service['systemConfiguration'] = { BetPack: { enableBetPack: true } };
    service.getHeaderSubMenu().subscribe();
    tick(1000);

    service['getData'] = jasmine.createSpy('getData').and.returnValue(of({ body: [{ linkTitle: '' }] }));
    service['systemConfiguration'] = { BetPack: { enableBetPack: true } };
    service.getHeaderSubMenu().subscribe();
    tick(1000);

    service['getData'] = jasmine.createSpy('getData').and.returnValue(of({}));
    service['systemConfiguration'] = { BetPack: { enableBetPack: true } };
    service.getHeaderSubMenu().subscribe();
    tick(1000);
    expect(service.getFanzoneSportCategories).toHaveBeenCalled();
  }));

  it('should call getFirstBetDetails()', () => {
    service['getData'] = jasmine.createSpy('getData').and.returnValue(of({ body: {} }));
    service.getFirstBetDetails().subscribe(data => {
      expect(service['getData']).toHaveBeenCalled();
      expect(data).toBeDefined;
    });
  });

  describe('#getCMSRGYconfig', () => {
    it('should call getCMSRGYconfig()', () => {
      service['getCMSRGYconfig']('1', '1').subscribe();
      expect(httpClient.get).toHaveBeenCalled();
    });
  });

  describe('#getCMSRGYconfigData', () => {
    it('should not call getCMSYellowFlagInfo when initialRGYData$ is present', () => {
      userService.status = true;
      spyOn(service, 'getCMSYellowFlagInfo');
      service['initialRGYData$'] = new ReplaySubject<any>(1);
      service['getCMSRGYconfigData']();
      expect(service.getCMSYellowFlagInfo).not.toHaveBeenCalled();
    });
    it('should not call service.getCMSYellowFlagInfo when bonus suppression is false', () => {
      userService.status = true;
      spyOn(service, 'getCMSYellowFlagInfo');
      service['initialRGYData$'] = new ReplaySubject<any>(1);
      service['getCMSRGYconfigData']();
      expect(service.getCMSYellowFlagInfo).not.toHaveBeenCalled();
    });
    it('should call service.getCMSYellowFlagInfo when initialRGYData$ is not present', () => {
      userService.status = true;
      userService.getPostLoginBonusSupValue = true;
      userService.getPostLoginBonusSupValue = jasmine.createSpy('getPostLoginBonusSupValue').and.returnValue(true);
      httpClient.get = jasmine.createSpy().and.returnValue(of({
        body: [{ modules: [] }]
      }));
      spyOn(service, 'getCMSYellowFlagInfo');
      service['initialRGYData$'] = null;
      service.cmsYellowFlagInfo = null;
      service['getCMSRGYconfigData']().subscribe();
      expect(service.getCMSYellowFlagInfo).toHaveBeenCalled();
    });
    it('should call service.getCMSYellowFlagInfo when initialRGYData$ is not present', () => {
      userService.status = true;
      service['initialRGYData$'] = null;
      userService.getPostLoginBonusSupValue = jasmine.createSpy('getPostLoginBonusSupValue').and.returnValue(true);
      service.cmsYellowFlagInfo = [];
      service['getCMSRGYconfigData']().subscribe();
      expect(service['initialRGYData$']).not.toBe(null);
    });
    it('should not call service.getCMSYellowFlagInfo when userService status is false', () => {
      userService.status = false;
      service['initialRGYData$'] = new ReplaySubject<any>(1);
      spyOn(service, 'getCMSYellowFlagInfo');
      service['getCMSRGYconfigData']();
      expect(service.getCMSYellowFlagInfo).not.toHaveBeenCalled();
    });
  });

  it('should call getNetworkIndicatorConfig()', () => {
    service.getNetworkIndicatorConfig().subscribe();

    expect(httpClient.get).toHaveBeenCalled();
    expect(httpClient.get).toHaveBeenCalledWith(
      `${environment.CMS_ENDPOINT}/${environment.brand}/network-indicator`,
      { observe: 'response', params: {} }
    );
  });

  it('should call with setCMSYellowFlagInfo with modules', () => {
    service.setCMSYellowFlagInfo([]);
    expect(service.cmsYellowFlagInfo).not.toBe(null);
  });
  it('should return data up on calling getCMSYellowFlagInfo', () => {
    service.cmsYellowFlagInfo = [];
    expect(service.getCMSYellowFlagInfo()).not.toBe(null);
  });
  it('should fetch the data from storage when cmsYellowFlagInfo is null', () => {
    service.cmsYellowFlagInfo = null;
    service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue({ modules: [] });

    expect(service.getCMSYellowFlagInfo()).not.toBe(null);
  });

  it('should fetch the data from storage when cmsYellowFlagInfo is null and storage also has null', () => {
    service.cmsYellowFlagInfo = null;
    service['fanzoneStorageService']['get'] = jasmine.createSpy('get').and.returnValue(null);

    expect(service.getCMSYellowFlagInfo()).toBe(null);
  });
  it('should call fetchBetShareConfigDetails()', () => {
    service['getData'] = jasmine.createSpy('getData').and.returnValue(of({ body: {} }));
    service.fetchBetShareConfigDetails().subscribe(data => {
      expect(service['getData']).toHaveBeenCalled();
      expect(data).toBeDefined;
    });
  });

  it('should check if betShareData is available', () => {
    const betShareData = {
      popUpDesc: 'hello',
      horseRacingUrl: 'Horse race',
      footBallUrl: 'football',
      url5ASide: '5 aside',
    } as any;
    service.betShareData = betShareData;
    expect(service.fetchBetShareConfigDetails()).toEqual(betShareData);
  })
  describe('#getQuickStakes', () => {
    it('should call getQuickStakes()', () => {
      service.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of(initialDataMock))
      service.getQuickStakes('quick_bet').subscribe(data=>{
        expect(data).toEqual(['1', '2', '3', '4']);
      })
    });
    it('should call getQuickStakes()', () => {
      service.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of(initialDataMock))
      service.getQuickStakes('test').subscribe(data=>{
        expect(data).toEqual(['10', '20', '30', '40']);
      })
    });
    it('should call getQuickStakes()', () => {
      const config = {
        PredefinedStakes : {
          global_stakes : '10,20,40'
        }
      }
      service.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(of(config))
      service.getQuickStakes('test').subscribe(data=>{
        expect(data).toEqual(['10','20','40']);
      })
    });
  });
});
