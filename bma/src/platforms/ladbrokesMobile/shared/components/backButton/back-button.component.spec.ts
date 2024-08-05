import { BackButtonComponent } from '@ladbrokesMobile/shared/components/backButton/back-button.component';

describe('BackButtonComponent', () => {
  let component: BackButtonComponent;

  const backButtonService = {
    redirectToPreviousPage: jasmine.createSpy('redirectToPreviousPage')
  } as any;

  beforeEach(() => {
    component = new BackButtonComponent(backButtonService);
  });

  it('should create an instance', () => {
    expect(component).toBeTruthy();
  });
});
