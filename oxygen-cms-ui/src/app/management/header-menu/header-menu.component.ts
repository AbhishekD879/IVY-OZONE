import { Component, OnInit } from '@angular/core';
import activateNavbar from './header-menu.api.js';

import { AuthService } from '../../auth/auth.service';
import { BrandService } from '../../client/private/services/brand.service';
import { Brand } from '../../client/private/models';
import {ActivatedRoute, Router} from '@angular/router';
import { SegmentStoreService } from '@root/app/client/private/services/segment-store.service';

@Component({
  selector: 'cms-header-menu',
  templateUrl: './header-menu.component.html',
  styleUrls: ['./header-menu.component.scss']
})
export class HeaderMenuComponent implements OnInit {
  activeBrand: string = this.brandService.brand;
  brandsList: Brand[];

  constructor(
    private auth: AuthService,
    private brandService: BrandService,
    private route: ActivatedRoute,
    private router: Router,
    private segmentStoreService: SegmentStoreService
  ) {}

  logOut(): void {
    this.segmentStoreService.initSegmentObj();
    this.auth.logOut();
  }

  onBrandSelect(brand: string): void {
    if (brand !== this.brandService.brand) {
      this.router.navigate(['/'])
        .then(() => {
          this.brandService.brand = brand;
          this.segmentStoreService.initSegmentObj();
        });
    }
  }

  ngOnInit(): void {
    const brandsList = this.route.snapshot.data['mainData'][1].body;

    if (Array.isArray(brandsList)) {
      this.brandsList = brandsList.filter(brand => !brand.disabled);
      this.brandService.brandsList = brandsList;
    }
    activateNavbar();
  }
}
