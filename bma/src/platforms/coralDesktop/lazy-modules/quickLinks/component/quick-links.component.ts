import { Component, ViewEncapsulation } from '@angular/core';
import { QuickLinksComponent as CoralMobileQuickLinksComponent} from '@app/lazy-modules/quickLinks/component/quick-links.component';

@Component({
  selector: 'quick-links',
  templateUrl: './quick-links.component.html',
  styleUrls: ['./quick-links.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class CoralQuickLinksComponent extends CoralMobileQuickLinksComponent {
}
