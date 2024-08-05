import { Component, Inject, OnInit, ViewChild } from '@angular/core';
import { DeviceService } from '@core/services/device/device.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA } from '@angular/material/legacy-dialog';
import environment from '@environment/oxygenEnvConfig';
@Component({
    selector: 'cash-out-popup',
    templateUrl: './cash-out-popup.component.html'
})
export class CashOutPopUpComponent extends AbstractDialogComponent implements OnInit {

    @ViewChild('cashOutPopUp', { static: true }) dialog;
    @Inject(MAT_DIALOG_DATA) public data: any;
    eventNames: string[];
    eventFlag: boolean = false;
    message: string;
    brand: string = environment.brand;
    constructor(
        device: DeviceService, windowRef: WindowRefService
    ) {
        super(device, windowRef);
    }

    /**
     * to open dialog box
     * @returns {void}
     */
    public open(): void {
        super.open();
        if (this.params && this.params.data && this.params.data.eventName) {
            this.eventNames = this.params.data.eventName;
            this.message = this.params.data.suspension;
            if (this.eventNames.length) {
                this.eventFlag = true;
            }
        }
    }
}
