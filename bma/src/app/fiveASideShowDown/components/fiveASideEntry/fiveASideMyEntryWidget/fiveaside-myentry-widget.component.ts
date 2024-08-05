import { Component, Input, OnDestroy, OnInit, ChangeDetectorRef } from '@angular/core';
import { IEntrySummaryInfo } from '@app/fiveASideShowDown/models/entry-information';
import { FiveAsideLiveServeUpdatesSubscribeService } from '@app/fiveASideShowDown/services/fiveaside-live-serve-updates-subscribe.service';
import { UserService } from '@app/core/services/user/user.service';
import { IShowDown } from '@app/fiveASideShowDown/models/show-down';
import { FiveasideLeaderBoardService } from '@app/fiveASideShowDown/services/fiveaside-leader-board.service';
import { IPrize } from '@app/fiveASideShowDown/models/IPrize';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { ITeamColor } from '@app/fiveASideShowDown/models/team-color';
import { PUBSUB_API } from '@app/fiveASideShowDown/constants/constants';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';

@Component({
    selector: 'fiveaside-myentry-widget',
    template: ``
})
export class FiveASideEntryWidgetComponent implements OnInit, OnDestroy {
    @Input() leaderboardData: IShowDown;
    @Input() myEntriesList: Array<IEntrySummaryInfo>;
    @Input() contestId: string;
    @Input() contestInfo: IShowDown;
    @Input() eventStatus?: string;
    @Input() teamColors:ITeamColor[];
    @Input() hasTeamImage: boolean;
    public channel: string;
    public prize: IPrize;
    public entryIdList: string[];
    componentId: string;

    constructor(private fiveAsideLiveServeUpdatesSubscribeService: FiveAsideLiveServeUpdatesSubscribeService,
        private userService: UserService,
        protected coreToolsService: CoreToolsService,
        private fiveasideLeaderBoardService: FiveasideLeaderBoardService,protected changeDetectorRef: ChangeDetectorRef,
        private pubsub: PubSubService,
        private awsService: AWSFirehoseService) { }
    ngOnInit() {
        this.componentId = this.coreToolsService.uuid();
        this.myEntriesList.forEach((entry: IEntrySummaryInfo, index: number) => {
            entry.currentIndex = index;
            entry.previousIndex = index;
        });
       this.prize = this.leaderboardData.prizeMap;
       this.entryIdList = this.myEntriesList.map(({ id }) => id);
       this.pubsub.publish(PUBSUB_API.PUBLISH_LEADERBOARD);

       this.pubsub.subscribe(this.componentId, PUBSUB_API.LEADERBOARD_UPDATE, (myEntries: { update: Array<IEntrySummaryInfo> })  => {
         this.updateHandler(myEntries.update);
       });
    }
    /**
     * @param  {Array<IEntrySummaryInfo>} entrySummary
     * @returns void
     */
    updateHandler(entrySummary: Array<IEntrySummaryInfo>): void {
        if (entrySummary) {
            /** To check negative sceario for my entries list */
            if (this.myEntriesList.length !== entrySummary.length) {
                this.awsService.addAction('MYENTRY_UPDATE=>COUNT=>MISMATCH',
                    {
                        initial: this.myEntriesList.length,
                        update: entrySummary.length
                    });
            }
            entrySummary.forEach((entry: IEntrySummaryInfo, index: number) => {
                entry.userEntry = true;
                entry.currentIndex = index;
                const myEntryList = this.myEntriesList;
                const currentInfo = myEntryList.find((prevEntry: IEntrySummaryInfo) => prevEntry.id === entry.id);
                entry.previousIndex = currentInfo.currentIndex;
            });
            this.pubsub.publish(PUBSUB_API.MY_ENTRY_UPDATE, { update: entrySummary });
            this.myEntriesList = entrySummary;
            this.changeDetectorRef.markForCheck();
        }
    }

    /**
     * @returns void
     */
    ngOnDestroy(): void {
        this.fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels([this.channel], this.updateHandler);
    }
}
