import { Component, ViewChild } from '@angular/core';
import { Router } from '@angular/router';

import { DeviceService } from '@core/services/device/device.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import environment from '@environment/oxygenEnvConfig';
import { IOutcome } from '@core/models/outcome.model';

import { IRoutingHelperEvent } from '@core/services/routingHelper/routing-helper.model';
import { TimeService } from '@core/services/time/time.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'selection-info-dialog',
  templateUrl: 'selection-info-dialog.component.html',
  styleUrls: ['selection-info-dialog.component.scss']
})
export class SelectionInfoDialogComponent extends AbstractDialogComponent {
  @ViewChild('dialog', { static: true }) dialog: any;

  title: string;
  cashoutValue: string;
  eventName: string;
  isVirtual: boolean;
  private readonly virtualId: any = environment.CATEGORIES_DATA.virtuals[0].id;

  constructor(
    device: DeviceService,
    private routingHelper: RoutingHelperService,
    private router: Router,
    private pubSubService: PubSubService,
    private timeService: TimeService,
    windowRef: WindowRefService
  ) {
    super(device, windowRef);
  }

  open(): void {
    super.open();
    this.isVirtual = this.getEventData().categoryId === Number(this.virtualId);
    this.setTitle();
    this.setCashoutValue();
    this.setEventName();
  }

  goToEvent(): void {
    if (this.isVirtual) {
      return;
    }
    const edpUrl: string = this.routingHelper.formEdpUrl(this.getEventData());
    this.router.navigateByUrl(edpUrl);
    this.pubSubService.publish(this.pubSubService.API['show-slide-out-betslip'], false);
  }

  private getEventData(): IRoutingHelperEvent {
    const stake = this.params.stake;
    const eventData: IRoutingHelperEvent = {
      originalName: `${stake.localTime} ${stake.eventName}`,
      name: stake.eventName,
      id: stake.eventIds.eventIds[0],
      categoryName: stake.sport,
      className: stake.className,
      categoryId: Number(stake.sportId),
      typeName: stake.Bet.legs[0].selection.typeName,
    };

    if (this.params.stake.isFCTC) {
      const details = stake.outcomes[0].details.info;

      Object.assign(eventData, {
        categoryName: details.sport,
        className: details.className,
        categoryId: Number(details.sportId),
        typeName: stake.eventName,
      });
    }

    return eventData;
  }

  private setTitle(): void {
    const stake = this.params.stake;

    if (stake.isFCTC) {
      const anyPlace = stake.combiName.endsWith('_COM');
      const placesMap = { '1': '1st', '2': '2nd', '3': '3rd' };
      this.title = stake.outcomes.map((outcome: IOutcome, index: number) => {
        return anyPlace ? outcome.name : `${placesMap[index + 1]}. ${outcome.name}`;
      }).join(', ');
    } else {
      this.title = stake.outcomeName;
    }
  }

  private setEventName(): void {
    const stake = this.params.stake;

    if (stake.isRacingSport) {
      this.eventName = `${stake.localTime} ${stake.eventName}`;
    } else if (this.isVirtual) {
      this.eventName = `${this.timeService.formatByPattern(stake.time, 'HH:mm')} ${stake.eventName}`;
    } else {
      this.eventName = stake.eventName;
    }
  }

  private setCashoutValue(): void {
    const details = this.params.stake.Bet.legs[0].parts[0].outcome.details;
    this.cashoutValue = (details.cashoutAvail === 'Y' && details.markets[0].cashoutAvail === 'Y') ? 'Y' : null;
  }
}
