import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PromotionsPageComponent } from './promotions-list/promotions.page.component';
import { PromotionPageComponent } from './promotions-edit/pageComponent/promotion.page.component';
import { CreatePromotionComponent } from './promotions-create/create.promotion.page.component';
import { SectionsComponent } from './sections/sections.component';
import { SectionComponent } from './section/section.component';
import { NavigationEditComponent } from '@root/app/promotions/navigation-edit/navigation-edit.component';
import { NavigationsComponent } from '@app/promotions/navigations/navigations.component';
import { LeaderboardComponent } from '@app/promotions/leaderboard/leaderboard.component';
import { LeaderboardEditComponent } from '@app/promotions/leaderboard-edit/leaderboard-edit.component';
import { LeaderboardCreateComponent } from '@app/promotions/leaderboard-create/leaderboard-create.component';
import { NavigationContentCreateComponent } from './navigation-content-create/navigation-content-create.component';

const promotionsRoutes: Routes = [
  { path: '', component: PromotionsPageComponent },
  { path: 'create',  component: CreatePromotionComponent },
  { path: 'promotion/:id',  component: PromotionPageComponent },
  { path: 'sections',  component: SectionsComponent },
  { path: 'section/:id',  component: SectionComponent },
  { path: 'navigations',  component: NavigationsComponent },
  { path: 'navigation/:id',  component: NavigationEditComponent },
  { path: 'navigationCreate/:id',  component: NavigationContentCreateComponent },
  { path: 'navigationEdit/:id/:nId',  component: NavigationContentCreateComponent },
  { path: 'leaderboard',  component: LeaderboardComponent },
  { path: 'createLeaderboard',  component: LeaderboardCreateComponent },
  { path: 'leaderboard/:id',  component: LeaderboardEditComponent },
];

@NgModule({
  imports: [
    RouterModule.forChild(promotionsRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class PromotionsRoutingModule {}
