import { BogLabelComponent } from '@shared/components/bogLabel/bog-label.component';
import { of } from 'rxjs';

describe('BogLabelComponent', () => {
  let component: BogLabelComponent,
    cmsService;

  beforeEach(() => {

    cmsService = {
      isBogFromCms: jasmine.createSpy('isBogFromCms').and.returnValue(of(true)),
      getSystemConfig: jasmine.createSpy('getSystemConfig')
    };

    component = new BogLabelComponent(cmsService);
  });

  describe('BogLabelComponent', () => {
    it('#onInit', () => {
      component.ngOnInit();
      expect(component).toBeTruthy();
    });

    describe('Should check isBogEnabled', () => {
      it('should check isBogEnabled when  isBogFromCms() = true', () => {
        component.ngOnInit();
        expect(component.isBogEnabled).toBe(true);
      });
      it('should check isBogEnabled when isBogFromCms() = false', () => {
        cmsService.isBogFromCms = jasmine.createSpy('isBogFromCms').and.returnValue(of(false));
        component.ngOnInit();

        expect(component.isBogEnabled).toBe(false);
      });
    });
  });
});
