import { CashOutPageWrapperComponent } from './cash-out-page-wrapper.component';

describe('CashOutPageWrapperComponent', () => {
  let component,
      editMyAccaService;
  beforeEach(() => {
    editMyAccaService = {
      canChangeRoute: jasmine.createSpy('editMyAccaService.canChangeRoute').and.returnValue(true),
      showEditCancelMessage: jasmine.createSpy('editMyAccaService.showEditCancelMessage')
    } as any;

    component = new CashOutPageWrapperComponent(editMyAccaService);
  });

  it('#canChangeRoute', () => {
    const result = component.canChangeRoute();

    expect(editMyAccaService.canChangeRoute).toHaveBeenCalled();
    expect(result).toBeTruthy();
  });

  it('#onChangeRoute', () => {
    component.onChangeRoute();

    expect(editMyAccaService.showEditCancelMessage).toHaveBeenCalled();
  });
});
