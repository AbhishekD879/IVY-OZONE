import { Component, OnInit } from '@angular/core';
import { BrandService } from '@app/client/private/services/brand.service';
import { MatDialogRef } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-add-navigation-group',
  templateUrl: './add-navigation-group.component.html',
  styleUrls: ['./add-navigation-group.component.scss']
})
export class AddNavigationGroupComponent implements OnInit {
  public newNavigationGroup: any;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit(): void {
    this.newNavigationGroup = {
      brand: this.brandService.brand,
      title: '',
      status: false
    };
  }

  getNewNavigationGroup(): any {
    return this.newNavigationGroup;
  }

  isValidNavigationGroup(): boolean {
    return !!this.newNavigationGroup.title;
  }

  closeDialog() {
    this.dialogRef.close();
  }

}
