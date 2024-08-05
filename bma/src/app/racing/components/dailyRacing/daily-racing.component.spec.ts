import { DailyRacingModuleComponent } from '@racing/components/dailyRacing/daily-racing.component';
import { BehaviorSubject } from 'rxjs/internal/BehaviorSubject';

describe('DailyRacingModuleComponent', () => {
  let component: DailyRacingModuleComponent;
  let routingHelperService,
    filterService, vEPService;

  beforeEach(() => {
    routingHelperService = {
      formEdpUrl: jasmine.createSpy()
    };
    filterService = {
      orderBy: jasmine.createSpy().and.callFake((...args) => args[0])
    };

    vEPService = {
      bannerBeforeAccorditionHeader:  new BehaviorSubject<any>('bannerBeforeAccorditionHeader' as any),
      targetTab:  new BehaviorSubject<any>('targetTab' as any),
    };
    component = new DailyRacingModuleComponent(routingHelperService, filterService, vEPService);
  });

  it('should test ngOnInit', () => {
    const resultMock = [{
      sectionName: 'section1',
      events: ['1']
    }];
    component.eventsBySections = {
      section1: ['1']
    } as any;
    component.ngOnInit();
    expect(filterService.orderBy).toHaveBeenCalledWith(['1'], ['startTime', 'name']);
    expect(component.filteredEventsBySection).toEqual(resultMock as any);
  });

  it('should test formEdpUrl', () => {
    component.formEdpUrl('test' as any);
    expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith('test');
  });

  it('should test trackByIndex', () => {
    component.formEdpUrl('test' as any);
    expect(component.trackByIndex(1)).toEqual(1);
  });

  describe('isDisplayBanner', () => {
    it('isDisplayBanner', () => {
      component.bannerBeforeAccorditionHeader = 'test'
      const retVal = component.isDisplayBanner('test');
      expect(retVal).toBeTruthy();
    })

    it('isDisplayBanner', () => {
      component.bannerBeforeAccorditionHeader = undefined;
      const retVal = component.isDisplayBanner(undefined);
      expect(retVal).toBeTruthy();
    })
  })
});
