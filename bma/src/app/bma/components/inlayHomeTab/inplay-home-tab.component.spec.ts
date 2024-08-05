import { InplayHomeTabComponent } from '@bma/components/inlayHomeTab/inplay-home-tab.component';

describe('InplayHomeTabComponent', () => {
  let component: InplayHomeTabComponent;

  beforeEach(() => {
    component = new InplayHomeTabComponent();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
    expect(component.initialized).toBeFalsy();
  });
  it('childComponentLoaded should set initialized to true', () => {
    component.childComponentLoaded();
    expect(component.initialized).toBeTruthy();
  });
});
