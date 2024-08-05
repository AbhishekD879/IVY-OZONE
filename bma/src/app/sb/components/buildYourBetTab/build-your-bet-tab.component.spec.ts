import { BuildYourBetTabComponent } from '@sb/components/buildYourBetTab/build-your-bet-tab.component';

describe('BuildYourBetTabComponent', () => {
  let component: BuildYourBetTabComponent;

  beforeEach(() => {
    component = new BuildYourBetTabComponent();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should set isBuildYourBetTabShown to true when ngOnInit invoked', () => {
    component.ngOnInit();

    expect(component.isBuildYourBetTabShown).toBeTruthy();
  });
});
