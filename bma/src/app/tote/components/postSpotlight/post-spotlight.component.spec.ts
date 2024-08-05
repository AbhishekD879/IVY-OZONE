import { PostSpotlightComponent  } from './post-spotlight.component';

describe('PostSpotlightComponent', () => {
  let component: PostSpotlightComponent, filterService;

  beforeEach(() => {
    filterService = {
      removeLineSymbol: jasmine.createSpy('filterService.removeLineSymbol')
    };

    component = new PostSpotlightComponent(filterService);
  });

  it('ngOnInit', () => {
    component.outcome = {
      racingFormOutcome: {}
    } as any;
    component.ngOnInit();

    expect(component.noDetails).toBeTruthy();
    expect(filterService.removeLineSymbol).toHaveBeenCalled();
    expect(component.sView).toBeTruthy();

    component.outcome.racingFormOutcome.age = '27';

    component.ngOnInit();
    expect(component.noDetails).toBeFalsy();
  });

  it('correctingWeight', () => {
    let result = component.correctingWeight('35kg');
    expect(result).toBe('2st-7lb');

    result = component.correctingWeight('28kg');
    expect(result).toBe('2st');
  });
});
