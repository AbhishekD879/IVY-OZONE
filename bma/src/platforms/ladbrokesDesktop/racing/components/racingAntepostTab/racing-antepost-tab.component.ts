import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import * as _ from 'underscore';
import { RacingAntepostTabComponent } from '@racing/components/racingAntepostTab/racing-antepost-tab.component';
import { IRacingMap, ITypeNamesEvent } from '@racing/models/racing-ga.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { RacingService } from '@ladbrokesMobile/core/services/sport/racing.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { GridHelperService } from '@ladbrokesDesktop/shared/services/gridHelperService/grid-helper.service';
import { IEmptyHorseAntepostEvent } from '@ladbrokesDesktop/racing/components/racingAntepostTab/racing-antepost-tab.model';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { DeviceService } from '@app/core/services/device/device.service';


@Component({
  selector: 'racing-antepost-tab',
  templateUrl: 'racing-antepost-tab.component.html',
  styleUrls: ['racing-antepost-tab.component.scss'],
  // eslint-disable-next-line
  encapsulation : ViewEncapsulation.None
})
export class DesktopRacingAntepostTabComponent extends RacingAntepostTabComponent implements OnInit {
  constructor(
    filtersService: FiltersService,
    localeService: LocaleService,
    racingService: RacingService,
    routingHelperService: RoutingHelperService,
    private gridHelperService: GridHelperService,
    public sessionStorageService: SessionStorageService,
    public pubSubService: PubSubService,
    public gtm: GtmService,
    public deviceService: DeviceService) {
      super(filtersService, localeService, racingService, routingHelperService, sessionStorageService, pubSubService, gtm, deviceService);
  }

  ngOnInit(): void {
    super.ngOnInit();
    _.each(this.eventsMap, (eventsByTab: IRacingMap) => {
      _.each(eventsByTab.typeNames, (eventsByAcc: ITypeNamesEvent) => {
        const events: (ISportEvent | IEmptyHorseAntepostEvent)[] = eventsByAcc.typeNameEvents;
        this.applyGrid(events);
      });
    });
  }

  /**
   * Add empty cells for grid layout 2 and 3 columns
   * @params {Array} events
   */
  private applyGrid(events: (ISportEvent | IEmptyHorseAntepostEvent)[]): void {
    if(!this.isFromOverlay){
      const rowForThree: number = this.gridHelperService.addCells(3, events.length);
      const rowForTwo: number = this.gridHelperService.addCells(2, events.length);
      const rowLimit: number = rowForThree + rowForTwo;
      for (let i = 0; rowLimit > i; i++) {
        const emptyHorseAntepostEvent: IEmptyHorseAntepostEvent = {
          type: {
            grid: rowForThree > i ? '3' : '2'
          }
        };
        events.push(emptyHorseAntepostEvent);
      }
    }
  }
}
