import {Component, OnInit, Renderer2} from '@angular/core';
import { FormControl, FormGroupDirective, NgForm, Validators } from '@angular/forms';
import { ErrorStateMatcher } from '@angular/material/core';
import { Router } from '@angular/router';

import { ApiClientService } from '@app/client/private/services/http';

/** Error when invalid control is dirty, touched, or submitted. */
export class MyErrorStateMatcher implements ErrorStateMatcher {

  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    const isSubmitted = form && form.submitted;
    return !!(control && control.invalid && (control.dirty || control.touched || isSubmitted));
  }

}

declare const window: any;

@Component({
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.scss']
})

export class AuthComponent implements OnInit {
  public interactionWithWindow: boolean = false;
  public errorMessage;
  public emailFormControl = new FormControl('', [
    Validators.required,
    Validators.email,
  ]);
  public passFormControl = new FormControl('', [
    Validators.required
  ]);
  public matcher = new MyErrorStateMatcher();

  constructor(
    private _apiClientService: ApiClientService,
    private router: Router,
    private renderer: Renderer2
  ) {

  }

  ngOnInit(): void {
    if (localStorage.getItem('token')) {
      this.router.navigate(['']);
    }

    // flag used to validate input fields only after interaction with window,
    // because browser input auto-prefill does not trigger any CHANGE event.
    this.renderer.listen(window, 'mousedown', () => {
      this.interactionWithWindow = true;
    });
  }

  isValid(): boolean {
    return !this.interactionWithWindow || (!!(this.emailFormControl.value && this.emailFormControl.value.length > 0 &&
              !this.emailFormControl.hasError('email') &&
              this.passFormControl.value && this.passFormControl.value.length > 0));
  }

  logIn(): void {
    const login = this.emailFormControl.value;
    const pass = this.passFormControl.value;
    localStorage.removeItem('token');
    this._apiClientService.authorisation().logIn(login, pass).subscribe(res => {
      let navigateTo: string = localStorage.getItem('redirectedFrom') ? localStorage.getItem('redirectedFrom') : '';
      localStorage.setItem('token', res.body.token);
      localStorage.setItem('refreshToken', res.body.refreshToken);
      if (navigateTo === '/login') {
        navigateTo = '';
      }
      this.router.navigate([navigateTo]);
    }, err => {
      if (err && err.error && err.error.message) {
        this.errorMessage = err.error.message;
        console.error(err);
      }
    });
  }
}
