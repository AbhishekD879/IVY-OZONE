import { SvgIconSelectInputComponent } from './svg-icon-select-input.component';
import { FormControl } from '@angular/forms';
import { Subscriber } from 'rxjs/Subscriber';
import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs/observable/of';

describe('SvgIconSelectInputComponent', () => {
  let component,
    sanitizer,
    imageManageLoader;

  beforeEach(() => {
    sanitizer = {};
    imageManageLoader = {};

    component = new SvgIconSelectInputComponent(sanitizer, imageManageLoader);
    component.formFieldsModels = {
      svgId: '1'
    } as any;

    component.externalForm = {
      addControl: jasmine.createSpy('addControl')
    } as any;
  });

  describe('ngOnInit', () => {
    it('should create create formcontrol with value', () => {
      component.ngOnInit();

      expect(component.input.constructor).toBe(FormControl);
      expect(component.externalForm.addControl).toHaveBeenCalledWith('svgId', component.input);
      expect(component.subscription$.constructor).toBe(Subscriber);
    });

    it('should create create formcontrol with value', () => {
      component.ngOnInit();

      expect(component.input.constructor).toBe(FormControl);
      expect(component.externalForm.addControl).toHaveBeenCalledWith('svgId', component.input);
      expect(component.subscription$.constructor).toBe(Subscriber);
    });

    it('should create create formcontrol without value', () => {
      component.formFieldsModels = {
        svgId: null
      };

      component.ngOnInit();

      expect(component.input.constructor).toBe(FormControl);
    });

    it('should not call getData',  () => {
      component.ngOnInit();
      component.input.setValue('t');

      expect(component.options.length).toBe(0);
    });

    it('should not call getData', fakeAsync(() => {
      component.ngOnInit();
      component.input.setValue('');
      tick(450);
      expect(component.haveData).toBe(false);
      expect(component.formFieldsModels.svgId).toBe('');
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
          value: 1
        }
      };

      component.selectChanges(event as any);

      expect(component.formFieldsModels.svgId).toBe(1);
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
