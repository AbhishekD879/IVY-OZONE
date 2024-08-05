import { async } from '@angular/core/testing';
import { ExtraNavigationPointsEditComponent } from './extra-navigation-points-edit.component';
import { of } from 'rxjs';
import { ExtraNavigationPoint } from '@app/client/private/models';
import { FormControl, FormGroup, Validators } from '@angular/forms';

describe('ExtraNavigationPointsEditComponent', () => {
  let component,
    router,
    activatedRoute,
    extraNavigationPointsApiService,
    dialogService;

  beforeEach(async(() => {
    router = { navigate: jasmine.createSpy('navigate') };
    activatedRoute = {
      params: of({
        id: 'mockid'
      })
    };
    extraNavigationPointsApiService = {
      getLandingPages: jasmine.createSpy('getLandingPages').and.returnValue(of([{}, {}, {}])),
      getSingleNavigationPoint: jasmine.createSpy('getSingleNavigationPoint').and.returnValue(of({
        body: { id: 'Mockid' }
      })),
      updateNavigationPoint: jasmine.createSpy('updateNavigationPoint').and.returnValue(of({ body: { title: '1234' } })),
      deleteNavigationPoint: jasmine.createSpy('deleteNavigationPoint').and.returnValue(of({ body: { id: 'Mockid' } })),
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callFake(({ title, message, closeCallback }) => {
        closeCallback();
      })
    };
    component = new ExtraNavigationPointsEditComponent(
      router,
      activatedRoute,
      extraNavigationPointsApiService,
      dialogService
    );

    component.ngOnInit();

  }));

  it('should create', () => {
    expect(component.homeTabs).toBeDefined();
    expect(component.sportCategories).toBeDefined();
    expect(component.bigCompetitions).toBeDefined();
    expect(component.extraNavigationPoint).toBeDefined();
    expect(component.form).toBeDefined();
  });

  describe('#save', () => {
    it('should save and open dialog', () => {
      component.actionButtons = { extendCollection: jasmine.createSpy('extendCollection') };
      component.save();

      expect(extraNavigationPointsApiService.updateNavigationPoint).toHaveBeenCalled();
      expect(component.extraNavigationPoint).toEqual(<ExtraNavigationPoint>{ title: '1234' });
      expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(component.extraNavigationPoint);
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
          title: 'Special Super Button Saving', message: 'Special Super Button is Successfully Saved.',
          closeCallback: jasmine.any(Function)
      });
    });
  });

  describe('#form validator and emitted data handler', () => {
    it('should handle form valid and check validation to true', () => {
      expect(component.form).toBeDefined();
      expect(component.validationHandler()).toBeFalsy();
    });
  });

  describe('formBreadcrumbs', () => {
    it('should set breadCrumbs', () => {
      component.extraavigationPoint = { id: 'Mockid', title: 'title' } as ExtraNavigationPoint;
      const breadcrumbsDataMock = [{ label: 'Special Super Buttons', url: '/quick-links/extra-navigation-points' }, {
        label: component.extraNavigationPoint.title, url: `/quick-links/extra-navigation-points/${component.extraNavigationPoint.id}`
      }];
      component.formBreadcrumbs();
      expect(component.breadcrumbsData).toEqual(breadcrumbsDataMock)
    });
  });

  describe('#revert', () => {
    it('should revert the data', () => {
      component.revert();
      expect(component.extraNavigationPoint).toBeDefined();
      expect(extraNavigationPointsApiService.getSingleNavigationPoint).toHaveBeenCalledWith('mockid');
    });
  });

  describe('#remove', () => {
    it('should remove the data', () => {
      let extraNavigationPoint = { id: 'Mockid', title: 'title' } as ExtraNavigationPoint;
      component.remove();
      expect(extraNavigationPointsApiService.deleteNavigationPoint).toHaveBeenCalledWith(extraNavigationPoint.id);
      expect(router.navigate).toHaveBeenCalledWith(['/quick-links/extra-navigation-points/']);
    });
  });

  describe('#actionsHandler', () => {
    beforeEach(() => {
      spyOn(component, 'remove');
      spyOn(component, 'save');
      spyOn(component, 'revert');
    });
    it('should call the actionitem as given', () => {
      component.actionsHandler('remove');
      expect(component.remove).toHaveBeenCalled();
      component.actionsHandler('save');
      expect(component.save).toHaveBeenCalled();
      component.actionsHandler('revert');
      expect(component.revert).toHaveBeenCalled();
    });
    it('should not call any action item', () => {
      component.actionsHandler('test-event');
      expect(component.remove).not.toHaveBeenCalled();
      expect(component.save).not.toHaveBeenCalled();
      expect(component.revert).not.toHaveBeenCalled();
    });
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
    it('should return true if title length is more than 45 charcters a true case check ', () => {
      component.form = new FormGroup({
        description: new FormControl('play 1-2 free and win 100 euros is used in ladbrokes and coral for promotions', [Validators.maxLength(45)]),
      });
    component.form.controls['description'].touched = true;
    expect(component.isMaxLengthReached('description')).toBeTruthy();
    });
  });

});
