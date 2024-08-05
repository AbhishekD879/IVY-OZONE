import {KnockoutsModuleComponent} from './knockouts-module.component';

describe('KnockoutsModuleComponent', () => {
  let component;

  beforeEach(() => {
    component = new KnockoutsModuleComponent();

    component.ngOnInit();
  });

  it('should create', () => {
    spyOn(component.changed, 'emit');

    const dataMock = {};

    component.handleModuleChange(dataMock);

    expect(component.changed.emit).toHaveBeenCalledWith(dataMock);
  });
});
