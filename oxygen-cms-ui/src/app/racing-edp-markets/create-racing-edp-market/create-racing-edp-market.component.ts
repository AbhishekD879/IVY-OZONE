import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../client/private/services/brand.service';
import { RacingEdpMarket } from '../../client/private/models/racing.edpmarket.model';
import { RACING_DEFAULT_VALUS } from '../constants/racing-edp.constants';

@Component({
  selector: 'app-create-racing-edp-market',
  templateUrl: './create-racing-edp-market.component.html'
})
export class CreateRacingEdpMarketComponent implements OnInit {
  racingEdpMarket: RacingEdpMarket;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
  ) { }

  ngOnInit(): void {
    this.racingEdpMarket = {
      ...RACING_DEFAULT_VALUS,
      brand: this.brandService.brand,
    };
  }

  /**
   * Fetched edp market
   */
  getNewEdpMarket(): RacingEdpMarket {
    return this.racingEdpMarket;
  }

  /**
   * Verify the validity of form
   */
  isValidEdpMarket(): boolean {
    return !!(this.racingEdpMarket.name);
  }

  /**
   * closes the dialog
   */
  closeDialog(): void {
    this.dialogRef.close();
  }

}
