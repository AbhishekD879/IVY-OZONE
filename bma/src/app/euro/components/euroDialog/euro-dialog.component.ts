import { Component, Inject, ViewChild } from '@angular/core';
import { PlatformLocation } from '@angular/common';
import { DeviceService } from '@core/services/device/device.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { Router } from '@angular/router';
import { MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA } from '@angular/material/legacy-dialog';
import { EURO_MESSAGES } from '@app/euro/constants/euro-constants';

@Component({
  selector: 'euro-dialog',
  templateUrl: 'euro-dialog.component.html',
  styleUrls: ['euro-dialog.component.scss']
})

export class EuroDialogComponent extends AbstractDialogComponent {
  @ViewChild('dialog', { static: true }) dialog: any;
  @Inject(MAT_DIALOG_DATA) public data: any;
  public howItWorks: string;
  public howItWorksLink: string;
  public howItWorksText: string[];

  constructor(protected router: Router, public device: DeviceService, windowRef: WindowRefService, private loc: PlatformLocation) {
    super(device, windowRef);
    // closes modal when back button is clicked
    loc.onPopState(() => super.closeDialog());
  }

  /**
   * to open dialog box of howitworks
   * @returns {void}
   */
  public open(): void {
    super.open();
    this.howItWorks = this.params.data.howItWorks;
    this.windowRef.document.body.classList.add('howItWorks-modal-open');
    this.htmlDecode(this.howItWorks);
  }

  /**
   * to open dialog box of howitworks
   * @param howItWorks {string}
   * @returns {void}
   */
  public htmlDecode(howItWorks: string): void {
    const htmlElement = document.createElement('div');
    htmlElement.innerHTML = howItWorks;
    const text = htmlElement.getElementsByTagName('p');
    this.howItWorksText = [];
    for (let i = 0; i < text.length; i++) {
      if(text[i].innerText.trim() !== '') {
        this.howItWorksText.push(text[i].innerText);
      }
    }
  }

  /**
   * to open new page when more is clicked
   * @returns {void}
   */
  public openPromotions(): void {
    this.howItWorksLink = this.params.data.howItWorksLink;
    this.windowRef.document.body.classList.remove('howItWorks-modal-open');
    this.router.navigate([EURO_MESSAGES.PROMOTIONS]);
  }
}
