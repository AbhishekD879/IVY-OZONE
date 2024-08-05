import { Directive, ViewContainerRef } from '@angular/core';

@Directive({
  selector: '[competition-module]',
})
export class CompetitionModuleDirective {
  constructor(public viewContainerRef: ViewContainerRef) { }
}
