import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'featured-events',
    loadChildren: () => import('app/sports-modules/featured-events-module/featured-events-module.module')
      .then(m => m.FeaturedEventsModuleModule)
  },
  {
    path: 'sports-quick-links',
    loadChildren: () => import('app/sports-modules/quick-links-module/sports-quick-links.module')
      .then(m => m.SportsQuickLinksModule)
  },
  {
    path: 'sports-highlight-carousels',
    loadChildren: () => import('app/sports-modules/highlight-carousels-module/highlight-carousels.module')
      .then(m => m.SportsHighlightCarouselsModule)
  },
  {
    path: 'inplay',
    loadChildren: () => import('app/sports-modules/inplay-module/inplay.module').then(m => m.InplayModule)
  },
  {
    path: 'surface-bets',
    loadChildren: () => import('app/sports-modules/surface-bets/surface-bets.module').then(m => m.SportsSurfaceBetsModule)
  },
  {
    path: 'recently-played-games',
    loadChildren: () => import('app/sports-modules/recently-played-games-module/recently-played-games.module')
      .then(m => m.RecentlyPlayedGamesModule)
  },
  {
    path: 'aem-banner',
    loadChildren: () => import('app/sports-modules/aem-banner-module/aem-banner.module').then(m => m.AemBannerModule)
  },
  {
    path: 'racing-module',
    loadChildren: () => import('app/sports-modules/racing-module/racing.module').then(m => m.RacingModule)
  },
  {
    path: 'sport-fanzone',
    loadChildren: () => import('app/sports-modules/sport-fanzone/sport-fanzone.module').then(m => m.SportFanzoneModule)
  },{
    path: 'pre-play',
    loadChildren: () => import('app/sports-modules/pre-play-popular-bets/pre-play-popular-bets.module').then(m => m.PreplayPopularbetsModule)
  },
  {
    path: 'next-event-carousel',
    loadChildren: () => import('app/sports-modules/next-event-carousel-module/next-event-carousel.module').then(m => m.NextEventCarouselModule)
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class SportsModulesRoutingModule { }
