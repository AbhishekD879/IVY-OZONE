import { ParticipantCreateComponent } from './participant-create.component';

describe('ParticipantCreateComponent', () => {
  let component: ParticipantCreateComponent;
  let dialogRef;

  beforeEach(() => {
    dialogRef = {};

    component = new ParticipantCreateComponent(
      dialogRef
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.participant).toBeDefined();
    expect(component.form).toBeDefined();
  });
});
