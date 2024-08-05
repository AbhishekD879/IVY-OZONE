import {RoundNamesAddComponent} from './round-names-add.component';

describe('RoundNamesAddComponent', () => {
  let component,
    data,
    dialog;

  beforeEach(() => {
    data = {
      rounds: []
    };
    dialog = {};

    component = new RoundNamesAddComponent(
      data,
      dialog
    );

    component.ngOnInit();
  });

  it('should create', () => {
    expect(component.form).toBeDefined();
  });
});
