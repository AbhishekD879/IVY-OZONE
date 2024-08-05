import {CMSDataTableComponent} from './cms.data.table.component';

describe('CMSDataTableComponent', () => {
  let component,
    sortableTableService,
    sanitizer,
    snackBar;

  beforeEach(() => {
    sortableTableService = {};
    sanitizer = {};

    component = new CMSDataTableComponent(
      sortableTableService,
      sanitizer,
      snackBar
    );
  });

  it('should create customTableColumns', () => {
    component.customTableData = [
      {
        name: 'Name'
      }
    ];

    component.ngOnInit();

    expect(component.customTableColumns.length).toEqual(1);
  });

  it('should not create customTableColumns', () => {
    component.ngOnInit();

    expect(component.customTableColumns.length).toEqual(0);
  });
});
