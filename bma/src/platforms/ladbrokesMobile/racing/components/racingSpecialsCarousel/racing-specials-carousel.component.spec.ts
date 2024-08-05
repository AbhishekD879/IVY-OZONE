import {
  LadbrokesRacingSpecialsCarouselComponent
} from '@ladbrokesMobile/racing/components/racingSpecialsCarousel/racing-specials-carousel.component';
import { of } from 'rxjs';

describe('LadbrokesRacingSpecialsCarouselComponent', () => {

  let component: LadbrokesRacingSpecialsCarouselComponent;

  let cmsService;
  let racingSpecialsCarouselService;
  let pubSubService;

  describe('ENABLED - RacingSpecialsCarouselComponent', () => {
    beforeEach(() => {
      cmsService = {
        getSystemConfig: jasmine.createSpy().and.returnValue(of({}))
      };
      racingSpecialsCarouselService = {};
      pubSubService = {};

      component = new LadbrokesRacingSpecialsCarouselComponent(cmsService,
        racingSpecialsCarouselService, pubSubService);
      component.ngOnInit();
    });
  });
});
