import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { DialogService } from '../dialogService/dialog.service';
import { ConnectionLostDialogComponent } from '@sharedModule/components/connectionLostDialog/connection-lost-dialog.component';
import { SessionLogoutDialogComponent } from '@shared/components/sessionLogoutDialog/session-logout-dialog.component';
import { InformationDialogComponent } from '@sharedModule/components/informationDialog/information-dialog.component';
import { IDialogButton, IDialogLinks } from '@core/services/dialogService/dialog-params.model';

@Injectable()
export class InfoDialogService {
  constructor(
    protected dialogService: DialogService
  ) { }

  /**
   * Creating simple popup dialog box with text and OK-button
   *
   * @param text - message
   * @param okButton - button label
   * @param dialogClass - extra class for dialog container
   * @param onClose - callback fn
   */
  openOkDialog(text: string, onClose?: Function, okButton: string = 'OK', dialogClass?: string): void {
    this.openInfoDialog(
      undefined,
      text,
      dialogClass ? `simpleDialog ${dialogClass}` : `simpleDialog`,
      undefined,
      onClose,
      [{
        caption: okButton,
        cssClass: 'btn-style2 okButton'
      }]);
  }

  /*
   * Creating popup dialog box with additional caption and text.
   * @param {string} caption
   * @param {string} text
   * @param {string} dialogClass
   * @param {string} identifier
   */
  openInfoDialog(
    caption: string,
    text: string,
    dialogClass?: string,
    identifier: string = 'informationDialog',
    onClose?: Function,
    buttons?: IDialogButton[],
    links?: IDialogLinks,
    hideCrossIcon?: boolean,
    compName?: string,
    label?: string
    
  ): void {
    this.dialogService.openDialog(identifier, InformationDialogComponent, true, {
      caption,
      text,
      dialogClass,
      buttons,
      links,
      hideCrossIcon,
      onBeforeClose: () => {
        if (_.isFunction(onClose)) {
          onClose();
        }
      },
      compName,
      label
    });
  }

  closePopUp() {
    this.dialogService.closeDialogs();
  }

  openLogoutPopup(): void {
    this.closePopUp();
    this.dialogService.openDialog(this.dialogService.ids.sessionLimitLogout, SessionLogoutDialogComponent, true);
  }

  openConnectionLostPopup(): void {
    this.dialogService.openDialog(this.dialogService.ids.connectLost, ConnectionLostDialogComponent, true);
  }

  closeConnectionLostPopup(): void {
    const dialogName = this.dialogService.ids.connectLost;
    if (this.dialogService.openedPopups[dialogName]) {
      this.dialogService.closeDialog(dialogName);
    }
  }
}
