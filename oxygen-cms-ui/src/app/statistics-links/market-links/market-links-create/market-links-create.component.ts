import { Component, OnInit } from '@angular/core';
import { MarketLink } from '@root/app/client/private/models/marketLink.model';
import { MatDialogRef } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '@root/app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@root/app/client/private/services/brand.service';
import { TAB_KEYS, OVERLAY_KEYS } from '../market-links.config';

@Component({
  selector: 'app-market-links-create',
  templateUrl: './market-links-create.component.html',
  styleUrls: ['./market-links-create.component.scss']
})
export class MarketLinksCreateComponent implements OnInit {
  public newMarketLink: MarketLink;
  public tabKeys = TAB_KEYS;
  public overlayKeys = OVERLAY_KEYS;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit(): void {
    this.newMarketLink = {
      id: '',
      updatedAt: '',
      createdAt: '',
      updatedBy: '',
      createdBy: '',
      updatedByUserName: '',
      createdByUserName: '',
      brand: this.brandService.brand,
      marketName: '',
      linkName: '',
      tabKey: '',
      overlayKey: '',
      enabled: true
    };
  }

  isValidFormData(): boolean {
    return this.newMarketLink.linkName.length > 0 &&
      this.isCorrectName(this.newMarketLink.linkName) &&
      this.newMarketLink.marketName.length > 0 &&
      this.isCorrectName(this.newMarketLink.marketName) &&
      this.newMarketLink.tabKey.length > 0 &&
      this.newMarketLink.overlayKey.length > 0;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  isCorrectName(value: string): boolean {
    return (/^[A-Za-z][A-Za-z0-9]*/ as RegExp).test(value);
  }

}
