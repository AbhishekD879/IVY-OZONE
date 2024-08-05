import {
  Component, Input, OnChanges, OnInit, SimpleChanges,
  Output, EventEmitter, OnDestroy
} from '@angular/core';
import { IConstant } from '@core/services/models/constant.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'bs-overlay-notification',
  template: '<bs-notification [bsIsClosable]="false" [bsType]="messageType" ' +
    '[bsMessage]="overlayMsg" *ngIf="overlayMsg"></bs-notification>',
  styleUrls: ['betslip-overlay-notification.component.scss']
})
export class BetslipOverlayNotificationComponent implements OnInit, OnChanges, OnDestroy {
  @Input() messageConfig: IConstant;
  @Output() readonly clear = new EventEmitter();

  overlayMsg: string;
  messageType: string;

  private timeoutId: number;
  private readonly duration: number = 5000;

  constructor(
    private windowRefService: WindowRefService
  ) {
  }

  ngOnInit() {
    if (this.messageConfig && this.messageConfig.message) {
      this.showMessage(this.messageConfig.message);
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes && changes.messageConfig && changes.messageConfig.currentValue.message) {
      this.showMessage(changes.messageConfig.currentValue.message);
    }
  }

  ngOnDestroy(): void {
    this.clear.emit();
  }

  /**
   * show overlay message
   * @param message
   */
  private showMessage(message: string): void {
    if (this.messageConfig.type === 'ACCA') {
      this.messageType = 'animated error acca-transparent';
    } else {
      this.messageType = 'animated error';
    }

    this.overlayMsg = message;
    this.windowRefService.nativeWindow.clearTimeout(this.timeoutId);
    this.timeoutId = this.windowRefService.nativeWindow.setTimeout(() => {
      this.overlayMsg = '';
      this.clear.emit();
    }, this.duration);
  }
}
