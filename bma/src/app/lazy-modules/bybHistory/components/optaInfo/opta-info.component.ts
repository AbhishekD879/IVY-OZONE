import {
  Component,
  Input,
  ComponentFactoryResolver,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  OnChanges,
  SimpleChanges
} from '@angular/core';

import { DeviceService } from '@core/services/device/device.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { OptaInfoPopupComponent } from '@lazy-modules/bybHistory/components/optaInfoPopup/opta-info-popup.component';


@Component({
  selector: 'opta-info',
  templateUrl: './opta-info.component.html',
  styleUrls: ['./opta-info.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OptaInfoComponent implements OnChanges {

  @Input() optaDisclaimer: string;
  @Input() isOptaAvailable: boolean;

  constructor(
    private device: DeviceService,
    private dialogService: DialogService,
    private infoDialog: InfoDialogService,
    private componentFactoryResolver: ComponentFactoryResolver,
    private changeDetectorRef: ChangeDetectorRef
  ) {}

  ngOnChanges(changes: SimpleChanges): void {
    if ((changes.optaDisclaimer.currentValue && !changes.optaDisclaimer.previousValue) || changes.isOptaAvailable) {
      this.changeDetectorRef.markForCheck();
    }
  }

  openSeeMorePopUp(): void {
    if (!this.device.isOnline()) {
      this.infoDialog.openConnectionLostPopup();
    } else {
      this.dialogService.openDialog(
        DialogService.API.optaInfoPopup,
        this.componentFactoryResolver.resolveComponentFactory(OptaInfoPopupComponent),
        true
      );
    }
  }
}
