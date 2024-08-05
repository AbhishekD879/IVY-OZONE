import { NgModule } from '@angular/core';
import { CommonModule, } from '@angular/common';
import { BrowserModule  } from '@angular/platform-browser';
import {Routes, RouterModule, ExtraOptions, NoPreloading} from '@angular/router';
import {
  AuthGuardService as AuthGuard
} from './auth/auth-guard.service';
import { AuthService } from './auth/auth.service';

const routes: Routes = [
  {
    path: '',
    loadChildren: () => import('app/home/home.module').then(m => m.HomeModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'login',
    loadChildren: () => import('app/auth/auth.module').then(m => m.AuthModule)
  },
  { path: '**', redirectTo: '', pathMatch: 'full' }
];

const extraOptions: ExtraOptions = {
  preloadingStrategy: NoPreloading
};

@NgModule({
  imports: [
    CommonModule,
    BrowserModule,
    RouterModule.forRoot(routes, extraOptions)
  ],
  exports: [
    RouterModule
  ],
  providers: [AuthService, AuthGuard]
})
export class AppRoutingModule { }
