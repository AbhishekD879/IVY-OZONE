import { Component, OnInit } from '@angular/core';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { BrandService } from '@app/client/private/services/brand.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { MatDialogRef } from '@angular/material/dialog';
import { VirtualSportParent } from '@app/client/private/models/virtualSportParent.model';

@Component({
  selector: 'app-parent-sports-create',
  templateUrl: './parent-sports-create.component.html',
  styleUrls: ['./parent-sports-create.component.scss']
})
export class ParentSportsCreateComponent implements OnInit {
  public form: FormGroup;

  newParentSport: VirtualSportParent;
  getDataError: string;

  breadcrumbsData: Breadcrumb[];

  constructor(private brandService: BrandService,
              private dialogRef: MatDialogRef<ConfirmDialogComponent>) { }

  ngOnInit() {
    this.newParentSport = {
      id: '',
      title: '',
      active: false,
      svgFilename: null,
      svgId: '',
      ctaButtonUrl: '',
      ctaButtonText: '',
      desktopImageId: '',
      mobileImageId: '',
      redirectionURL: '',
      signposting: '',
      topSports: false,
      topSportsIndex: null,
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',
      brand: this.brandService.brand,
    };

    this.form = new FormGroup({
      name: new FormControl('', [Validators.required]),
    });
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  getParentSport(): any {
    const form = this.form.value;
    this.newParentSport.title = form.name;
    return this.newParentSport;
  }
}
