import { of } from 'rxjs';
import { WMatchCentreComponent } from '@lazy-modules/rightColumn/components/wMatchCentre/w-match-centre.component';

describe('#WMatchCentreComponent', () => {
  const staticStreamDetailsMock = {
    detail: {
      selectionId: 'test-id',
      settingValue: 'test-value',
      isOpen: false
    }
  };
  const staticDataMock: any = {};
  let component: WMatchCentreComponent;
  let windowRefService, deviceService, visDataHandlerService;

  beforeEach(() => {

    windowRefService = {
      document: {
        addEventListener: jasmine.createSpy().and.callFake((e, cb) => cb(staticStreamDetailsMock)),
        removeEventListener: jasmine.createSpy().and.callFake((e, cb) => cb(staticStreamDetailsMock))
      }
    } as any;

    visDataHandlerService = {
      init: jasmine.createSpy('visDataHandlerService.init'),
    } as any;

    deviceService = {
      isWrapper: false
    };

    component = new WMatchCentreComponent(
      windowRefService,
      deviceService,
      visDataHandlerService
    );
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
    expect(component.document).toBe(windowRefService.document);
  });

  describe('#onInit', () => {
    it('should get visData', () => {
      visDataHandlerService.init.and.returnValue(of(staticDataMock));
      component.ngOnInit();
      expect(component.visData).toEqual(staticDataMock);
    });

    it('should add listener for native player only on wrapper and set stream shown', () => {
      visDataHandlerService.init.and.returnValue(of(staticDataMock));
      deviceService.isWrapper = true;
      component.ngOnInit();
      expect(windowRefService.document.addEventListener)
        .toHaveBeenCalledWith('CURRENT_WATCH_LIVE_STATE_CHANGED', jasmine.any(Function));
      expect(component.streamShown).toEqual(staticStreamDetailsMock.detail.settingValue);
    });
  });

  describe('#onDestroy', () => {
    it('should remove listener', () => {
      component.ngOnDestroy();
      expect(windowRefService.document.removeEventListener).toHaveBeenCalledWith('CURRENT_WATCH_LIVE_STATE_CHANGED', jasmine.any(Function));
    });
  });
});
