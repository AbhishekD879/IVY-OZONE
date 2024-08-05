import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { IBYBMarket } from '@app/lazy-modules/bybHistory/constants/byb-constants';
import environment from '@environment/oxygenEnvConfig';
@Component({
    selector: 'byb-tab',
    templateUrl: './byb-tab.component.html',
    styleUrls: ['./byb-tab.component.scss'],
})
export class BybTabComponent implements OnInit{
    @Input() tab: IBYBMarket;
    @Output() readonly tabChange: EventEmitter<IBYBMarket> = new EventEmitter<IBYBMarket>();
    @Input() index: number;
    isCoral:boolean;

    ngOnInit(): void {
      this.isCoral = environment && environment.brand === 'bma';
      if(this.index == 0) {
        this.tab.active = true;
      }
    }

    /**
     * Emits tab to the parent component
     * @param {IBYBMarket} tab
     */
    onTabSelect(tab: IBYBMarket): void {
      tab.active = !tab.active;

      this.tabChange.emit(tab);
    }
}