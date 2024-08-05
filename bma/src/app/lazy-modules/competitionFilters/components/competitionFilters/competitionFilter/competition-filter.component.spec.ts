import { CompetitionFilterComponent } from './competition-filter.component';

describe('CompetitionFilterComponent', () => {
  let component: CompetitionFilterComponent;

  beforeEach(() => {
    component = new CompetitionFilterComponent();
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('#onFilterSelect', () => {
    it('should emin filterChange and change active property in filter', () => {
      const filter = {
        id: '1',
        active: false,
        name: '1h',
        type: 'Time',
        value: 1
      };
      component.filterChange.emit = jasmine.createSpy('emit');
      component.onFilterSelect(filter as any);


      expect(component.filterChange.emit).toHaveBeenCalledWith({
        id: '1',
        active: true,
        name: '1h',
        type: 'Time',
        value: 1
      });
    });
  });
});
