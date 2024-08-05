import { Injectable } from '@angular/core';
import { UserService } from '@core/services/user/user.service';
import { CommandService } from '@coreModule/services/communication/command/command.service';
import { Observable, from } from 'rxjs';

@Injectable()
export class SessionService {
  constructor(
    private userService: UserService,
    private command: CommandService
  ) {
    this.command.register(this.command.API.WHEN_PROXY_SESSION, () =>
      this.whenProxySession().catch(e => console.warn(e)));
  }

  whenSession(): Promise<void> {
    /**
     * it has a method with the name of the old service which we don't use in vanilla,
     * but we resolve or reject it via events from vanilla auth
     */
    return this.userService.getOpenApiAuth();
  }

  whenProxySession<T>(): Promise<T> {
    if (this.userService.sessionToken) {
      return this.userService.getProxyAuth();
    }

    return Promise.reject('no Session Token');
  }

  whenUserSession<T>(): Observable<T> {
    return from(this.whenSession().then(() => this.userService.getProxyAuth()));
  }
}
