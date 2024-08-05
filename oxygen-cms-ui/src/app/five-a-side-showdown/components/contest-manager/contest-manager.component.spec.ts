import { of } from 'rxjs';
import { CONTESTS, CREATE_CONTEST_MOCK, REMOVE_CONTEST_MOCK, REORDER_MOCK
} from '@app/five-a-side-showdown/components/contest-manager/contests.mock';

import { ContestManagerComponent } from '@app/five-a-side-showdown/components/contest-manager/contest-manager.component';
import { throwError } from 'rxjs';
import { EDIT_CONTEST_MOCK } from '@app/five-a-side-showdown/components/edit-contest/edit-contest.mock';
import { REMOVE_CONFIRMATION_DIALOG } from '@app/five-a-side-showdown/constants/contest-manager.constants';

describe('ContestManagerComponent', () => {
  let component: ContestManagerComponent;
  let router;
  let globalLoaderService;
  let apiClientService;
  let dialogService;
  let contestManagerService;
  let snackbar;
  let errorService;

  beforeEach(() => {
    router = {
      navigate: jasmine.createSpy('navigate'),
      url: '/five-a-side-showdown/'
    };
    errorService  = {
      emitError:  jasmine.createSpy('emitError')
    }
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ title, message, yesCallback }) => yesCallback()),
      showCustomDialog: jasmine.createSpy('showCustomDialog').and
        .callFake((AddContestComponent,{width, title, yesOption, noOption, yesCallback}) => 
        yesCallback(CONTESTS[0]))
    };
    contestManagerService = {
      getContests: jasmine.createSpy('getContests').and.returnValue(of({
        body: CONTESTS
      })),
      createContest: jasmine.createSpy('createContest').and.returnValue(of({
        body: CREATE_CONTEST_MOCK
      })),
      removeContestForId : jasmine.createSpy('removeContestForId').and.returnValue(of({
        body: REMOVE_CONTEST_MOCK
      })),
      postNewOrder : jasmine.createSpy('postNewOrder').and.returnValue(of({
        body: []
      }))
    };
    apiClientService = {
      contestManagerService: () => contestManagerService
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    snackbar = {
      open: jasmine.createSpy('open')
    } as any;
    component = new ContestManagerComponent(
      router,
      globalLoaderService,
      dialogService,
      apiClientService,
      snackbar,
      errorService
    )
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should fetch contests data on init', () => {
      spyOn(component as any, 'showHideSpinner');
      component.ngOnInit();
      expect(component.isLoading).toBe(false);
      expect(component.contests).toEqual(CONTESTS);
    });
    it('should not fetch contests if the service returns error', () => {
      contestManagerService.getContests = jasmine.createSpy().and.returnValue(throwError({error: '401'}));
      spyOn(component as any, 'showHideSpinner');
      component.ngOnInit();
      expect(component['showHideSpinner']).toHaveBeenCalledWith(false);
    });
  });

  describe('#showHideSpinner', () => {
    it('should show loader when we pass true', () => {
      component['showHideSpinner']();
      expect(component.isLoading).toBeTruthy();
    });
    it('should not show loader when we pass false', () => {
      component['showHideSpinner'](false);
      expect(component.isLoading).toBeFalsy();
    });
  });

  describe('#removeContestElement', () => {
    it('should remove the contest based on the provided name', () => {
      component.contests = [{id:'abc123'},{id:'123'},{id:'456'}] as any;
      component['removeContestElement'](EDIT_CONTEST_MOCK);
      expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
        title: REMOVE_CONFIRMATION_DIALOG.title,
        message: `${REMOVE_CONFIRMATION_DIALOG.message} ${EDIT_CONTEST_MOCK.name}`,
        yesCallback: jasmine.any(Function)
      });
      expect(component.contests as any).toEqual([{id:'123'},{id:'456'}])
    });
  });
  describe('#reorderHandler', () => {
    it('should re order the contests based on the selected order', () => {
      component['reorderHandler'](REORDER_MOCK);
      expect(globalLoaderService['hideLoader']).toHaveBeenCalled();
      expect(snackbar.open).toHaveBeenCalled();
    });
  });

  describe('#createContestModule', () => {
    it('should create the contest (Case: Success)', () => {
      component['createContestModule']();
      expect(dialogService.showCustomDialog).toHaveBeenCalled();
      expect(router.navigate).toHaveBeenCalled();
    });
    it('should create the contest (Case: Failure)', () => {
      contestManagerService.createContest.and.returnValue(throwError({error: '401'}));
      component['createContestModule']();
      expect(component.isLoading).toBe(false);
    });
  });

  describe('#removeHandlerMulty', () => {
    it('should remove multiple records', () => {
      component.contests = [{id:'34'},{id:'123'},{id:'456'}] as any;
      component.removeHandlerMulty(['123', '456']);
      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
      expect(component.contests as any).toEqual([{id:'34'}])
    });
  });
  
});
