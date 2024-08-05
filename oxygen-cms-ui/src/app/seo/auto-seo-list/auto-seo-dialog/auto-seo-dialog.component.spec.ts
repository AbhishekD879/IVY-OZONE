import { async } from '@angular/core/testing';
import { AutoSeoPage } from '@app/client/private/models/seopage.model';
import { AutoseoPageDialogComponent } from './auto-seo-dialog.component';

describe('AutoSeoDialogComponent', () => {
  let component: AutoseoPageDialogComponent;
  let dialogRef;
  let brandService;
  let dialog;
  beforeEach(async(() => {
    dialogRef = { close: jasmine.createSpy('close') };
    brandService = {};
    dialog = { data: { id: '' } };
    component = new AutoseoPageDialogComponent(dialogRef, brandService, dialog);
  }));


  it('should create', () => {
    expect(component).toBeTruthy();
  });
  describe('#ngOnInit', () => {
    it('should define newAutoSeoPage', () => {
      component.ngOnInit();
      expect(component.newAutoSeoPage).toBeDefined();
      expect(component.dailogTitle).toEqual('Create a New AutoSeo Page');
    });
    it('should define autoseoPage', () => {
      dialog.data.id = '1';
      component.ngOnInit();
      expect(component.autoseoPage).toBeDefined();
      expect(component.dailogTitle).toEqual('Edit a Auto Seo Page');
    });
  });
  describe('#isValidUrl', () => {
    it('should be 0 if uri.length is 0', () => {
      let autoseopage = { uri: '' };
      const result = component.isValidUrl(autoseopage.uri);
      expect(result).toBeFalse();
    });
    it('should be 0 if does not match as requrired', () => {
      let autoseopage = { uri: '1' };
      const result = component.isValidUrl(autoseopage.uri);
      expect(result).toBeFalse();
    });
    it('should be 0 if does not match as requrired', () => {
      let autoseopage = { uri: '/event' };
      const result = component.isValidUrl(autoseopage.uri);
      expect(result).toBeTrue();
    });
  });
  describe('#isValidFormData', () => {
    it('should return 0 if all parameters are null', () => {
      let autoseopage = { uri: '', metaTitle: '', metaDescription: '' } as AutoSeoPage;
      const result = component.isValidFormData(autoseopage);
      expect(result).toBeFalse();
    });
    it('should return 0 if metaTitle parameter is null', () => {
      let autoseopage = { uri: '/', metaTitle: '', metaDescription: 'bet' } as AutoSeoPage;
      const result = component.isValidFormData(autoseopage);
      expect(result).toEqual(0);
    });
    it('should return 0 if metaDescription parameter is null', () => {
      let autoseopage = { uri: '/', metaTitle: 'bet', metaDescription: '' } as AutoSeoPage;
      const result = component.isValidFormData(autoseopage);
      expect(result).toEqual(0);
    });
    it('should return 0 if uri  parameter is not matched', () => {
      let autoseopage = { uri: 'one', metaTitle: 'bet', metaDescription: 'bet on event' } as AutoSeoPage
      const result = component.isValidFormData(autoseopage);
      expect(result).toBeFalse();
    });
    it('should return 1 if all parameters are true', () => {
      let autoseopage = { uri: '/', metaTitle: 'bet', metaDescription: 'bet on event' } as AutoSeoPage
      const result = component.isValidFormData(autoseopage);
      expect(result).not.toEqual(0);
    });
  });
  it('closeDialog should call close()', () => {
    spyOn(component, 'closeDialog').and.callFake(function () {
      return dialogRef.close();
    });
    component.closeDialog();
    expect(dialogRef.close).toHaveBeenCalled();
  });
});
