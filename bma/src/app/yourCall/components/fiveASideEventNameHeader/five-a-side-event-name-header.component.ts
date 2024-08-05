import { Component, Input, OnInit, ChangeDetectionStrategy,
  ChangeDetectorRef, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { FiveASideService } from '@yourcall/services/fiveASide/five-a-side.service';
import { ITeamColours, ITeamsExist } from '@yourcall/services/fiveASide/five-a-side.model';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISystemConfig } from '@app/core/services/cms/models';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import environment from '@environment/oxygenEnvConfig';
@Component({
  selector: 'five-a-side-event-name-header',
  templateUrl: './five-a-side-event-name-header.component.html',
  styleUrls: ['./five-a-side-event-name-header.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FiveASideEventNameHeaderComponent implements OnInit, OnDestroy {
  @Input() eventId: number;
  @Input() sportId: string;
  @Input() eventCategory: string;

  readonly TEAMSIMAGEPATH: string = environment.CMS_ROOT_URI + environment.FIVEASIDE.svgImagePath;
  teamsColors: ITeamColours[] = [];
  noEntityName: string = 'No entity name';
  isLineupAvailable: boolean = false;
  lineupsTooltip: string;
  toolTipArgs: {[key: string]: string};
  showLineUp: boolean = false;
  private lineupsSubscription: Subscription;
  private readonly LINE_UPS_TOOLTIP = 'FiveASideLineUps';

  constructor(
    private fiveASideService: FiveASideService,
    private changeDetectorRef: ChangeDetectorRef,
    private cmsService: CmsService,
    private gtmService: GtmService) {
  }

  /**
   * Check if teams image exist on both home and away
   * @returns { boolean }
   */
  get teamsImgExistOnHomeAway(): boolean {
    return Object.keys(this.fiveASideService.imagesExistOnHomeAway).length === 2
      && Object.values(this.fiveASideService.imagesExistOnHomeAway).every(
        (team: ITeamsExist) => team.fiveASideToggle && team.filename);
  }

  set teamsImgExistOnHomeAway(value: boolean) {}

  ngOnInit(): void {
    this.fiveASideService.initTeamsColors(this.sportId, this.eventId).subscribe(() => {
      const colors = Object.entries(this.fiveASideService.teamsColors);
      colors.forEach(([key, value]) => {
        this.teamsColors.push({teamName: key, colors: value});
      });
      this.changeDetectorRef.markForCheck();
    });
    this.isLineupAvailable = this.fiveASideService.isLineupAvailable(this.eventId);
    this.setLineupsTooltip();
  }

  /**
   * To show/Hide tooltip
   */
  toggleLineups(): void {
    this.showLineUp = !this.showLineUp;
    const gtmData = {
      eventCategory: '5-A-Side',
      eventAction: 'click',
      eventLabel: 'Line Ups Not Available'
    };
    this.gtmService.push('trackEvent', gtmData);
  }

  /**
   * To trigger event on lineups button click
   */
  onOpenLineUp(): void {
    this.fiveASideService.setLineUps(this.eventId, this.eventCategory);
    const gtmData = {
      eventCategory: '5-A-Side',
      eventAction: 'click',
      eventLabel: 'Line Ups Button'
    };
    this.gtmService.push('trackEvent', gtmData);
  }

  ngOnDestroy(): void {
    this.lineupsSubscription && this.lineupsSubscription.unsubscribe();
  }

  /**
   * To get data from cms and show as part of lineups
   */
  private setLineupsTooltip(): void {
    this.lineupsSubscription = this.cmsService.getFeatureConfig(this.LINE_UPS_TOOLTIP).subscribe(
      (config: ISystemConfig) => {
        if (config && config.enabled) {
          this.lineupsTooltip = config.title;
          this.lineupsTooltip = this.lineupsTooltip.length > 200 ?
          `${this.lineupsTooltip.substring(0, 200)}...` : this.lineupsTooltip;
          this.toolTipArgs = {
            lineups: this.lineupsTooltip
          };
        }
      });
  }

}
