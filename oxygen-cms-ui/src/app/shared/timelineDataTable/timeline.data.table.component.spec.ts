import { TimelineDataTableComponent } from '@app/shared/timelineDataTable/timeline.data.table.component';

describe('TimelineDataTableComponent', () => {
  let component,
    sortableTableService;

  beforeEach(() => {
    sortableTableService = {};

    component = new TimelineDataTableComponent(
      sortableTableService
    );
  });

  it('should init customTableColumns', () => {
    component.customTableData = [{
      name: 'nameMock'
    }];
    component.ngOnInit();

    expect(component.customTableColumns.length).toEqual(1);
  });

  it('should not init customTableColumns', () => {
    component.ngOnInit();

    expect(component.customTableColumns.length).toEqual(0);
  });
});
