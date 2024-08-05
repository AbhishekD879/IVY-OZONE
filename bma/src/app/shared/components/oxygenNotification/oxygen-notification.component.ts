import {
  Component,
  ComponentFactoryResolver,
  ComponentRef,
  ElementRef,
  OnDestroy,
  Type,
  ViewChild,
  ViewContainerRef,
  ChangeDetectorRef
} from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { AbstractNotificationComponent } from '@shared/components/oxygenNotification/abstract-notification';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';

@Component({
  selector: 'oxygen-notification',
  templateUrl: './oxygen-notification.component.html',
  styleUrls: ['oxygen-notification.component.scss']
})
export class OxygenNotificationComponent implements OnDestroy {
  offsetTop: number = 0;

  @ViewChild('componentHolder', { read: ViewContainerRef, static: false }) componentHolder: ViewContainerRef;
  @ViewChild('notificationsContainer', {static: false}) notificationsContainer: ElementRef;

  private componentRef: ComponentRef<any>;

  constructor(
    private pubsubService: PubSubService,
    private componentFactoryResolver: ComponentFactoryResolver,
    private domTools: DomToolsService,
    private changeDetectionReference: ChangeDetectorRef
  ) {

    this.pubsubService.subscribe('notificationComponent', this.pubsubService.API.NOTIFICATION_SHOW,
      (component: Type<AbstractNotificationComponent>) => {
        this.setNotificationOffset();
        this.createComponent(component);
        this.changeDetectionReference.markForCheck();
      });

    this.pubsubService.subscribe('notificationComponent', this.pubsubService.API.NOTIFICATION_HIDE, () => {
      if (this.componentRef) {
        this.componentRef.destroy();
        this.changeDetectionReference.markForCheck();
      }
    });
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe('notificationComponent');
  }

  private createComponent(component: Type<AbstractNotificationComponent>): void {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(component);
    this.componentRef = this.componentHolder.createComponent(componentFactory);
  }

  private setNotificationOffset(): void {
    this.offsetTop = this.domTools.HeaderEl.clientHeight - 6;
  }
}
