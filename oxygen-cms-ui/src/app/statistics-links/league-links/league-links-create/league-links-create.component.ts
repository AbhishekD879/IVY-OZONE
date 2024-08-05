import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { LeagueLink } from '@root/app/client/private/models';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@app/client/private/services/brand.service';

@Component({
  selector: 'app-league-links-create',
  templateUrl: './league-links-create.component.html',
  styleUrls: ['./league-links-create.component.scss']
})
export class LeagueLinksCreateComponent implements OnInit {
  public newLeagueLink: LeagueLink;
  public pattern = /^(\s*|\d+)$/;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit(): void {
    this.newLeagueLink = {
      id: '',
      updatedAt: '',
      createdAt: '',
      updatedBy: '',
      createdBy: '',
      updatedByUserName: '',
      createdByUserName: '',
      brand: this.brandService.brand,
      obLeagueId: '',
      dhLeagueId: '',
      enabled: true,
      linkName: '',
      couponIds: [],
    };
  }

  updateCouponIds(values: Array<number>): void {
    this.newLeagueLink.couponIds = values;
  }

  isValidFormData(): boolean {
    return this.newLeagueLink.linkName.length > 0 &&
    this.isCorrectName(this.newLeagueLink.linkName) &&
    this.newLeagueLink.obLeagueId.length > 0 &&
    this.isNumber(this.newLeagueLink.obLeagueId) &&
    this.newLeagueLink.dhLeagueId.length > 0 &&
    this.isNumber(this.newLeagueLink.dhLeagueId) &&
    this.newLeagueLink.couponIds.length > 0;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  isCorrectName(value: string): boolean {
    return (/^[A-Za-z][A-Za-z0-9]*/ as RegExp).test(value);
  }

  isNumber(value: any): boolean {
    return this.pattern.test(value);
  }

}
