import { CompetitionAddComponent } from './competition-add.component';

describe('CompetitionAddComponent', () => {
  let component: CompetitionAddComponent;
  let spaceToDashPipe;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    spaceToDashPipe = {};
    dialogRef = {};
    brandService = {};

    component = new CompetitionAddComponent(
      spaceToDashPipe, dialogRef, brandService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.competition).toBeDefined();
    expect(component.form).toBeDefined();
  });
});
