import { AppPage } from './app.po';
import { browser, ExpectedConditions } from 'protractor';

describe('Log In', () => {
  let page: AppPage;

  beforeAll(() => {
    page = new AppPage();
    page.navigateTo();
    browser.sleep(5000);
  });

  it('should display Log In button', () => {
    expect(page.getLoginButton().getText()).toBe('LOG IN');
  });

  it('should display Log In popup', () => {
    page.getLoginButton().click();
    expect(page.getLoginModal().isDisplayed()).toBe(true);
  });

  it('should Log In successfully', () => {
    page.logIn();
    browser.wait(ExpectedConditions.visibilityOf(page.getUserAccountIcon()), 5000);
    expect(page.getUserAccountIcon().isDisplayed()).toBe(true);
  });
});
