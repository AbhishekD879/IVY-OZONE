import { async } from '@angular/core/testing';
import { NavigationPointsCreateComponent } from './navigation-points-create.component';
import { of } from 'rxjs';
import { NavigationPoint } from '@app/client/private/models';
import { FormControl, FormGroup, Validators } from '@angular/forms';

describe('NavigationPointsCreateComponent', () => {
  let component,
    navigationPointsApiService,
    dialogRef,
    brandService;

  beforeEach(async(() => {
    navigationPointsApiService = {
      getLandingPages: jasmine.createSpy('getLandingPages').and.returnValue(of([{}, {}, {}]))
    };
    dialogRef = { close: jasmine.createSpy('dialogRef.close') };
    brandService = {
      brand: 'coral'
    };

    component = new NavigationPointsCreateComponent(
      navigationPointsApiService,
      dialogRef,
      brandService
    );
    component.navigationPoint = { validityPeriodStart: '', validityPeriodEnd: '' } as NavigationPoint;

    component.ngOnInit();
  }));

  it('should Init component data', () => {
    expect(component.form).toBeDefined();
    expect(component.navigationPoint).toBeDefined();

    expect(navigationPointsApiService.getLandingPages).toHaveBeenCalled();
    expect(component.homeTabs).toBeDefined();
    expect(component.sportCategories).toBeDefined();
    expect(component.bigCompetitions).toBeDefined();
  });
  it('CloseDialog should call close()', () => {
    spyOn(component, 'closeDialog').and.callFake(function () {
      return dialogRef.close();
    });
    component.closeDialog();
    expect(dialogRef.close).toHaveBeenCalled();
  });

  describe('#handleDateUpdate', () => {
    it('should set start and end date', () => {
      const DataMock = { startDate: '01/02/2021', endDate: '10/02/2021' };
      component.handleDateUpdate(DataMock);
      expect(component.navigationPoint.validityPeriodStart).toEqual(DataMock.startDate);
      expect(component.navigationPoint.validityPeriodEnd).toEqual(DataMock.endDate);
    });
  });

  describe('#isMaxLengthReached', () => {
    it('should return false if title length is more than 25 charcters', () => {
      component.form = new FormGroup({
        title: new FormControl('play 1-2 free and win 100 euros', [Validators.required, Validators.maxLength(25)]),
      });
      expect(component.isMaxLengthReached('title')).toBeFalse();
    });

    it('should return false if title length is more than 45 charcters', () => {
      component.form = new FormGroup({
        description: new FormControl('play 1-2 free and win 100 euros is used in ladbrokes and coral for promotions', [Validators.maxLength(45)]),
      });
      expect(component.isMaxLengthReached('description')).toBeFalse();
    });
  });
});
