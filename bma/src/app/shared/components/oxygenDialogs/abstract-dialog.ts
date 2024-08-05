import { OnInit, ChangeDetectorRef, Component } from '@angular/core';

import { IDialogParams } from '@core/services/dialogService/dialog-params.model';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

export interface IOxygenDialog {
  visible: boolean;
  visibleAnimate: boolean;
  changeDetectorRef: ChangeDetectorRef;
  open(): void;
  close(isOnSignUpClick?: boolean): void;
  onKeyDownHandler(event: KeyboardEvent): void;
}
@Component({
  selector: 'abstract-dialog',
  template: ''
})
export class AbstractDialogComponent implements OnInit {
  dialog: IOxygenDialog;
  params: IDialogParams;

  constructor(
    protected device: DeviceService,
    protected windowRef: WindowRefService
  ) {
  }

  ngOnInit(): void {
    const originalDialogClose = this.dialog.close.bind(this.dialog);

    this.dialog.close = (isOnSignUpClick?: boolean) => {
      if (this.dialog.visible) {
        this.addRemoveClasses(false);
        this.params && this.params.onBeforeClose && this.params.onBeforeClose();
        this.params && this.params.closeNative && this.params.closeNative(isOnSignUpClick);
        this.dialog.visible = false;

        originalDialogClose();
        this.dialog.changeDetectorRef.detectChanges();
      }
    };

    const originalOnKeyDownHandler = this.dialog.onKeyDownHandler.bind(this.dialog);

    this.dialog.onKeyDownHandler = event => {
      if (this.params && this.params.closeByEsc) {
        originalOnKeyDownHandler(event);
      }
    };
  }

  public open(): void {
    this.addRemoveClasses(true);

    if (!this.dialog.visible) {
      this.windowRef.document.body.classList.add('modal-open');
      this.dialog.visible = true;
      this.dialog.visibleAnimate = true;
      this.dialog.changeDetectorRef.detectChanges();
    }
  }

  public closeDialog(isOnSignUpClick?: boolean): void {
    this.dialog.close(isOnSignUpClick);
  }

  public setParams(params: IDialogParams): void {
    this.params = params;
  }

  private addRemoveClasses(isAdd: boolean): void {
    if (this.device.isIos) {
      if (isAdd) {
        this.windowRef.document.body.classList.add('ios-modal-opened');
        this.device.isWrapper && document.body.classList.add('ios-modal-wrapper');
      } else {
        this.windowRef.document.body.classList.remove('ios-modal-opened');
        this.device.isWrapper && document.body.classList.remove('ios-modal-wrapper');
      }
    }

    if (!isAdd) {
      this.windowRef.document.body.classList.remove('modal-open');
    }
  }
}
