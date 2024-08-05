import { of as observableOf, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { PromotionIconComponent } from '@promotions/components/promotionIcon/promotion-icon.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { SECTION_TYPE } from '@promotions/constants/promotion-description';
import { DRILLDOWNTAGNAMES } from '@promotions/constants/tag-names-config.constant';

describe('PromoLabelsComponent', () => {
  let cmsService;
  let promotionsService;
  let pubSubService;
  let coreToolsService;
  let component: PromotionIconComponent;
  let commandService;
  let changeDetectorRef;
  let device;
  const markets = ['M1', 'M2'];
  const systemConfig: any = { HorseRacingBIR: { marketsEnabled: markets, inplaySignpostEnabled: true } };

  beforeEach(() => {
    cmsService = {
      getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(observableOf(true)),
      isBogFromCms: jasmine.createSpy('isBogFromCms').and.returnValue(observableOf(true)),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf(systemConfig)),
    };
    promotionsService = {
      getSpPromotionData: jasmine.createSpy().and.returnValue(observableOf([
        {
          eventLevelFlag: 'EVFLAG_EPR',
          iconId: '#EPR_ICON',
          marketName: 'Match Result'
        },
        {
          eventLevelFlag: 'EVFLAG_FIN'
        },
        {
          eventLevelFlag: 'EVFLAG_IHR',
          title: 'Bet in Inplay'
        }
      ])),
      openPromotionDialog: jasmine.createSpy(),
      trackBogDialog: jasmine.createSpy(),
      trackSignPosting: jasmine.createSpy()
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),   
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    coreToolsService = {
      uuid: () => '1234'
    };
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve({})),
      API: {
        DS_WHEN_YC_READY: 'DS_WHEN_YC_READY',
        DS_IS_AVAILABLE_FOR_COMPETITION: 'DS_IS_AVAILABLE_FOR_COMPETITION',
        DS_IS_AVAILABLE_FOR_EVENTS: 'DS_IS_AVAILABLE_FOR_EVENTS'
      }
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy('detectChanges')
    };
    device = {
      isMobile: jasmine.createSpy().and.returnValue(false)
    };
    component = new PromotionIconComponent(
      cmsService,
      promotionsService,
      pubSubService,
      coreToolsService,
      commandService,
      changeDetectorRef,
      device
    );
    component.display = 'EVFLAG_EPR,,,,EVFLAG_FIN';
    component.type = 'event';
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  describe('processFlags', () => {
    it('should initialize promoIcons property with icons' +
      ' with promoIcons which have iconId', fakeAsync(() => {
      spyOn(component.setPromotionIconStatus, 'emit');
      component.isHeaderBIRAvailable = true;
      component.showBIRSignPost = true;
      component['BIR_PromoIcon'] = {
        eventLevelFlag: 'EVFLAG_IHR',
        title: 'Bet in Inplay'
      } as any;
      component['processFlags']();
      tick();

      expect(component.promoIcons.length).toEqual(1);
      expect(component.setPromotionIconStatus.emit).toHaveBeenCalledWith(true);
    }));
    it('should assign BIR_PromoIcon', () => {
      promotionsService.getSpPromotionData.and.returnValue(observableOf([
        {
          eventLevelFlag: 'EVFLAG_IHR',
          title: 'Bet in Inplay'
        }]));
      component['processFlags']();
      component.isHeaderBIRAvailable = true;
      component.showBIRSignPost = true;
      expect(component['BIR_PromoIcon']).toBeDefined();
      expect(component['BIR_PromoIcon']).toEqual({
        eventLevelFlag: 'EVFLAG_IHR',
        title: 'Bet in Inplay'
      } as any);
    });
  });

  describe('#ngOnInit', () => {
    beforeEach(() => {
      component['updateIconsCount'] = jasmine.createSpy();
      component['checkBybIcon'] = jasmine.createSpy('checkBybIcon').and.returnValue(observableOf(true));
      component.marketName = markets[1];
      component.type = SECTION_TYPE.MARKET;
      component.eventDrillDownTags = `${DRILLDOWNTAGNAMES.HR_BIR},`;
    });

    it('should update icons count if cahsout is available', () => {
      component.cashoutAvailable = true;

      component.ngOnInit();

      expect(component['updateIconsCount']).toHaveBeenCalledWith(1);
    });

    it('should return if toggle status of false', () => {
      component['processFlags'] = jasmine.createSpy('processFlags');
      component['cmsService'].getToggleStatus = jasmine.createSpy('getToggleStatus').and.returnValue(observableOf(false));

      component.ngOnInit();

      expect(component['processFlags']).not.toHaveBeenCalledTimes(2);
      expect(pubSubService.subscribe)
        .not
        .toHaveBeenCalledWith('PromotionIconComponent1234', 'SESSION_LOGIN', jasmine.any(Function));
    });

    it('should call subscribe for SESSION_LOGIN', () => {
      let callback;

      pubSubService.subscribe.and.callFake((name: string, apis: string[], cb) => callback = cb);
      component['processFlags'] = jasmine.createSpy('processFlags');

      component.ngOnInit();

      callback && callback();

      expect(component['processFlags']).toHaveBeenCalledTimes(2);
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith('PromotionIconComponent1234', 'SESSION_LOGIN', jasmine.any(Function));
    });

    it('should set isFlagChecked true', () => {
      const componentName = `PromotionIconComponent${ coreToolsService.uuid() }`;

      component.ngOnInit();

      expect(component.isFlagChecked).toBe(true);
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith(componentName, pubSubService.API.SESSION_LOGIN, jasmine.any(Function));
      expect(changeDetectorRef.markForCheck).toHaveBeenCalledTimes(2);
    });

    it('should not set isFlagChecked true in case of error', () => {
      component['cmsService'].getToggleStatus = jasmine.createSpy('getToggleStatus').and.returnValue(throwError('error'));
      component.ngOnInit();

      expect(component.isFlagChecked).toBe(false);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalledTimes(1);
    });

    it('should set buildYourBetAvailable', () => {
      component.ngOnInit();

      expect(component.buildYourBetAvailable).toBe(true);
      expect(component['updateIconsCount']).toHaveBeenCalled();
      expect(component.isBYBChecked).toBe(true);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalledTimes(2);
    });

    it('should not call updateIconsCount if buildYourBetAvailable is false', () => {
      component['checkBybIcon'] = jasmine.createSpy('checkBybIcon').and.returnValue(observableOf(false));
      component['processFlags'] = jasmine.createSpy();
      component.ngOnInit();

      expect(component.isBYBChecked).toBe(true);
      expect(component['updateIconsCount']).not.toHaveBeenCalledTimes(2);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalledTimes(2);
    });

    it('should not set isBYBChecked to true in case of error', () => {
      component['checkBybIcon'] = jasmine.createSpy('checkBybIcon').and.returnValue(throwError('error'));
      component.ngOnInit();

      expect(component.isBYBChecked).toBe(false);
    });

    it('case when buildYourBetAvailable is defined', () => {
      component.buildYourBetAvailable = true;
      component.typeId = 123;
      component.ngOnInit();

      expect(component.isBYBChecked).toBe(true);
    });

    it('case when typeId is not defined', () => {
      component.buildYourBetAvailable = undefined;
      component.typeId = undefined;
      component.ngOnInit();

      expect(component.isBYBChecked).toBe(true);
    });
  });

  describe('#checkBybIcon', () => {
    it('should return Byb value',  (done) =>  {
      component.buildYourBetAvailable = false;
      component['updateIconsCount'] = jasmine.createSpy('updateIconsCount');

      component.checkBybIcon().subscribe((data: boolean) => {
        expect(data).toBeFalsy();
        expect(component['updateIconsCount']).not.toHaveBeenCalledTimes(3);
        done();
      });
    });

    it('should return Byb value and update icons count',  (done) =>  {
      component.buildYourBetAvailable = true;
      component['updateIconsCount'] = jasmine.createSpy('updateIconsCount');

      component.checkBybIcon().subscribe((data: boolean) => {
        expect(data).toBeTruthy();
        expect(component['updateIconsCount']).toHaveBeenCalledWith(1);
        done();
      });
    });

    it('should call executeAsync two times with relevant parameters for competition', fakeAsync(() => {
      component.buildYourBetAvailable = undefined;
      component.eventId = undefined;
      component.typeId = 123;

      component.checkBybIcon().subscribe();
      tick();

      expect(commandService.executeAsync)
        .toHaveBeenCalledWith(commandService.API.DS_WHEN_YC_READY, [ 'isEnabledYCIcon', true ], {});
      expect(commandService.executeAsync)
        .toHaveBeenCalledWith(commandService.API.DS_IS_AVAILABLE_FOR_COMPETITION, [component.typeId], {});
    }));

    it('should call executeAsync two times with relevant parameters for events', fakeAsync(() => {
      component.buildYourBetAvailable = undefined;
      component.typeId = 123;
      component.eventId = 12;

      component.checkBybIcon().subscribe();
      tick();

      expect(commandService.executeAsync)
        .toHaveBeenCalledWith(commandService.API.DS_WHEN_YC_READY, [ 'isEnabledYCIcon', true ], {});
      expect(commandService.executeAsync)
        .toHaveBeenCalledWith(commandService.API.DS_IS_AVAILABLE_FOR_EVENTS, [component.eventId], {});
    }));
  });

  describe('ngOnDestroy', () => {
    it('should unsync and unsubscribe from events if isPromoSignpostingEnabled', () => {
      const componentName = `PromotionIconComponent${coreToolsService.uuid()}`;

      component.isPromoSignpostingEnabled = true;

      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith(componentName);
    });

    it('should not unsync and unsubscribe from events if no isPromoSignpostingEnabled', () => {
      component.isPromoSignpostingEnabled = false;

      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).not.toHaveBeenCalled();
    });
  });

  it('iconAction should open promotion dialog', () => {
    const event = {
        preventDefault: jasmine.createSpy('preventDefault'),
        stopPropagation: jasmine.createSpy('stopPropagation')
      } as any,
      icon = {
        templateMarketName: 'customTypeLevelFlag',
        customTypeLevelFlag: 'test1'
      } as any,
    flag :string ='test'
    component.accordionTitle = 'test';
    component.marketName = 'test';
    component.type = 'customType';
    component['promotionsService'].openPromotionDialog = jasmine.createSpy('openPromotionDialog');
    component.iconAction(event, icon, flag);

    expect(event.stopPropagation).toHaveBeenCalled();
    expect(event.preventDefault).toHaveBeenCalled();
  });
  it('iconAction should call promotionsService.trackSignPosting if all conditions are statisfied', () => {
    const event = {
      preventDefault: jasmine.createSpy('preventDefault'),
      stopPropagation: jasmine.createSpy('stopPropagation')
    } as any,
      icon = {
        customTypeLevelFlag: 'EVFLAG_IHR',
        title: 'Bet in Inplay',
        marketLevelFlag: null
      } as any;
    component.iconAction(event, icon, 'EVFLAG_IHR');
    expect(promotionsService.trackSignPosting).toHaveBeenCalledOnceWith(icon.title, 'EVFLAG_IHR', icon.marketLevelFlag);
  });
  it('iconAction should not call promotionsService.trackSignPosting if all conditions are not statisfied', () => {
    const event = {
      preventDefault: jasmine.createSpy('preventDefault'),
      stopPropagation: jasmine.createSpy('stopPropagation')
    } as any,
      icon = {
        title: 'Bet in Inplay'
      } as any;
    component.iconAction(event, icon);
    expect(promotionsService.trackSignPosting).not.toHaveBeenCalledOnceWith(icon.title, 'EVFLAG_IHR', null);
  });
  it('iconAction should not call promotionsService.trackSignPosting if is flag is not in gatrackingconfig', () => {
    const event = {
      preventDefault: jasmine.createSpy('preventDefault'),
      stopPropagation: jasmine.createSpy('stopPropagation')
    } as any,
      icon = {
        customTypeLevelFlag: 'EVFLAG',
        title: 'Bet in Inplay'
      } as any;
    component.iconAction(event, icon);
    expect(promotionsService.trackSignPosting).not.toHaveBeenCalledOnceWith(icon.title, 'EVFLAG_IHR', null);
  });
  it('trackByPromoIcon should return promo icon index', () => {
    const item = { flagName: 'flagName', iconId: 'iconId', promoKey: 'promoKey' } as any;

    expect(component.trackByPromoIcon(1, item)).toEqual('1flagNameiconIdpromoKey');
  });

  describe('Tests for BOG', () => {
    it('should check isBogCmsEnabled when isGpAvailable = undefined', () => {
      component.isGpAvailable = undefined;
      expect(cmsService.isBogFromCms).not.toHaveBeenCalled();
    });

    it('should check isBogCmsEnabled when isGpAvailable = false', () => {
      component.isGpAvailable = false;
      expect(cmsService.isBogFromCms).not.toHaveBeenCalled();
    });

    it('should check isBogCmsEnabled when isGpAvailable = true', () => {
      component.isGpAvailable = true;
      component['cmsService'].isBogFromCms = jasmine.createSpy('isBogFromCms').and.returnValue(observableOf(true));
      component.signPost = ['#two-up'];
      component.ngOnInit();
      expect(component.isBogCmsEnabled).toBe(true);
    });

    it('should check isBogCmsEnabled when isGpAvailable = true and isBogFromCms = false', () => {
      component.isGpAvailable = true;
      component['cmsService'].isBogFromCms = jasmine.createSpy('isBogFromCms').and.returnValue(observableOf(false));
      component.ngOnInit();
      expect(component.isBogCmsEnabled).toBe(false);
    });

    it('should call bogAction()', () => {
      const event = {
        stopPropagation: jasmine.createSpy('stopPropagation'),
        preventDefault: jasmine.createSpy('preventDefault')
      } as any;
      component['promotionsService'].openPromotionDialog = jasmine.createSpy('openPromotionDialog');
      component['promotionsService'].trackBogDialog = jasmine.createSpy('trackBogDialog');
      component.bogAction(event);

      expect(event.stopPropagation).toHaveBeenCalledTimes(1);
      expect(event.preventDefault).toHaveBeenCalledTimes(1);
      expect(component['promotionsService'].openPromotionDialog).toHaveBeenCalled();
      expect( component['promotionsService'].trackBogDialog).toHaveBeenCalledWith('MKTFLAG_BOG', 'ok');
    });
  });

  describe('updateIconsCount', () => {
    it('should update icons count and do not change mode', () => {
      component['updateIconsCount'](1);

      expect(component.iconsCount).toEqual(1);
      expect(component.mode).toEqual('md');
    });

    it('should update icons count and change mode', () => {
      component.mode = 'sm';

      component['updateIconsCount'](2);

      expect(component.iconsCount).toEqual(2);
      expect(component.mode).toEqual('mini');
    });

    it('should update signpost status when greater then 2', () => {
      component.type = 'market';
      component.iconsCount=3;
      component.accordionTitle='#YourCall - Real Madrid Player Shots Outside Box';
      component.sport='sport';
      component.signPost=['cashoutAvailable','priceboost']
      component['updateIconsCount'](3);

      expect(component.singleSignPost).toEqual(true);
      expect(component.mulSignPosts).toEqual(false);
      expect(component.signpostIconDisplay).toEqual(component.signPost[1]);
      
    });
    it('should get the signpostIconDisplay first icon', () => {
      component.type = 'market';
      component.iconsCount=3;
      component.accordionTitle='#YourCall - Real Madrid Player Shots Outside Box';
      component.sport='sport';
      component.signPost=['extraspace','priceboost']
      component['updateIconsCount'](3);

      expect(component.singleSignPost).toEqual(true);
      expect(component.mulSignPosts).toEqual(false);
      expect(component.signpostIconDisplay).toEqual(component.signPost[0]);
      
    });

    it('iconAction should open promotion custom dialog', () => {
      const event = {
          preventDefault: jasmine.createSpy('preventDefault'),
          stopPropagation: jasmine.createSpy('stopPropagation')
        } as any,
        icon = {
          templateMarketName: 'test data',
          customTypeLevelFlag: 'test flag'
        } as any;
        component['promotionsService'].openPromotionDialog = jasmine.createSpy('openPromotionDialog');
        
        component.accordionTitle='test data';
        component.marketName = 'test data';
        component.type = 'customType';
        component.iconAction(event, icon);
        expect(event.stopPropagation).toHaveBeenCalled();
        expect(event.preventDefault).toHaveBeenCalled();
    });

    it('should call markForCheck after count updated', () => {
      component.iconsCount = 5;
      component['updateIconsCount'](5);

      expect(component.iconsCount).toBe(10);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });
  });

 describe('mulSignPostsClick', () => {
    it('should change the status of signpost and multisignpost and signflag', () => {
      const event = {
        stopPropagation: jasmine.createSpy('stopPropagation'),
        preventDefault: jasmine.createSpy('preventDefault')
      } as any;
      component['mulSignPostsClick'](event);
      expect(component.singleSignPost).toEqual(false);
      expect(component.mulSignPosts).toEqual(true);
      expect(component.signflag).toEqual(false);
      
    });
    
  });


  describe('signPostFilter', () => {
    it('should get the filtered signposts ', () => {
      const event = {
        stopPropagation: jasmine.createSpy('stopPropagation'),
        preventDefault: jasmine.createSpy('preventDefault')
      } as any;
      //component.signpostIconDisplay=undefined;
      component.signpostIconDisplay='cashoutAvailable';
      component['mulSignPostsClick'](event);
      expect(component.signPostFilteredObj).toEqual([]);
    });
    it('should get the filtered signposts ', () => {
      const event = {
        stopPropagation: jasmine.createSpy('stopPropagation'),
        preventDefault: jasmine.createSpy('preventDefault')
      } as any;
      //component.signpostIconDisplay=undefined;
      component.signpostIconDisplay='buildYourBetAvailable'; 
      component['mulSignPostsClick'](event);
      expect(component.signPostFilteredObj).toEqual([]);
    });
    it('should get the filtered signposts ', () => {
      const event = {
        stopPropagation: jasmine.createSpy('stopPropagation'),
        preventDefault: jasmine.createSpy('preventDefault')
      } as any;
     // component.signpostIconDisplay=undefined;
      component.signpostIconDisplay='isGpAvailable'; 
      component['mulSignPostsClick'](event);
      expect(component.signPostFilteredObj).toEqual([]);
    });
    it('should get the filtered signposts ', () => {
      const event = {
        stopPropagation: jasmine.createSpy('stopPropagation'),
        preventDefault: jasmine.createSpy('preventDefault')
      } as any;
      component.signpostIconDisplay=undefined;
      component['mulSignPostsClick'](event);
      expect(component.signPostFilteredObj).toEqual([]);
    });
    it('should get the filtered signposts ', () => {
    const promoIcons=[{
      iconId:'oddsBoost'
    }]
    const event = {
      stopPropagation: jasmine.createSpy('stopPropagation'),
      preventDefault: jasmine.createSpy('preventDefault')
    } as any;
    component.signpostIconDisplay='oddsBoost';
    expect(component.signPostFilteredObj).withContext('oddsBoost'); 
    });
  });
  describe('#lazyPromotionComponentLoaded', () => {
    it('should call changeDetectorRef.markForCheck', () => {
      component.lazyPromotionComponentLoaded();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });
  });
  describe('#handleLazyPromotionIconEvent', () => {
    it('should call updateIconsCount', () => {
      const event = { output: 'iconCountUpdated', value: '1' } as any
      spyOn(component as any, 'updateIconsCount')
      component.handleLazyPromotionIconEvent(event);
      expect(component['updateIconsCount']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should not call updateIconsCount', () => {
      const event = { output: 'test-string', value: '1' } as any
      spyOn(component as any, 'updateIconsCount')
      component.handleLazyPromotionIconEvent(event);
      expect(component['updateIconsCount']).not.toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
    });
  });
});
