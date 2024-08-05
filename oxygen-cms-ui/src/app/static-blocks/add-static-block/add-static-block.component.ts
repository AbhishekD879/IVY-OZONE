import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { StaticBlock } from '@app/client/private/models/staticblock.model';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@app/client/private/services/brand.service';

@Component({
  selector: 'app-add-static-block',
  templateUrl: './add-static-block.component.html',
  styleUrls: ['./add-static-block.component.scss']
})
export class AddStaticBlockComponent implements OnInit {
  public newStaticBlock: StaticBlock;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit(): void {
    this.newStaticBlock = {
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      title_brand: '',
      uri: '',
      title: '',
      lang: '',
      brand: this.brandService.brand,
      enabled: true,
      htmlMarkup: '',
      updatedByUserName: '',
      createdByUserName: ''
    };
  }

  getNewStaticBlock(): StaticBlock {
    return this.newStaticBlock;
  }

  isValidStaticBlock(): boolean {
    return !!(this.newStaticBlock.title &&
              this.newStaticBlock.uri);
  }

  closeDialog() {
    this.dialogRef.close();
  }
}
