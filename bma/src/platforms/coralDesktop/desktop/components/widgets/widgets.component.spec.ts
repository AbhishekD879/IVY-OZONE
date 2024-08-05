import { WidgetsComponent } from './widgets.component';
import { IWidgetConfig } from '@desktop/models/wigets.model';
import { ISportConfigurationTabs } from '@sb/models/sport-configuration.model';

describe('WidgetsComponent', () => {
  let component: WidgetsComponent;

  let widgetsService, pubSubService;
  let cmsService;

  const activeWidgets: IWidgetConfig = {
    inPlay: true,
    liveStream: true,
    table: false,
    results: false,
  };

  const sportConfigData: ISportConfigurationTabs[] = [
    {
      name: 'name'
    }
  ];

  const sportActiveTabData = 'matches';
  const sportNameData = 'football';
  const sportDetailPage = '';

  beforeEach(() => {
    widgetsService = {
      getConfig: jasmine.createSpy().and.returnValue(activeWidgets),
      getWidgetsVisibility: jasmine.createSpy('getWidgetsVisibility'),
    };
    pubSubService = {
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: {
        WIDGET_VISIBILITY: 'WIDGET_VISIBILITY'
      }
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.callFake(() => {
        return { subscribe: jasmine.createSpy() };
      })
    };

    component = new WidgetsComponent(widgetsService, pubSubService, cmsService);
    component.sportConfig = sportConfigData;
    component.sportActiveTab = sportActiveTabData;
    component.sportName = sportNameData;
    component.sportDetailPage = sportDetailPage;
    component['widgets'] = {};
  });

  it('should create  instance', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', done => {
    component.ngOnInit();
    expect(widgetsService.getConfig).toHaveBeenCalledWith(component.sportConfig);
    expect(cmsService.getSystemConfig).toHaveBeenCalled();
    component['widgets'] = widgetsService.getConfig(component.sportConfig);
    setTimeout(() => {
      expect(pubSubService.subscribe).toHaveBeenCalledWith('WidgetsController', pubSubService.API.WIDGET_VISIBILITY, jasmine.anything());
      done();
    });
  });

  it('ngOnDestroy', () => {
    component.ngOnInit();
    expect(component).toBeDefined();
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledTimes(1);
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('WidgetsController');
  });

  describe('WidgetsComponent:setWidgetsVisibility', () => {
    it('should check if widgets visible', () => {
      component.setWidgetsVisibility();
      expect(widgetsService.getWidgetsVisibility).toHaveBeenCalled();
    });
  });
});

