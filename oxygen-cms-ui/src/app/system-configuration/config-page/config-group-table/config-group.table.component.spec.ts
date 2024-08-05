import {ConfigGroupTableComponent} from './config-group.table.component';

describe('ConfigGroupTableComponent', () => {
  let component: ConfigGroupTableComponent;
  let dialogService;
  beforeEach(() => {
    dialogService = {};
    component = new ConfigGroupTableComponent(
      dialogService
    );
    component.configGroup = {id: 1} as any;
    component.ngOnInit();
  });

  it('should set initial data', () => {
    expect(component.configGroupBackup).toEqual(component.configGroup);
  });
});
