import { ConfigTableComponent } from './configTable.component';

describe('ConfigTableComponent', () => {
  let component: ConfigTableComponent;
  let dialogService, apiClientService, snackBar;

  beforeEach(() => {
    dialogService = {};
    apiClientService = {};
    snackBar = {};
    component = new ConfigTableComponent(
      dialogService, apiClientService, snackBar
    );

    component.configItem = {items: [{type: 'svg', realValue: ''}, {type: 'file'}]};
    component.ngOnInit();
  });

  it('should addFileToRowItem', () => {
    expect(component.configItem.items[0].filename).toBeDefined();
    expect(component.configItem.items[1].filename).not.toBeDefined();
  });
});
