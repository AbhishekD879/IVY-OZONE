import { Component, Output, OnInit, EventEmitter, HostListener, OnDestroy, Input, ChangeDetectorRef } from '@angular/core';
import * as _ from 'underscore';

import { QuickbetNotificationService } from '@app/quickbet/services/quickbetNotificationService/quickbet-notification.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IQuickbetNotificationModel } from '@app/quickbet/models/quickbet-notification.model';
import { Router } from '@angular/router';

@Component({
  selector: 'quickbet-info-panel',
  templateUrl: 'quickbet-info-panel.component.html',
  styleUrls: ['quickbet-info-panel.component.scss']
})
export class QuickbetInfoPanelComponent implements OnInit, OnDestroy {
  @Output() readonly notificationsPanelClickFn: EventEmitter<void> = new EventEmitter();
  @Output() readonly externalLinksFn: EventEmitter<boolean> = new EventEmitter();
  @Input() qdIsShown?: boolean;

  infoPanel: IQuickbetNotificationModel;
  name: string;

  constructor(
    protected quickbetNotificationService: QuickbetNotificationService,
    protected pubsub: PubSubService,
    protected router: Router,
    protected changeDetectorRef: ChangeDetectorRef
  ) {
    this.name = this.constructor.name;

    this.updatePanelMessage = this.updatePanelMessage.bind(this);
  }

  ngOnInit(): void {
    this.updatePanelMessage(this.quickbetNotificationService.config);

    this.pubsub.subscribe(this.name, this.pubsub.API.QUICKBET_INFO_PANEL, this.updatePanelMessage);
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe(this.name);
  }

  @HostListener('click', ['$event'])
  onHostClick(event: MouseEvent): void {
    // Close quickbet panel when user click on external link
    const redirectUrl: string = (<HTMLElement>event.target).dataset.routerlink;
    if (redirectUrl) {
      this.externalLinksHandler();
      this.router.navigateByUrl(redirectUrl);
    }
  }

  /**
   * Open quick deposit panel if quick-deposit error is shown
   * @returns {*}
   */
  openQuickDepositPanel(): void {
    return this.infoPanel.location.indexOf('quick-deposit') > -1 ? this.onClickHandler() : _.noop();
  }

  showInfoPanel(): boolean {
    return this.infoPanel && this.infoPanel.msg && (this.qdIsShown ? this.infoPanel.location !== 'quick-deposit' : true);
  }

  /**
   * HTML element class for different types of messages
   * @returns {string}
   */
  get messageTypeClass(): string {
    const className = this.infoPanel.msg ? `${this.infoPanel.type}-panel` : '';

    return this.qdIsShown ? `${className} qd-info-panel` : className;
  }
  set messageTypeClass(value:string){}
  private onClickHandler(): void {
    this.notificationsPanelClickFn.emit();
  }

  private externalLinksHandler(): void {
    this.externalLinksFn.emit(true);
  }

  private updatePanelMessage(infoPanelObj: IQuickbetNotificationModel): void {
    infoPanelObj.msg = infoPanelObj.msg.replace(/href="(?!https:)/g, 'data-routerlink="');
    const skipDepositMessage = this.qdIsShown && infoPanelObj.location === 'quick-deposit';
    const isErrorCodeCleared = !!(this.infoPanel && this.infoPanel.errorCode && !infoPanelObj.errorCode);

    if (!skipDepositMessage || isErrorCodeCleared) {
      this.infoPanel = Object.assign({}, infoPanelObj);
    }

    this.changeDetectorRef.detectChanges();
  }
}
