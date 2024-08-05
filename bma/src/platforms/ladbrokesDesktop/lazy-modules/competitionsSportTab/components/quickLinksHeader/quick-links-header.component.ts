import { Component } from '@angular/core';

import QuickLinks from '../../constants/quickLinks';
import { IQuickLink } from '@ladbrokesDesktop/lazy-modules/competitionsSportTab/components/quickLinksHeader/quick-links-header.model';

@Component({
  selector: 'quick-links-header',
  templateUrl: './quick-links-header.component.html',
  styleUrls: ['./quick-links-header.component.scss']
})
export class QuickLinksHeaderComponent {
  ycIconDisplay: string = 'general';
  quickLinks: IQuickLink[] = QuickLinks;


  constructor() {}

  trackQuickLink(index: number, item: {[key: string]: any}): any {
    return item.id;
  }
}
