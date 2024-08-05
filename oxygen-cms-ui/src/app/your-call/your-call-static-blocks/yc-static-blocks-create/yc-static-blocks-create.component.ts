import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { BrandService } from '@app/client/private/services/brand.service';
import { YourCallStaticBlock } from '@app/client/private/models/yourcallstaticblock.model';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-yc-static-blocks-create',
  templateUrl: './yc-static-blocks-create.component.html',
  styleUrls: ['./yc-static-blocks-create.component.scss']
})
export class YcStaticBlocksCreateComponent implements OnInit {
  public yourCallStaticBlock: YourCallStaticBlock;

  constructor(private brandService: BrandService,
              private dialogRef: MatDialogRef<ConfirmDialogComponent>) { }

  ngOnInit() {
    const brand = this.brandService.brand;
    this.yourCallStaticBlock = {
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',
      title_brand: '',
      title: '',
      lang: '',
      brand: brand,
      enabled: false,
      htmlMarkup: '',
      fiveASide: false
    };
  }

  isValidYourCallStaticBlock(): boolean {
    return !!(this.yourCallStaticBlock.title && this.yourCallStaticBlock.brand);
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
