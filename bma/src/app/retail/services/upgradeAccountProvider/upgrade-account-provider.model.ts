export interface IResponseCommonModel {
  id: string;
  errorCode: number;
  errorMessage: string;
  data: any;
  accessToken: string;
  body?: IGetIdTokenInfoFromUserNameResponseModel;
}

export interface IRequestCommonModel {
  username?: string;
  customerSessionId?: string;
  cardNo?: string;
  pin?: number;
  cardNumber?: string;
}

export interface IAuthenticateResponseModel extends IResponseCommonModel {
  data: {
    resultMessage: string;
    resultCode: number;
    authenticationStatus: string;
    playerCode: string;
  };
}

export interface ICheckEligibilityResponseModel extends IResponseCommonModel {
  data: {
    isEligible: boolean;
    resultMessage: string;
    resultCode: number;
  };
}

export interface IGetPlayerInfoResponseModel extends IResponseCommonModel {
  data: {
    activeIdToken: string;
    accountBusinessPhase: string;
    address: string;
    ageVerificationStatus: string;
    birthDate: string;
    cellPhone: string;
    city: string;
    countryCode: string;
    currency: string;
    email: string;
    firstName: string;
    frozen: string;
    lastName: string;
    phone: string;
    suspended: string;
    title: string;
    username: string;
    signupDate: string;
    zip: string;
    smsPromo: boolean;
    emailPromo: boolean;
  };
}

export interface IUpgradeAccountResponseModel extends IResponseCommonModel {
  data: {
    resultMessage: string;
    reason: string;
  };
}

export interface IGetIdTokenInfoFromUserNameResponseModel extends IResponseCommonModel {
  data: {
    printedTokenCode: string;
  };
}

export interface IGetWebTokenResponseModel extends IResponseCommonModel {
  data: {
    token: string;
  };
}
