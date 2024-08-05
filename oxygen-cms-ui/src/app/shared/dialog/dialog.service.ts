import {Injectable} from '@angular/core';
import {ConfirmDialogComponent} from './confirm-dialog/confirm-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import {PromptDialogComponent} from './prompt-dialog/prompt-dialog.component';
import {NotificationDialogComponent} from './notification-dialog/notification-dialog.component';
import {DialogOptions} from '../../client/private/models/dialog.model';
import { DeleteDialogComponent } from '@app/shared/dialog/delete-dialog/delete-dialog.component';

@Injectable()
export class DialogService {
  constructor(private dialog: MatDialog) {}

  showConfirmDialog(options) {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: options.title,
        question: options.message,
        noOption: 'No',
        yesOption: 'Yes'
      }
    });

    dialogRef.afterClosed().subscribe(callbackData => {
      /* tslint:disable */
      // Maksym Shturmin
      if (callbackData) {
        options.yesCallback && typeof options.yesCallback === 'function' && options.yesCallback();
      } else {
        options.noCallback && typeof options.yesCallback === 'function' && options.noCallback();
      }
      /* tslint:enable */
    });
    return dialogRef;
  }

  showNotificationDialog(options: DialogOptions) {
    const dialogRef = this.dialog.open(NotificationDialogComponent, {
      data: {
        title: options.title,
        message: options.message,
        messagesArray: options.messagesArray
      }
    });

    dialogRef.afterClosed().subscribe(() => {
      /* tslint:disable */
      // Maksym Shturmin
      options.closeCallback && typeof options.closeCallback === 'function' && options.closeCallback();
      /* tslint:enable */
    });
  }

  showPromptDialog(options: DialogOptions) {
    const dialogRef = this.dialog.open(PromptDialogComponent, {
      width: options.width,
      data: {
        title: options.title,
        question: options.message,
        hint: options.hint,
        controls: options.controls,
        noOption: 'No',
        yesOption: 'Yes'
      }
    });

    dialogRef.afterClosed().subscribe(callbackData => {
      /* tslint:disable */
      // Maksym Shturmin
      if (callbackData) {
        options.yesCallback && typeof options.yesCallback === 'function' && options.yesCallback(callbackData);
      } else {
        options.noCallback && typeof options.yesCallback === 'function' && options.noCallback();
      }
      /* tslint:enable */
    });
  }

  showCustomDialog(component, options: DialogOptions) {

    const dialogRef = this.dialog.open(component, {
      width: options.width,
      data: {
        title: options.title,
        noOption: options.noOption,
        yesOption: options.yesOption,
        data: options.data || {}
      }
    });

    dialogRef.afterClosed().subscribe(callbackData => {
      /* tslint:disable */
      // Oleg Shpaner
      if (callbackData && !callbackData.closeCallback) {
        options.yesCallback && typeof options.yesCallback === 'function' && options.yesCallback(callbackData);
      } else {
        options.noCallback && typeof options.yesCallback === 'function' && options.noCallback(callbackData);
      }
      /* tslint:enable */
    });

  }

  showDeleteDialog(options): void {
    const dialogRef = this.dialog.open(DeleteDialogComponent, {
      data: {
        title: options.title,
        noOption: 'Cancel',
        yesOption: 'Delete',
        question: options.question
      }
    });

    dialogRef.afterClosed().subscribe(isConfirm => {
      /* tslint:disable */
      if (isConfirm) {
        options.deleteCallback && typeof options.deleteCallback === 'function' && options.deleteCallback();
      } else {
        options.cancelCallback && typeof options.cancelCallback === 'function' && options.cancelCallback();
      }
      /* tslint:enable */
    });
  }
}
