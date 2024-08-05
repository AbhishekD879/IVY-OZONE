import { BppErrorDialogComponent } from './bpp-error-dialog.component';

describe('BppErrorDialogComponent', () => {
  let deviceService, windowRef;
  let component: BppErrorDialogComponent;

  beforeEach(() => {
    deviceService = {};
    windowRef = {};

    component = new BppErrorDialogComponent(deviceService, windowRef);
    component.params = { error: 'noConnection' };
  });

  it('getHeaderTitle', () => {
    expect(component.getHeaderTitle()).toBe(`bpp.${component.params.error}Header`);
  });

  it('getBodyMessage', () => {
    expect(component.getBodyMessage()).toBe(`bpp.${component.params.error}Message`);
  });
});
