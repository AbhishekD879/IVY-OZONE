import { TimelineActionButtonsComponent } from './timeline-action-buttons.component';

describe('TimelineActionButtonsComponent', () => {
  let component,
    dialogService;

  beforeEach(() => {
    dialogService = {};

    component = new TimelineActionButtonsComponent(
      dialogService
    );
  });

  it('should create', () => {
    component.nameField = 'nameFieldMock';
    component.collection = {};

    component.ngOnInit();

    expect(component.actionCollection).toBeDefined();
  });
});
