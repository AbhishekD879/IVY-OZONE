import { Directive, HostBinding, HostListener } from '@angular/core';

// eslint-disable-next-line
@Directive({ selector: '[disable-dragging]' })
export class DisableDraggingDirective {
  @HostBinding('attr.draggable') draggable: string = 'false';

  @HostListener('mousedown', ['$event'])
  onMouseDown($event: MouseEvent): void {
    $event.preventDefault && $event.preventDefault();
  }
}
