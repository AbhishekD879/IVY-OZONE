import {
  Directive,
  AfterViewInit
} from '@angular/core';

import { ScrollableDirective } from '@shared/directives/scrollable.directive';

// eslint-disable-next-line
@Directive({ selector: '[scrollable-racing]' })
export class ScrollableRacingDirective extends ScrollableDirective implements AfterViewInit {
  ngAfterViewInit(): void {
    this.windowRef.nativeWindow.setTimeout(() => {
      this.element = this.el.nativeElement;
      this.scrollToSelected();
      this.setScrollable();
    });
  }

  /**
   * Show last 2 resulted / race-off items if possible
   */
  protected scrollToSelected(): void {
    let scrollRaceStart: Element = this.element.querySelector('.active') || this.element.querySelector('li.race-on');

    // two nodes before first active race or selected in the meetings list
    scrollRaceStart = scrollRaceStart ? scrollRaceStart.previousElementSibling : null;
    scrollRaceStart = scrollRaceStart ? scrollRaceStart.previousElementSibling : null;

    this.element.scrollLeft = scrollRaceStart ? (scrollRaceStart as HTMLElement).offsetLeft : 0;
  }
}
