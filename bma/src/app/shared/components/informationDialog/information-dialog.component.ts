import { AfterViewInit, Component, OnDestroy, ViewChild } from '@angular/core';
import * as _ from 'underscore';

import { AbstractDialogComponent } from '../oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { IDialogButton } from '@core/services/dialogService/dialog-params.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { GtmService } from '@core/services/gtm/gtm.service';

@Component({
  selector: 'information-dialog',
  templateUrl: './information-dialog.component.html',
})
export class InformationDialogComponent extends AbstractDialogComponent implements AfterViewInit, OnDestroy {

  @ViewChild('informationDialog', {static: true}) dialog;
  params: any = {};
  redirectListener;

  constructor(deviceService: DeviceService,
              private rendererService: RendererService,
              protected windowRef: WindowRefService,
              private pubSubService: PubSubService,
              private navigationService: NavigationService,
              private gtmService: GtmService) {
    super(deviceService, windowRef);
    this.checkLink = this.checkLink.bind(this);
  }

  ngAfterViewInit(): void {
    this.init();
    this.pubSubService.subscribe('InformationDialogComponent', this.pubSubService.API.NEW_DIALOG_OPENED, () => {
      this.dialog.changeDetectorRef.detectChanges();
      this.init();
    });
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('InformationDialogComponent');
  }

  handleBtnClick(button) {
    if(this.params.hideCrossIcon){
      this.addGaTracking(button.caption);
    }
    if (_.isFunction(button.handler)) {
      button.handler();
    } else {
      this.closeDialog();
    }
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'footballsuperseries',
      'component.ActionEvent': 'click',
      'component.LabelEvent': 'entry popup',
      'component.PositionEvent': 'not applicable',
      'component.LocationEvent': 'entry popup',
      'component.EventDetails':button.caption,
      'component.URLClicked': 'not applicable'
    }
    this.gtmService.push(gtmData.event, gtmData);
  }

  addGaTracking(caption, link = '') {
    const gtmData={
      event: 'Event.Tracking',
     'component.CategoryEvent': 'betslip',
     'component.LabelEvent': 'lucky bonus',
     'component.ActionEvent': 'click',
     'component.PositionEvent': this.params.label,
     'component.LocationEvent':  this.params && this.params.compName,
     'component.EventDetails': caption.toLowerCase()=="ok"? "ok cta": caption.toLowerCase(),
     'component.URLClicked': caption == 'OK' ? 'not applicable' : link
  }
  this.gtmService.push(gtmData.event, gtmData);

  }

  trackByFn(index: number, item: IDialogButton): string {
    return `${index}_${item.caption}`;
  }

  private init(): void {
    const textBlock = this.windowRef.document.querySelector('.modal-body');
    const link = textBlock.querySelector('a');
    if (link) {
      this.redirectListener = this.rendererService.renderer.listen(link, 'click', this.checkLink);
    }
  }

  private checkLink(e): void {
    e.preventDefault();
    const href = e.target.attributes && e.target.attributes.href && e.target.attributes.href.value;
    if(this.params.hideCrossIcon){
      this.addGaTracking(e.target.innerHTML , href);
    }
    if (href) {
      this.navigationService.openUrl(href, true);
    }
  }
}
