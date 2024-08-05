import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { LiveStreamWrapperComponent } from '@bma/components/liveStream/live-stream-wrapper.component';

const routes: Routes = [
  {
    path: '',
    component: LiveStreamWrapperComponent,
    data: {
      segment: 'liveStream'
    }
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class LiveStreamWrapperRoutingModule {}

