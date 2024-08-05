import {
  InformationDialogComponent
} from '@sharedModule/components/informationDialog/information-dialog.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('InformationDialogComponent', () => {
  let component: InformationDialogComponent;
  let clickEventMock;
  let deviceServiceStub;
  let rendererService;
  let windowRefStub;
  let pubSubStub;
  let rountingUtilsServiceStub;
  let gtmService;

  beforeEach(() => {
    clickEventMock = {
      target: {
        attributes: {
          href: {
            value: 'testHref'
          }
        },
        innerHTML:'ok'
      },
      preventDefault: jasmine.createSpy()
    };

    deviceServiceStub = {
      isWrapper: false,
      isIos: false,
      visible: false,
      visibleAnimate: false
    };

    rendererService = {
      renderer: {
        listen: jasmine.createSpy().and.returnValue(() => {})
      }
    };

    windowRefStub = {
      setTimeout: jasmine.createSpy('setTimeout').and.callFake(cb => cb()),
      document: {
        querySelector: jasmine.createSpy().and.returnValue({
          querySelector: jasmine.createSpy()
        })
      }
    };
    pubSubStub = {
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };

    rountingUtilsServiceStub = {
      openUrl: jasmine.createSpy()
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };

    component = new InformationDialogComponent(deviceServiceStub, rendererService, windowRefStub,
      pubSubStub, rountingUtilsServiceStub,gtmService);

    component.dialog = {
      changeDetectorRef: {
        detectChanges: jasmine.createSpy('detectChanges')
      }
    };
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should test init function', () => {
    component.params.hideCrossIcon = true;
    component.ngAfterViewInit();
    component['redirectListener'] = () => {};
    component['checkLink'](clickEventMock);
    expect(windowRefStub.document.querySelector).toHaveBeenCalledWith('.modal-body');
    expect(rountingUtilsServiceStub.openUrl).toHaveBeenCalledWith('testHref', true);
  });

  it('should test init function when new modal opened inside', () => {
    spyOn(component as any, 'init').and.callThrough();

    pubSubStub.subscribe.and.callFake((name, event, callback) => {
       callback();

       expect(component.dialog.changeDetectorRef.detectChanges).toHaveBeenCalled();
       expect(component['init']).toHaveBeenCalled();
    });

    component.ngAfterViewInit();

    expect(pubSubStub.subscribe).toHaveBeenCalledWith('InformationDialogComponent',
      pubSubStub.API.NEW_DIALOG_OPENED, jasmine.any(Function));
  });

  describe('@handleBtnClick', () => {
    beforeEach(() => {
      spyOn(component, 'closeDialog');
    });

    it('should call provided handler', () => {
      const btnStub = {handler: jasmine.createSpy('handler'),caption: "Yes"};
      component.handleBtnClick(btnStub);
      const gtmData = {
        event: 'Event.Tracking',
        'component.CategoryEvent': 'footballsuperseries',
        'component.ActionEvent': 'click',
        'component.LabelEvent': 'entry popup',
        'component.PositionEvent': 'not applicable',
        'component.LocationEvent': 'entry popup',
        'component.EventDetails':btnStub.caption,
        'component.URLClicked': 'not applicable'
      }
      expect(component.closeDialog).not.toHaveBeenCalled();
      expect(btnStub.handler).toHaveBeenCalled();
      expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData)
    });

    it('should close dialog if no handler provided', () => {
      component.handleBtnClick({});

      expect(component.closeDialog).toHaveBeenCalled();
    });

    it('should call addGaTracking if hideCrossIcon is true', () => {
      spyOn(component, 'addGaTracking');
      component.params.hideCrossIcon = true;
      const btnStub = {caption:'ok'};
      component.handleBtnClick(btnStub);
      expect(component.addGaTracking).toHaveBeenCalled();
    });

    it('should call addGaTracking if hideCrossIcon is true without GA data', () => {
      spyOn(component, 'addGaTracking');
      component.params = {hideCrossIcon: true, label: 'Lucky 15', compName: 'bet slip'};
      const btnStub = {caption:'ok cta'};
      component.handleBtnClick(btnStub);
      expect(component.addGaTracking).toHaveBeenCalled();
    });

    it('should call addGaTracking if hideCrossIcon is true with GA data', () => {
      spyOn(component, 'addGaTracking');
      component.params = {hideCrossIcon: true, label: 'Lucky 15', compName: 'bet slip'};
      const btnStub = {caption:'OK'};
      component.handleBtnClick(btnStub);
      expect(component.addGaTracking).toHaveBeenCalled();
    });
  });

  describe('#GA tracking on click', () => {
    it('sendGTMData', () => {
      component.params = {
        label: '',
        compName: '',
      } as any;
      component['addGaTracking']('OK','OK');
      expect(gtmService.push).toHaveBeenCalled();
      component['addGaTracking']('Success','Success');
      expect(gtmService.push).toHaveBeenCalled();
      component['addGaTracking']('Success');
      expect(gtmService.push).toHaveBeenCalled();
    }); 
  });
});
