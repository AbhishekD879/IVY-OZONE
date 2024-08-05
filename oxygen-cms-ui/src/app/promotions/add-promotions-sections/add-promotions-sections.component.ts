import { PromotionsSections } from '@root/app/client/private/models/promotions-sections.model';
import { Component, OnInit } from '@angular/core';
import { BrandService } from '../../client/private/services/brand.service';
import { MatDialogRef } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../shared/dialog/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-add-promotions-sections',
  templateUrl: './add-promotions-sections.component.html',
  styleUrls: ['./add-promotions-sections.component.scss']
})
export class AddPromotionsSectionsComponent implements OnInit {
  public newPromotionsSections: PromotionsSections;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit(): void {
    this.newPromotionsSections = {
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      name: '',
      brand: this.brandService.brand,
      disabled: false,
      updatedByUserName: '',
      createdByUserName: '',
      id: '',
      promotionIds: null
    };
  }

  getNewPromotionsSections(): PromotionsSections {
    return this.newPromotionsSections;
  }

  isValidPromotionsSections(): boolean {
    return !!this.newPromotionsSections.name;
  }

  closeDialog() {
    this.dialogRef.close();
  }

}
