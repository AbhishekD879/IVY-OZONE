import { Injectable } from '@angular/core';
import { MenuCountersProvider, MenuCounters } from '@frontend/vanilla/core';
import { IFreeBetsBadgeModel } from '@vanillaInitModule/models/free-bets.interface';

@Injectable({
    providedIn: 'root'
})
export class FreeBetsBadgeService implements MenuCountersProvider {
    freeBetCounters: IFreeBetsBadgeModel[] = [];

    get order() { return 50; }
    set order(value:any){}

    setCounters(counters: MenuCounters): void {
        this.freeBetCounters.forEach(
            (c: IFreeBetsBadgeModel) => counters.set(c.section, c.item, c.count, c.cssClass, c.type)
        );
    }
}
