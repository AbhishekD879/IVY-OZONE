import { CommonSvgInputSelectComponent } from './common-svg-input-select.component';
import { FormControl } from '@angular/forms';
import { Subscriber } from 'rxjs/Subscriber';
import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs/observable/of';

describe('CommonSvgInputSelectComponent', () => {
  let component,
    sanitizer,
    imageManageLoader;

  beforeEach(() => {
    sanitizer = {};
    imageManageLoader = {};

    component = new CommonSvgInputSelectComponent(sanitizer, imageManageLoader);
    component.formFieldsModels = {
      svgBgId: '1',
      svgBgImgPath: "/images/uploads/svg/32a3c994-2259-4b1a-8c1e-2049fa62a6ac.svg",
    } as any;

    component.externalForm = {
      addControl: jasmine.createSpy('addControl')
    } as any;
    component.type = "svgBgId";
    component.path = "svgBgImgPath";
  });

  describe('ngOnInit', () => {
    it('should create create formcontrol with value', () => {
      component.ngOnInit();

      expect(component.input.constructor).toBe(FormControl);
      expect(component.externalForm.addControl).toHaveBeenCalledWith(component.type, component.input);
      expect(component.subscription$.constructor).toBe(Subscriber);
    });

    it('should create create formcontrol with value', () => {
      component.ngOnInit();

      expect(component.input.constructor).toBe(FormControl);
      expect(component.externalForm.addControl).toHaveBeenCalledWith(component.type, component.input);
      expect(component.subscription$.constructor).toBe(Subscriber);
    });

    it('should create create formcontrol without value', () => {
      component.formFieldsModels = {
        svgBgId: null
      };

      component.ngOnInit();

      expect(component.input.constructor).toBe(FormControl);
    });

    it('should call updateFormFieldModelSvgPath on load', () => {
      spyOn(component, 'updateFormFieldModelSvgPath');
      component.ngOnInit();

      expect(component.updateFormFieldModelSvgPath).toHaveBeenCalledWith(component.formFieldsModels.svgBgId);

      const svgPath = "/images/uploads/svg/32a3c994-2259-4b1a-8c1e-2049fa62a6ac.svg";
      expect(component.formFieldsModels.svgBgImgPath).toBe(svgPath);
    });

    it('should set path to svg image path when type has a non-empty value on load', () => {
      spyOn(component, 'updateFormFieldModelSvgPath');
      component.ngOnInit();
      const initialValue = component.formFieldsModels.svgBgId;
      expect(component.updateFormFieldModelSvgPath).toHaveBeenCalledWith(initialValue);

      const svgPath = "/images/uploads/svg/32a3c994-2259-4b1a-8c1e-2049fa62a6ac.svg";
      expect(component.formFieldsModels.svgBgImgPath).toBe(svgPath);
    });

    it('should call getData', () => {
      component.ngOnInit();
      component.input.setValue('t');

      expect(component.options.length).toBe(0);
    });

    it('should not call getData', fakeAsync(() => {
      component.ngOnInit();
      component.input.setValue('');
      tick(450);
      expect(component.haveData).toBe(false);
      expect(component.formFieldsModels.svgBgId).toBe('');
    }));

    it('Should set select options', fakeAsync(() => {
      component.imageManageLoader.getData = jasmine.createSpy('getData').and.returnValue(of(['test']));
      component.ngOnInit();
      component.input.pristine = false;
      component.input.setValue('test');

      tick(450);

      expect(component.haveData).toBe(true);
      expect(component.options.length).toBe(2);
    }));

    it('Should not set select options', fakeAsync(() => {
      component.imageManageLoader.getData = jasmine.createSpy('getData').and.returnValue(of([]));

      component.ngOnInit();
      component.input.pristine = false;
      component.input.setValue('test');

      tick(450);

      expect(component.haveData).toBe(false);
    }));
  });

  describe('selectChanges', () => {
    it('should call updateFormFieldModel', () => {
      const event = {
        source: {
          value: '1'
        }
      };
      const svgPath = "/images/uploads/svg/32a3c994-2259-4b1a-8c1e-2049fa62a6ac.svg";
      expect(component.formFieldsModels.svgBgId).toBe(event.source.value);
      expect(component.formFieldsModels.svgBgImgPath).toBe(svgPath);
    });
  });

  describe('ngOnDestroy', () => {
    it('', () => {
      component.subscription$ = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      };

      component.ngOnDestroy();

      expect(component.subscription$.unsubscribe).toHaveBeenCalled();
    });
  });
});

