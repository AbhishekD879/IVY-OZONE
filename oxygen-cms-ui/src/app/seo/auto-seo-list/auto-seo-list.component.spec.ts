import { async } from '@angular/core/testing';
import { AppConstants } from '@app/app.constants';
import { AutoSeoPage } from '@app/client/private/models/seopage.model';
import { Observable, of } from 'rxjs';
import { AutoseoPageDialogComponent } from './auto-seo-dialog/auto-seo-dialog.component';
import { AutoSeolistComponent } from './auto-seo-list.component';

describe('AutoSeoListComponent', () => {
  let component: AutoSeolistComponent;
  let seoAPIService;
  let dialogService;

  beforeEach(async(() => {
    seoAPIService = {
      getAutoSeoListData: jasmine.createSpy('getAutoSeoListData').and.returnValue(of({
        body: [{ uri: '/event', metaTitle: 'bet', metaDescription: 'bet on event' }]
      })),
      putAutoSeoItemChanges: jasmine.createSpy('putAutoSeoItemChanges').and.returnValue(of({
        body: {}
      })),
      createAutoSeoItem: jasmine.createSpy('createAutoSeoItem').and.returnValue(of({
        body: {}
      })),
      deleteAutoSeoPage: jasmine.createSpy('deleteAutoSeoPage').and.returnValue(of({
        body: {}
      }))
    }
    dialogService = {
      showConfirmDialog: jasmine.createSpy('showConfirmDialog')
        .and.callFake(({ title, message, yesCallback }) => yesCallback()),
      showCustomDialog: jasmine.createSpy('showCustomDialog')
        .and.callFake((AutoseoPageDialogComponent, { width, title, yesOption, noOption, yesCallback }) => yesCallback()),
      showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.returnValue(of({}))
    };
    component = new AutoSeolistComponent(dialogService, seoAPIService);
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  describe('#ngOnInit', () => {
    it('should call loadIntialData', () => {
      spyOn(component, 'loadIntialData');
      component.ngOnInit();
      expect(component.loadIntialData).toHaveBeenCalled();
    });
  });

  describe('#LoadIntialData', () => {
    it('should load all the autoseopagesData', () => {
      let autoseopagesData = [{ uri: '/event', metaTitle: 'bet', metaDescription: 'bet on event' }] as AutoSeoPage[];
      component.loadIntialData();
      expect(seoAPIService.getAutoSeoListData).toHaveBeenCalled();
      expect(component.autoseoPagesData).toEqual(autoseopagesData);
    });
    it('should throw error', () => {
      seoAPIService.getAutoSeoListData.and.returnValue(Observable.throw({ message: 'error' }));
      component.loadIntialData();
      expect(component.getDataError).toBeDefined();
    });
  });
  describe('#addNewAutoSeoPage', () => {
    it('should create new autoseopage', () => {
      component.autoseoPagesData = [{ uri: '/event' }] as AutoSeoPage[]
      component.addNewAutoSeoPage();
      expect(dialogService.showCustomDialog).toHaveBeenCalledWith(
        AutoseoPageDialogComponent, {
        width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
        title: 'Add New Auto Seo Page',
        yesOption: 'Save',
        noOption: 'Cancel',
        yesCallback: jasmine.any(Function)
      });
      expect(seoAPIService.createAutoSeoItem).toHaveBeenCalled();
      expect(component.autoseoPagesData.length).toBe(2);
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
        title: 'Create Completed',
        message: 'AutoSeo Page is Created.'
      });
    });
    it('should throw error', () => {
      seoAPIService.createAutoSeoItem.and.returnValue(Observable.throw({ message: 'error' }));
      component.addNewAutoSeoPage();
      expect(component.getDataError).toBeDefined();
    });
  });
  describe('editAutoSeoPage', () => {
    it('should edit a autoseopage', () => {
      spyOn(component, 'loadIntialData');
      let autoseopage = { uri: '/event', metaTitle: 'bet', metaDescription: 'bet on event' } as AutoSeoPage;
      component.editAutoSeoPage(autoseopage);
      expect(dialogService.showCustomDialog).toHaveBeenCalledWith(
        AutoseoPageDialogComponent, {
        width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
        title: 'Edit Auto Seo Page',
        yesOption: 'Save',
        noOption: 'Cancel',
        data: autoseopage,
        yesCallback: jasmine.any(Function)
      });
      expect(seoAPIService.putAutoSeoItemChanges).toHaveBeenCalled();
      expect(component.loadIntialData).toHaveBeenCalled();
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
        title: 'Upload Completed',
        message: 'AutoSeo Page Changes are Saved.'
      });
    });
    it('should throw error', () => {
      let autoseopage = { uri: '/event', metaTitle: 'bet', metaDescription: 'bet on event' } as AutoSeoPage
      seoAPIService.putAutoSeoItemChanges.and.returnValue(Observable.throw({ message: 'error' }));
      component.editAutoSeoPage(autoseopage);
      expect(component.getDataError).toBeDefined();
    });
  });
  describe('#handleRemoveAutoSeoPage', () => {
    it('should call RemoveAutoSeoPage', () => {
      spyOn(component, 'removeAutoSeoPage');
      const autoseopage = { uri: '/event', metaTitle: 'bet', metaDescription: 'bet on event' } as AutoSeoPage;
      component.autoseoPagesData = [{ uri: '/event', metaTitle: 'bet', metaDescription: 'bet on event' }, { uri: '/competiton', metaTitle: 'bet on competitionname', metaDescription: 'bet on competition' }] as AutoSeoPage[];
      component.handleRemoveAutoSeoPage(autoseopage);
      expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
        title: 'Auto Seo Pages List Change',
        message: 'Are You Sure You Want to Remove This Page?',
        yesCallback: jasmine.any(Function)
      });
      expect(component.removeAutoSeoPage).toHaveBeenCalledWith(autoseopage);
    });
  });
  describe('#RemoveAutoSeoPage', () => {
    it('should remove AutoSeoPage', () => {
      let autoseopage = { id: '2' } as AutoSeoPage;
      component.autoseoPagesData = [{ id: '2' }] as AutoSeoPage[];
      component.removeAutoSeoPage(autoseopage);
      expect(seoAPIService.deleteAutoSeoPage).toHaveBeenCalledWith('2');
      expect(component.autoseoPagesData.length).toBe(0);
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
        title: 'Remove Completed',
        message: 'AutoSeo Page is Removed.'
      });
    });
    it('should not remove autoseopage', () => {
      let autoseopage = { id: '2' } as AutoSeoPage;
      component.autoseoPagesData = [{ id: '3' }] as AutoSeoPage[];
      component.removeAutoSeoPage(autoseopage);
      expect(seoAPIService.deleteAutoSeoPage).not.toHaveBeenCalled();
      expect(component.autoseoPagesData.length).toBe(1);
      expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
        title: 'Remove Completed',
        message: 'AutoSeo Page is Removed.'
      });
    });
    it('should throw error', () => {
      let autoseopage = { id: '2' } as AutoSeoPage;
      component.autoseoPagesData = [{ id: '2' }] as AutoSeoPage[];
      seoAPIService.deleteAutoSeoPage.and.returnValue(Observable.throw({ message: 'error' }));
      component.removeAutoSeoPage(autoseopage);
      expect(component.getDataError).toBeDefined();
    });
  });
});
