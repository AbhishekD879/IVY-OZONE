import { StreamBetTemplateDropDownComponent } from './sb-template-drop-down.component';

describe('StreamBetTemplateDropDownComponent', () => {
  let component: StreamBetTemplateDropDownComponent;

  beforeEach(() => {
    component = new StreamBetTemplateDropDownComponent();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should emit outcomeName', () => {
    component.itemEmit.emit = jasmine.createSpy('itemEmit.emit');
    component.onValueChange('TeamA');
    expect(component.itemEmit.emit).toHaveBeenCalledOnceWith('TeamA');
  });

  it('should trackByIndex', () => {
    expect(component.trackByIndex(1)).toEqual(1);
  });
});
