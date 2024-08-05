import {
    Directive,
    ElementRef,
    EventEmitter,
    Output
  } from '@angular/core';

  @Directive({
    selector: '[transition-group-item]'
  })
  export class TransitionGroupItemDirective {
    prevPos: ClientRect;
    newPos: ClientRect;

    translateX: number;
    translateY: number;

    el: HTMLElement;
    moved: boolean;
    /* eslint-disable */
    @Output() move = new EventEmitter<void>();

    moveCallback: any;

    constructor(elRef: ElementRef) {
      this.el = elRef.nativeElement;
    }
}
