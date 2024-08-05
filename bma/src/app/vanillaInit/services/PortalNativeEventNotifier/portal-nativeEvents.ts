export enum PortalNativeEvents {
  OpenRegistrationScreen = 'openRegistrationScreen',
  CloseRegistrationScreen = 'CLOSEREGISTRATIONSCREEN',
  RegistrationScreenActive = 'Registration_Screen_Active',
  RegistrationSuccessful = 'REGISTRATION',
  UpdatePassword = 'PasswordUpdate',
  PreLogin = 'PRE_LOGIN',
  PostLogin = 'POST_LOGIN',
  Login = 'LOGIN',
  MenuScreenActive = 'MENU_SCREEN_ACTIVE'
}

export type LoginType = 'Manual' | 'Autologin';
