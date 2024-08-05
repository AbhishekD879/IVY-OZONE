import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import {ConfirmDialogComponent} from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import {BrandService} from '@app/client/private/services/brand.service';
import {AssetManagement, AssetManagementExt} from '@app/client/private/models/assetManagement.model';

@Component({
  templateUrl: './asset-management-create.component.html',
  styleUrls: ['./asset-management-create.component.scss']
})
export class AssetManagementCreateComponent implements OnInit {
  public form: FormGroup;
  public assetManagement: AssetManagementExt;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
  ) { }

  ngOnInit(): void {
    this.assetManagement = {
      id: null,
      createdAt: null,
      createdBy: null,
      updatedByUserName: null,
      createdByUserName: null,
      updatedAt: null,
      updatedBy: null,
      brand: this.brandService.brand,

      teamName: '',
      secondaryNames: null,
      secondaryNamesStr: '',
      sportId: null,
      primaryColour: '',
      secondaryColour: ''
    };

    this.form = new FormGroup({
      teamName: new FormControl('', [Validators.required]),
      secondaryNamesStr: new FormControl(''),
      sportId: new FormControl(null, [Validators.required]),
      primaryColour: new FormControl('', [Validators.required]),
      secondaryColour: new FormControl('', [Validators.required])
    });
  }

  getAssetManagement(): AssetManagement {
    const form = this.form.value;
    this.assetManagement.teamName = form.teamName.toUpperCase();
    this.assetManagement.secondaryNames = form.secondaryNamesStr
      ? form.secondaryNamesStr.split(',').map(item => item.trim().toUpperCase())
      : null;
    this.assetManagement.sportId = form.sportId;
    this.assetManagement.primaryColour = form.primaryColour;
    this.assetManagement.secondaryColour = form.secondaryColour;
    return this.assetManagement;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  isAssetManagementValid(): boolean {
    return this.form.valid;
  }
}
