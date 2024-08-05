import {
  ForecastTricastCheckboxMatrixComponent
} from '@lazy-modules/forecastTricast/components/forecastTricastCheckboxMatrix/forecast-tricast-checkbox-matrix.component';
import {
  forecastTricatMatrixMock as mock
} from '@lazy-modules/forecastTricast/components/forecastTricastCheckboxMatrix/forecast-tricast-checkbox-matrix-mock';

describe('ForecastTricastCheckboxMatrixComponent', () => {
  let component: ForecastTricastCheckboxMatrixComponent;

  beforeEach(() => {
    createComponent();
    const mapMock = {
      532178415: {
        '1st': 'checked',
        '2nd': 'disabled',
        'any': 'disabled'
      },
      532178416: {
        '1st': 'disabled',
        '2nd': 'open',
        'any': 'open'
      }
    };
    component.map = mapMock;
  });

  function createComponent() {
    component = new ForecastTricastCheckboxMatrixComponent();
  }

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('trackByCheckBox', () => {
    expect(component.trackByCheckBox(0, {key: '1st', value: 'open'})).toEqual('01stopen');
  });

  it('checkBoxMatrix', () => {
    component.outcome = {
      id: '532178415'
    } as any;
    const checkBoxMatrix = [
      {key: '1st', value: 'checked'},
      {key: '2nd', value: 'disabled'},
      {key: 'any', value: 'disabled'}
    ];

    expect(component.checkBoxMatrix).toEqual(checkBoxMatrix);
  });

  it('getCssClass', () => {
    component.isSuspended = true;
    component.outcome = {
      nonRunner: false
    } as any;
    expect(component.getCssClass({key: '1st', value: 'open'})).toEqual('open disabled ');

    component.isSuspended = false;
    component.outcome = {
      nonRunner: true
    } as any;
    expect(component.getCssClass({key: '1st', value: 'open'})).toEqual('open  non-runner');
  });

  describe('checkPlace', () => {
    it('should disable row and column', () => {
      const id = '532178415';
      component.map = JSON.parse(JSON.stringify(mock.beforeFirstSelectMap));
      spyOn(component.mapUpdate, 'emit');
      component.checkPlace(id, '1st');

      expect(component.map).toEqual(mock.afterFirstSelectMap);
      expect(component.mapUpdate.emit).toHaveBeenCalledWith(component.map);
    });

    it('should disable other columns except ANY', () => {
      const id = '532178416';
      component.map = JSON.parse(JSON.stringify(mock.afterFirstSelectMap));
      component.checkPlace(id, 'any');

      expect(component.map).toEqual(mock.afterAnySelectMap);
    });

    it('should enable all columns', () => {
      const id = '532178416';
      component.map = JSON.parse(JSON.stringify(mock.afterAnySelectMap));
      component.checkPlace(id, 'any');

      expect(component.map).toEqual(mock.afterSecondAnySelectMap);
    });

    it('should select tricast', () => {
      component.map = JSON.parse(JSON.stringify(mock.tricastMapBeforeSelect));
      component.checkPlace('532178415', '1st');
      component.checkPlace('532178416', '2nd');
      component.checkPlace('532178416', '2nd');
      component.checkPlace('532178417', '3rd');

      expect(component.map).toEqual(mock.tricastMapAfterSelect);
    });

    it('should select tricast ANY', () => {
      component.map = JSON.parse(JSON.stringify(mock.tricastMapBeforeSelect));
      component.checkPlace('532178415', 'any');
      component.checkPlace('532178416', 'any');
      component.checkPlace('532178417', 'any');

      expect(component.map).toEqual(mock.tricastMapAfterSelectAny);
    });

    describe('preventDoubleClick', () => {
      beforeEach(() => {
        component.map = JSON.parse(JSON.stringify(mock.beforeFirstSelectMap));
      });

      it('doubleClick same btn', () => {
        component.checkPlace('532178415', '1st');
        component.checkPlace('532178415', '1st');
        component.checkPlace('532178415', '1st');
        expect(component.map).toEqual(mock.afterFirstSelectMap);
      });

      it('doubleClick same btn', () => {
        component.checkPlace('532178416', 'any');
        component.checkPlace('532178415', '1st');
        expect(component.map).toEqual(mock.afterSecondSelectMap);
      });

      it('doubleClick row', () => {
        component.checkPlace('532178415', '1st');
        component.checkPlace('532178415', '2nd');
        expect(component.map).toEqual(mock.afterFirstSelectMap);
      });

      it('doubleClick column', () => {
        component.checkPlace('532178415', '1st');
        component.checkPlace('532178416', '1st');
        component.checkPlace('532178417', '1st');
        expect(component.map).toEqual(mock.afterFirstSelectMap);
      });
    });
  });
});
