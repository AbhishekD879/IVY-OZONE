import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@app/shared/shared.module';
import { SportsSurfaceBetsRoutingModule } from '@app/sports-modules/surface-bets/surface-bets-routing.module';
import { SportsSurfaceBetsListComponent } from '@app/sports-modules/surface-bets/surface-bets-list/surface-bets-list.component';
import { SportsSurfaceBetsDetailsComponent } from '@app/sports-modules/surface-bets/surface-bets-details/surface-bets-details.component';
import { SportsSurfaceBetsService } from '@app/sports-modules/surface-bets/surface-bets.service';
import { SurfaceBetModuleComponent } from '@app/sports-modules/surface-bets/surface-bet-module/surface-bet-module.component';
import { SortByPipe } from '@app/client/private/pipes/sortBy.pipe';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    SportsSurfaceBetsRoutingModule
  ],
  declarations: [
    SportsSurfaceBetsListComponent,
    SurfaceBetModuleComponent,
    SportsSurfaceBetsDetailsComponent,
    SortByPipe
  ],
  entryComponents: [
    SurfaceBetModuleComponent,
    SportsSurfaceBetsListComponent
  ],
  providers: [SportsSurfaceBetsService,SortByPipe],
  exports: []
})
export class SportsSurfaceBetsModule {
}
