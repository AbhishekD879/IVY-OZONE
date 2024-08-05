import {
  LadbrokesMobileRacingSpecialsTabComponent
} from '@ladbrokesMobile/racing/components/racingSpecialsTab/racing-specials-tab.component';

describe('LadbrokesMobileRacingSpecialsTabComponent', () => {
  let component;

  let smartBoostsService;
  let filtersService;
  let sbFiltersService;
  let routingHelperService;

  const testStr = 'TestString';
  const wasPriceStub = 'TestWasPrice';

  beforeEach(() => {
    filtersService = jasmine.createSpyObj(['date', 'orderBy']);
    sbFiltersService = jasmine.createSpyObj(['orderOutcomeEntities']);
    smartBoostsService = {
      isSmartBoosts: jasmine.createSpy().and.returnValue(true),
      parseName: jasmine.createSpy().and.returnValue({ name: testStr, wasPrice: wasPriceStub })
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy()
    };

    component = new LadbrokesMobileRacingSpecialsTabComponent(
      filtersService,
      sbFiltersService,
      smartBoostsService,
      routingHelperService
    );

    component.eventsByType = [
      {
        typeName: 'typeName',
        events: [
          {
            isExpandedEvent: false
          }
        ]
      },
      {
        typeName: 'typeName',
        events: [
          {
            isExpandedEvent: false
          }
        ]
      }
    ] as any[];

    component.racing = {
      events: [{ markets: [{ outcomes: [{ name: '' }] }] }],
      classesTypeNames: {}
    }  as any;
  });

  it('ngOnInit should set isExpandedGroup field', () => {
    component.ngOnInit();
    expect(component.eventsByType[0]['isExpandedGroup']).toBeTruthy();
    expect(component.eventsByType[1]['isExpandedGroup']).toBeFalsy();
  });

  it('formEdpUrl', () => {
    const eventEmtity = {
      id: 123
    } as any;
    component.formEdpUrl(eventEmtity);

    expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith(eventEmtity);
  });
});
