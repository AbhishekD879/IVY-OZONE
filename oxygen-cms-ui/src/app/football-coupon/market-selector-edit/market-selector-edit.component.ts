import * as _ from 'lodash';
import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { MarketSelector, MarketSelectorExt } from '@app/client/private/models/marketselector.model';
import { MARKET_TEMPLATE_NAMES } from '@app/core/constants/market-template-names.constant';

@Component({
  templateUrl: './market-selector-edit.component.html',
  styleUrls: ['./market-selector-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class MarketSelectorEditComponent implements OnInit {
  public marketTemplateNames: string[] = MARKET_TEMPLATE_NAMES.slice(); // array of free constant template names for dropdown list
  public isLoading: boolean = false;
  public marketSelector: MarketSelectorExt;
  public form: FormGroup;
  public breadcrumbsData: Breadcrumb[];
  public isTemplateNameFree: boolean = true;

  private allUsedTemplateNames: string[];                               // array of all used template names from DB without current edited
  private keyUpTimeout: number = null;

  @ViewChild('actionButtons') actionButtons;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
  ) {
    this.isValidModel = this.isValidModel.bind(this);
  }

  ngOnInit(): void {
    this.form = new FormGroup({
      title: new FormControl('', [Validators.required]),
      templateMarketName: new FormControl('', [Validators.required]),
      headers: new FormControl('')
    });
    this.loadInitData();
  }

  loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;

    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService
        .marketSelector()
        .getById(params['id'])
        .map((marketSelector: HttpResponse<MarketSelector>) => {
          return marketSelector.body;
        }).subscribe((marketSelector: MarketSelector) => {
          this.marketSelector = marketSelector as MarketSelectorExt;
          this.marketSelector.headerStr = marketSelector.header ? marketSelector.header.toString() : '';
          this.availableMarketTemplateNames();
          this.setBreadcrumbsData();
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        }, () => {
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        });
    });
  }

  /**
   *  Get used templateMarketNames and exclude them from dropdown box of edit page
   */
  private availableMarketTemplateNames(): void {
    this.apiClientService.marketSelector()
      .getUsedMarketTemplateNames()
      .subscribe((data: string[]) => {
        this.marketTemplateNames = _.difference(this.marketTemplateNames, data);
        this.marketTemplateNames.push(this.marketSelector.templateMarketName);
        this.allUsedTemplateNames = _.difference(data, [ this.marketSelector.templateMarketName ]);
      }, error => {
        console.warn(`Error in availableMarketTemplateNames of market-selector-edit component: ${error.message}`);
      });
  }

  private setBreadcrumbsData(): void {
    this.breadcrumbsData = [];
    this.breadcrumbsData.push({
      label: `Coupon Market Selectors`,
      url: `/football-coupon/coupon-market-selectors`
    });
    this.breadcrumbsData.push({
      label: this.marketSelector.title,
      url: `/football-coupon/coupon-market-selectors/${this.marketSelector.id}`
    });
  }

  save(): void {
    this.globalLoaderService.showLoader();
    this.marketSelector.header = this.marketSelector.headerStr ? this.marketSelector.headerStr.split(',').map(item => item.trim()) : null;
    this.apiClientService.marketSelector()
      .edit(this.marketSelector)
      .map((data: HttpResponse<MarketSelector>) => {
        return data.body;
      })
      .subscribe((data: MarketSelector) => {
        this.marketSelector = data as MarketSelectorExt;
        this.marketSelector.headerStr = data.header ? data.header.toString() : '';
        this.actionButtons.extendCollection(this.marketSelector);
        this.dialogService.showNotificationDialog({
          title: 'Coupon Market Selector',
          message: 'Market Selector is Saved.'
        });
        this.globalLoaderService.hideLoader();
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  revert(): void {
    this.loadInitData();
  }

  remove(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.marketSelector()
      .delete(this.marketSelector.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/football-coupon/coupon-market-selectors/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.remove();
        break;
      case 'save':
        this.save();
        break;
      case 'revert':
        this.revert();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
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

  /**
   *  Check if headers in the string are less then three and no one empty
   */
  isValidHeaders(str: string): boolean {
    if (str) {
      const headers = str.split(',');
      return headers.length <= 3 && !_.some(headers, item => item.trim() === '');
    } else {
      return true;
    }
  }

  isValidModel(marketSelector: MarketSelectorExt): boolean {
    return marketSelector && marketSelector.title !== '' && marketSelector.templateMarketName !== ''  && this.isTemplateNameFree &&
      this.isValidHeaders(marketSelector.headerStr);
  }
}
