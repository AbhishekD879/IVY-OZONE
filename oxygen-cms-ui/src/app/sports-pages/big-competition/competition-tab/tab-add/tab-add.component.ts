import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import {CompetitionTab} from '../../../../client/private/models';
import {BrandService} from '@app/client/private/services/brand.service';
import {ConfirmDialogComponent} from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';

@Component({
  templateUrl: './tab-add.component.html'
})
export class TabAddComponent implements OnInit {
  public competitionTab: CompetitionTab;
  public form: FormGroup;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService) {
  }

  ngOnInit() {
    this.competitionTab = {
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',
      brand: this.brandService.brand,
      name: '',
      uri: '',
      displayOrder: 0,
      enabled: false,
      hasSubtabs: false,
      competitionSubTabs: [],
      competitionModules: []
    };

    this.form = new FormGroup({
      name: new FormControl('', [Validators.required]),
      enabled: new FormControl('', []),
      hasSubtabs: new FormControl('', [])
    });
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
