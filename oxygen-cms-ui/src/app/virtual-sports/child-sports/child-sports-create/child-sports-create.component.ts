import { Component, Inject, OnInit } from '@angular/core';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { BrandService } from '@app/client/private/services/brand.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { VirtualSportChild } from '@app/client/private/models/virtualSportChild.model';

@Component({
  selector: 'app-parent-sports-create',
  templateUrl: './child-sports-create.component.html',
  styleUrls: ['./child-sports-create.component.scss']
})
export class ChildSportsCreateComponent implements OnInit {
  public form: FormGroup;

  newChildSport: VirtualSportChild;
  getDataError: string;

  breadcrumbsData: Breadcrumb[];

  constructor(private brandService: BrandService,
              private dialogRef: MatDialogRef<ConfirmDialogComponent>,
              @Inject(MAT_DIALOG_DATA) private data: any) { }

  ngOnInit() {
    this.newChildSport = {
      id: '',
      sportId: this.data.sportId,
      title: '',
      active: false,
      streamUrl: '',
      classId: '',
      typeIds: '',
      numberOfEvents: 10,
      showRunnerNumber: true,
      showRunnerImages: true,
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',
      runnerImages: [],
      brand: this.brandService.brand,
    };

    this.form = new FormGroup({
      name: new FormControl('', [Validators.required]),
      streamUrl: new FormControl('', []),
      classId: new FormControl('', [Validators.required]),
      typeIds: new FormControl('', []),
      numberOfEvents: new FormControl(10, [Validators.min(1)]),
    });
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  getChildSport(): any {
    const form = this.form.value;
    this.newChildSport.title = form.name;
    this.newChildSport.classId = form.classId;
    this.newChildSport.typeIds = form.typeIds;
    this.newChildSport.streamUrl = form.streamUrl;
    this.newChildSport.numberOfEvents = form.numberOfEvents;
    return this.newChildSport;
  }
}
