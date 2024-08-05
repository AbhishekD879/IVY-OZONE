import { Component, Input, ViewChild } from '@angular/core';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { ILottoCmsPage } from '../../models/lotto.model';
import { LOTTO_TEMPLATES } from '../../services/mainLotto/main-lotto.constant';


@Component({
  selector: 'lotto-info-dialog',
  templateUrl: './lotto-info-dialog.component.html',
  styleUrls: ['./lotto-info-dialog.component.scss']
})
export class LottoInfoDialogComponent extends AbstractDialogComponent {
  @ViewChild('dialog', { static: true }) dialog;
  @Input() singleData: ILottoCmsPage;
  cmsLotto: {};
  lotto = LOTTO_TEMPLATES;
  brandType: string;
    
  constructor(
    device: DeviceService, windowRef: WindowRefService,
  ) {
    super(device, windowRef);
  }

  ngOnInit(): void {
    this.cmsLotto = this.params;
    this.brandType = this.device.brand;
    super.ngOnInit();
}

  closeThisDialog() {
    super.closeDialog();
  }

}
