import { LottoInfoDialogComponent } from './lotto-info-dialog.component';

describe('whatIsLottoInfo', () => {
  let component: LottoInfoDialogComponent;
  let device, windowRef;
  beforeEach(() => {
    device = {};
    windowRef = {};
    component = new LottoInfoDialogComponent(device, windowRef);

    component.dialog = {
      close: jasmine.createSpy('close'),
      open: jasmine.createSpy('open'),
      changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') }
    };

  });

  describe('ngOnInit', () => {
    it('ngOnInit should call super.ngOnInit and set text value', () => {
      const parentNgOnInit = spyOn(LottoInfoDialogComponent.prototype['__proto__'], 'ngOnInit');
      component.params = {
        enabled: true,
        sortOrder: 2
      };
      component.ngOnInit();
      expect(component.cmsLotto).toEqual(component.params)
      expect(parentNgOnInit).toHaveBeenCalled();

    })
  });

  describe('closeThisDialog', () => {
    it('should call closeDialog', () => {
      component['closeDialog'] = jasmine.createSpy('closeDialog');
      component.closeThisDialog();
      expect(component['dialog'].close).toHaveBeenCalled();
    });
  });
});
