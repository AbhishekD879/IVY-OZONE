import * as _ from 'lodash';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@app/client/private/services/brand.service';
import { MarketSelector, MarketSelectorExt } from '@app/client/private/models/marketselector.model';
import { MARKET_TEMPLATE_NAMES } from '@app/core/constants/market-template-names.constant';
import { ApiClientService } from '@app/client/private/services/http';

@Component({
  templateUrl: './market-selector-create.component.html',
  styleUrls: ['./market-selector-create.component.scss']
})
export class MarketSelectorCreateComponent implements OnInit {
  public marketTemplateNames: string[] = MARKET_TEMPLATE_NAMES.slice();  // array of free constant template names for dropdown list
  public form: FormGroup;
  public marketSelector: MarketSelectorExt;
  public isTemplateNameFree: boolean = true;

  private allUsedTemplateNames: string[];                               // array of all used template names from DB without current edited
  private keyUpTimeout: number = null;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private apiClientService: ApiClientService,
    private brandService: BrandService
  ) { }

  ngOnInit(): void {
    this.marketSelector = {
      id: null,
      createdAt: null,
      createdBy: null,
      updatedByUserName: null,
      createdByUserName: null,
      updatedAt: null,
      updatedBy: null,
      brand: this.brandService.brand,

      title: '',
      templateMarketName: '',
      header: null,
      headerStr: '',
      sortOrder: 0
    };
    this.availableMarketTemplateNames();

    this.form = new FormGroup({
      title: new FormControl('', [Validators.required]),
      templateMarketName: new FormControl('', [Validators.required]),
      headers: new FormControl('')
    });
  }

  /**
   *  Get used templateMarketNames and exclude them from dropdown box of a page
   */
  private availableMarketTemplateNames(): void {
    this.apiClientService.marketSelector()
      .getUsedMarketTemplateNames()
      .subscribe((data: string[]) => {
        this.marketTemplateNames = _.difference(this.marketTemplateNames, data);
        this.allUsedTemplateNames = data.slice();
      }, error => {
        console.warn(`Error in availableMarketTemplateNames of market-selector-create component: ${error.message}`);
      });
  }

  getMarketSelector(): MarketSelector {
    const form = this.form.value;
    this.marketSelector.title = form.title;
    this.marketSelector.templateMarketName = form.templateMarketName;
    this.marketSelector.header = form.headers ? form.headers.split(',').map(item => item.trim()) : null;
    return this.marketSelector;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  private checkTemplateNameFree(): void {
    this.isTemplateNameFree = (_.indexOf(this.allUsedTemplateNames, this.marketSelector.templateMarketName) === -1);
  }

  /**
   *  onKeyUp handler for templateMarketName input
   */
  isTemplateNameValid(): void {
    clearTimeout(this.keyUpTimeout);
    this.keyUpTimeout = window.setTimeout( this.checkTemplateNameFree.bind(this), 300);
  }

  isValidHeaders(): boolean {
    const form = this.form.value;
    if (form.headers) {
      const headers = form.headers.split(',');
      return headers.length <= 3 && !_.some(headers, item => item.trim() === '');       // less then three and no one empty
    } else {
      return true;
    }
  }

  isMarketSelectorValid(): boolean {
    return this.form.valid && this.isValidHeaders() && this.isTemplateNameFree;
  }
}
