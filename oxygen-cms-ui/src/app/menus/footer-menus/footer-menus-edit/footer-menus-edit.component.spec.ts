import { of as observableOf } from 'rxjs/observable/of';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/throw';
import { FooterMenusEditComponent } from './footer-menus-edit.component';
import { FormControl, FormGroup } from '@angular/forms';
import { AppConstants } from '@app/app.constants';
import { FooterMenu } from '@app/client/private/models';

describe('FooterMenusEditComponent', () => {
  let component: FooterMenusEditComponent;
  let globalLoaderService, apiClientService, dialogService;
  let router, activatedRoute;
  let snackBar;
  let brandService;
  let segmentStoreService;

  beforeEach(() => {
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    apiClientService = {
      footerMenu: jasmine.createSpy('footerMenu').and.returnValue({
        update: jasmine.createSpy('update').and.returnValue(observableOf({ body: { createdBy: '123' } })),
        uploadImage: jasmine.createSpy('uploadImage').and.returnValue(observableOf({ body: { createdBy: '123' } })),
        removeImage: jasmine.createSpy('removeImage').and.returnValue(observableOf({ body: { createdBy: '123' } })),
        uploadSvg: jasmine.createSpy('uploadSvg').and.returnValue(observableOf({ body: { createdBy: '123' } })),
        removeSvg: jasmine.createSpy('removeSvg').and.returnValue(observableOf({ body: { createdBy: '123' } })),
        delete: jasmine.createSpy('delete').and.returnValue(observableOf({ body: {} })),
        findOne: jasmine.createSpy('findOne').and.returnValue(observableOf({ body: { id: 'MockId', linkTitle: '/' } }))
      }),
    };
    segmentStoreService = {
      setSegmentValue: jasmine.createSpy('setSegmentValue'),
    };
    dialogService = jasmine.createSpyObj('dialogServiceSpy', ['showNotificationDialog']);
    router = jasmine.createSpyObj('routerSpy', ['navigate']);
    activatedRoute = {
      params: { subscribe: jasmine.createSpy('subscribe').and.callFake((cb) => cb({ id: 'MockId' })) }
    };
    snackBar = jasmine.createSpyObj('snackBarSpy', ['open']);
    brandService = {
      isIMActive: jasmine.createSpy('isIMActive')
    };
    component = new FooterMenusEditComponent(
      router,
      activatedRoute,
      apiClientService,
      dialogService,
      globalLoaderService,
      snackBar,
      brandService,
      segmentStoreService
    );
    component.footerMenu = { id: 'MockId', linkTitle: '/', showItemFor: '' } as FooterMenu
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#uploadImageHandler', () => {
    beforeEach(() => {
      component.footerMenu = <any>{
        id: 'id',
        linkTitle: 'title',
        targetUri: 'targetUri',
        mobile: true
      };
      component.form = new FormGroup({
        linkTitle: new FormControl(component.footerMenu.linkTitle),
        targetUri: new FormControl(component.footerMenu.targetUri),
        mobile: new FormControl(component.footerMenu.mobile)
      });
    });
    it('should handle image uploading', () => {
      component.uploadImageHandler({ file: 'file' });

      expect(apiClientService.footerMenu).toHaveBeenCalled();
      expect(apiClientService.footerMenu().uploadImage).toHaveBeenCalledWith('id', { file: 'file' });
      expect(component.footerMenu).toEqual(<any>{
        linkTitle: 'title',
        targetUri: 'targetUri',
        mobile: true,
        createdBy: '123'
      });
      expect(snackBar.open).toHaveBeenCalledWith('Image Uploaded.', 'Ok!', {
        duration: AppConstants.HIDE_DURATION
      });
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });

    it('should throw error', () => {
      apiClientService.footerMenu().uploadImage.and.returnValue(Observable.throw({ status: 404 }));
      component.uploadImageHandler({ file: 'file' });
      expect(component.footerMenu).toEqual(<any>{
        id: 'id',
        linkTitle: 'title',
        targetUri: 'targetUri',
        mobile: true
      });
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
      expect(snackBar.open).not.toHaveBeenCalled();
    });
  });

  describe('#removeImageHandler', () => {
    beforeEach(() => {
      component.footerMenu = <any>{
        id: 'id',
        linkTitle: 'title',
        targetUri: 'targetUri',
        mobile: true
      };
      component.form = new FormGroup({
        linkTitle: new FormControl(component.footerMenu.linkTitle),
        targetUri: new FormControl(component.footerMenu.targetUri),
        mobile: new FormControl(component.footerMenu.mobile)
      });
    });
    it('should handle image removing', () => {
      component.removeImageHandler();

      expect(apiClientService.footerMenu).toHaveBeenCalled();
      expect(apiClientService.footerMenu().removeImage).toHaveBeenCalledWith('id');
      expect(component.footerMenu).toEqual(<any>{
        linkTitle: 'title',
        targetUri: 'targetUri',
        mobile: true,
        createdBy: '123'
      });
      expect(snackBar.open).toHaveBeenCalledWith('Image Deleted.', 'Ok!', {
        duration: AppConstants.HIDE_DURATION
      });
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });

    it('should throw error', () => {
      apiClientService.footerMenu().removeImage.and.returnValue(Observable.throw({ status: 404 }));
      component.removeImageHandler();
      expect(component.footerMenu).toEqual(<any>{
        id: 'id',
        linkTitle: 'title',
        targetUri: 'targetUri',
        mobile: true
      });
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
      expect(snackBar.open).not.toHaveBeenCalled();
    });
  });

  describe('#uploadSvgHandler', () => {
    beforeEach(() => {
      component.footerMenu = <any>{
        id: 'id',
        linkTitle: 'title',
        targetUri: 'targetUri',
        mobile: true
      };
      component.form = new FormGroup({
        linkTitle: new FormControl(component.footerMenu.linkTitle),
        targetUri: new FormControl(component.footerMenu.targetUri),
        mobile: new FormControl(component.footerMenu.mobile)
      });
    });
    it('should handle image uploading', () => {
      component.uploadSvgHandler({ file: 'file' });

      expect(apiClientService.footerMenu).toHaveBeenCalled();
      expect(apiClientService.footerMenu().uploadSvg).toHaveBeenCalledWith('id', { file: 'file' });
      expect(component.footerMenu).toEqual(<any>{
        linkTitle: 'title',
        targetUri: 'targetUri',
        mobile: true,
        createdBy: '123'
      });
      expect(snackBar.open).toHaveBeenCalledWith('Svg Uploaded.', 'Ok!', {
        duration: AppConstants.HIDE_DURATION
      });
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });

    it('should throw error', () => {
      apiClientService.footerMenu().uploadSvg.and.returnValue(Observable.throw({ status: 404 }));
      component.uploadSvgHandler({ file: 'file' });
      expect(component.footerMenu).toEqual(<any>{
        id: 'id',
        linkTitle: 'title',
        targetUri: 'targetUri',
        mobile: true
      });
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
      expect(snackBar.open).not.toHaveBeenCalled();
    });
  });

  describe('#removeSvgHandler', () => {
    beforeEach(() => {
      component.footerMenu = <any>{
        id: 'id',
        linkTitle: 'title',
        targetUri: 'targetUri',
        mobile: true
      };
      component.form = new FormGroup({
        linkTitle: new FormControl(component.footerMenu.linkTitle),
        targetUri: new FormControl(component.footerMenu.targetUri),
        mobile: new FormControl(component.footerMenu.mobile)
      });
    });
    it('should handle image removing', () => {
      component.removeSvgHandler();

      expect(apiClientService.footerMenu).toHaveBeenCalled();
      expect(apiClientService.footerMenu().removeSvg).toHaveBeenCalledWith('id');
      expect(component.footerMenu).toEqual(<any>{
        linkTitle: 'title',
        targetUri: 'targetUri',
        mobile: true,
        createdBy: '123'
      });
      expect(snackBar.open).toHaveBeenCalledWith('Svg Deleted.', 'Ok!', {
        duration: AppConstants.HIDE_DURATION
      });
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });

    it('should throw error', () => {
      apiClientService.footerMenu().removeSvg.and.returnValue(Observable.throw({ status: 404 }));
      component.removeSvgHandler();
      expect(component.footerMenu).toEqual(<any>{
        id: 'id',
        linkTitle: 'title',
        targetUri: 'targetUri',
        mobile: true
      });
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
      expect(snackBar.open).not.toHaveBeenCalled();
    });
  });

  describe('#save', () => {
    beforeEach(() => {
      component.footerMenu = <FooterMenu>{ desktop: true };
    });
    it('should save and open dialog', () => {
      component.actionButtons = { extendCollection: jasmine.createSpy('extendCollection') };
      component.save();
      expect(apiClientService.footerMenu).toHaveBeenCalled();
      expect(apiClientService.footerMenu().update).toHaveBeenCalledWith({ desktop: true });
      expect(component.footerMenu).toEqual(<FooterMenu>{ createdBy: '123' });
      expect(component.actionButtons.extendCollection).toHaveBeenCalledWith(component.footerMenu);
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith(
        {
          title: 'Footer Menu', message: 'Footer Menu is Saved',
          closeCallback: jasmine.any(Function)
        }
      );
      expect(segmentStoreService.setSegmentValue).toHaveBeenCalled();
    });

    it('should throw error when 404', () => {
      apiClientService.footerMenu().update.and.returnValue(Observable.throw({ status: 404 }));
      component.save();
      expect(component.footerMenu).toEqual(<FooterMenu>{ desktop: true });
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
  });

  describe('#form validator and emitted data handler', () => {
    beforeEach(() => {
      component.footerMenu = <any>{
        id: 'id',
        linkTitle: 'title',
        targetUri: 'targetUri',
        mobile: true
      };
      component.form = new FormGroup({
        linkTitle: new FormControl(component.footerMenu.linkTitle),
        targetUri: new FormControl(component.footerMenu.targetUri),
        mobile: new FormControl(component.footerMenu.mobile)
      });
    });

    it('should handle form valid and check validation to true', () => {
      expect(component.form).toBeDefined();
      component.isSegmentValid = true;
      expect(component.validationHandler()).toBeTruthy();
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

    it('ngonInit should call load init', () => {
      spyOn(component, 'loadInitData');
      component.ngOnInit();
      expect(component.loadInitData).toHaveBeenCalled();
    });
  });

  describe('#loadinint', () => {
    it('should load with intialdata', () => {
      const breadcrumbsDataMock = [{ label: `Footer Menus`, url: `/menus/footer-menus` }, {
        label: component.footerMenu.linkTitle, url: `/menus/footer-menus/MockId`
      }];
      component.loadInitData();
      expect(globalLoaderService.showLoader).toHaveBeenCalledBefore(apiClientService.footerMenu);
      expect(apiClientService.footerMenu).toHaveBeenCalled();
      expect(apiClientService.footerMenu().findOne).toHaveBeenCalledWith('MockId');
      expect(component.footerMenu).toBeDefined();
      expect(component.form).toBeDefined();
      expect(component.breadcrumbsData).toEqual(breadcrumbsDataMock)
    });
    it('should throw error', () => {
      component.loadInitData();
      apiClientService.footerMenu().findOne.and.returnValue(Observable.throw({ status: 404 }));
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
  });

  describe('#revert', () => {
    beforeEach(() => {
      spyOn(component, 'loadInitData');
    });
    it('should call load init', () => {
      component.revert();
      expect(component.loadInitData).toHaveBeenCalled();
    });
  });

  describe('#remove', () => {
    it('delete the footermenu', () => {
      component.remove();
      expect(globalLoaderService.showLoader).toHaveBeenCalledBefore(apiClientService.footerMenu);
      expect(apiClientService.footerMenu).toHaveBeenCalled();
      expect(apiClientService.footerMenu().delete).toHaveBeenCalledWith(component.footerMenu.id);
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
      expect(router.navigate).toHaveBeenCalledWith([`/menus/footer-menus/`]);
    });
    it('should throw error', () => {
      component.remove();
      apiClientService.footerMenu().delete.and.returnValue(Observable.throw({ status: 404 }));
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    });
  });

  describe('#OnShowModechanges', () => {
    it('should set footermenu show item with option', () => {
      const option: string = 'sport';
      component.onShowModeChanged(option);
      expect(component.footerMenu.showItemFor).toEqual(option);
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

  describe('modifiedSegmentsHandler', () => {
    it('when segmentConfig data is not defined', () => {
      const segmentConfigData = undefined;
      component.modifiedSegmentsHandler(segmentConfigData);
      expect(component.footerMenu).toEqual(component.footerMenu);
    });

    it('when segmentConfig data is defined', () => {
      const segmentConfigData = { exclusionList: [], inclusionList: [], universalSegment: true };
      component.modifiedSegmentsHandler(segmentConfigData);
      const result = { ...component.footerMenu, ...segmentConfigData };
      expect(component.footerMenu).toEqual(result);
    });
  });
});
