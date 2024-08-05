import { BackButtonDirective } from '@shared/directives/back-button.directive';

describe('BackButtonDirective', () => {
  let directive: BackButtonDirective;

  const backButtonService = {
      redirectToPreviousPage: jasmine.createSpy()
    } as any;

  beforeEach(() => {
    directive = new BackButtonDirective(backButtonService);
  });

  it('should create an instance', () => {
    expect(directive).toBeTruthy();
  });

  it('should call redirectToPreviousPage', () => {
    directive.redirect();
    expect(backButtonService.redirectToPreviousPage).toHaveBeenCalled();
  });
});
