import { async } from '@angular/core/testing';
import { NavigationPointsEditComponent } from './navigation-points-edit.component';
import { of } from 'rxjs';
import { NavigationPoint } from '@app/client/private/models';
import { FormControl, FormGroup, Validators } from '@angular/forms';

describe('NavigationPointsEditComponent', () => {
  let component,
    router,
    activatedRoute,
    navigationPointsApiService,
    segmentStoreService,
    dialogService,
    brandService,
    globalLoaderService;

  beforeEach(async(() => {
    router = { navigate: jasmine.createSpy('navigate') };
    activatedRoute = {
      params: of({
        id: 'mockid'
      })
    };
    segmentStoreService = {
      setSegmentValue: jasmine.createSpy('setSegmentValue'),
    };
    navigationPointsApiService = {
      getLandingPages: jasmine.createSpy('getLandingPages').and.returnValue(of([{}, {}, {}])),
      getSingleNavigationPoint: jasmine.createSpy('getSingleNavigationPoint').and.returnValue(of({
        body: { id: 'Mockid' }
      })),
      updateNavigationPoint: jasmine.createSpy('updateNavigationPoint').and.returnValue(of({ body: { title: '1234' } })),
      deleteNavigationPoint: jasmine.createSpy('deleteNavigationPoint').and.returnValue(of({ body: { id: 'Mockid' } })),
    };
    dialogService = jasmine.createSpyObj('dialogServiceSpy', ['showNotificationDialog']);
    component = new NavigationPointsEditComponent(
      router,
      activatedRoute,
      navigationPointsApiService,
      dialogService,
      segmentStoreService,
      brandService,
      globalLoaderService
    );

    component.ngOnInit();

  }));

  it('should create', () => {
    expect(component.homeTabs).toBeDefined();
    expect(component.sportCategories).toBeDefined();
    expect(component.bigCompetitions).toBeDefined();
    expect(component.navigationPoint).toBeDefined();

    expect(component.form).toBeDefined();
  });

  it('should initialize component properties for "ADD" mode', () => {
    expect(component.typeAddEdit).toBe('ADD');
    expect(component.navigationPoint).toEqual(jasmine.objectContaining({
      message: null,
      categoryId: [],
      competitionId: [],
      homeTabs: [""],
      enabled: false,
      targetUri: "",
      title: "",
      description: "",
      validityPeriodEnd: "",
      validityPeriodStart: "",
      shortDescription: "",
      ctaAlignment: "",
      themes: null,
      id: "",
      brand: "",
      createdBy: "",
      createdAt: '',
      updatedBy: "",
      updatedAt: "",
      updatedByUserName: "",
      createdByUserName: "",
      inclusionList: [],
      exclusionList: [],
      universalSegment: true
    }));
    expect(navigationPointsApiService.getLandingPages).toHaveBeenCalled();
    expect(component.alignment).toEqual(component.ctaAlignment);
    expect(component.form.controls.title.value).toBe('');
    expect(component.form.controls.targetUri.value).toBe('');
    expect(component.form.controls.description.value).toBe('');
    expect(component.form.controls.homeTabs.value).toBe('');
    expect(component.form.controls.sportCategories.value).toBe('');
    expect(component.form.controls.competitions.value).toBe('');
    expect(component.form.controls.ctaAlignment.value).toBe('');
    expect(component.form.controls.shortDescription.value).toBe('');
    expect(component.form.controls.themes.value).toBe('');
  });

  it('should initialize component properties for "EDIT" mode', () => {
    expect(component.typeAddEdit).toBe('EDIT');
    expect(component.homeCatTabs).toHaveBeenCalled();
    expect(component.alignment).toEqual(component.navigationPoint.ctaAlignment || 'center');
    expect(component.form.controls.title.value).toBe('');
    expect(component.form.controls.targetUri.value).toBe('');
    expect(component.form.controls.description.value).toBe('');
    expect(component.form.controls.homeTabs.value).toBe('');
    expect(component.form.controls.sportCategories.value).toBe('');
    expect(component.form.controls.competitions.value).toBe('');
    expect(component.form.controls.ctaAlignment.value).toBe('');
    expect(component.form.controls.shortDescription.value).toBe('');
    expect(component.form.controls.themes.value).toBe('');
  });

  it('should create the form with the correct initial values', () => {

    component.initAddEditButton();
  
    expect(component.form.get('title').value).toEqual('');
    expect(component.form.get('targetUri').value).toEqual('');
    expect(component.form.get('description').value).toEqual('');
    expect(component.form.get('homeTabs').value).toEqual('');
    expect(component.form.get('sportCategories').value).toEqual('');
    expect(component.form.get('competitions').value).toEqual('');
    expect(component.form.get('ctaAlignment').value).toEqual(component.alignment);
    expect(component.form.get('shortDescription').value).toEqual('');
    expect(component.form.get('themes').value).toEqual('');
  });
  
  it('should update form control validators when ctaAlignment value changes', () => {
    const formConfig = {
      key: 'center',
      config: {
        title: { maxLength: 50 },
        description: { maxLength: 100 },
        shortDescription: { coral: { maxLength: 25 }, lads: { maxLength: 30 } }
      }
    };
    component.titleOptions = [formConfig];
    component.alignment = 'center';
  
    component.initAddEditButton();
    component.form.controls.ctaAlignment.setValue('right');
  
    expect(component.form.controls.title.validator).toBe(Validators.maxLength(formConfig.config.title.maxLength));
    expect(component.form.controls.description.validator).toBe(Validators.maxLength(formConfig.config.description.maxLength));
    expect(component.form.controls.shortDescription.validator).toBe(Validators.maxLength(formConfig.config.shortDescription.lads.maxLength));
  });
  
  it('should update form control validators based on different ctaAlignment center and right values and form configurations', () => {
    
    const formConfigCenter = {
      key: 'center',
      config: {
        title: { maxLength: 50 },
        description: { maxLength: 100 },
        shortDescription: { coral: { maxLength: 25 }, lads: { maxLength: 30 } }
      }
    };
    const formConfigRight = {
      key: 'right',
      config: {
        title: { maxLength: 60 },
        description: { maxLength: 80 },
        shortDescription: { coral: { maxLength: 35 }, lads: { maxLength: 40 } }
      }
    };
    component.titleOptions = [formConfigCenter, formConfigRight];
  
    component.alignment = 'center';
    component.initAddEditButton();
  
    expect(component.form.controls.title.validator).toBe(Validators.maxLength(formConfigCenter.config.title.maxLength));
    expect(component.form.controls.description.validator).toBe(Validators.maxLength(formConfigCenter.config.description.maxLength));
    expect(component.form.controls.shortDescription.validator).toBe(Validators.maxLength(formConfigCenter.config.shortDescription.coral.maxLength));
  
    component.alignment = 'right';
    component.initAddEditButton();

    expect(component.form.controls.title.validator).toBe(Validators.maxLength(formConfigRight.config.title.maxLength));
    expect(component.form.controls.description.validator).toBe(Validators.maxLength(formConfigRight.config.description.maxLength));
    expect(component.form.controls.shortDescription.validator).toBe(Validators.maxLength(formConfigRight.config.shortDescription.lads.maxLength));
  });
  
  it('should assign the segmentsList property with correct values', () => {
    
    const exclusionList = ['exclusion1', 'exclusion2'];
    const inclusionList = ['inclusion1', 'inclusion2'];
    const universalSegment = 'universal';
  
    component.navigationPoint = {
      exclusionList,
      inclusionList,
      universalSegment
    };
    component.initAddEditButton();
  
    expect(component.segmentsList.exclusionList).toEqual(exclusionList);
    expect(component.segmentsList.inclusionList).toEqual(inclusionList);
    expect(component.segmentsList.universalSegment).toEqual(universalSegment);
  });

  describe('#save', () => {
    it('should save and open dialog', () => {
      component.actionButtons = { extendCollection: jasmine.createSpy('extendCollection') };
      component.save();
      expect(navigationPointsApiService.updateNavigationPoint).toHaveBeenCalled();
      expect(component.navigationPoint).toEqual(<NavigationPoint>{ title: '1234' });
      expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(component.navigationPoint);
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
        {
          title: 'Super Button Saving', message: 'Super Button is Successfully Saved.',
          closeCallback: jasmine.any(Function)
        }
      );
      expect(segmentStoreService.setSegmentValue).toHaveBeenCalled();
    });
  });

  describe('#form validator and emitted data handler', () => {
    it('should handle form valid and check validation to true', () => {
      expect(component.form).toBeDefined();
      component.isSegmentValid = true;
      expect(component.validationHandler()).toBeFalsy();
    });

    it('check validation to true', () => {
      component.isSegmentValid = false;
      expect(component.validationHandler()).toBeFalsy();
    });

    it('should check if segment is valid', () => {
      let flag = true;
      component.isSegmentFormValid(flag);
      expect(component.isSegmentValid).toBeTrue();
    });

    it('should check if segment is valid', () => {
      let flag = false;
      component.isSegmentFormValid(flag);
      expect(component.isSegmentValid).toBeFalse();

    });
  });

  describe('formBreadcrumbs', () => {
    it('should set breadCrumbs', () => {
      component.navigationPoint = { id: 'Mockid', title: 'title' } as NavigationPoint;
      const breadcrumbsDataMock = [{ label: 'Super Buttons', url: '/quick-links/navigation-points' }, {
        label: component.navigationPoint.title, url: `/quick-links/navigation-points/${component.navigationPoint.id}`
      }];
      component.formBreadcrumbs();
      expect(component.breadcrumbsData).toEqual(breadcrumbsDataMock)
    });
  });

  describe('#revert', () => {
    it('should revert the data', () => {
      component.revert();
      expect(component.navigationPoint).toBeDefined();
      expect(navigationPointsApiService.getSingleNavigationPoint).toHaveBeenCalledWith('mockid');
    });
  });

  describe('#remove', () => {
    it('should remove the data', () => {
      let navigationPoint = { id: 'Mockid', title: 'title' } as NavigationPoint;
      component.remove();
      expect(navigationPointsApiService.deleteNavigationPoint).toHaveBeenCalledWith(navigationPoint.id);
      expect(router.navigate).toHaveBeenCalledWith(['/quick-links/navigation-points/']);
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

  describe('modifiedSegmentsHandler', () => {
    it('when segmentConfig data is not defined', () => {
      const segmentConfigData = undefined;
      component.modifiedSegmentsHandler(segmentConfigData);
      expect(component.navigationPoint).toEqual(component.navigationPoint);
    });

    it('when segmentConfig data is defined', () => {
      const segmentConfigData = { exclusionSegments: '', inclusionSegments: '', activeSegment: '' };
      component.modifiedSegmentsHandler(segmentConfigData);
      const result = { ...component.navigationPoint, ...segmentConfigData };
      expect(component.navigationPoint).toEqual(result);
    });
  });
});
