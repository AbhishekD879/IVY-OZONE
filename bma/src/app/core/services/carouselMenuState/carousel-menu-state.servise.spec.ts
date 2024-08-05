import { CarouselMenuStateService } from '@core/services/carouselMenuState/carousel-menu-state.service';

describe('CarouselMenuStateService', () => {
  let service: CarouselMenuStateService;


  beforeEach(() => {
    service = new CarouselMenuStateService();
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect (service.carouselStick$).toBeDefined();
  });
});
