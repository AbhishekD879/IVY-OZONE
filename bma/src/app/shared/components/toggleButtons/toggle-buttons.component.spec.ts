import { ToggleButtonsComponent } from '@shared/components/toggleButtons/toggle-buttons.component';

describe('ToggleButtonsComponent', () => {
  let component: ToggleButtonsComponent;

  beforeEach(() => {
    component = new ToggleButtonsComponent();

    component.toggleData.emit = jasmine.createSpy('emit');
    component.selectedBtn = '';
  });

  it('toggleBtnOnClick', () => {
    const btnVal = 'btnVal';
    component.toggleBtnOnClick(btnVal);

    expect(component.selectedBtn).toEqual(btnVal);
    expect(component['toggleData'].emit).toHaveBeenCalledWith(btnVal);
  });

  it('trackByIndex', () => {
    const index = 1;
    const result = component.trackByIndex(index);

    expect(result).toEqual(index);
  });
});
