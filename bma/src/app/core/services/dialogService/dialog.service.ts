import { Observable, Subject } from 'rxjs';
import { Injectable, Type, ComponentFactory } from '@angular/core';
import * as _ from 'underscore';

import { dialogIdentifierDictionary } from '../../constants/dialog-identifier-dictionary.constant';
import { dialogsImplementedOnNative, dialogsDisabledOnWrapper } from '../../constants/dialogs-on-native-wrapper.constant';
import { DeviceService } from '../device/device.service';
import { NativeBridgeService } from '../nativeBridge/native-bridge.service';
import { IDialogEvent, IDialogParams, IOpenedDialogsMap } from './dialog-params.model';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';

@Injectable()
export class DialogService {

  private openedDialogs: IOpenedDialogsMap = {};
  private openedModal: Subject<IDialogEvent>;

  static get API() {
    return dialogIdentifierDictionary;
  }

  static set API(value:any){}

  constructor(
    private nativeBridgeService: NativeBridgeService,
    private device: DeviceService,
  ) {
    this.openedModal = new Subject();
    if (this.device && this.device.deviceType && this.device.deviceType.indexOf('iPad') !== -1) {
      // eslint-disable-next-line
      console.log('Removed "dialogsImplementedOnNative.selfExclusionLogoutDialog"');
      delete dialogsImplementedOnNative.selfExclusionLogoutDialog;
    }
  }

  get openedPopups(): IOpenedDialogsMap {
    return this.openedDialogs;
  }
  set openedPopups(value:IOpenedDialogsMap){}

register(dialogName: string, dialog: Type<AbstractDialogComponent>, create: boolean = false) {
    this.openedModal.next({
      type: 'register',
      params: { dialog, create },
      name: dialogName,
      forceCloseOther: false
    });
  }

  openDialog(dialogName: string, component: Type<AbstractDialogComponent>|ComponentFactory<any>,
             closeOther: boolean, params: IDialogParams = {},
             handleNative: boolean = true, solidOverlay: boolean = false): void {
    const isNativePage: boolean = this.nativeBridgeService.isNativePage;
    const isWrapper: boolean = this.nativeBridgeService.isWrapper;

    if ((isNativePage && !this.device.isTablet && _.contains(dialogsImplementedOnNative, dialogName)) ||
      (isWrapper && _.contains(dialogsDisabledOnWrapper, dialogName))) {
      return;
    }
    params = Object.assign(params, { closeByEsc: true, isPersistent: false });

    if (handleNative) {
      params.closeNative = (isOnSignUpClick?: boolean) => {
        delete this.openedDialogs[dialogName];
        if (isOnSignUpClick) {
          this.openedDialogs['Registration'] = true;
        }
        this.nativeBridgeService.onClosePopup(dialogName, this.openedDialogs);
      };
    }

    this.openedModal.next({
      type: 'open',
      params: params,
      name: dialogName,
      component: component,
      forceCloseOther: closeOther,
      solidOverlay
    });
    this.openedDialogs[dialogName] = true;
    this.nativeBridgeService.onOpenPopup(dialogName);
  }

  closeDialogs(): void {
    this.openedModal.next({
      type: 'closeAll',
      forceCloseOther: false
    });
  }

  closeDialog(dialogName: string, closeOthers: boolean = false): void {
    this.openedModal.next({
      type: 'close',
      name: dialogName,
      forceCloseOther: closeOthers
    });
  }

  get modalListener(): Observable<IDialogEvent> {
    return this.openedModal.asObservable();
  }
  set modalListener(value:Observable<IDialogEvent>){}
  get ids() {
    return dialogIdentifierDictionary;
  }
  set ids(value:any){}
}
