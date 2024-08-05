import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable()
export class AuthService {

  constructor(private router: Router) {}

  // ...
  public logOut(): any {
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }
  // ...
  public isAuthenticated(): boolean {
    const token = localStorage.getItem('token');
    // Check whether the token is expired and return
    // true or false
    return token ? true : false;
  }
}
