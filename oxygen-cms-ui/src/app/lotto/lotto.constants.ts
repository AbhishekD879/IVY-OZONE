import { ILotto, ILottos, ILottoUpdate } from "./lotto.model";

export const LOTTO_ROUTES = {
    base: '/lotto',
    add: 'add',
    details: ':id'
  };
export const LOTTO_VALUES: ILotto = {
    id: '',
    updatedBy: '',
    updatedAt: '',
    createdBy: '',
    createdAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    brand: 'ladbrokes',
    globalBannerLink: '',
    globalBannerText: '',
    dayCount: null,
    svgId: "",
    lottoConfig: [
        {
        id: '',
        createdAt: '',
        createdBy: '',
        updatedAt: '',
        updatedBy: '',
        updatedByUserName: '',
        createdByUserName: '',
        brand: null,
        label: '',
        infoMessage: '',
        nextLink: '',
        bannerLink: '',
        bannerText: '',
        ssMappingId: '',
        maxPayOut: null,
        svgId: '',
        sortOrder: null,
        enabled: false,
        svgFilename: {
            filename: '',
            path: '',
            size: null,
            filetype: '',
            originalname: ''
          }
        }
    ],
    ids: null
}
export const LOTTOS_VALUES: ILottos = {
    id: '',
    updatedBy: '',
    updatedAt: '',
    createdBy: '',
    createdAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    brand: '',
    label: '',
    infoMessage: '',
    nextLink: '',
    bannerLink: '',
    bannerText: '',
    ssMappingId: '',
    maxPayOut: null,
    svgId: '',
    sortOrder: 0,
    enabled: false,
    svgFilename: {
        filename: '',
        path: '',
        size: null,
        filetype: '',
        originalname: '',
      },
}
export const LOTTOS_UPDATE: ILottoUpdate = {
  globalBannerLink: '',
  globalBannerText: '',
  dayCount: null,
  ids: null
}