import { Directive, ElementRef, Input, OnChanges } from '@angular/core';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';

@Directive({
  // eslint-disable-next-line
  selector: '[scrollto]'
})
export class ScrollToDirective implements OnChanges {
  @Input() uptoscroll: boolean;
  constructor(public elr: ElementRef, public window: WindowRefService) {
  }
  ngOnChanges() {
    if (this.uptoscroll) {
      const removepixel = 80;
      this.window.nativeWindow.scrollTo(0, this.elr.nativeElement.offsetTop - removepixel);
    }
  }
}
