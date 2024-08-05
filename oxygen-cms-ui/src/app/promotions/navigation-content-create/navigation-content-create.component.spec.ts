
import { of } from 'rxjs';

import { NavigationContentCreateComponent } from './navigation-content-create.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';

describe('NavigationContentCreateComponent', () => {
  let component: NavigationContentCreateComponent;
  let globalLoaderService;
  let dialogService;
  let activatedRoute;
  let router;
  let apiClientService;
  let mockNavTypeContent;

  beforeEach(() => {
    mockNavTypeContent = {
      name: 'Cricket2',
      navType: 'url',
      url: null,
      leaderboardId: null,
      descriptionTxt: null,
      navigationGroupId: '62c80d5cbc54f74ed94d52d9'
    };
    

    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog')
    };

    activatedRoute = {
      params: of({ 'id': '123' })
    };

    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    router = {
      navigate: jasmine.createSpy('navigate'),
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };

    apiClientService = {
      promotionsNavigationsService: jasmine.createSpy('promotionsNavigationsService').and.returnValue({
        remove: jasmine.createSpy('remove').and.returnValue(of({ body: [] })),
        getNavListById: jasmine.createSpy('getNavListById').and.returnValue(of({ body: [] })),
        removeNavContent: jasmine.createSpy('removeNavContent').and.returnValue(of({ body: [] })),
        postNavContent: jasmine.createSpy('postNavContent').and.returnValue(of({ body: [] })),
        updateNavContent: jasmine.createSpy('updateNavContent').and.returnValue(of({ body: mockNavTypeContent as any })),
      })
    };
    component = new NavigationContentCreateComponent(
      globalLoaderService, apiClientService, activatedRoute, dialogService, router
    );

    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any as ActionButtonsComponent;
  });

  it('constructor', () => {
    expect(component).toBeDefined();
  });


  describe('isValidForm', () => {
    it('isValidForm if form has no title field', () => {

      mockNavTypeContent.leaderboardId = null;
      mockNavTypeContent.description = null;
      component.isValidForm();

      expect(component.isValidForm()).toBeFalsy();
    });
  });

  describe('isValidModel', () => {
    it('isValidModel if form has no title field', () => {

      mockNavTypeContent.leaderboardId = null;
      mockNavTypeContent.description = null;
      component.isValidModel(mockNavTypeContent);

      expect(component.isValidModel(mockNavTypeContent)).toBeFalsy();
    });
  });

  describe('actionsHandler', () => {
    it('if event is save', () => {
      const spySaveNavContent = spyOn(component, 'updateNavContent');

      component.actionsHandler('save');

      expect(spySaveNavContent).toHaveBeenCalled();
    });
    it('if event is remove', () => {
      const spyRemoveNavigationGroups = spyOn(component, 'removeNavContent');

      component.actionsHandler('remove');

      expect(spyRemoveNavigationGroups).toHaveBeenCalled();
    });
    it('if event is revert', () => {
      const spyRevertNavContent = spyOn(component, 'revertNavContent');

      component.actionsHandler('revert');

      expect(spyRevertNavContent).toHaveBeenCalled();
    });
    it('default action', () => {
      const spyConsole = spyOn(console, 'error');

      component.actionsHandler('revert11');

      expect(spyConsole).toHaveBeenCalled();
    });
  });

  describe('saveNavContent', () => {

    it('saveNavContent', fakeAsync(() => {

      component.navTypeContent = mockNavTypeContent;
      component.saveNavContent();
      tick();
      tick();
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    }));
  });

});
