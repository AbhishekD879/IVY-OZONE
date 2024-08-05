import { Directive, ElementRef, OnInit, Input } from '@angular/core';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import * as _ from 'underscore';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Directive({
  // eslint-disable-next-line
  selector: '[equal-column]'
})

export class EqualColumnDirective implements OnInit {
  @Input() 'equal-column': boolean;
  private maxHeight: number;
  constructor(
    private windowRef: WindowRefService,
    private element: ElementRef,
    private rendererService: RendererService
  ) { }

  ngOnInit(): void {
    this.windowRef.nativeWindow.setTimeout(() => {
      this.setMaxHeight();
    });

    this.rendererService.renderer.listen(this.windowRef.nativeWindow, 'resize', () => {
      this.setMaxHeight();
    });
  }

  private setMaxHeight(): void {
    const columns: HTMLElement[] = this.element.nativeElement.children,
      cells: HTMLCollection[] = [];
    _.each(columns, column => Array.prototype.push.apply(cells, column.children as any));

    if (cells.length > 2 && !this.maxHeight && this['equal-column']) {
      const childHeights: number[] | any[] = _.map(cells, (child: HTMLElement) => child.clientHeight);
      this.maxHeight = Math.max(...childHeights);

      _.each(cells, child => {
        if (this.maxHeight) {
          const height = this.maxHeight;
          this.rendererService.renderer.setStyle(child, 'height', `${height}px`);
        }
      });
    }
  }
}
