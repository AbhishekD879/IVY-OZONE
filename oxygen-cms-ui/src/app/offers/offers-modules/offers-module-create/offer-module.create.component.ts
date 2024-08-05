import {Component, OnInit} from '@angular/core';
import {OfferModule} from '../../../client/private/models/offermodule.model';
import {ConfirmDialogComponent} from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { MatDialogRef } from '@angular/material/dialog';
import {BrandService} from '../../../client/private/services/brand.service';

@Component({
  selector: 'offer-module-create-dialog',
  templateUrl: './offer-module.create.component.html',
  styleUrls: ['./offer-module.create.component.scss'],
  providers: []
})
export class OfferModuleCreateComponent implements OnInit {
  offerModulesData: OfferModule[] = [];
  getDataError: string;
  newOfferModule: OfferModule;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) {}

  /**
   * Checks whether offer module data are provided correctly
   */
  isValidModel() {
    return this.newOfferModule.name.length > 0;
  }

  /**
   * Closes modal windo
   */
  closeDialog() {
    this.dialogRef.close();
  }

  ngOnInit() {
    this.newOfferModule = {
        // values will be set from form
      name: '',
      showModuleOn: 'both',
      // default automatically created values
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      sortOrder: 0,
      brand: this.brandService.brand,
      disabled: false,
      updatedByUserName: '',
      createdByUserName: ''
    };
  }
}
