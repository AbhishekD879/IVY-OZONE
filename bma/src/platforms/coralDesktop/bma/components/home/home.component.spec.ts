import { of } from 'rxjs';
import { DesktopHomeComponent } from './home.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('#DesktopHomeComponent', () => {
  let component: DesktopHomeComponent;
  let cms, dynamicComponentLoader, pubSubService;
  const futureTimeStamp = ((new Date()).getTime() + 10000000000);
  const futureIsoTime = (new Date(futureTimeStamp)).toISOString();

  const statsDataMock = {
    getRibbonModule: [
      {
        directiveName: 'Featured',
        id: 'tab-featured',
        showTabOn: 'both',
        title: 'Featured',
        url: '/home/featured',
        visible: true
      },
      {
        directiveName: 'EventHub',
        id: 'tab-eventhub-4',
        showTabOn: 'both',
        displayFrom: '2019-02-18T13:12:01Z',
        displayTo: '2019-02-18T15:12:01Z',
        title: 'hub 4',
        url: '/home/eventhub/4',
        visible: true
      },
      {
        directiveName: 'EventHub',
        id: 'tab-eventhub-5',
        showTabOn: 'both',
        displayFrom: '2019-02-18T13:12:01Z',
        displayTo: futureIsoTime,
        title: 'hub 5',
        url: '/home/eventhub/5',
        visible: true
      }
    ] as any,
    getMMOutcomesByEventType: { },
    getSystemConfig: {
      moduleOrder: [
        ['yourCall', 80],
        ['featured', 60],
        ['nextRace', 40],
        ['inPlay', 22]
      ],
      DesktopHomePageOrder:{ nextRace: 40, featured: 60, inPlay: 22, yourCall: 80 }
    } as any
  };

  beforeEach(() => {
    cms = {
      getRibbonModule: jasmine.createSpy('cms.getRibbonModule'),
      getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(of(true)),
      getSystemConfig: jasmine.createSpy('getSystemCOnfig').and.returnValue(of(statsDataMock.getSystemConfig))
    } as any;
    dynamicComponentLoader = {},
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.callFake((p1, p2, cb) => {
        cb({data: [1]});
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
    };

    component = new DesktopHomeComponent(
      cms,
      dynamicComponentLoader,
      pubSubService
    );
  });

  describe('#ngOnInit CD', () => {
    it('should call getSystemConfig and set moduleorder', () => {
      cms.getRibbonModule.and.returnValue(of(statsDataMock));
      component.ngOnInit();
      expect(component.moduleOrder).toEqual(statsDataMock.getSystemConfig.moduleOrder);
    });
    it('should call getSystemConfig and empty DesktopHomePageOrder', () => {
      cms.getRibbonModule.and.returnValue(of(statsDataMock));
      const sysConfig = {
        moduleOrder: [
          ['yourCall', 80],
          ['featured', 60],
          ['nextRace', 40],
          ['inPlay', 22]
        ]
      };
      cms.getSystemConfig.and.returnValue(of(sysConfig));
      component.ngOnInit();
      expect(component.moduleOrder).not.toEqual(statsDataMock.getSystemConfig.moduleOrder);
    });
    it('should call getSystemConfig and empty config', () => {
      cms.getRibbonModule.and.returnValue(of(statsDataMock));
      cms.getSystemConfig.and.returnValue(of());
      component.ngOnInit();
      expect(component.moduleOrder).not.toEqual(statsDataMock.getSystemConfig.moduleOrder);
    });
  });
});

