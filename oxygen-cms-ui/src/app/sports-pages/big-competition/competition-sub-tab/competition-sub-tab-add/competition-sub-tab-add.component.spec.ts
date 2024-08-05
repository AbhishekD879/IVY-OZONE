import { CompetitionSubTabAddComponent } from './competition-sub-tab-add.component';

describe('CompetitionSubTabAddComponent', () => {
  let component: CompetitionSubTabAddComponent;
  let dialogRef, brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};

    component = new CompetitionSubTabAddComponent(dialogRef, brandService);
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.tab).toBeTruthy();
    expect(component.form).toBeTruthy();
  });
});
