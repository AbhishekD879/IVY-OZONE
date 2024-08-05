export interface ILoginOpenDialogEvent {
  moduleName: string;
  placeBet: string | boolean;
  isDuplicateError: boolean;
  disableRememberMe: boolean;
  message: string;
}
