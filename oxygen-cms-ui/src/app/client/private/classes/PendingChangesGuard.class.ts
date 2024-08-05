import {Observable} from 'rxjs/Observable';
import {CanDeactivate} from '@angular/router';
import { forwardRef, Inject, Injectable } from '@angular/core';

import {ComponentCanDeactivate} from '../interfaces/pending-changes.guard';
import {DialogService} from '../../../shared/dialog/dialog.service';

/**
 * Guard for executing actions before route change. Component should have implementation
 * of ComponentCanDeactivate and also components's route should contain such property: 'canDeactivate: [PendingChangesGuard]'
 */
@Injectable()
export class PendingChangesGuard implements CanDeactivate<ComponentCanDeactivate> {
  constructor(
    @Inject(forwardRef(() => DialogService)) public dialogService: DialogService) {
  }

  canDeactivate(component: ComponentCanDeactivate): boolean | Observable<boolean> {
    const defaultMessage = 'Your Changes Are Not Saved. Exit Page Without Saving?';

    if (component.canDeactivate()) {
      return true;
    }

    const dialogRef = this.dialogService.showConfirmDialog({
      title: 'Leaving',
      message: defaultMessage
    });

    return dialogRef.afterClosed()
      .map(yes => {
        return !!yes;
      })
      .catch(() => {
        return Observable.of(false);
      });
  }
}
