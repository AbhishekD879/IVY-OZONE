import { of } from 'rxjs';

import { UsersComponent } from './users.component';

describe('UsersComponent', () => {
  let component: UsersComponent;
  let userService;
  let apiClientService;
  let dialogService;
  let fullNamePipe;
  let globalLoaderService;


  beforeEach(() => {
    userService = {
      retrieveAllUsers: jasmine.createSpy('retrieveAllUsers').and.returnValue(of({ body: [] }))
    };
    apiClientService = {
      user: () => userService
    };
    dialogService = {};
    fullNamePipe = {
      transform: jasmine.createSpy('transform')
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    component = new UsersComponent(
      apiClientService, dialogService, fullNamePipe, globalLoaderService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(userService.retrieveAllUsers).toHaveBeenCalled();
  });
});
