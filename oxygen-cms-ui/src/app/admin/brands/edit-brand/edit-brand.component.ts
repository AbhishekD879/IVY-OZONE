import {Component, OnInit, ViewChild} from '@angular/core';
import {HttpResponse} from '@angular/common/http';
import {ActivatedRoute, Params, Router} from '@angular/router';

import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {DialogService} from '../../../shared/dialog/dialog.service';
import {BrandsAPIService} from '../service/brands.api.service';
import {Brand} from '../../../client/private/models';

@Component({
  selector: 'edit-brand',
  templateUrl: './edit-brand.component.html',
  styleUrls: ['./edit-brand.component.scss'],
  providers: [
    DialogService
  ]
})
export class EditBrandComponent implements OnInit {

  getDataError: string;
  public isLoading: boolean = true;
  public brand: Brand;
  @ViewChild('actionButtons') actionButtons;

  constructor(
    private globalLoaderService: GlobalLoaderService,
    private brandsAPIService: BrandsAPIService,
    private activatedRoute: ActivatedRoute,
    private dialogService: DialogService,
    private router: Router
  ) { }

  ngOnInit() {
    this.loadInitData();
  }

  saveChanges(): void {
    this.brandsAPIService
      .putBrandChanges(this.brand)
      .map((response: HttpResponse<Brand>) => {
        return response.body;
      })
      .subscribe((brand) => {
        this.brand = brand;
        this.actionButtons.extendCollection(this.brand);
        this.dialogService.showNotificationDialog({
          title: `Brand`,
          message: `Brand is Saved`
        });
      });
  }

  revertChanges(): void {
    this.loadInitData(false);
  }

  removeBrand(): void {
    this.brandsAPIService.deleteBrand(this.brand.id)
      .subscribe(() => {
        this.router.navigate(['/admin/brands']);
      });
  }

  isValidBrandCode(): boolean {
    return this.brand.brandCode.indexOf(' ') === -1;
  }

  isValidForm(brand: Brand): boolean {
    return brand.brandCode.length && brand.brandCode.indexOf(' ') === -1 &&
      brand.title.length > 0;
  }


  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeBrand();
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  private loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;
    this.getDataError = '';

    this.activatedRoute.params.subscribe((params: Params) => {
      this.brandsAPIService.getSingleBrandData(params['id'])
        .map((brand: HttpResponse<Brand>) => {
          return brand.body;
        })
        .subscribe((brand: Brand) => {
          this.brand = brand;
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        }, error => {
          this.globalLoaderService.hideLoader();
          this.getDataError = error.message;
          this.isLoading = false;
        });
    });
  }
}

