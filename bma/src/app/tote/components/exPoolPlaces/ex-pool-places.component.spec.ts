import { ExPoolPlacesComponent } from './ex-pool-places.component';

describe('ExPoolPlacesComponent', () => {
  let component: ExPoolPlacesComponent;

  const exTrCheckboxMap  = {
    '1' : ['checked', 'checked'],
    '12' : ['checked', 'checked'],
    '13' : ['unchecked', 'checked'],
    '14' : ['enabled', 'checked'],
    '15' : ['checked', 'checked', 'unchecked'],
    '16' : ['checked', 'unchecked', 'checked'],
  } as any;

  beforeEach(() => {
    component = new ExPoolPlacesComponent();
    component.map = exTrCheckboxMap;

    spyOn(component.checkFn, 'emit');
  });

  it('onChange', () => {
    component.onChange();

    expect(component.checkFn.emit).toHaveBeenCalled();
  });

  it('runChecks', () => {
    component.setEnables = jasmine.createSpy('setEnables');
    component.setDisables = jasmine.createSpy('setDisables');
    component.selectedPlaces = {};

    component.runChecks(exTrCheckboxMap);

    expect(component.setEnables).toHaveBeenCalled();
    expect(component.outcomeIds).toEqual(['16', '15', '16']);
    expect(component.selectedPlaces.status).toBeTruthy();
    expect(component.checkFn.emit).toHaveBeenCalled();
    expect(component.setDisables).toHaveBeenCalledTimes(10);
  });


  describe('setEnables/Disables', () => {
    const mapMock = {
      '1' : ['unchecked'],
      '2' : ['checked'],
      '3' : ['checked']
    } as any;

    it('setEnables', () => {
      component.setEnables(mapMock);

      expect(mapMock).toEqual({
        '1' : ['enabled'],
        '2' : ['checked'],
        '3' : ['checked']
      });
    });

    it('setDisables', () => {
      component.setDisables(mapMock, '1', 0);

      expect(mapMock).toEqual({
        '1' : ['disabled'],
        '2' : ['checked'],
        '3' : ['checked']
      });
    });
  });

  it('checkPlace', () => {
    spyOn(component, 'runChecks');

    component.checkPlace('1', 0);

    expect(component.runChecks).toHaveBeenCalled();
    expect(component.map['1'][0]).toEqual('enabled');

    component.checkPlace('14', 0);

    expect(component.map['14'][0]).toEqual('checked');
  });

  it('trackByIndex', () => {
    const result = component.trackByIndex(1);

    expect(result).toEqual(1);
  });
});
