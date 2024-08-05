import { ITypedMessage } from '@app/bpp/services/bppProviders/bpp-providers.model';

export interface IVoucher {
  isSent: boolean;
  gamingMessage: ITypedMessage;
  sportMessage: ITypedMessage;
  isValid: boolean;
  value: string;
  pattern: string;
}
