import environment from '@environment/oxygenEnvConfig';
import { LeavingCasinoDialogComponent } from './leaving-casino-info-dialog.component';

describe('LeavingCasinoDialogComponent', () => {
  let component: LeavingCasinoDialogComponent;
  let locale;
  let event;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy().and.returnValue('Ladbrokes')
    };
    event = {
      stopPropagation: jasmine.createSpy('stopPropagation')
    };

    component = new LeavingCasinoDialogComponent(locale);
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('should execute ngOnInit', () => {
    environment.brand = 'ladbrokes';
    component.ngOnInit();
    expect(component['locale'].getString).toHaveBeenCalled();
  });

  it('should execute popupClickHandler', () => {
    component.dontShowPopupAgain = false;
    const userActionSpy = spyOn(component.userAction, 'emit');
    component.popupClickHandler(event, 'no thanks');
    expect(userActionSpy).toHaveBeenCalled();
  });
});
