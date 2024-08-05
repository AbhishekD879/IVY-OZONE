import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';

describe('AbstractDialog', () => {
  let component, device, windowRef;

  beforeEach(() => {
    device = {
      deviceType: 'iPad',
      isTablet: false
    };
    windowRef = {
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('add'),
            remove: jasmine.createSpy('remove')
          }
        }
      }
    };

    component = new AbstractDialogComponent(device, windowRef);
  });

  describe('ngOnInit', () => {
    let originalClose, originalOnKeyDownHandler, onBeforeClose, closeNative;
    beforeEach(() => {
      spyOn(component as any, 'addRemoveClasses').and.callThrough();
      originalClose = jasmine.createSpy('originalClose');
      originalOnKeyDownHandler = jasmine.createSpy('originalOnKeyDownHandler');
      onBeforeClose = jasmine.createSpy('onBeforeClose');
      closeNative = jasmine.createSpy('closeNative');
      component.dialog = {
        close: originalClose,
        onKeyDownHandler: originalOnKeyDownHandler,
        changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') }
      };
      component.params = { onBeforeClose, closeNative, closeByEsc: true };
      component.ngOnInit();
    });
    it('should reassign close and onKeyDownHandler dialog methods', () => {
      expect(component.dialog.close).toEqual(jasmine.any(Function));
      expect(component.dialog.onKeyDownHandler).toEqual(jasmine.any(Function));
      expect(component.dialog.close).not.toEqual(originalClose);
      expect(component.dialog.onKeyDownHandler).not.toEqual(originalOnKeyDownHandler);
    });

    describe('new dialog.close method', () => {
      it('should do nothing if dialog is not visible', () => {
        expect(component.visible).toBeFalsy();
        component.dialog.close();
        expect(onBeforeClose).not.toHaveBeenCalled();
        expect(closeNative).not.toHaveBeenCalled();
        expect(originalClose).not.toHaveBeenCalled();
        expect(component.dialog.changeDetectorRef.detectChanges).not.toHaveBeenCalled();
      });

      describe('if dialog is visible should clear classes, hide dialog, execute original close method', () => {
        beforeEach(() => {
          component.dialog.visible = true;
        });

        it('and call onBeforeClose callback if provided', () => {
          component.dialog.close();
          expect(onBeforeClose).toHaveBeenCalled();
        });
        describe('and not call onBeforeClose callback', () => {
          it('if not provided', () => {
            component.params.onBeforeClose = null;
          });
          it('if no parameters are available', () => {
            component.params = null;
          });
          afterEach(() => {
            component.dialog.close();
            expect(onBeforeClose).not.toHaveBeenCalled();
          });
        });

        it('and call closeNative callback (without argument) if provided', () => {
          component.dialog.close();
          expect(closeNative).toHaveBeenCalledWith(undefined);
        });
        it('and call closeNative callback (with argument) if provided', () => {
          component.dialog.close(true);
          expect(closeNative).toHaveBeenCalledWith(true);
        });

        describe('and not call closeNative callback', () => {
          it('if not provided', () => {
            component.params.closeNative = null;
          });
          it('if no parameters are available', () => {
            component.params = null;
          });
          afterEach(() => {
            component.dialog.close();
            expect(closeNative).not.toHaveBeenCalled();
          });
        });

        afterEach(() => {
          expect(originalClose).toHaveBeenCalled();
          expect((component as any).addRemoveClasses).toHaveBeenCalledWith(false);
          expect(component.dialog.visible).toEqual(false);
          expect(component.dialog.changeDetectorRef.detectChanges).toHaveBeenCalled();
        });
      });
    });

    describe('new dialog.onKeyDownHandler method', () => {
      it('should call original onKeyDownHandler if params.closeByEsc is truthy', () => {
        component.dialog.onKeyDownHandler({ event: 'event' });
        expect(originalOnKeyDownHandler).toHaveBeenCalledWith({ event: 'event' });
      });
      describe('should not call original onKeyDownHandler', () => {
        it('if params.closeByEsc is falsy', () => {
          component.params.closeByEsc = null;
        });
        it('if params are not provided', () => {
          component.params = null;
        });
        afterEach(() => {
          component.dialog.onKeyDownHandler({ event: 'event' });
          expect(originalOnKeyDownHandler).not.toHaveBeenCalled();
        });
      });
    });
  });

  it('setParams should set params', () => {
    component.setParams({ params: 'params' });
    expect(component.params).toEqual({ params: 'params' });
  });

  describe('closeDialog', () => {
    beforeEach(() => {
      component.dialog = { close: jasmine.createSpy('close') };
    });
    it(' should call dialog.close (no arguments)', () => {
      component.closeDialog();
      expect(component.dialog.close).toHaveBeenCalledWith(undefined);
    });

    it(' should call dialog.close (arguments provided)', () => {
      component.closeDialog(true);
      expect(component.dialog.close).toHaveBeenCalledWith(true);
    });
  });

  describe('open should add classes', () => {
    beforeEach(() => {
      spyOn(component as any, 'addRemoveClasses').and.callThrough();
      component.dialog = { visible: true, visibleAnimate: undefined,
        changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') } };
    });

    it('and do nothing else if dialog is visible', () => {
      component.open();
      expect(windowRef.document.body.classList.add).not.toHaveBeenCalled();
      expect(component.dialog.visibleAnimate).toEqual(undefined);
      expect(component.dialog.changeDetectorRef.detectChanges).not.toHaveBeenCalled();
    });

    it('and add class to document body and update visibility properties', () => {
      component.dialog.visible = false;
      component.open();
      expect(windowRef.document.body.classList.add).toHaveBeenCalledWith('modal-open');
      expect(component.dialog.visible).toEqual(true);
      expect(component.dialog.visibleAnimate).toEqual(true);
      expect(component.dialog.changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    afterEach(() => {
      expect((component as any).addRemoveClasses).toHaveBeenCalledWith(true);
    });
  });
});
