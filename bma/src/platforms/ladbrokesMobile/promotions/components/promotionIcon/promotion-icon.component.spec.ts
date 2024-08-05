import { PromotionIconComponent } from './promotion-icon.component';
import { of as observableOf } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('PromotionIconComponent', () => {
  let component: PromotionIconComponent;
  let cmsService,
      promotionsService,
      pubSubService,
      coreToolsService,
      commandService,
      changeDetectorRef,
      device;
  
    beforeEach(() => {
    cmsService = {
      getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(observableOf(true))
    };
    promotionsService = {
      getSpPromotionData: jasmine.createSpy().and.returnValue(observableOf([
        {
          eventLevelFlag: 'EVFLAG_EPR',
          iconId: '#EPR_ICON'
        },
        {
          eventLevelFlag: 'EVFLAG_FIN'
        }
      ]))
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    coreToolsService = {
      uuid: () => '1234'
    };
    commandService = {};
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
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
  });
  it('should create PromotionIconComponent instance', () => {
    expect(component).toBeTruthy();
  });

  it('should turn off BYB for Ladbrokes', () => {
    component.ngOnInit();
    expect(component.buildYourBetAvailable).toBe(false);
  });
});
