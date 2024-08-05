import { BppErrorDialogComponent } from './bpp-error-dialog.component';
import { BppErrorDialogComponent as AppBppErrorDialogComponent } from '@shared/components/bppErrorDialog/bpp-error-dialog.component';

describe('BppErrorDialogComponent', () => {
  let component;
  let device, windowRef;

  beforeEach(() => {
    device = {};
    windowRef = {};
    component = new BppErrorDialogComponent(device, windowRef);
  });

  describe('instance', () => {
    it('should be created', () => {
      expect(component).toBeTruthy();
    });

    it('should extend AbstractDialog', () => {
      expect(component instanceof AppBppErrorDialogComponent).toBeTruthy();
    });
  });
});
