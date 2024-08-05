import { LazyPromotionIconsComponent } from './lazy-promotion-icons.component';
import { of as observableOf } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { SECTION_TYPE } from '@promotions/constants/promotion-description';
import { DRILLDOWNTAGNAMES } from '@promotions/constants/tag-names-config.constant';

describe('#LazyPromotionIconsComponent', () => {
  let cmsService,
      pubSubService,
      promotionsService,
      coreToolsService,
      commandService,
      changeDetectorRef,
      device;
  let component: LazyPromotionIconsComponent;
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
          iconId: '#EPR_ICON'
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
      markForCheck: jasmine.createSpy('markForCheck')
    };
    device = {
      isMobile: jasmine.createSpy().and.returnValue(false)
    };

    component = new LazyPromotionIconsComponent(
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


  describe('#ngOnInit', () => {
    beforeEach(() => {
      component['updateIconsCount'] = jasmine.createSpy();
      component['checkBybIcon'] = jasmine.createSpy('checkBybIcon').and.returnValue(observableOf(true));
      component.marketName = markets[1];
      component.type = SECTION_TYPE.MARKET;
      component.eventDrillDownTags = `${DRILLDOWNTAGNAMES.HR_BIR},`;
    });

    it('BIR changes', () => {
      component.isLazyBIRSignpost = true;
      component.isHeaderBIRAvailable = true;
      component.showBIRSignPost = true;
      component.ngOnInit();

      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(component['isBIRAvailable']).toBeTrue();
      expect(component['isDisplayBIRSignpost']).toBeTrue();
      expect(component['updateIconsCount']).toHaveBeenCalledWith(1);
    });
    it('BIR changes and isHeaderBIRAvailable is false and eventDrillDownTags is null', () => {
      component.isLazyBIRSignpost = true;
      component.isHeaderBIRAvailable = false;
      component.display = 'EVFLAG_EPR,,,,EVFLAG_FIN,EVFLAG_IHR';
      component.eventDrillDownTags = null;
      component.showBIRSignPost = true;
      component.ngOnInit();

      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(component['isBIRAvailable']).toBeTrue();
      expect(component['isDisplayBIRSignpost']).toBeTrue();
      expect(component['updateIconsCount']).toHaveBeenCalledWith(1);
    });
    it('BIR changes - undefined marketName', () => {
      component.isLazyBIRSignpost = true;
      component.isHeaderBIRAvailable = true;
      component.showBIRSignPost = true;
      component.marketName = undefined;
      component.ngOnInit();

      expect(component['isDisplayBIRSignpost']).toBeFalsy();
      expect(component['updateIconsCount']).not.toHaveBeenCalledTimes(3);
    });

    it('BIR changes - null marketName', () => {
      component.isLazyBIRSignpost = true;
      component.isHeaderBIRAvailable = true;
      component.showBIRSignPost = true;
      component.marketName = null;
      component.ngOnInit();

      expect(component['isDisplayBIRSignpost']).toBeFalsy();
      expect(component['updateIconsCount']).not.toHaveBeenCalledTimes(3);
    });

    it('BIR changes - null config', () => {
      component.isLazyBIRSignpost = true;
      component.isHeaderBIRAvailable = true;
      component.showBIRSignPost = true;
      cmsService.getSystemConfig.and.returnValue(observableOf(null));

      component.ngOnInit();

      expect(component['isDisplayBIRSignpost']).toBeFalsy();
      expect(component['updateIconsCount']).not.toHaveBeenCalledTimes(3);
    });

    it('BIR changes - undefined config', () => {
      component.isLazyBIRSignpost = true;
      component.isHeaderBIRAvailable = true;
      component.showBIRSignPost = true;
      cmsService.getSystemConfig.and.returnValue(observableOf());

      component.ngOnInit();

      expect(component['isDisplayBIRSignpost']).toBeFalsy();
      expect(component['updateIconsCount']).not.toHaveBeenCalledTimes(3);
    });

    it('BIR changes - null config horseracing', () => {
      component.isLazyBIRSignpost = true;
      component.isHeaderBIRAvailable = true;
      component.showBIRSignPost = true;
      const config = { ...systemConfig };
      config.HorseRacingBIR = null;
      cmsService.getSystemConfig.and.returnValue(observableOf(config));

      component.ngOnInit();

      expect(component['isDisplayBIRSignpost']).toBeFalsy();
      expect(component['updateIconsCount']).not.toHaveBeenCalledTimes(3);
    });

    it('BIR changes - undefined config horseracing', () => {
      component.isLazyBIRSignpost = true;
      component.isHeaderBIRAvailable = true;
      component.showBIRSignPost = true;
      cmsService.getSystemConfig.and.returnValue(observableOf({}));

      component.ngOnInit();

      expect(component['isDisplayBIRSignpost']).toBeFalsy();
      expect(component['updateIconsCount']).not.toHaveBeenCalledTimes(3);
    });

    it('BIR changes - null config marketsEnabled', () => {
      component.isLazyBIRSignpost = true;
      component.isHeaderBIRAvailable = true;
      component.showBIRSignPost = true;
      const config = { ...systemConfig };
      config.HorseRacingBIR.marketsEnabled = null;
      cmsService.getSystemConfig.and.returnValue(observableOf(config));

      component.ngOnInit();

      expect(component['isDisplayBIRSignpost']).toBeFalsy();
      expect(component['updateIconsCount']).not.toHaveBeenCalledTimes(3);
    });

    it('BIR changes - undefined config marketsEnabled', () => {
      component.isLazyBIRSignpost = true;
      component.isHeaderBIRAvailable = true;
      component.showBIRSignPost = true;
      const config = { ...systemConfig };
      config.HorseRacingBIR = {};
      cmsService.getSystemConfig.and.returnValue(observableOf(config));

      component.ngOnInit();

      expect(component['isDisplayBIRSignpost']).toBeFalsy();
      expect(component['updateIconsCount']).not.toHaveBeenCalledTimes(3);
    });
  });
});