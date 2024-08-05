import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';
import { BrandService } from '@app/client/private/services/brand.service';

/**
 * Five a side guard used to validate if five a side module
 * is loaded only for ladbrokes module
 */
@Injectable()
export class FiveASideShowDownGuardService implements CanActivate {
  readonly DEFAULT_BRAND = this.brandService.defaultBrand;
  readonly HOME_ROUTE = '/featured-modules';
  constructor(public brandService: BrandService, public router: Router) {}
  canActivate(): boolean {
    if (this.brandService.brand === this.DEFAULT_BRAND) {
      this.router.navigate([this.HOME_ROUTE]);
      return false;
    }
    return true;
  }
}
