import { WidgetsService } from './widgets.service';
import { IWidgetConfig } from '@desktop/models/wigets.model';
import { ISportConfigurationTabs } from '@sb/models/sport-configuration.model';

describe('WidgetsService', () => {
  let service: WidgetsService;
  let activeWidgets: IWidgetConfig;
  let inactiveWidgets: IWidgetConfig;

  const defaultArr = ['one', 'two', 'three'];

  const sportConfigData: ISportConfigurationTabs[] = [
    {
      name: 'name'
    }
  ];
  beforeEach(() => {
    activeWidgets = {
      inPlay: true,
      liveStream: true,
      table: false,
      results: false,
    };
    inactiveWidgets = {
      inPlay: false,
      liveStream: false,
      table: false,
      results: false,
    };
    service = new WidgetsService();
  });

  it('WidgetsService should be created', () => {
    expect(service).toBeTruthy();
  });

  it('convertArrayToObject should return object', () => {
    const result = service['convertArrayToObject'](defaultArr);
    expect(result).toEqual(jasmine.any(Object));
  });

  describe('getWidgetsVisibility', () => {
    it('should return true with enabled widget', () => {
      const result = service.getWidgetsVisibility(activeWidgets);
      expect(result).toBeTruthy();
    });
    it('should return false with disabled widget', () => {
      const result = service.getWidgetsVisibility(inactiveWidgets);
      expect(result).toBeFalsy();
    });
  });

  describe('getConfig', () => {
    beforeEach(() => {
      service['getConfig'] = jasmine.createSpy().and.returnValue(jasmine.any(Object));
    });
    it('array transformed to object', () => {
      const result = service['getConfig'](sportConfigData);
      expect(service.getConfig).toHaveBeenCalledWith(sportConfigData);
      expect(result).toEqual(jasmine.any(Object));
    });
  });
});
