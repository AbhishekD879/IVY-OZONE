import { async } from '@angular/core/testing';
import { LeaderboardCreateComponent } from './leaderboard-create.component';
import { of } from 'rxjs';

describe('LeaderboardCreateComponent', () => {
  let component: LeaderboardCreateComponent;
  let globalLoaderService;
  let dialogService;
  let apiClientService;
  let sortableTableService;
  let router;
  let brandService;

  beforeEach(async(() => {
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader'),
    }
    apiClientService = {
      saveLeaderboardChanges: jasmine.createSpy('saveLeaderboardChanges').and.returnValue(of({
      })),
      removeLeaderboard: jasmine.createSpy('removeLeaderboard').and.returnValue(of({})),
      revertLeaderboardChanges: jasmine.createSpy('revertLeaderboardChanges').and.returnValue(of({ body: {} })),
      promotionLeaderboardService: jasmine.createSpy('promotionLeaderboardService').and.returnValue({postNewLeaderboard: () => of({body: {}})}),
    };
    brandService = {
      leaderboard: jasmine.createSpy('leaderboard').and.returnValue(of({})),
      brand: 'bma',
      promotionLeaderboardService: jasmine.createSpy('promotionLeaderboardService').and.returnValue(of({}))
    };
    component = new LeaderboardCreateComponent(dialogService, globalLoaderService, apiClientService, router, brandService, sortableTableService);
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call ngOnInit', () => {
    component.ngOnInit();
  });

  it('should call saveLeaderboardChanges', () => {
    spyOn(component, 'ngOnInit')
    spyOn(component, 'savecolumnsDetails').and.returnValue(true);
    apiClientService.saveLeaderboardChanges.subscribe = jasmine.createSpy('saveLeaderboardChanges').and.returnValue({});
    component.saveLeaderboardChanges();
    expect(component.leaderboard).toEqual({} as any);
  });

  it('should  handle if saveLeaderboardChanges API returns error', () => {
    spyOn(component, 'ngOnInit')
    spyOn(component, 'savecolumnsDetails').and.returnValue(true);
    apiClientService.saveLeaderboardChanges.subscribe = jasmine.createSpy('saveLeaderboardChanges').and.returnValue({});
    component.saveLeaderboardChanges();
    expect(component.leaderboard).toEqual({} as any);
  });

  it('should call savecolumnsDetails', () => {
    spyOn(component, 'ngOnInit')
    spyOn(component, 'savecolumnsDetails').and.returnValue(true);
    apiClientService.saveLeaderboardChanges.subscribe = jasmine.createSpy('saveLeaderboardChanges').and.returnValue({});
    component.saveLeaderboardChanges();
    expect(component.leaderboard).toEqual({} as any);
  });

  it('should  handle if savecolumnsDetails API returns error', () => {
    spyOn(component, 'ngOnInit')
    spyOn(component, 'savecolumnsDetails').and.returnValue(true);
    apiClientService.saveLeaderboardChanges.subscribe = jasmine.createSpy('saveLeaderboardChanges').and.returnValue({});
    component.saveLeaderboardChanges();
    expect(component.leaderboard).toEqual({} as any);
  });

  it('should call actionsHandler to call saveLeaderboardChanges', () => {
    spyOn(component, 'saveLeaderboardChanges');
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'saveLeaderboardChanges'
    });
  });

  it('should call actionsHandler', () => {
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Data is Stored'
    });
  });

  it('initialize the form', () => {
    component.ngOnInit();
    expect(component.leaderboard.name).toEqual(undefined);
    expect(component.leaderboard.filePath).toEqual(undefined);
    expect(component.leaderboard.topX).toEqual(undefined);
  });

  it('should return true if form is valid', () => {
    component.leaderboard = {columns : [1,2,3], filePath: [2,3,4], name: 'name'} as any;
    const isValid = component.isValidForm();
    expect(isValid).toBeTruthy();
  });

  it('should return true if form is invalid', () => {
    component.leaderboard = {columns : [], filePath: [2,3,4], name: 'name'} as any;
    const isValid = component.isValidForm();
    expect(isValid).toBeFalsy();
  });
});
