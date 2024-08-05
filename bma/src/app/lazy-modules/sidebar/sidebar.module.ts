import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from './components/sidebar.component';
import { SharedModule } from '@sharedModule/shared.module';
@NgModule({
  imports: [CommonModule, SharedModule],
  declarations: [SidebarComponent],
  exports: [SidebarComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class SideBarModule {
  static entry = SidebarComponent;
}