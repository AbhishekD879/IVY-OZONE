import { browser, by, element } from 'protractor';

export class AppPage {
  navigateTo() {
    browser.waitForAngularEnabled(false);
    return browser.get('http://bm-tst1.coral.co.uk');
  }

  getLoginButton() {
    return element(by.css('[data-crlat="signInButton"]'));
  }

  getLoginModal() {
    return element(by.css('.login-form'));
  }

  getUserAccountIcon() {
    return element(by.css('[data-crlat="accountIcon"]'));
  }

  logIn() {
    const username = element(by.css('[data-crlat="username"]'));
    const password = element(by.css('[data-crlat="password"]'));
    username.sendKeys('felino');
    password.sendKeys('qwerty');
    element(by.css('[data-crlat="loginButton"]')).click();
  }
}
