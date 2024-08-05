import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { BybSelectionsComponent } from '@lazy-modules/bybHistory/components/bybSelections/byb-selections.component';
import { BetStatusIndicatorComponent } from '@lazy-modules/bybHistory/components/betStatusIndicator/bet-status-indicator.component';
import { ProgressBarComponent } from '@lazy-modules/bybHistory/components/progressBar/progress-bar.component';
import { SharedModule } from '@sharedModule/shared.module';
import { OptaInfoComponent } from '@lazy-modules/bybHistory/components/optaInfo/opta-info.component';
import { AlignTooltipDirective } from '@bybHistoryModule/directives/align-tooltip.directive';
import { BybProgressBarComponent } from '@lazy-modules/bybHistory/components/bybProgressBar/byb-progress-bar.component';
import { BybLayoutComponent } from '@lazy-modules/bybHistory/components/bybLayout/byb-layout.component';
import { BybTimelineComponent } from '@lazy-modules/bybHistory/components/bybTimeline/byb-timeline.component';
import { BybTeamNameComponent } from '@lazy-modules/bybHistory/components/bybTeamNames/byb-teamname.component';
import { BybIncrementComponent } from '@lazy-modules/bybHistory/components/bybIncrement/byb-increment.component';
import { BybCounterComponent } from '@lazy-modules/bybHistory/components/bybCounter/byb-counter.component';
import { BybCustomComponent } from './components/bybCustom/byb-custom.component';
import { BybTabsComponent } from './components/bybTabs/byb-tabs.component';
import { BybTabComponent } from './components/bybTab/byb-tab.component';
import { BybPlayerstatsComponent } from './components/bybPlayerstats/byb-player-stats.component';
@NgModule({
  imports: [
    SharedModule,

],
  declarations: [
    BybTabsComponent,
    BybTabComponent,
    BybSelectionsComponent,
    BetStatusIndicatorComponent,
    ProgressBarComponent,
    OptaInfoComponent,
    AlignTooltipDirective,
    BybProgressBarComponent,
    BybLayoutComponent,
    BybTimelineComponent,
    BybTeamNameComponent,
    BybCounterComponent,
    BybCustomComponent,
    BybIncrementComponent,

    BybPlayerstatsComponent,
  ],
  providers: [],
  exports: [
    BybSelectionsComponent,
    OptaInfoComponent,
    AlignTooltipDirective,
    ProgressBarComponent,
    BybLayoutComponent,
    BybTabsComponent,
    BybTabComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class LazyBybHistoryModule {
  static entry = { BybSelectionsComponent, OptaInfoComponent, BybLayoutComponent};
}
