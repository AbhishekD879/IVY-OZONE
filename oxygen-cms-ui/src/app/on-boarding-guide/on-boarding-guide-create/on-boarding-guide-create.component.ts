import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {OnBoardingGuide} from '@app/client/private/models/onBoardingGuide';
import { MatDialogRef } from '@angular/material/dialog';
import {ConfirmDialogComponent} from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import {BrandService} from '@app/client/private/services/brand.service';

@Component({
  selector: 'app-on-boarding-guide-create',
  templateUrl: './on-boarding-guide-create.component.html'
})
export class OnBoardingGuideCreateComponent implements OnInit {

  public form: FormGroup;
  public onBoardingGuide: OnBoardingGuide;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit(): void {
    this.onBoardingGuide = {
      id: '',
      brand: this.brandService.brand,
      createdBy: '',
      createdAt: '',
      updatedBy: '',
      updatedAt: '',
      updatedByUserName: '',
      createdByUserName: '',

      enabled: true,
      guideName: '',
      guidePath: '',
      svgFilename: {
        filename: '',
        originalfilename: '',
        path: '',
        size: 0,
        filetype: ''
      }
    };
    this.form = new FormGroup({
      name: new FormControl('', [Validators.required])
    });
  }

  getOnBoardingGuide(): OnBoardingGuide {
    this.onBoardingGuide.guideName = this.form.value.name;
    return this.onBoardingGuide;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

}
