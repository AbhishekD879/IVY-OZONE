import { Component, OnInit, OnDestroy, Input, Output, EventEmitter, ChangeDetectionStrategy } from '@angular/core';

import { IUkToteMatrixMap } from './uk-tote-matrix.model';
import { IUkTotePoolBet } from '../../models/tote-pool.model';
import { IOutcome } from '@core/models/outcome.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { UkToteBetBuilderService } from '../../services/ukTotebetBuilder/uk-tote-bet-builder.service';
import { IPoolGuides } from '@uktote/models/tote-event.model';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'uk-tote-checkbox-matrix',
  templateUrl: './uk-tote-check-box-matrix.component.html'
})
export class UkToteCheckBoxMatrixComponent implements OnInit, OnDestroy {

  @Input() map: IUkToteMatrixMap;
  @Input() outcomesMap: { [key: string]: IOutcome };
  @Input() outcome: IOutcome;
  @Input() currentPool: IUkTotePoolBet;
  @Input() isSuspended: boolean;
  @Input() guide: IPoolGuides;

  @Output() readonly mapUpdate: EventEmitter<IUkToteMatrixMap> = new EventEmitter();

  selectedOutcomes: IOutcome[];
  any = [];

  private subscriberName: string;

  constructor(
    private betBuilderService: UkToteBetBuilderService,
    private pubsub: PubSubService,
    private coreToolsService: CoreToolsService
  ) {
    this.subscriberName = `checkboxMatrixCtrl ${this.coreToolsService.uuid()}`;
  }

  ngOnInit(): void {
    this.pubsub.subscribe(this.subscriberName, this.pubsub.API.CLEAR_BETBUILDER, (outcomeId: string) => {
      this.clear(outcomeId);
    });
  }

  ngOnDestroy(): void {
    this.pubsub.publishSync(this.pubsub.API.CLEAR_BETBUILDER);
    this.pubsub.unsubscribe(this.subscriberName);
  }

  trackByIndex(index: number): number {
    return index;
  }

  get checkBoxMatrix() {
    const currentMap = this.map[this.outcome.id];
    return Object.keys(currentMap).map((key: string) => {
      return {
        key: key,
        value: currentMap[key]
      };
    });
  }
  set checkBoxMatrix(value:any){}

  getCssClass(element: {key: string; value: string}): string {
    return `${element.value} ${this.isSuspended ? 'disabled' : ''} ${this.outcome.nonRunner ? 'non-runner' : ''}`;
  }

  /**
   * Run checkboxes validation
   * @param {String} id
   * @param {String} index
   */
  checkPlace(id: string, index: string): void {
    const checkbox = this.map[id][index];

    if (checkbox === 'open') {
      this.map[id][index] = 'checked';
    }

    if (checkbox === 'checked') {
      this.map[id][index] = 'open';
    }

    this.runChecks(this.map);
    this.mapUpdate && this.mapUpdate.emit(this.map);
  }

  /**
   * Clear checkbox map entirely or by outcomeId(if present)
   * @param {String} outcomeId
   */
  clear(outcomeId: string): void {
    if (outcomeId && this.map[outcomeId]) {
      Object.entries(this.map[outcomeId]).forEach((entry) => {
        const [ index, place ] = entry;
        if (place === 'checked' || place === 'open') {
          this.map[outcomeId][index] = 'open';
        } else {
          this.map[outcomeId][index] = 'disabled';
        }
      }, this);

      this.runChecks(this.map);
    } else {
      Object.values(this.map).forEach((places) => {
        Object.keys(places).forEach((index: string) => {
          places[index] = 'open';
        });
      });
    }
    this.mapUpdate && this.mapUpdate.emit(this.map);
  }

  runChecks(map: IUkToteMatrixMap): void {
    this.setEnables(map);
    this.selectedOutcomes = [];
    Object.entries(map).forEach((entry) => {
      const [ id, places ] = entry;
      Object.keys(places).forEach((index) => {
        if (places[index] === 'checked') {
          if (index === 'any') {
            this.any.push(this.outcomesMap[id]);
            this.selectedOutcomes[index] = this.any;
          } else {
            this.selectedOutcomes[index] = this.outcomesMap[id];
          }
          this.setDisables(map, id, index);
        }
      });
    });

    this.betBuilderService.add({
      betModel: this.selectedOutcomes,
      poolType: this.currentPool && this.currentPool.poolType,
      currentPool: this.currentPool
    });

    this.any = [];
  }

  setEnables(map: IUkToteMatrixMap): void {
    Object.values(map).forEach((places) => {
      Object.entries(places).forEach((placeEntry) => {
        const [ index, place ] = placeEntry;
        if (place !== 'checked') {
          places[index] = 'open';
        }
      });
    });
  }

  setDisables(map: IUkToteMatrixMap, row: string, col: string): void {
    Object.entries(map).forEach((entry) => {
      const [ id, places ] = entry;
      Object.keys(places).forEach((index: string) => {
        if (places[index] !== 'checked') {
          if ((col === 'any' && index !== 'any') || (col !== 'any' && index === 'any') || (col !== 'any' && index !== 'any' && (id === row || index === col))) {
            places[index] = 'disabled';
          }
        }
      });
    });
  }
}
