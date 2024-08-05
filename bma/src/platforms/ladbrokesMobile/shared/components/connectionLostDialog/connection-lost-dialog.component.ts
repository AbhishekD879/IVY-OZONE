import { Component } from '@angular/core';
// eslint-disable-next-line max-len
import { ConnectionLostDialogComponent as AppConnectionLostDialogComponent } from '@app/shared/components/connectionLostDialog/connection-lost-dialog.component';

@Component({
  selector: 'connection-lost-dialog',
  templateUrl: 'connection-lost-dialog.component.html',
})
export class ConnectionLostDialogComponent extends AppConnectionLostDialogComponent  {
}
