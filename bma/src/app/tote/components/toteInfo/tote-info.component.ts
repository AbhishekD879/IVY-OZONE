import { Component, OnInit } from '@angular/core';

import { CmsService } from '@coreModule/services/cms/cms.service';
import { TOTE_CONFIG } from '../../tote.constant';

@Component({
  selector: 'tote-info',
  templateUrl: './tote-info.component.html'
})
export class ToteInfoComponent implements OnInit {
  svg: string;
  svgId: string;

  readonly bannerCategory: string = TOTE_CONFIG.TOTE_INFO_BANNER_TARGET_URI;

  constructor(private cmsService: CmsService) {
  }

  ngOnInit(): void {
    this.cmsService.getItemSvg('International Tote')
      .subscribe((icon) => {
        this.svg = icon ? icon.svg : null;
        this.svgId = icon ? icon.svgId : null;
      });
  }

}
