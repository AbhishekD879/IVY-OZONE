
import {Component,EventEmitter,Output,OnInit, Input } from '@angular/core';
import { IBYBMarket, Tabs } from '@app/lazy-modules/bybHistory/constants/byb-constants';
import { IEnableSwitchers, ITabEvent } from '@app/lazy-modules/bybHistory/components/bybLayout/byb-markets-mock';

@Component({
    selector: 'byb-tabs',
    templateUrl: './byb-tabs.component.html',
    styleUrls: ['./byb-tabs.component.scss'],
})

export class BybTabsComponent implements OnInit {
    tabs: IBYBMarket[] = Tabs;
    @Input() enabledMarketSwitchers: IEnableSwitchers;
    @Output() readonly tabChange: EventEmitter<IBYBMarket> = new EventEmitter<IBYBMarket>();

    ngOnInit(): void {
        this.tabs = this.tabs.map((tab: IBYBMarket) => ({ ...tab, active: false }));
    }

    /**
     * Emits selected tab to parent and marks only it as active
     * @param {IBYBMarket} event
    */
    onTabChange(event: IBYBMarket): void {
        this.tabs = this.tabs.map((tab: IBYBMarket) => {
            if (event.market === tab.market) {
                tab.active = true;
            } else {
                tab.active = false;
            }
            return { ...tab };
        });
        this.tabChange.emit(event);
    }

    /**
     * ngFor trackBy function
     * @param {number} index
     * @return {number}
     */
    trackByIndex(index: number): number {
        return index;
    }

    /**
     * change filter
     * @param {ITabEvent} tab
     * @return {void}
     */
    isEnabledMarketSwitchers(tab: ITabEvent): void {
        return this.enabledMarketSwitchers[tab.market];
    }
}