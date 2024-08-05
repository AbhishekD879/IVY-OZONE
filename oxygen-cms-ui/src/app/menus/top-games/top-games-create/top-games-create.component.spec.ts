import { TopGamesCreateComponent } from './top-games-create.component';

describe('TopGamesCreateComponent', () => {
  let component: TopGamesCreateComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};

    component = new TopGamesCreateComponent(
      dialogRef, brandService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.topGame).toBeDefined();
    expect(component.form).toBeDefined();
  });
});
