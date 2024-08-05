import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { fakeAsync } from '@angular/core/testing';
import { IDialogEvent, IDialogParams, IOpenedDialogsMap } from '@core/services/dialogService/dialog-params.model';
import { Type } from '@angular/core';
import { dialogIdentifierDictionary } from '../../constants/dialog-identifier-dictionary.constant';
import { dialogsImplementedOnNative } from '../../constants/dialogs-on-native-wrapper.constant';
import { DialogService } from './dialog.service';

describe('DialogService', () => {
  let service: DialogService;

  let nativeBridgeService;
  let device;

  beforeEach(() => {
    nativeBridgeService = {
      isWrapper: true,
      isNativePage: true,
      onOpenPopup: jasmine.createSpy('onOpenPopup'),
      onClosePopup: jasmine.createSpy('onClosePopup')
    };
    device = {
      deviceType: 'iPad',
      isTablet: false
    };

    service = new DialogService(nativeBridgeService, device);
  });

  describe('#constructor', () => {
    it('ipad selfExclusionLogoutDialog', () => {
      expect(service['openedModal']).toBeDefined();
      delete dialogsImplementedOnNative.selfExclusionLogoutDialog;
      expect(dialogsImplementedOnNative).toEqual(dialogsImplementedOnNative);
      expect(dialogsImplementedOnNative.hasOwnProperty('selfExclusionLogoutDialog')).toBeFalsy();
    });

    it('default', () => {
      expect(service['openedModal']).toBeDefined();
      expect(dialogsImplementedOnNative).toEqual(dialogsImplementedOnNative);
    });
  });

  it('API', () => {
    expect(DialogService.API).toEqual(dialogIdentifierDictionary);
  });

  it('ids', () => {
    expect(service.ids).toEqual(dialogIdentifierDictionary);
  });

  describe('#openDialog', () => {
    it('isWrapper = true, isNativePage = true', () => {
      nativeBridgeService.isNativePage = true;
      nativeBridgeService.isWrapper = true;
      service['openedModal'] = {
        next: jasmine.createSpy('next')
      } as any;

      service.openDialog('connectionLost', undefined, true, { id: 1 });
      expect(service['openedModal'].next).not.toHaveBeenCalled();
      expect(nativeBridgeService.onOpenPopup).not.toHaveBeenCalled();
    });

    it('isWrapper = false, isNativePage = false', () => {
      nativeBridgeService.isWrapper = false;
      nativeBridgeService.isNativePage = false;
      service['openedModal'] = {
        next: jasmine.createSpy('next')
      } as any;
      service.openDialog('connectionLost', undefined, true, { id: 1 });
      expect(service['openedModal'].next).toHaveBeenCalled();
      expect(nativeBridgeService.onOpenPopup).toHaveBeenCalled();
    });

    it('isWrapper = true, isNativePage = false', () => {
      nativeBridgeService.isWrapper = true;
      nativeBridgeService.isNativePage = false;
      service['openedModal'] = {
        next: jasmine.createSpy('next')
      } as any;
      service.openDialog('connectionLost', undefined, true, { id: 1 });
      expect(service['openedModal'].next).not.toHaveBeenCalled();
      expect(nativeBridgeService.onOpenPopup).not.toHaveBeenCalled();
    });

    it('isWrapper = true, isNativePage = false', () => {
      nativeBridgeService.isWrapper = true;
      nativeBridgeService.isNativePage = false;
      service['openedModal'] = {
        next: jasmine.createSpy('next')
      } as any;
      service.openDialog('AboutToExpire', undefined, true, { id: 1 });
      expect(service['openedModal'].next).toHaveBeenCalled();
      expect(nativeBridgeService.onOpenPopup).toHaveBeenCalled();
    });

    it('isWrapper = false, isNativePage = true', () => {
      nativeBridgeService.isWrapper = false;
      nativeBridgeService.isNativePage = true;
      service['openedModal'] = {
        next: jasmine.createSpy('next')
      } as any;
      service.openDialog('connectionLost', undefined, true, { id: 1 });
      expect(service['openedModal'].next).toHaveBeenCalled();
      expect(nativeBridgeService.onOpenPopup).toHaveBeenCalled();
    });

    it('isWrapper = false, isNativePage = true', () => {
      nativeBridgeService.isWrapper = false;
      nativeBridgeService.isNativePage = true;
      service['openedModal'] = {
        next: jasmine.createSpy('next')
      } as any;
      service.openDialog('AboutToExpire', undefined, true, { id: 1 });
      expect(service['openedModal'].next).not.toHaveBeenCalled();
      expect(nativeBridgeService.onOpenPopup).not.toHaveBeenCalled();
    });

    it('OpenDialog solidOverlay false', () => {
      nativeBridgeService.isWrapper = false;
      nativeBridgeService.isNativePage = false;
      const fakeComponent = {} as any;
      const params = {} as IDialogParams;
      const fakeDialogName = 'AboutToExpire';
      service['openedModal'] = {
        next: jasmine.createSpy('next')
      } as any;
      service.openDialog(fakeDialogName, fakeComponent, true, params, true);
      expect(nativeBridgeService.onOpenPopup).toHaveBeenCalledWith(fakeDialogName);
      expect(service['openedModal'].next).toHaveBeenCalledWith(jasmine.objectContaining({solidOverlay: false}));
    });

    it('OpenDialog with solidOverlay - true', () => {
      nativeBridgeService.isWrapper = false;
      nativeBridgeService.isNativePage = false;
      const fakeComponent = {} as any;
      const params = {} as IDialogParams;
      const fakeDialogName = 'AboutToExpire';
      service['openedModal'] = {
        next: jasmine.createSpy('next')
      } as any;
      service.openDialog(fakeDialogName, fakeComponent, true, params, true, true);
      expect(nativeBridgeService.onOpenPopup).toHaveBeenCalledWith(fakeDialogName);
      expect(service['openedModal'].next).toHaveBeenCalledWith(jasmine.objectContaining({solidOverlay: true}));
    });
  });

  it('openedPopups', () => {
    const mockOpenDialog = ({ fake: true } as IOpenedDialogsMap);
    service['openedDialogs'] = mockOpenDialog;
    expect(service.openedPopups).toEqual(mockOpenDialog);
  });

  it('register', fakeAsync((done) => {
    service.modalListener.subscribe((data: IDialogEvent) => {
      expect(data).toEqual({
        type: 'register',
        params: { dialog: {}, create: false },
        name: 'test-suit',
        forceCloseOther: false
      });
    });

    service.register('test-suit', {} as Type<AbstractDialogComponent>);
  }));

  it('register', fakeAsync((done) => {
    service.modalListener.subscribe((data: IDialogEvent) => {
      expect(data).toEqual({
        type: 'register',
        params: { dialog: {}, create: true },
        name: 'test-suit',
        forceCloseOther: false
      });
    });

    service.register('test-suit', {} as Type<AbstractDialogComponent>, true);
  }));

  it('closeDialogs', fakeAsync(() => {
    service.modalListener.subscribe((data: IDialogEvent) => {
      expect(data).toEqual({
        type: 'closeAll',
        forceCloseOther: false
      });
    });
    service.closeDialogs();
  }));

  it('closeDialog', fakeAsync(() => {
    service.modalListener.subscribe((data: IDialogEvent) => {
      expect(data).toEqual({
        type: 'close',
        name: 'test-suit',
        forceCloseOther: true
      });
    });
    service.closeDialog('test-suit', true);
  }));

  it('closeDialog', fakeAsync(() => {
    service.modalListener.subscribe((data: IDialogEvent) => {
      expect(data).toEqual({
        type: 'close',
        name: 'test-suit',
        forceCloseOther: false
      });
    });
    service.closeDialog('test-suit', false);
  }));

  describe('#openDialog', () => {
    it('isWrapper = true, isNativePage = true', () => {
      nativeBridgeService.isNativePage = true;
      nativeBridgeService.isWrapper = true;
      service['openedModal'] = {
        next: jasmine.createSpy('next')
      } as any;

      service.openDialog('connectionLost', undefined, true, { id: 1 });
      expect(service['openedModal'].next).not.toHaveBeenCalled();
      expect(nativeBridgeService.onOpenPopup).not.toHaveBeenCalled();
    });

    it('isWrapper = false, isNativePage = false', () => {
      nativeBridgeService.isWrapper = false;
      nativeBridgeService.isNativePage = false;
      service['openedModal'] = {
        next: jasmine.createSpy('next')
      } as any;
      service.openDialog('connectionLost', undefined, true, { id: 1 });
      expect(service['openedModal'].next).toHaveBeenCalled();
      expect(nativeBridgeService.onOpenPopup).toHaveBeenCalled();
    });

    it('isWrapper = true, isNativePage = false', () => {
      nativeBridgeService.isWrapper = true;
      nativeBridgeService.isNativePage = false;
      service['openedModal'] = {
        next: jasmine.createSpy('next')
      } as any;
      service.openDialog('connectionLost', undefined, true, { id: 1 });
      expect(service['openedModal'].next).not.toHaveBeenCalled();
      expect(nativeBridgeService.onOpenPopup).not.toHaveBeenCalled();
    });

    it('isWrapper = true, isNativePage = false', () => {
      nativeBridgeService.isWrapper = true;
      nativeBridgeService.isNativePage = false;
      service['openedModal'] = {
        next: jasmine.createSpy('next')
      } as any;
      service.openDialog('AboutToExpire', undefined, true);
      expect(service['openedModal'].next).toHaveBeenCalled();
      expect(nativeBridgeService.onOpenPopup).toHaveBeenCalled();
    });

    it('isWrapper = false, isNativePage = true', () => {
      nativeBridgeService.isWrapper = false;
      nativeBridgeService.isNativePage = true;
      service['openedModal'] = {
        next: jasmine.createSpy('next')
      } as any;
      service.openDialog('connectionLost', undefined, true, { id: 1 });
      expect(service['openedModal'].next).toHaveBeenCalled();
      expect(nativeBridgeService.onOpenPopup).toHaveBeenCalled();
    });

    it('isWrapper = false, isNativePage = true', () => {
      nativeBridgeService.isWrapper = false;
      nativeBridgeService.isNativePage = true;
      service['openedModal'] = {
        next: jasmine.createSpy('next')
      } as any;
      service.openDialog('AboutToExpire', undefined, true, { id: 1 });
      expect(service['openedModal'].next).not.toHaveBeenCalled();
      expect(nativeBridgeService.onOpenPopup).not.toHaveBeenCalled();
    });

    it('should not implement native dialogs for tablet', () => {
      nativeBridgeService.isWrapper = true;
      nativeBridgeService.isNativePage = true;
      device.isTablet = true;
      service['openedModal'] = {
        next: jasmine.createSpy('next')
      } as any;
      service.openDialog('AboutToExpire', undefined, true, { id: 1 });
      expect(service['openedModal'].next).toHaveBeenCalled();
      expect(nativeBridgeService.onOpenPopup).toHaveBeenCalled();
    });

    it('should implement closeNative method and pass Registration true to nativeBridgeService', () => {
      const params = {} as any;
      service.openDialog('Login', undefined, false, params, true);
      expect(params.closeNative).toBeDefined();

      params.closeNative(true);

      expect(service['openedDialogs']).toEqual({ Registration: true });
      expect(nativeBridgeService.onClosePopup).toHaveBeenCalledWith('Login', { Registration: true });
    });

    it('should implement closeNative method and don"t pass Registration true to nativeBridgeService', () => {
      const params = {} as any;
      service.openDialog('Login', undefined, false, params, true);
      expect(params.closeNative).toBeDefined();

      params.closeNative();

      expect(service['openedDialogs']).toEqual({});
      expect(nativeBridgeService.onClosePopup).toHaveBeenCalledWith('Login', {});
    });
  });
});
