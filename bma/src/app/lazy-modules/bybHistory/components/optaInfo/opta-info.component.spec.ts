import { OptaInfoComponent } from './opta-info.component';

describe('OptaInfoComponent', () => {
  let component: OptaInfoComponent;
  let device,
    dialogService,
    infoDialog,
    componentFactoryResolver,
    changeDetectorRef;

  beforeEach(() => {
    device = {
      isOnline: jasmine.createSpy('isOnline').and.returnValue(true)
    };
    dialogService = {
      openDialog: jasmine.createSpy('openDialog')
    };
    infoDialog = {
      openConnectionLostPopup: jasmine.createSpy('openConnectionLostPopup')
    };
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue(jasmine.any(Object))
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };

    component = new OptaInfoComponent(
      device,
      dialogService,
      infoDialog,
      componentFactoryResolver,
      changeDetectorRef
    );
  });

  describe('OptaInfoComponent', () => {

    it('should create component instance', () => {
      expect(component).toBeTruthy();
    });

    it('openSeeMorePopUp', () => {
      component.openSeeMorePopUp();
      expect(dialogService.openDialog).toHaveBeenCalledWith('optaInfoPopup', jasmine.any(Object), true);
      expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
    });

    it('lost connection if device is offline', () => {
      device.isOnline.and.returnValue(false);
      component.openSeeMorePopUp();
      expect(infoDialog.openConnectionLostPopup).toHaveBeenCalled();
    });

    describe('ngOnChanges', () => {
      it('should check if optaDisclaimer first update', () => {
        const changes = {
          optaDisclaimer: {
            currentValue: {},
            previousValue: undefined
          },
          isOptaAvailable: true
        } as any;
        component.ngOnChanges(changes);

        expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      });

      it('should check check', () => {
        const changes = {
          optaDisclaimer: {
            currentValue: undefined,
            previousValue: {}
          },
          isOptaAvailable: false
        } as any;
        component.ngOnChanges(changes);

        expect(changeDetectorRef.markForCheck).not.toHaveBeenCalled();
      });
    });
  });
});
