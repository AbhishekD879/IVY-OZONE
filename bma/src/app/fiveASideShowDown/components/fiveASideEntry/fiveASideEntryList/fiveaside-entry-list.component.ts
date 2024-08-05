import { Component, Input, OnInit } from '@angular/core';
import { FiveASideEntryInfoService } from '@app/fiveASideShowDown/services/fiveaside-entryInfo-handler.service';
import { IEntrySummaryInfo } from '@app/fiveASideShowDown/models/entry-information';
import { EVENTSTATUS } from '@app/fiveASideShowDown/constants/constants';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';

@Component({
  selector: 'fiveaside-entry-list',
  template: ``
})
export class FiveASideEntryListComponent implements OnInit {
  @Input() myEntriesList: Array<IEntrySummaryInfo>;
  @Input() isFullTime: boolean;
  @Input() userEntryLimit: string;
  @Input() eventStatus: string = EVENTSTATUS.LIVE;
  @Input() eventEntity: ISportEvent;

  public entries: Array<IEntrySummaryInfo>;
  componentId:string;
  constructor(public fiveASideEntryInfoService: FiveASideEntryInfoService,
     protected coreToolsService: CoreToolsService) { }

  ngOnInit(): void {
    this.componentId = this.coreToolsService.uuid();
    if (this.eventStatus !== 'live' && this.eventStatus !== 'post') {
      this.entries = this.fiveASideEntryInfoService.entriesCreation(this.myEntriesList);
      this.rankBasedOnOdds();
    } else {
      this.entries = this.myEntriesList;
    }
  }

  /**
   * rankBasedOnOdds if we have same odds rank will be same
   * @returns void
   */
  private rankBasedOnOdds(): void {
    let rank = 1; let tieCount = 1; const entriesRanking: { [key: number]: number } = {};
    this.entries.forEach((entry: IEntrySummaryInfo, index: number) => {
      if (index > 0 && Number(this.entries[index].oddsDecimal) < Number(this.entries[index - 1].oddsDecimal)) {
        rank = tieCount > 1 ? rank + tieCount : rank + 1;
        tieCount = 1;
      } else if (index > 0) {
        tieCount++;
      }
      this.entries[index].rank = rank;
      entriesRanking[entry.rank] = entriesRanking[entry.rank] ? entriesRanking[entry.rank] + 1 : 1;
    });
    this.entries.forEach((entry: IEntrySummaryInfo) => {
      if (entriesRanking[entry.rank] > 1) {
        entry.rankEqual = `${entry.rank}=`;
      } else {
        entry.rankEqual = entry.rank.toString();
      }
    });
  }
}
