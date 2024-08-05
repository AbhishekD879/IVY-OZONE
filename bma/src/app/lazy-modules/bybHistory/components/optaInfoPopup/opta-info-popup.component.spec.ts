import { OptaInfoPopupComponent } from './opta-info-popup.component';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';

describe('OptaInfoPopupComponent', () => {
  let component: OptaInfoPopupComponent;
  let device, windowRef, changeDetectorRef;
  beforeEach(() => {
    device = {};
    windowRef = {};
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy('detectChanges')
    };
    component = new OptaInfoPopupComponent(device, windowRef, changeDetectorRef);
  });
  describe('ngOnInit', () => {
    it('should create component instance', () => {
      expect(component).toBeTruthy();
    });

    it('should open popup', () => {
      spyOn(AbstractDialogComponent.prototype, 'open');
      component.open();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();

      expect(AbstractDialogComponent.prototype.open).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });
  });
});
