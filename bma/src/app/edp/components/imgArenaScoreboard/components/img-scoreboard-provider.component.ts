import { Component, NgZone, Input, AfterViewInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { IWindow } from '@app/core/models/sport-event.model';
import { ITimeHydraModel } from '@app/core/services/timeSync/timeModel';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { UserService } from '@app/core/services/user/user.service';
import { ISystemConfig } from '@app/core/services/cms/models';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { TimeSyncService } from '@app/core/services/timeSync/time-sync.service';
import { Observable, Subscription } from 'rxjs';
import { IMGArenaScoreboard, IInitialContextForGolf } from '@edp/components/imgArenaScoreboard/models/img-arena-scoreboard';
import { IMG_ARENA_DEFAULT_GOLF, IMG_OPERATORS } from '@edp/components/imgArenaScoreboard/constants/Img-Arena-Scoreboard-constants';
import * as md5 from 'blueimp-md5';
import environment from '@environment/oxygenEnvConfig';

@Component({
    selector: 'img-scoreboard-provider',
    templateUrl: './img-scoreboard-provider.html',
    styleUrls: ['./img-scoreboard-provider.scss']
})
export class ImgScoreboardProviderComponent implements AfterViewInit, OnDestroy {
    @Input() imgEventDetails: string;
    public sportName: string;
    public showImgScoreboardLoader: boolean = false;
    public showImgScoreboard: boolean = true;
    public imgEventCenter = {} as IMGArenaScoreboard;
    public isLoggedIn: boolean = false;
    private IMG_ARENA_SCOREBOARD: string;
    private windowObj: IWindow = this.windowRefService.nativeWindow as IWindow;
    private asyncLoaderSub: Subscription;

    constructor(
        private ngZone: NgZone,
        private windowRefService: WindowRefService,
        private asyncLoaderService: AsyncScriptLoaderService,
        private timeSyncService: TimeSyncService,
        private activatedRoute: ActivatedRoute,
        private userService: UserService,
        protected cmsService: CmsService,
        private deviceService: DeviceService
    ) {
        this.imgEventCenter.initialContext = {} as IInitialContextForGolf;
        this.IMG_ARENA_SCOREBOARD = environment.IMG_ARENA_SCOREBOARD;
        this.isLoggedIn = this.userService.status;
    }

    ngAfterViewInit(): void {
        this.ngZone.runOutsideAngular(() => {
            this.loadImgScoreBoard();
        });
    }

    ngOnDestroy(): void {
        this.asyncLoaderSub && this.asyncLoaderSub.unsubscribe();
    }

    /**
     * Load the scoreboard from unpkg
     * @private
     */
    private loadImgScoreBoard(): void {
        this.showImgScoreboardLoader = true;
        if (this.windowObj.frontRowSeat) {
            this.addImgScoreBoard();
        } else {
            this.initImgScoreBoardLoader();
        }
    }

    /**
     * Add the img scoreboard widget
     * @private
     */
    private addImgScoreBoard(): void {
        if (this.windowObj.frontRowSeat) {
            this.showImgScoreboardLoader = false;
            this.sportName = this.activatedRoute.snapshot.paramMap.get('sport');
            if (this.sportName == environment.CATEGORIES_DATA.golfSport) {
                const [imgEventId, imgRoundNo, imgGroupNo, imgHoleNo] = this.imgEventDetails.split(':');
                this.imgEventCenter = IMG_ARENA_DEFAULT_GOLF;
                this.imgEventCenter.operator = environment.DOMAIN.includes('coral') ? IMG_OPERATORS.CORAL : IMG_OPERATORS.LADBROKES;
                this.imgEventCenter.eventId = imgEventId;
                this.imgEventCenter.initialContext.roundNo = imgRoundNo;
                this.imgEventCenter.initialContext.groupNo = imgGroupNo;
                this.imgEventCenter.initialContext.holeNo = imgHoleNo;
                this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
                    this.imgEventCenter.options.videoPlaybackEnabled = this.isLoggedIn && config.IMGScoreboardHoleStreaming[this.deviceService.requestPlatform];
                });
            }
            else {
                this.showImgScoreboard = false
            }
            const { MessageTopics } = this.windowObj.frontRowSeat.eventCentreUtils;
            const eventCentreInstance = this.windowObj.frontRowSeat.eventCentre(this.imgEventCenter);

            if (this.imgEventCenter.options && this.imgEventCenter.options.videoPlaybackEnabled) {
                (this.timeSyncService.getUserSessionTime(true, false) as Observable<ITimeHydraModel>).subscribe(serverData => {

                    eventCentreInstance.on(
                        MessageTopics.VIDEO_PLAYBACK_AUTH_REQUEST, () => {
                            const timestamp = serverData.timestamp,
                                userIP = serverData['x-forward-for'],
                                accessString = `${environment.IMG_ARENA_OPERATOR_SECRET_KEY}:${userIP}:${timestamp}`;

                            eventCentreInstance.emit(MessageTopics.VIDEO_PLAYBACK_AUTH_RESPONSE, {
                                auth: md5(accessString, environment.IMG_ARENA_OPERATOR_SECRET_KEY),
                                timestamp: timestamp,
                                operatorId: environment.IMG_ARENA_OPERATOR_ID
                            });
                        }
                    );
                });
            }
        }
    }

    /**
     * Initialise img scoreboard window obj
     * @private
     */
    private initImgScoreBoardLoader(): void {
        this.asyncLoaderSub = this.asyncLoaderService.loadJsFile(this.IMG_ARENA_SCOREBOARD)
            .subscribe(() => {
                this.addImgScoreBoard();
            });
    }
}