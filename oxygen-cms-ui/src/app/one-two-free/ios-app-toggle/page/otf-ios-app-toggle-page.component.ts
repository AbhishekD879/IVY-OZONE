import {Component, OnInit} from '@angular/core';
import {DialogService} from '@app/shared/dialog/dialog.service';

import {BrandService} from '@app/client/private/services/brand.service';
import {OtfIosAppToggle} from '@app/client/private/models/otfIosAppToggle.model';
import {OtfIosAppToggleApiService} from '@app/one-two-free/service/otfIosAppToggle.api.service';

@Component({
  selector: 'otf-ios-app-toggle-page',
  templateUrl: './otf-ios-app-toggle-page.component.html',
  styleUrls: ['./otf-ios-app-toggle-page.component.scss']
})
export class OtfIosAppTogglePageComponent implements OnInit {
  otfIosAppToggle: OtfIosAppToggle;

  constructor(private api: OtfIosAppToggleApiService,
              private dialogService: DialogService,
              private brandService: BrandService) {

  }

  ngOnInit(): void {
    this.load();
  }

  actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.save();
        break;
      case 'revert':
        this.revert();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  private load() {
    this.api.getOneByBrand()
      .subscribe((data: any) => {
        this.otfIosAppToggle = data.body;
      }, error => {
        if (error.status === 404) {
          this.otfIosAppToggle = this.empty();
        } else {
          console.log(error);
          this.openErrorDialog();
        }
      });
  }

  private save() {
    if (this.isNotValid()) {
      this.dialogService.showNotificationDialog({
        title: 'Error on saving',
        message: 'Text and Close CTA button text must not be empty'
      });
    } else if (this.otfIosAppToggle.createdAt) {
      this.api.update(this.otfIosAppToggle)
        .subscribe((data: any) => {
          this.otfIosAppToggle = data.body;
          this.openSuccessDialog();
        }, error => {
          console.log(error);
          this.openErrorDialog();
        });
    } else {
      this.api.create(this.otfIosAppToggle)
        .subscribe((data: any) => {
          this.otfIosAppToggle = data.body;
          this.openSuccessDialog();
        }, error => {
          console.log(error);
          this.openErrorDialog();
        });
    }
  }

  private revert() {
    this.load();
  }

  private isNotValid() {
    return !this.otfIosAppToggle.text
      || !this.otfIosAppToggle.closeCtaText;
  }

  private openErrorDialog() {
    this.dialogService.showNotificationDialog({
      title: 'Error on saving',
      message: 'Ooops... Something went wrong, please contact support team'
    });
  }

  private openSuccessDialog() {
    this.dialogService.showNotificationDialog({
      title: 'Success',
      message: 'Your changes have been saved'
    });
  }

  private empty(): OtfIosAppToggle {
    return {
      brand: this.brandService.brand,
      text: null,
      createdAt: null,
      createdBy: null,
      createdByUserName: null,
      iosAppOff: null,
      url: null,
      urlText: null,
      closeCtaText: null,
      proceedCtaText: null,
      id: null,
      updatedAt: null,
      updatedBy: null,
      updatedByUserName: null
    };
  }
}
