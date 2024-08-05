import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { BYBSwitcher } from '../../../client/private/models';
import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../../client/private/services/brand.service';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'byb-switchers-create',
  templateUrl: './byb-switchers-create.component.html',
  styleUrls: ['./byb-switchers-create.component.scss']
})
export class BYBSwitchersCreateComponent implements OnInit {
  public form: FormGroup;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService) {
  }

  ngOnInit() {
    this.form = new FormGroup({
      name: new FormControl('', [Validators.required]),
      provider: new FormControl('', [Validators.required]),
      enabled: new FormControl('true', []),
      default: new FormControl('', []),
      brand: new FormControl(this.brandService.brand, [])
    });
  }

  public get name(): AbstractControl {
    return this.form.get('name');
  }

  public get provider(): AbstractControl {
    return this.form.get('provider');
  }

  public get enabled(): AbstractControl {
    return this.form.get('enabled');
  }

  public get default(): AbstractControl {
    return this.form.get('default');
  }

  public getBYBSwitcher(): BYBSwitcher {
    return this.form.value;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
