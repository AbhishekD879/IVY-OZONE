import { YourCallIconComponent } from './your-call-icon.component';
import { of } from 'rxjs';

describe('YourCallIconComponent', () => {
  let component: YourCallIconComponent;
  let yourCallService;
  let promotionsService;

  beforeEach(() => {
    yourCallService = {
      whenYCReady: jasmine.createSpy().and.returnValue(of([])),
      isBYBIconAvailable: jasmine.createSpy().and.returnValue(true),
      isYCIconAvailable: jasmine.createSpy().and.returnValue(true),
      isAvailableForCompetition: jasmine.createSpy().and.returnValue(true)
    };
    promotionsService = {
      openPromotionDialog: jasmine.createSpy()
    };

    component = new YourCallIconComponent(yourCallService, promotionsService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('should set isBybAvailable and isYcAvailable to TRUE if display is equal to general', () => {
      component.display = 'general';

      component.ngOnInit();
      expect(component.isBybAvailable).toBe(true);
      expect(component.isYcAvailable).toBe(true);
    });
    it('should set isBybAvailable and isYcAvailable to FALSE if display is NOT equal to general', () => {
      component.ngOnInit();
      expect(component.isBybAvailable).toBe(false);
      expect(component.isYcAvailable).toBe(false);
    });
  });

  describe('iconAction', () => {
    it('should set isBybAvailable and isYcAvailable to TRUE if display is equal to general', () => {
      const event = {
        stopPropagation: jasmine.createSpy()
      } as any;
      component.iconAction(event);

      expect(event.stopPropagation).toHaveBeenCalled();
      expect(promotionsService.openPromotionDialog).toHaveBeenCalledWith('YOUR_CALL');
    });
  });
});
