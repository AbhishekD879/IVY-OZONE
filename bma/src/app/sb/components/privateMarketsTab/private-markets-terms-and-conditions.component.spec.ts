import { PrivateMarketsTermsAndConditionsComponent } from '@sb/components/privateMarketsTab/private-markets-terms-and-conditions.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { of, throwError } from 'rxjs';

describe('PrivateMarketsTermsAndConditionsComponent', () => {
  let component: PrivateMarketsTermsAndConditionsComponent;
  let cms: any;

  beforeEach(() => {
    cms = jasmine.createSpyObj('cms', ['getPrivateMarketsTermsAndConditions']);

    component = new PrivateMarketsTermsAndConditionsComponent(cms);

    spyOn(component, 'hideSpinner');
  });

  describe('ngOnInit', () => {
    it('should call correct methods', fakeAsync(() => {
      cms.getPrivateMarketsTermsAndConditions.and.returnValue(of(12345));

      component.ngOnInit();

      tick();

      expect(component.hideSpinner).toHaveBeenCalled();
      expect(component.privateMarketsTermsAndConditionsText).toEqual(12345 as any);
    }));

    it('should call correct methods after error', fakeAsync(() => {
      spyOn(component, 'showError');

      cms.getPrivateMarketsTermsAndConditions.and.returnValue(throwError('some error'));

      component.ngOnInit();

      tick();

      expect(component.showError).toHaveBeenCalled();
    }));
  });
});
