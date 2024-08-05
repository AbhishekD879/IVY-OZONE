import { MaxpayoutErrorContainerComponent } from './maxpayout-error-container.component';
import { of } from 'rxjs';

describe('MaxpayoutErrorContainerComponent', () => {
  let component: MaxpayoutErrorContainerComponent, gtmService, cmsService;
  beforeEach(() => {
    gtmService = {
      push: jasmine.createSpy()
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        maxPayOut: {
          link: 'https:// coral.co.uk/',
          click: 'here'
        }
      }))
    };
    component = new MaxpayoutErrorContainerComponent(cmsService, gtmService);
    component.errorMsg = 'Test message';
    component.betType = 'quick bet';
  });
  it('should create', () => {
    expect(component).toBeTruthy();
  });
  describe('ngOnInit', () => {
    beforeEach(() => {
      spyOn(component, 'sendGtmData');
    });
    it('should not call sendGtmData', () => {
      component.betType = 'my bets';
      component.ngOnInit();
      expect(component.sendGtmData).not.toHaveBeenCalled();
    });
    it('should call sendGtmData', () => {
      component.ngOnInit();
      expect(component.sendGtmData).toHaveBeenCalled();
    });
  });
  describe('sendGtmData', () => {
    it('is gtmService push called', () => {
      const gtmData = {
        event: 'trackEvent',
        eventAction: 'rendered',
        eventCategory: 'maximum returns',
        eventLabel: component.betType
      };
      component.sendGtmData('rendered');
      expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);
    });
  });
  describe('expanded', () => {
    beforeEach(() => {
      spyOn(component as any, 'sendGtmData');
    });
    it('should not call sendGtmData when betType is betslip', () => {
      component.betType = 'betslip';
      component.expanded();
      expect(component.sendGtmData).not.toHaveBeenCalled();
    });
    it('should not call sendGtmData when betType is quick bet', () => {
      component.expanded();
      expect(component.sendGtmData).not.toHaveBeenCalled();
    });
    it('should call sendGtmData when betType is bet reciept', () => {
      component.betType = 'bet receipt';
      component.expanded();
      expect(component.sendGtmData).toHaveBeenCalled();
    });
    it('should call sendGtmData when betType is my bets', () => {
      component.betType = 'my bets';
      component.expanded();
      expect(component.sendGtmData).toHaveBeenCalled();
    });
  });

  it('cms with undefined', () => {
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({}))
    };
    component = new MaxpayoutErrorContainerComponent(cmsService, gtmService);
  });
  it('cms with null', () => {
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of(null))
    };
    component = new MaxpayoutErrorContainerComponent(cmsService, gtmService);
  });
});
