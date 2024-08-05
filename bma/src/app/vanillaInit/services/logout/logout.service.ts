import { of as observableOf, Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { AuthService } from '@frontend/vanilla/core';
@Injectable({
  providedIn: 'root'
})
export class LogoutResolver {
  constructor(private authService: AuthService) {
  }

  resolve(): Observable<void> {
    this.authService.logout();
    return observableOf(null);
  }
}
