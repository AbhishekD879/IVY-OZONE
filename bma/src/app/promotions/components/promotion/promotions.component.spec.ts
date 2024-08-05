import { PromotionsComponent } from '@promotions/components/promotion/promotions.component';
import { of } from 'rxjs';
import PROMOTIONS_TABS, {
  ID_TAB_PROMOTION_ALL,
  ID_TAB_PROMOTION_CONNECT
} from '@promotions/constants/promotion-tabs.constant';

describe('PromotionsComponent', () => {
  let component: PromotionsComponent,
    cmsService;

  beforeEach(() => {
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig')
    };

    component = new PromotionsComponent(cmsService);
  });

  it('constructor', () => {
    expect(component.title).toEqual('Promotions');
  });

  describe('ngOnInit', () => {
    it('should set all promotionTabs and ID_TAB_PROMOTION_ALL id for promotionActiveTab', () => {
      cmsService.getSystemConfig.and.returnValue(of({
        Connect: {
          promotions: true
        }
      }));

      component.ngOnInit();

      expect(component.promotionTabs).toEqual(PROMOTIONS_TABS);
      expect(component.promotionActiveTab).toEqual({ id: ID_TAB_PROMOTION_ALL });
    });

    it('should set first promotionTab and ID_TAB_PROMOTION_CONNECT id for promotionActiveTab', () => {
      component.isRetail = true;
      cmsService.getSystemConfig.and.returnValue(of({ Connect: {} }));

      component.ngOnInit();

      expect(component.promotionTabs).toEqual([PROMOTIONS_TABS[0]]);
      expect(component.promotionActiveTab).toEqual({ id: ID_TAB_PROMOTION_CONNECT });
    });

    afterEach(() => {
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
    });
  });
});
