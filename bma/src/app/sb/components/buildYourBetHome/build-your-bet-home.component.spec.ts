import { BuildYourBetHomeComponent } from '@sb/components/buildYourBetHome/build-your-bet-home.component';

describe('BuildYourBetHomeComponent', () => {
  let component: BuildYourBetHomeComponent;

  beforeEach(() => {
    component = new BuildYourBetHomeComponent();
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
