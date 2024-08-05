import {NgModule} from '@angular/core';
import {SharedModule} from '../shared/shared.module';
import {PromotionsRoutingModule} from './promotions-routing.module';
import {PromotionsPageComponent} from './promotions-list/promotions.page.component';
import {PromotionsAPIService} from './service/promotions.api.service';
import {PromotionPageComponent} from './promotions-edit/pageComponent/promotion.page.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {CreatePromotionComponent} from './promotions-create/create.promotion.page.component';
import { SectionsComponent } from './sections/sections.component';
import { SectionComponent } from './section/section.component';
import { AddPromotionsSectionsComponent } from './add-promotions-sections/add-promotions-sections.component';
import { NavigationEditComponent } from '@root/app/promotions/navigation-edit/navigation-edit.component';
import { NavigationsComponent } from '@app/promotions/navigations/navigations.component';
import { AddNavigationGroupComponent } from '@app/promotions/add-navigation-group/add-navigation-group.component';
import { CommonModule } from '@angular/common';
import { LeaderboardComponent } from '@app/promotions/leaderboard/leaderboard.component';
import { LeaderboardEditComponent } from '@app/promotions/leaderboard-edit/leaderboard-edit.component';
import { LeaderboardCreateComponent } from '@app/promotions/leaderboard-create/leaderboard-create.component';
import { NavigationContentCreateComponent } from './navigation-content-create/navigation-content-create.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    PromotionsRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ],
  declarations: [
    PromotionPageComponent,
    PromotionsPageComponent,
    CreatePromotionComponent,
    SectionsComponent,
    SectionComponent,
    AddPromotionsSectionsComponent,
    NavigationEditComponent,
    NavigationsComponent,
    AddNavigationGroupComponent,
    NavigationContentCreateComponent,
    LeaderboardComponent,
    LeaderboardCreateComponent,
    LeaderboardEditComponent,
  ],
  providers: [
    PromotionsAPIService
  ],
  entryComponents: [
    AddPromotionsSectionsComponent,
    AddNavigationGroupComponent
  ]
})
export class PromotionsModule { }
