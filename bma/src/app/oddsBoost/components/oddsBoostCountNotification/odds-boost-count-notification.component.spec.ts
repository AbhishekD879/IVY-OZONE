import { of } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { OddsBoostCountNotificationComponent } from './odds-boost-count-notification.component';

describe('OddsBoostCountNotificationComponent', () => {
  let component;
  let oddsBoostService;
  let location;

  beforeEach(() => {
    oddsBoostService = {
      getOddsBoostTokensCount: jasmine.createSpy('getOddsBoostTokensCount').and.returnValue(of(0)),
      oddsBoostsCountListener: of(5)
    };

    location = {
      path: jasmine.createSpy('path')
    };

    component = new OddsBoostCountNotificationComponent(
      oddsBoostService,
      location
    );
  });

  describe('ngOnInit', () => {
    it('should subscribe to count listener', fakeAsync(() => {
      component.ngOnInit();
      tick();
      expect(component.oddsBoostCount).toBe(5);
    }));

    it('should get tokens count on my account page', fakeAsync(() => {
      location.path.and.returnValue('/my-account');
      component.ngOnInit();
      tick();
      expect(oddsBoostService.getOddsBoostTokensCount).toHaveBeenCalledTimes(1);
    }));
  });

  it('ngOnDestroy', () => {
    component['countListener'] = { unsubscribe: jasmine.createSpy('countListener') };
    component.ngOnDestroy();
    expect(component['countListener'].unsubscribe).toHaveBeenCalled();
  });
});
