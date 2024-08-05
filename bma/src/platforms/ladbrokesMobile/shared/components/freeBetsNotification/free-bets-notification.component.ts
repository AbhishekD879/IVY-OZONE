import { ChangeDetectionStrategy, Component } from '@angular/core';
import { FreeBetsNotificationComponent as AppFreeBetsNotificationComponent } from '@app/shared/components/freeBetsNotification/free-bets-notification.component';

@Component({
    selector: 'free-bets-notification',
    templateUrl: '../../../../../app/shared/components/freeBetsNotification/free-bets-notification.component.html',
    styleUrls: ['../../../../../app/shared/components/freeBetsNotification/free-bets-notification.component.scss', 'free-bets-notification.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush
  })
  export class FreeBetsNotificationComponent extends AppFreeBetsNotificationComponent{}