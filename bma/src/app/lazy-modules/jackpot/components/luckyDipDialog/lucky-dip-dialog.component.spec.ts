import { LuckyDipDialogComponent } from './lucky-dip-dialog.component';

describe('LuckyDipDialogComponent', () => {
  let component: LuckyDipDialogComponent;
  let device;
  let windowRef;

  beforeEach(() => {
    device = jasmine.createSpyObj('device', ['path']);
    windowRef = {};
    component = new LuckyDipDialogComponent(device, windowRef);
  });

  it('makeLuckyDip should call correct methodlive-stream-home-tab.components', () => {
    component.params = jasmine.createSpyObj('params', ['makeLuckyDip']);
    spyOn(component, 'closeDialog');

    component.makeLuckyDip();

    expect(component.params.makeLuckyDip).toHaveBeenCalled();
    expect(component.closeDialog).toHaveBeenCalled();
  });
});
