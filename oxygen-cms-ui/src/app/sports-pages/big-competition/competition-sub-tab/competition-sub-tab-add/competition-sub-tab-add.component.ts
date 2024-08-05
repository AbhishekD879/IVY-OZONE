import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import {CompetitionTab} from '@app/client/private/models';
import {BrandService} from '@app/client/private/services/brand.service';
import {ConfirmDialogComponent} from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';

@Component({
  templateUrl: './competition-sub-tab-add.component.html'
})
export class CompetitionSubTabAddComponent implements OnInit {
  public form: FormGroup;
  public tab: CompetitionTab;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) {}

  ngOnInit() {
    this.tab = {
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
      enabled: new FormControl('', [])
    });
  }

  public closeDialog(): void {
    this.dialogRef.close();
  }
}
