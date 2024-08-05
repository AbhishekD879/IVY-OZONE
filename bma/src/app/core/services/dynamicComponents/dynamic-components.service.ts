import {
  Injectable,
  Injector,
  ComponentFactoryResolver,
  ApplicationRef,
  EmbeddedViewRef } from '@angular/core';
import { IDynamicComponent, IComponentInstance } from '@core/services/dynamicComponents/dynamic-components.model';

@Injectable()
export class DynamicComponentsService {

  constructor(
    private componentFactoryResolver: ComponentFactoryResolver,
    private appRef: ApplicationRef,
    private injector: Injector
  ) { }

  /**
   * Adds component's element to DOM, attaches to the appRef
   *
   * @param newComponent - the angular component to be added
   * @param data - data (basically inputs) of component' instance
   * @param target - target (parent) node that receives new component. Omit to append component to body.
   * @param referenceNode - existing node to put component before. Omit to append component to parent.
   * @return IDynamicComponent - api with destroy function and reference to component instance
   */
  addComponent(
    newComponent: any,
    data: IComponentInstance = {},
    target: Node = document.body,
    referenceNode: Node = null
  ): IDynamicComponent {
    const appRef = this.appRef;
    const componentRef = this.componentFactoryResolver
      .resolveComponentFactory(newComponent)
      .create(this.injector);
    const componentInstance = <IComponentInstance>componentRef.instance;

    Object.assign(componentInstance, data, {isPanelShown: true} );
    appRef.attachView(componentRef.hostView);
    const domElem = (componentRef.hostView as EmbeddedViewRef<any>).rootNodes[0] as HTMLElement;
    target.insertBefore(domElem, referenceNode);

    return {
      destroy: () => {
        appRef.detachView(componentRef.hostView);
        componentRef.destroy();
      },
      instance: componentInstance
    };
  }
}
