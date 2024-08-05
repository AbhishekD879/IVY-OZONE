import { Directive, ViewContainerRef } from '@angular/core';

@Directive({
  // eslint-disable-next-line
  selector: '[oxygen-dialog-container]',
})
export class OxygenDialogContainerDirective {
  constructor(public viewContainerRef: ViewContainerRef) { }
}
