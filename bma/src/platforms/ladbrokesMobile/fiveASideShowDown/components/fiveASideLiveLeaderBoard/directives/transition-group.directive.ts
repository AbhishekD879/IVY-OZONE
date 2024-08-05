import {
  AfterViewInit,
  ContentChildren,
  Directive,
  Input,
  QueryList
} from '@angular/core';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';

import {
  TransitionGroupItemDirective
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideLiveLeaderBoard/directives/transition-group-item.directive';

@Directive({
  selector: '[transition-group]'
})
export class TransitionGroupDirective implements AfterViewInit {
  @Input('transition-group') class;

  @ContentChildren(TransitionGroupItemDirective)
  items: QueryList<TransitionGroupItemDirective>;
  constructor(
    private windowRef: WindowRefService
  ) { }
  ngAfterViewInit() {
    this.windowRef.nativeWindow.setTimeout(() => this.refreshPosition('prevPos'), 0); // save init positions on next 'tick'

    this.items.changes.subscribe(items => {
      if (this.items.first.el.className.indexOf('sameUpdate') !== -1) {
        return;
      }
      items.forEach(item => item.prevPos = item.newPos || item.prevPos);
      items.forEach(this.runCallback);
      this.refreshPosition('newPos');
      items.forEach(item => item.prevPos = item.prevPos || item.newPos); // for new items

      const animate = () => {
        items.forEach(this.applyTranslation);
        this['_forceReflow'] = document.body.offsetHeight; // force reflow to put everything in position
        this.items.forEach(this.runTransition.bind(this));
      };

      const willMoveSome = items.some((item) => {
        const dx = item.prevPos.left - item.newPos.left;
        const dy = item.prevPos.top - item.newPos.top;
        return dx || dy;
      });

      if (willMoveSome) {
        animate();
      } else {
        this.windowRef.nativeWindow.setTimeout(() => { // for removed items
          this.refreshPosition('newPos');
          animate();
        }, 0);
      }
    });
  }

  runCallback(item: TransitionGroupItemDirective) {
    if (item.moveCallback) {
      item.moveCallback();
    }
  }

  runTransition(item: TransitionGroupItemDirective) {
    if (!item.moved) {
      return;
    }
    const cssClass = `${this.class}-move`;
    const el = item.el;
    const style: any = el.style;
    el.classList.add(cssClass);
    style.transform = style.WebkitTransform = style.transitionDuration = '';
    /* eslint-disable */
    el.addEventListener('transitionend', item.moveCallback = (e: any) => {
      if (!e || /transform$/.test(e.propertyName)) {
        el.removeEventListener('transitionend', item.moveCallback);
        item.moveCallback = null;
        el.classList.remove(cssClass);
      }
    });
  }

  refreshPosition(prop: string) {
    this.items.forEach(item => {
      item[prop] = {
        top: item.el.offsetTop,
        left: item.el.offsetLeft
      };
    });
  }

  applyTranslation(item: TransitionGroupItemDirective) {
    item.moved = false;
    if (item && item.prevPos && item.newPos) {
      const dx = item.prevPos.left - item.newPos.left;
      const dy = item.prevPos.top - item.newPos.top;
      if (dx || dy) {
        item.moved = true;
        const style: any = item.el.style;
        /* eslint-disable */
        style.transform = style.WebkitTransform = 'translate(' + dx + 'px,' + dy + 'px)';
        style.transitionDuration = '0s';
      }
    }
  }
}
