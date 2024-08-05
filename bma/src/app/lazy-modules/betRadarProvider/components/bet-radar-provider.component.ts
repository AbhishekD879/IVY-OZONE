import {
    Component,
    OnInit,
    NgZone,
    Input,
    AfterViewInit,
    ChangeDetectionStrategy,
    OnDestroy,
  } from '@angular/core';
  import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
  import environment from '@environment/oxygenEnvConfig';
  import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
  import { IWindow } from '@app/core/models/sport-event.model';
  import { Subscription } from 'rxjs';
  @Component({
    selector: 'bet-radar-provider',
    templateUrl: './bet-radar-provider.html',
    styleUrls: ['./bet-radar-provider.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush
  })
  export class BetRadarProviderComponent implements OnInit, AfterViewInit, OnDestroy {
    @Input() betRadarMatchId: number;
    public showBetRadarLoader: boolean = false;
    public widgetID: string;
    private BETRADAR_WIDGETLOADERURL: string;
    private windowObj: IWindow = this.windowRefService.nativeWindow as IWindow;
    private asyncLoaderSub: Subscription;
    constructor(
      private ngZone: NgZone,
      private windowRefService: WindowRefService,
      private asyncLoaderService: AsyncScriptLoaderService
    ) {
      this.BETRADAR_WIDGETLOADERURL = environment.BETRADAR_WIDGETLOADERURL;
    }
    ngOnInit(): void {
      this.widgetID = `sr-widget-${this.betRadarMatchId}`;
    }
    ngAfterViewInit(): void {
      this.ngZone.runOutsideAngular(() => {
        this.loadBetRadarWidget();
      });
    }
    ngOnDestroy(): void {
      this.asyncLoaderSub && this.asyncLoaderSub.unsubscribe();
    }
    /**
     * Load the bet radar widget scoreboard from widget loader
     * @private
     */
    private loadBetRadarWidget(): void {
      this.showBetRadarLoader = true;
      // Check if Sportradar Isomorphic Rendering Obj is available or not for widget loading and rendering
      if (this.windowObj.SIR) {
        this.addBetRadarWidget();
      } else {
        this.initWidgetLoader();
      }
    }
    /**
     * Add the bet radar widget
     * @private
     */
    private addBetRadarWidget(): void {
      const widgetID: string = `#sr-widget-${this.betRadarMatchId}`;
      if(this.windowObj.SIR) {
        this.windowObj.SIR(
          'addWidget',
          widgetID,
          'match.lmtplus',
          {
            showOdds: true,
            matchId: this.betRadarMatchId,
            tabsPosition: 'top',
            logo:['assets/images/betRadarLogo.png']
          },
        );
      }
      this.showBetRadarLoader = false;
    }
    /**
     * Initialise the bet radar widget loader
     * @private
     */
    private initWidgetLoader(): void {
      this.asyncLoaderSub = this.asyncLoaderService.loadJsFile(this.BETRADAR_WIDGETLOADERURL)
        .subscribe(() => {
          this.addBetRadarWidget();
      });
    }
  }
