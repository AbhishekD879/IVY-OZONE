import { Routes } from '@angular/router';

export const ROOT_APP_ROUTES: Routes = [
  {
    path: 'p',
    loadChildren: () => import('@frontend/vanilla/features/public-page').then(m => m.ROUTES),
    data: {
        publicPageRoot: 'Playground-v1.0/PublicPages/'
    },
  },
  {
    path: '**',
    redirectTo: '/'
  }
];
