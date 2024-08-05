import { HttpResponse } from '@angular/common/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { CouponMarketMapping } from '@root/app/client/private/models/couponMarketMapping.model';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { DialogService } from '@app/shared/dialog/dialog.service';

@Component({
  selector: 'app-coupon-market-mapping-edit',
  templateUrl: './coupon-market-mapping-edit.component.html',
  styleUrls: ['./coupon-market-mapping-edit.component.scss']
})
export class CouponMarketMappingEditComponent implements OnInit {
  public form: FormGroup;
  public breadcrumbsData: Breadcrumb[];
  isLoading: boolean = false;
  couponMarketMapping: CouponMarketMapping;
  @ViewChild('actionButtons') actionButtons;
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private dialogService: DialogService,
    private apiClientService: ApiClientService,
  ) {
    this.isValidModel = this.isValidModel.bind(this);
   }

  ngOnInit(): void {
    this.form = new FormGroup({
      couponId: new FormControl('', [Validators.required]),
      marketName: new FormControl('', [Validators.required]),
    });
    this.loadInitData();
  }

  loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;

    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService
        .couponMarketMapping()
        .getById(params['id'])
        .map((couponMarketMapping: HttpResponse<CouponMarketMapping>) => {
          return couponMarketMapping.body;
        }).subscribe((couponMarketMapping: CouponMarketMapping) => {
          this.couponMarketMapping = couponMarketMapping as CouponMarketMapping;
          // this.availableMarketTemplateNames();
          this.setBreadcrumbsData();
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        }, () => {
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        });
    });
  }

  private setBreadcrumbsData(): void {
    this.breadcrumbsData = [];
    this.breadcrumbsData.push({
      label: `Coupon Market Mapping`,
      url: `/football-coupon/coupon-market-selectors`
    });
    this.breadcrumbsData.push({
      label: this.couponMarketMapping.couponId,
      url: `/football-coupon/coupon-market-selectors/mapping/${this.couponMarketMapping.id}`
    });
  }

  isValidModel(couponMarketMapping: any): boolean {
    return couponMarketMapping && couponMarketMapping.couponId !== '' && couponMarketMapping.marketName !== '';
  }

  save(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.couponMarketMapping()
      .edit(this.couponMarketMapping)
      .map((data: HttpResponse<CouponMarketMapping>) => {
        return data.body;
      })
      .subscribe((data: CouponMarketMapping) => {
        this.couponMarketMapping = data as CouponMarketMapping;
        this.actionButtons.extendCollection(this.couponMarketMapping);
        this.dialogService.showNotificationDialog({
          title: 'Coupon Market Mapping',
          message: 'Coupon Market Mapping is Saved.'
        });
        this.globalLoaderService.hideLoader();
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

  revert(): void {
    this.loadInitData();
  }

  remove(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.couponMarketMapping()
      .delete(this.couponMarketMapping.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/football-coupon/coupon-market-selectors/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

}
