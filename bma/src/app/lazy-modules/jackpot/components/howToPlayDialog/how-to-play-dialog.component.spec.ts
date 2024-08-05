import { HowToPlayDialogComponent } from './how-to-play-dialog.component';

describe('HowToPlayDialogComponent', () => {
  let component: HowToPlayDialogComponent;
  let device;
  let windowRef;

  beforeEach(() => {
    device = jasmine.createSpyObj('device', ['path']);
    windowRef = {};

    component = new HowToPlayDialogComponent(device, windowRef);
  });

  it('init', () => {
    expect(component).toBeDefined();
  });
});
