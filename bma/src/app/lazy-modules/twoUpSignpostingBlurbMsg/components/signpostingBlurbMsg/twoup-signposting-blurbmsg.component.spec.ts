import { of } from "rxjs";
import { TwoUpSignPostingBlurbMsgComponent } from "./twoup-signposting-blurbmsg.component";
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('TwoUpSignPostingBlurbMsgComponent', () => {
  let component: TwoUpSignPostingBlurbMsgComponent;
  let localeService,
  cmsService, existNewUserService, gtm, pubSubService;

  const mockData = {marketName:'2Up',action:'open',eventName:'test event'};
  beforeEach(() => {
    cmsService = {
      getSignpostingPromotionsLight: jasmine.createSpy('getSignpostingPromotionsLight').and.returnValue(of({templateMarketName: '2Up - Instant Win',blurbMessage: 'test'}))
    }
    localeService = {
      getString: jasmine.createSpy('locale.getString').and.returnValue('2Up - Instant Win')
    };
    existNewUserService = {
      filterExistNewUserItems: jasmine.createSpy('filterExistNewUserItems').and.returnValue([{templateMarketName:'2Up - Instant Win'}])
    };
    gtm = {
      push: jasmine.createSpy('push')
    };
    pubSubService = {
      cbMap : {},
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriber, method, handler) => {
        if (method === 'TWO_UP_TRACKING') {
          handler(mockData);
        }
      }),
      API: pubSubApi
    } as any;
    component = new TwoUpSignPostingBlurbMsgComponent(cmsService, localeService, existNewUserService, gtm, pubSubService);
    component.marketName = '2Up - Instant Win'
  });

  it('should create', () => {
    component.ngOnInit();
    expect(component).toBeTruthy();
    expect(localeService.getString).toHaveBeenCalled();
  });

  it('should create with diff action', () => {
    component.gtaEventName = 'test data';
    const mockData = {marketName:'2Up',action:'closed',eventName:''};
    pubSubService.subscribe.and.callFake((subscriber, method, handler) => {
      if (method === 'TWO_UP_TRACKING') {
        handler(mockData);
      }
    }),
    component.ngOnInit();
    expect(gtm.push).toHaveBeenCalled();
    expect(component.marketName).toEqual(component.twoUpMarketPromotionData.templateMarketName);
  });

});
