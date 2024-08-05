import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { GamingMenusModule } from './gaming-menus/gaming-menus.module';
import { HeaderMenusModule } from './header-menus/header-menus.module';
import { HeaderSubMenusModule } from './header-sub-menus/header-sub-menus.module';
import { HeaderMenusCreateComponent } from './header-menus/header-menus-create/header-menus-create.component';
import { ConnectMenusModule } from './connect-menus/connect-menus.module';
import { ConnectMenusCreateComponent } from './connect-menus/connect-menus-create/connect-menus-create.component';
import { RightMenusModule } from './right-menus/right-menus.module';
import { BankingMenusModule } from './banking-menus/banking-menus.module';
import { RightMenusCreateComponent } from './right-menus/right-menus-create/right-menus-create.component';
import { UserMenusModule } from './user-menus/user-menus.module';
import { UserMenusCreateComponent } from './user-menus/user-menus-create/user-menus-create.component';
import { FooterLogosModule } from './footer-logos/footer-logos.module';
import { FooterLogosCreateComponent } from './footer-logos/footer-logos-create/footer-logos-create.component';
import { FooterMenusModule } from './footer-menus/footer-menus.module';
import { FooterMenusCreateComponent } from './footer-menus/footer-menus-create/footer-menus-create.component';
import { TopGamesModule } from './top-games/top-games.module';
import { TopGamesCreateComponent } from './top-games/top-games-create/top-games-create.component';
import { BottomMenusModule } from './bottom-menus/bottom-menus.module';
import { BottomMenusCreateComponent } from './bottom-menus/bottom-menus-create/bottom-menus-create.component';
import { HeaderContactMenusModule } from './header-contact-menus/header-contact-menus.module';
import { HeaderContactMenusCreateComponent } from './header-contact-menus/header-contact-menus-create/header-contact-menus-create.component';
import { BankingMenusCreateComponent } from '@app/menus/banking-menus/banking-menus-create/banking-menus-create.component';
import { GamingMenusCreateComponent } from './gaming-menus/gaming-menus-create/gaming-menus-create.component';

@NgModule({
  imports: [
    CommonModule,
    HeaderMenusModule,
    HeaderSubMenusModule,
    ConnectMenusModule,
    RightMenusModule,
    BankingMenusModule,
    UserMenusModule,
    FooterLogosModule,
    FooterMenusModule,
    TopGamesModule,
    BottomMenusModule,
    HeaderContactMenusModule,
    GamingMenusModule
  ],
  entryComponents: [
    HeaderMenusCreateComponent,
    ConnectMenusCreateComponent,
    RightMenusCreateComponent,
    BankingMenusCreateComponent,
    UserMenusCreateComponent,
    FooterLogosCreateComponent,
    FooterMenusCreateComponent,
    TopGamesCreateComponent,
    BottomMenusCreateComponent,
    HeaderContactMenusCreateComponent,
    GamingMenusCreateComponent
  ]
})
export class MenusModule { }
