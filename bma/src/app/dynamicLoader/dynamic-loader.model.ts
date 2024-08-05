import { ComponentFactory, ComponentRef, ViewContainerRef } from '@angular/core';

export interface ILazyComponent {
  viewContainer: ViewContainerRef;
  factory: ComponentFactory<any>;
  componentRef: ComponentRef<any>;
}
