import { OlympicsPageComponent } from '@app/olympics/components/olympicsPage/olympics-page.component';
import { of as observableOf, throwError as observableThrowError } from 'rxjs';

describe('OlympicsPageComponent', () => {
  let component;
  let olympicsService;
  let olympicsMenuActual, olympicsMenuExpected;

  beforeEach(() => {
    olympicsMenuActual = [{
      imageTitle: 'c',
      ssCategoryCode: 'other'
    }, {
      imageTitle: 'b',
      ssCategoryCode: 'OLYMPICS'
    }, {
      imageTitle: 'b',
      ssCategoryCode: 'other'
    }];

    olympicsMenuExpected = [{
      imageTitle: 'b',
      ssCategoryCode: 'OLYMPICS'
    }, {
      imageTitle: 'b',
      ssCategoryCode: 'other'
    }, {
      imageTitle: 'c',
      ssCategoryCode: 'other'
    }];

    olympicsService = {
      getCMSConfig: jasmine.createSpy('getCMSConfig').and.returnValue(observableOf({})),
      getMenuConfigs: jasmine.createSpy('getMenuConfigs').and.returnValue(olympicsMenuActual)
    };

    component = new OlympicsPageComponent(olympicsService);
  });

  it('constructor executes', () => {
    expect(component.olympicsService).toBeTruthy();
    expect(component.state).toEqual({
      loading: true,
      error: false
    });
    expect(component.isUsedFromWidget).toBe(false);
  });

  describe('#ngOnInit', () => {
    it('#ngOnInit success response', () => {
      component.ngOnInit();
      expect(component.state.error).toBe(false);
      expect(component.state.loading).toBe(false);
      expect(component.olympicsMenu).toEqual(olympicsMenuExpected);
    });

    it('failure response', () => {
      (olympicsService.getCMSConfig as jasmine.Spy).and.returnValue(observableThrowError('no data'));
      component.ngOnInit();
      expect(component.state.error).toBe(true);
      expect(component.state.loading).toBe(false);
      expect(component.olympicsMenu).toBeFalsy();
    });
  });

  it('#trackById should thack menu by ids', () => {
    expect(component.trackById({ id: '1' } as any)).toBe('1');
  });

  it('#sortOlympicsMenu should sort menu with olympics games', () => {
    expect(component['sortOlympicsMenu']({ id: '1' } as any)).toEqual(olympicsMenuExpected);
    expect(olympicsService.getMenuConfigs).toHaveBeenCalledWith({ id: '1' });
  });
});
