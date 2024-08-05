import { Component } from '@angular/core';

import { YourCallTabContentComponent } from '@yourcall/components/yourCallTabContent/your-call-tab-content.component';

@Component({
  selector: 'yourcall-tab-content',
  templateUrl: './your-call-tab-content.component.html'
})
export class DesktopYourCallTabContentComponent extends YourCallTabContentComponent {

  getTitle(title: string): string {
    return title && title.toLowerCase() || '';
  }
}
