import { Component } from '@angular/core';

@Component({
  selector: 'single-promotion-page',
  templateUrl: 'single-promotion-page.component.html'
})

export class SinglePromotionPageComponent {
  title: string = 'promotions.promotions';

  /**
   * changes the name of the title dynamically
   */
  changeTitle(title: string): void {
    this.title = title;
  }
}
