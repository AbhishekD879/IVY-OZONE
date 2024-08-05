import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@app/core/models/outcome.model';
import { TemplateService } from "@app/shared/services/template/template.service";
@Component({
  selector: 'sb-single-drop-down-single-odd',
  templateUrl: './sb-single-drop-down-single-odd.component.html',
  styleUrls: ['./sb-single-drop-down-single-odd.component.scss']
})
export class SbSingleDropDownSingleOddComponent implements OnInit {
  outcomeEntity: IOutcome
  alteredOutComes: string[];
  @Input() market: IMarket;
  @Input() event: ISportEvent;
  @Output() selectionClickEmit?: EventEmitter<IMarket> = new EventEmitter();

  constructor(private templateService: TemplateService) {
  }
  ngOnInit(): void {
    this.alteredOutComes = this.getOutcomeNames(this.market?.outcomes);
  }

  getOutcomeNames(outcomes:IOutcome[]){
    const alteredOutComes = [];
    outcomes = this.templateService.sortOutcomesByPriceAndDisplayOrder(outcomes);
    outcomes.forEach((outcome: IOutcome) =>
    {
      outcome.name && alteredOutComes.push(outcome.name)
    });
    return alteredOutComes;
  }

  handleSelectionClick(market: IMarket) {
    this.selectionClickEmit.emit(market);
  }

  onValueChange(outcomeName:string) {
    if (outcomeName) {
      this.outcomeEntity = this.market?.outcomes.find((currentOutcome: IOutcome) => currentOutcome.name === outcomeName);
    }
  }
}
