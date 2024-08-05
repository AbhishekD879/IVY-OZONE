import { Component, ChangeDetectionStrategy } from '@angular/core';
import { MultipleSportsSectionsComponent } from '@app/inPlay/components/multipleSportsSections/multiple-sports-sections.component';
import { StickyVirtualScrollerService } from '@app/shared/components/stickyVirtualScroller/sticky-virtual-scroller.service';

@Component({
  selector: 'multiple-sports-sections',
  templateUrl: '../../../../../app/inPlay/components/multipleSportsSections/multiple-sports-sections.component.html',
  styleUrls: [
    '../../../../../app/inPlay/components/multipleSportsSections/multiple-sports-sections.component.scss',
    './multiple-sports-sections.component.scss'
  ],
  providers: [StickyVirtualScrollerService],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LadbrokesMultipleSportsSectionsComponent extends MultipleSportsSectionsComponent { }
