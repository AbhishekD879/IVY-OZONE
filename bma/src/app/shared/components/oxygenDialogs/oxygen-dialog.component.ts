import {
  Component,
  ComponentFactory,
  ComponentFactoryResolver,
  ComponentRef,
  OnDestroy,
  OnInit,
  Type,
  ViewChild,
  ViewContainerRef,
  ViewEncapsulation
} from '@angular/core';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

import { DialogService } from '@core/services/dialogService/dialog.service';
import { IDialogEvent } from '@core/services/dialogService/dialog-params.model';
import { AbstractDialogComponent } from './abstract-dialog';
import { OxygenDialogContainerDirective } from '@shared/directives/oxygen-dialog-container.directive';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'oxygen-dialog',
  templateUrl: './oxygen-dialog.component.html',
  styleUrls: ['./oxygen-dialog.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class OxygenDialogComponent implements OnInit, OnDestroy {
  @ViewChild(OxygenDialogContainerDirective, {static: true}) dialogContainerProvider: OxygenDialogContainerDirective;

  solidOverlay: boolean = false;

  private viewContainerRef: ViewContainerRef;

  // registered dialog component types
  private dialogTypes: Map<string, Type<AbstractDialogComponent> | ComponentFactory<any>> = new Map();

  // dialog component instances
  private dialogRefs: Map<string, ComponentRef<AbstractDialogComponent>> = new Map();

  private destroyed$ = new Subject();

  constructor(
    private dialogService: DialogService,
    private componentFactoryResolver: ComponentFactoryResolver,
    private pubSubService: PubSubService
  ) { }

  ngOnInit(): void {
    this.viewContainerRef = this.dialogContainerProvider.viewContainerRef;

    this.dialogService.modalListener
      .pipe(takeUntil(this.destroyed$))
      .subscribe((event: IDialogEvent) => {
        if (event.forceCloseOther) {
          this.closeOtherDialogs(event.name);
        }

        switch (event.type) {
          case 'open':
            if (this.dialogTypes.has(event.name) || event.component) {
              this.solidOverlay = event.solidOverlay;
              this.registerDialog(event.name, event.component);
              const dialog: AbstractDialogComponent = this.getDialog(event.name);
              dialog.setParams(event.params);
              dialog.open();
              this.pubSubService.publish(this.pubSubService.API.NEW_DIALOG_OPENED);
            } else {
              console.warn(`Dialog "${event.name}" does not exist`);
            }
            break;
          case 'close':
            this.closeDialogByKey(event.name, true);
            break;
          case 'closeAll':
            this.closeAllDialogs();
            break;
          case 'register':
            this.registerDialog(event.name, event.params.dialog);
            break;
          default:
            break;
        }
      }
    );
  }

  ngOnDestroy(): void {
    this.destroyed$.next(null);
    this.destroyed$.complete();
  }

  private closeAllDialogs(): void {
    this.dialogRefs.forEach((componentRef: ComponentRef<AbstractDialogComponent>, key: string) => {
      this.closeDialogByKey(key);
    });
  }



  private registerDialog(name: string, dialog: Type<AbstractDialogComponent>|ComponentFactory<any>): void {
    if (!this.dialogTypes.has(name)) {
      this.dialogTypes.set(name, dialog);
    }
  }

  private createDialog(name: string): void {
    const dialogComponent: Type<AbstractDialogComponent>|ComponentFactory<any> = this.dialogTypes.get(name);
    const componentFactory = dialogComponent instanceof ComponentFactory
      ? dialogComponent
      : this.componentFactoryResolver.resolveComponentFactory(dialogComponent);
    const componentRef: ComponentRef<AbstractDialogComponent> = this.viewContainerRef.createComponent(componentFactory);
    this.dialogRefs.set(name, componentRef);
  }

  private getDialog(name: string): AbstractDialogComponent {
    if (this.dialogRefs.has(name)) {
      return this.dialogRefs.get(name).instance;
    }
    if (this.dialogTypes.has(name)) {
      this.createDialog(name);
      return this.dialogRefs.get(name).instance;
    }
    return null;
  }

  private closeOtherDialogs(dialogName: string): void {
    this.dialogRefs.forEach((componentRef: ComponentRef<AbstractDialogComponent>, key: string) => {
      if (dialogName !== key) {
        this.closeDialogByKey(key);
      }
    });
  }

  private closeDialogByKey(refName: string, ignorePersistence = false) {
    if (this.dialogRefs.has(refName)) {
      const componentRef: ComponentRef<AbstractDialogComponent> = this.dialogRefs.get(refName);
      const instance = componentRef.instance;

      if (!instance.params.isPersistent || ignorePersistence) {
        instance.closeDialog();
        componentRef.destroy();
        this.dialogRefs.delete(refName);
      }
    }
  }
}
