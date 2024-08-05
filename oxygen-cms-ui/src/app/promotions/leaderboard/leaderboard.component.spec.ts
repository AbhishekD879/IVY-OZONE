import { async } from '@angular/core/testing';
import { LeaderboardComponent } from './leaderboard.component';
import { of } from 'rxjs';

describe('LeaderboardComponent', () => {
  let component: LeaderboardComponent;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let router;

  beforeEach(async(() => {
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ yesCallback }) => yesCallback())
    };
    apiClientService = {
      saveLeaderboardChanges: jasmine.createSpy('saveLeaderboardChanges').and.returnValue(of({
      })),
      removeLeaderboard: jasmine.createSpy('removeLeaderboard').and.returnValue(of({})),
      findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({})),
      hideSpinner: jasmine.createSpy('hideSpinner').and.returnValue(of({})),
      promotionLeaderboardService: jasmine.createSpy('promotionLeaderboardService').and.returnValue({remove: () => of({body: {}})}),
    };
    globalLoaderService = {
        showLoader: jasmine.createSpy('showLoader').and.returnValue(of({})),
        hideLoader: jasmine.createSpy('hideLoader').and.returnValue(of({}))
      };
      router = {};

    component = new LeaderboardComponent(router, apiClientService, globalLoaderService, dialogService);
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call removeLeaderboard to remove Leaderboard', () => {
    let lb = undefined;
    spyOn(component, 'ngOnInit')
    spyOn(component, 'removeLeaderboard').and.returnValue();
    apiClientService.saveLeaderboardChanges.subscribe = jasmine.createSpy('saveLeaderboardChanges').and.returnValue({});
    component.removeLeaderboard(lb);
    expect(component.leaderboard).toEqual(undefined);
  });

});
