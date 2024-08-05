import { EnhancedMultiplesCarouselComponent } from '@desktop/components/enchancedMultiplesCarousel/enhancedMultiplesCarousel.component';
import { of } from 'rxjs';

describe('EnhancedMultiplesCarouselComponent', () => {
  let component: EnhancedMultiplesCarouselComponent;

  let carouselService;
  let enhancedMultiplesCarouselService;

  beforeEach(() => {
    carouselService = {
      isFreeBetVisible: jasmine.createSpy().and.returnValue(true)
    } as any;

    enhancedMultiplesCarouselService = {
      setEventDate: jasmine.createSpy('setEventDate'),
      buildEnhancedMultiplesData: jasmine.createSpy('buildEnhancedMultiplesData').and.returnValue([{ name: 'Event' }]),
      getEnhancedMultiplesEvents: jasmine.createSpy('getEnhancedMultiplesEvents').and.returnValue(of([{name: 'Event'}]))
    };

    component = new EnhancedMultiplesCarouselComponent(carouselService, enhancedMultiplesCarouselService);
    component.sportName = 'football';
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('onInit', () => {
    component.ngOnInit();

    expect(enhancedMultiplesCarouselService.setEventDate).toHaveBeenCalledWith([{ name: 'Event' }]);
    expect(enhancedMultiplesCarouselService.buildEnhancedMultiplesData).toHaveBeenCalledWith([{ name: 'Event' }], 'football');
    expect(enhancedMultiplesCarouselService.getEnhancedMultiplesEvents).toHaveBeenCalledWith('football');
    expect(component.isSingleSlide).toEqual(true);
  });

  it('trackByOutcomeId', () => {
    const res = component.trackById(1, { id: '123' } as any);

    expect(res).toEqual('1123');
  });
});
