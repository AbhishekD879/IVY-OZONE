import { BehaviorSubject } from 'rxjs';
import { NextRacesHomeTabComponent } from './next-races-home-tab.component';

describe('NextRacesHomeTabComponent', () => {
  let component: NextRacesHomeTabComponent;
  let navigationService;

  beforeEach(() => {
    navigationService = jasmine.createSpyObj('navigationService', ['emitChangeSource']);
    component = new NextRacesHomeTabComponent(navigationService);
  });
  describe('toggleLoader', () => {
    it('should toggle showLoader property', () => {
      navigationService.emitChangeSource = new BehaviorSubject(null);
      expect(component['showLoader']).toEqual(true);
      component.toggleLoader(true);
      expect(component['showLoader']).toEqual(false);
      component.toggleLoader(false);
      expect(component['showLoader']).toEqual(true);
      component.toggleLoader();
      expect(component['showLoader']).toEqual(true);
    });
  });
});
