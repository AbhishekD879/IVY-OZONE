import { CreateLeagueDialogComponent } from './create-league-dialog.component';

describe('CreateLeagueDialogComponent', () => {
  let component: CreateLeagueDialogComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};

    component = new CreateLeagueDialogComponent(
      dialogRef, brandService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.league).toBeDefined();
  });
});
