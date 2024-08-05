import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GamificationListComponent } from './gamification-list/gamification-list.component';
import { GamificationDetailsComponent } from './gamification-details/gamification-details.component';
import { OtfGamificationRoutingModule } from './otf-gamification-routing.module';
import { SharedModule } from '@root/app/shared/shared.module';
import { SeasonsApiService } from '@root/app/one-two-free//service/seasons.api.service';

@NgModule({
  declarations: [
    GamificationListComponent,
    GamificationDetailsComponent
  ],
  imports: [
    CommonModule,
    OtfGamificationRoutingModule,
    SharedModule
  ],
  providers: [SeasonsApiService],
  schemas: [NO_ERRORS_SCHEMA]

})
export class OtfGamificationModule { }
