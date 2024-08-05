import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { throwError, of } from 'rxjs';
import { HomeComponent } from './home.component';

describe('#HomeComponent', () => {
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
  };

  let component: HomeComponent;
  let cms, dynamicComponentLoader,pubsub;

  beforeEach(() => {
    cms = {
      getRibbonModule: jasmine.createSpy('cms.getRibbonModule'),
      getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(of(true))
    } as any;
    dynamicComponentLoader = {};
    pubsub = {
      publish: jasmine.createSpy(),
      API: pubSubApi,
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };

    component = new HomeComponent(
      cms,
      dynamicComponentLoader,pubsub
    );
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should get ribbon data', () => {
      spyOn(component, 'hideSpinner');
      cms.getRibbonModule.and.returnValue(of(statsDataMock));
      component.ngOnInit();
      expect(component.ribbon).toEqual(statsDataMock.getRibbonModule);
      expect(component.femData).toEqual(statsDataMock.getMMOutcomesByEventType);
      expect(component.hideSpinner).toHaveBeenCalled();
    });
   it('should call the subscriber',()=>{
     spyOn(component,'moduleRibbonData')
     pubsub.subscribe.and.callFake((a, method, cb) => {
       if (method === 'SEGMENTED_INIT_FE_REFRESH') {
         cb();
       }
     });
     component.ngOnInit();
     expect(component.moduleRibbonData).toHaveBeenCalled();
   })
    it('should throw error', () => {
      cms.getRibbonModule.and.returnValue(throwError('error'));
      component.showError = jasmine.createSpy('showError');
      component.ngOnInit();
      expect(component.showError).toHaveBeenCalled();
    });
  });
  describe('#getIsEnhancedMultiplesEnabled', () => {
    it('isEnhancedMultiplesEnabled true', () => {
      component['getIsEnhancedMultiplesEnabled']().subscribe((value) => {
        expect(value).toBeTruthy();
      });
      expect(cms.getToggleStatus).toHaveBeenCalledWith('EnhancedMultiples');
    });

    it('isEnhancedMultiplesEnabled false', () => {
      cms.getToggleStatus = jasmine.createSpy().and.returnValue(of(false));
      component['getIsEnhancedMultiplesEnabled']().subscribe((value) => {
        expect(value).toBeFalsy();
      });
      expect(cms.getToggleStatus).toHaveBeenCalledWith('EnhancedMultiples');
    });
  });
});
