import { Component } from '@angular/core';

import {
  BannersSectionComponent as CoralBannersSectionComponent
} from '@app/lazy-modules/banners/bannersSection/banners-section.component';

@Component({
  selector: 'banners-section',
  templateUrl: 'banners-section.component.html',
  styleUrls: [
    '../../../../../app/lazy-modules/banners/bannersSection/styles/banners-section.component.scss',
    'styles/lc-carousel.scss'
  ]
})

export class BannersSectionComponent extends CoralBannersSectionComponent {
  //Property added to fix strict mode issue fix
  disableScroll: boolean;
}
