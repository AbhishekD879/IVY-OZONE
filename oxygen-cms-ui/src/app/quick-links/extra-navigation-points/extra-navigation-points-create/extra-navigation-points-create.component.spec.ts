import { async } from '@angular/core/testing';

import { ExtraNavigationPointsCreateComponent } from './extra-navigation-points-create.component';

import { of } from 'rxjs';
import { ExtraNavigationPoint } from '@app/client/private/models';
import { FormControl, FormGroup, Validators } from '@angular/forms';

describe('', () => {
  let component,
    extraNavigationPointsApiService,
    dialogRef,
    brandService;

  beforeEach(async(() => {
    extraNavigationPointsApiService = {
      getLandingPages: jasmine.createSpy('getLandingPages').and.returnValue(of([{}, {}, {}]))
    };
    dialogRef = { close: jasmine.createSpy('dialogRef.close') };
    brandService = {
      brand: 'coral'
    };

    component = new ExtraNavigationPointsCreateComponent(
      extraNavigationPointsApiService,
      dialogRef,
      brandService
    );
    component.extraNavigationPoint = { validityPeriodStart: '', validityPeriodEnd: '' } as ExtraNavigationPoint;

    component.ngOnInit();
  }));

  it('should Init component data', () => {
    expect(component.form).toBeDefined();
    expect(component.extraNavigationPoint).toBeDefined();

    expect(extraNavigationPointsApiService.getLandingPages).toHaveBeenCalled();
    expect(component.homeTabs).toBeDefined();
    expect(component.sportCategories).toBeDefined();
    expect(component.bigCompetitions).toBeDefined();
  });
  it('CloseDialog should call close()', () => {
    component.closeDialog();
    expect(dialogRef.close).toHaveBeenCalled();
  });

  describe('#handleDateUpdate', () => {
    it('should set start and end date', () => {
      const DataMock = { startDate: '01/02/2021', endDate: '10/02/2021' };
      component.handleDateUpdate(DataMock);
      expect(component.extraNavigationPoint.validityPeriodStart).toEqual(DataMock.startDate);
      expect(component.extraNavigationPoint.validityPeriodEnd).toEqual(DataMock.endDate);
    });
  });

  describe('#isMaxLengthReached', () => {
    it('should return false if title length is more than 25 charcters', () => {
      component.form = new FormGroup({
        title: new FormControl('play 1-2 free and win 100 euros', [Validators.required, Validators.maxLength(25)]),
      });
      expect(component.isMaxLengthReached('title')).toBeFalse();
    });

    it('should return true if title length is more than 45 charcters', () => {
      component.form = new FormGroup({
        description: new FormControl('play 1-2 free and win 100 euros is used in ladbrokes and coral for promotions this is check for true case', [Validators.maxLength(45)]),
      });
      component.form.controls['description'].touched = true;
      expect(component.isMaxLengthReached('description')).toBeTruthy();
    });
  });
});
