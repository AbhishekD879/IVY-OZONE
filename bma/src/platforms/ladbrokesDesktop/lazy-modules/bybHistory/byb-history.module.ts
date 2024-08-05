import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';



import {
  LadbrokesBybSelectionsComponent
} from '@ladbrokesMobile/lazy-modules/bybHistory/components/bybSelections/byb-selections.component';
import { BetStatusIndicatorComponent } from '@lazy-modules/bybHistory/components/betStatusIndicator/bet-status-indicator.component';
import { ProgressBarComponent } from '@lazy-modules/bybHistory/components/progressBar/progress-bar.component';
import { SharedModule } from '@sharedModule/shared.module';
import { OptaInfoComponent } from '@lazy-modules/bybHistory/components/optaInfo/opta-info.component';
import { AlignTooltipDirective } from '@bybHistoryModule/directives/align-tooltip.directive';
import { BybProgressBarComponent } from '@app/lazy-modules/bybHistory/components/bybProgressBar/byb-progress-bar.component';
import { BybTimelineComponent } from '@app/lazy-modules/bybHistory/components/bybTimeline/byb-timeline.component';
import { BybTeamNameComponent } from '@app/lazy-modules/bybHistory/components/bybTeamNames/byb-teamname.component';
import { BybIncrementComponent } from '@app/lazy-modules/bybHistory/components/bybIncrement/byb-increment.component';
import { BybCounterComponent } from '@app/lazy-modules/bybHistory/components/bybCounter/byb-counter.component';
import { BybCustomComponent } from '@app/lazy-modules/bybHistory/components/bybCustom/byb-custom.component';
import { BybLayoutComponent } from '@app/lazy-modules/bybHistory/components/bybLayout/byb-layout.component';
import { BybTabsComponent } from '@app/lazy-modules/bybHistory/components/bybTabs/byb-tabs.component';
import { BybTabComponent } from '@app/lazy-modules/bybHistory/components/bybTab/byb-tab.component';
import { BybPlayerstatsComponent } from '@app/lazy-modules/bybHistory/components/bybPlayerstats/byb-player-stats.component';



@NgModule({
  imports: [
    SharedModule,

  ],
  declarations: [
    LadbrokesBybSelectionsComponent,
    BetStatusIndicatorComponent,
    ProgressBarComponent,
    OptaInfoComponent,
    AlignTooltipDirective,
    BybProgressBarComponent,
    BybTimelineComponent,
    BybTeamNameComponent,
    BybIncrementComponent,
    BybCounterComponent,
    BybCustomComponent,
    BybLayoutComponent,
    BybTabsComponent,
    BybTabComponent,

    BybPlayerstatsComponent,
  ],
  providers: [],
  exports: [
    LadbrokesBybSelectionsComponent,
    OptaInfoComponent,
    AlignTooltipDirective,
    ProgressBarComponent,
    BybLayoutComponent,
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class LazyBybHistoryModule {
  static entry = { LadbrokesBybSelectionsComponent, OptaInfoComponent, BybLayoutComponent };
}
