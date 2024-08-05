import { Directive, HostBinding, HostListener } from '@angular/core';
import { IPosition } from '@shared/models/position.model';

// eslint-disable-next-line
@Directive({ selector: '[click-link]' })
export class ClickLinkDirective {
  @HostBinding('attr.draggable') draggable: string = 'false';

  private readonly CLICK_THRESHOLD_PX: number = 3;
  private moved: boolean = false;
  private position: IPosition = { x: 0, y: 0 };

  @HostListener('mousedown', ['$event'])
  onMouseDown($event: MouseEvent): void {
    this.position.x = $event.pageX;
    this.position.y = $event.pageY;
    this.moved = false;
  }

  @HostListener('mouseup', ['$event'])
  onMouseUp($event: MouseEvent): void {
    this.moved = Math.abs(this.position.x - $event.pageX) > this.CLICK_THRESHOLD_PX ||
      Math.abs(this.position.y - $event.pageY) > this.CLICK_THRESHOLD_PX;
  }

  @HostListener('click', ['$event'])
  onClick($event: MouseEvent): void {
    this.moved && $event.preventDefault();
  }
}
