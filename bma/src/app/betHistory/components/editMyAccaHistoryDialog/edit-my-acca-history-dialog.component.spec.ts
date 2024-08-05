import { EditMyAccaHistoryDialogComponent } from './edit-my-acca-history-dialog.component';

describe('EditMyAccaHistoryDialogComponent', () => {
  let deviceService, windowRef;
  let component: EditMyAccaHistoryDialogComponent;

  beforeEach(() => {
    deviceService = {};
    windowRef = {
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('add')
          }
        }
      }
    };

    component = new EditMyAccaHistoryDialogComponent(
      deviceService, windowRef
    );
    component.dialog = { changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') } };
  });

  it('open', () => {
    component.params = { open: jasmine.createSpy() };
    component.open();
    expect(component.params.open).toHaveBeenCalledTimes(1);
  });
});
