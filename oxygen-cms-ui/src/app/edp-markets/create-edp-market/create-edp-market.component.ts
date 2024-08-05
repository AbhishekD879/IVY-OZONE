import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { EdpMarket } from '../../client/private/models/edpmarket.model';
import { ConfirmDialogComponent } from '../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../client/private/services/brand.service';
import { ApiClientService } from '../../client/private/services/http/index';
import { HttpResponse } from '@angular/common/http';

@Component({
  selector: 'app-create-edp-market',
  templateUrl: './create-edp-market.component.html',
  styleUrls: ['./create-edp-market.component.scss']
})
export class CreateEdpMarketComponent implements OnInit {

  public edpMarket: EdpMarket;
  public isLastItemAvalaible: boolean = false;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
    private apiClientService: ApiClientService
  ) { }

  ngOnInit(): void {
    this.apiClientService.edp()
        .findAllByBrand()
        .map((res: HttpResponse<EdpMarket[]>) => res.body)
        .subscribe((edpList: EdpMarket[]) => {
          this.isLastItemAvalaible = edpList.filter(e => e.lastItem).length === 0;
        });

    this.edpMarket = {
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',

      sortOrder: -1,
      name: '',
      lang: '',
      brand: this.brandService.brand,
      lastItem: false,
    };
  }

  public getNewEdpMarket(): EdpMarket {
    return this.edpMarket;
  }

  public isValidEdpMarket(): boolean {
    return !!(this.edpMarket.name);
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

}
