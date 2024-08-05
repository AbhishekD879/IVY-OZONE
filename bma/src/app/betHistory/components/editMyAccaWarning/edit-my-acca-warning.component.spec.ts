import { EditMyAccaWarningComponent } from '@app/betHistory/components/editMyAccaWarning/edit-my-acca-warning.component';

describe('EditMyAccaRemoveIconComponent', () => {
  let editMyAccaService, component: EditMyAccaWarningComponent;

  beforeEach(() => {
    editMyAccaService = {
      hasSuspendedLegs: jasmine.createSpy('hasSuspendedLegs').and.returnValue(true),
      hasLegsWithLostStatus: jasmine.createSpy('hasLegsWithLostStatus')
    };

    component = new EditMyAccaWarningComponent(editMyAccaService);
  });

  it('constructor', () => {
    expect(component).toBeDefined();
  });

  describe('getMessage', () => {
    it('should getMessage (has suspended legs)', () => {
      expect(component.getMessage()).toEqual('ema.suspensionWarning');
    });

    it('should getMessage (no suspended legs)', () => {
      editMyAccaService.hasSuspendedLegs.and.returnValue(false);
      expect(component.getMessage()).toEqual('ema.editWarning');
    });

    it('should getMessage (has legs with lost status)', () => {
      editMyAccaService.hasLegsWithLostStatus.and.returnValue(true);
      expect(component.getMessage()).toEqual('ema.noActiveWarning');
    });
  });
});
