import {
  FootballFilterConfirmDialogComponent
} from '@app/retail/components/footballFilterConfirmDialog/football-filter-confirm-dialog.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('FootballFilterConfirmDialogComponent', () => {
  let deviceService;
  let windowRef;
  let pubSubService;
  let component: FootballFilterConfirmDialogComponent;

  beforeEach(() => {
    deviceService = {};
    windowRef = {
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('add')
          }
        }
      }
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };

    component = new FootballFilterConfirmDialogComponent(
      deviceService,
      windowRef,
      pubSubService
    );
    component.dialog = {
      changeDetectorRef: {
        detectChanges: jasmine.createSpy('detectChanges')
      }
    };
  });

  it('#ngAfterViewInit', () => {
    pubSubService.subscribe.and.callFake((name, event, callback) => {
      callback();
      expect(component.dialog.changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    component.ngAfterViewInit();
    expect(pubSubService.subscribe).toHaveBeenCalledWith('FootballFilterConfirmDialogComponent',
      pubSubService.API.NEW_DIALOG_OPENED, jasmine.any(Function));
  });

  it ('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('FootballFilterConfirmDialogComponent');
  });

  describe('@handleBtnClick', () => {
    it('should call provided handler', () => {
      const btnStub = {handler: jasmine.createSpy('handler')};
      component.handleBtnClick(btnStub, 'online');
      expect(btnStub.handler).toHaveBeenCalled();
    });

    it('should call provided handler', () => {
      const btnStub = {handler: jasmine.createSpy('handler')};
      component.handleBtnClick(btnStub, 'inshop');
      expect(btnStub.handler).toHaveBeenCalled();
    });
  });
});
