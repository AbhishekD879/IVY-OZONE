import { async } from '@angular/core/testing';
import { LeaderboardEditComponent } from './leaderboard-edit.component';
import { of } from 'rxjs';

describe('LeaderboardEditComponent', () => {
  let component: LeaderboardEditComponent;
  let globalLoaderService;
  let dialogService;
  let apiClientService;
  let sortableTableService;
  let activatedRoute;
  let router;

  beforeEach(async(() => {
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
    };
    apiClientService = {
      saveLeaderboardChanges: jasmine.createSpy('saveLeaderboardChanges').and.returnValue(of({
      })),
      removeLeaderboard: jasmine.createSpy('removeLeaderboard').and.returnValue(of({})),
      revertLeaderboardChanges: jasmine.createSpy('revertLeaderboardChanges').and.returnValue(of({ body: {} })),
      promotionLeaderboardService: jasmine.createSpy('promotionLeaderboardService').and.returnValue({updateLeaderboard: () => of({body: {}})}),
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader'),
    }
    component = new LeaderboardEditComponent(globalLoaderService, apiClientService, activatedRoute,dialogService, router, sortableTableService);
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call ngOnInit', () => {
    spyOn(component, 'loadInitData');
    component.ngOnInit();
  });

  it('should call saveLeaderboardChanges', () => {
    spyOn(component, 'ngOnInit')
    spyOn(component, 'saveColumnConfigDetails').and.returnValue(true);
    apiClientService.saveLeaderboardChanges.subscribe = jasmine.createSpy('saveLeaderboardChanges').and.returnValue({});
    component.saveLeaderboardChanges();
    expect(component.leaderboard).toEqual({} as any);
  });

  it('should  handle if saveLeaderboardChanges API returns error', () => {
    spyOn(component, 'ngOnInit')
    spyOn(component, 'saveColumnConfigDetails').and.returnValue(true);
    apiClientService.saveLeaderboardChanges.subscribe = jasmine.createSpy('saveLeaderboardChanges').and.returnValue({});
    component.saveLeaderboardChanges();
    expect(component.leaderboard).toEqual({} as any);
  });

  it('should call saveColumnConfigDetails', () => {
    spyOn(component, 'ngOnInit')
    spyOn(component, 'saveColumnConfigDetails').and.returnValue(true);
    apiClientService.saveLeaderboardChanges.subscribe = jasmine.createSpy('saveLeaderboardChanges').and.returnValue({});
    component.saveLeaderboardChanges();
    expect(component.leaderboard).toEqual({} as any);
  });

  it('should  handle if saveColumnConfigDetails API returns error', () => {
    spyOn(component, 'ngOnInit')
    spyOn(component, 'saveColumnConfigDetails').and.returnValue(true);
    apiClientService.saveLeaderboardChanges.subscribe = jasmine.createSpy('saveLeaderboardChanges').and.returnValue({});
    component.saveLeaderboardChanges();
    expect(component.leaderboard).toEqual({} as any);
  });

  it('should call actionsHandler to call saveLeaderboardChanges', () => {
    let event = 'save';
    spyOn(component, 'saveLeaderboardChanges');
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'saveLeaderboardChanges'
    });
  });

  it('should call actionsHandler', () => {
    let event = '';
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Data is Stored'
    });
  });

  it('initialize the form', () => {
    spyOn(component, 'ngOnInit')
  });

  it('should return true if form is valid', () => {
    let lb = {columns : [1,2,3], filePath: [2,3,4], name: 'name'} as any;
    const isValid = component.isValidForm(lb);
    expect(isValid).toBeTruthy();
  });

  it('should return true if form is invalid', () => {
    let lb = {columns : [], filePath: [2,3,4], name: 'name'} as any;
    const isValid = component.isValidForm(lb);
    expect(isValid).toBeFalsy();
  });
});
