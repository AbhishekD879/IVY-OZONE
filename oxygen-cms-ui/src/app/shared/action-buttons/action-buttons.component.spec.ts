import { ActionButtonsComponent } from './action-buttons.component';

describe('ActionButtonsComponent', () => {
  let component,
    dialogService;

  beforeEach(() => {
    dialogService = {};

    component = new ActionButtonsComponent(
      dialogService
    );

    component.collection = {};
    component.ngOnInit();
  });

  it('should init', () => {
    expect(component.actionCollection).toBeDefined();
  });
});
