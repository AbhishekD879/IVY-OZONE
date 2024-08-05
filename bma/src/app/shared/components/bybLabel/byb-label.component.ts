import {
  ChangeDetectionStrategy,
  Component, Input
} from '@angular/core';
import { DeviceService } from '@core/services/device/device.service';

@Component({
  selector: 'byb-label',
  templateUrl: 'byb-label.component.html',
  styleUrls: ['byb-label.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BybLabelComponent {
  @Input() mode: string = 'sm';
  isMobileOnly: boolean;

  constructor(
    private deviceService: DeviceService
  ) {
    this.isMobileOnly = this.deviceService.isMobileOnly;
  }
}
