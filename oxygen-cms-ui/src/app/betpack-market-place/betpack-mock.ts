export const BetPackModelMock: any = {
    betPackId: null,
    betPackTitle: 'x',
    betPackPurchaseAmount: null,
    betPackFreeBetsAmount: null,
    betPackFrontDisplayDescription: '',
    betPackMoreInfoText: '',
    betPackSpecialCheckbox: false,
    sportsTag: [],
    betPackStartDate: new Date(),
    betPackEndDate: null,
    maxTokenExpirationDate: new Date().toISOString(),
    futureBetPack: false,
    filterBetPack: false,
    filterList: [],
    betPackActive: false,
    triggerID: null,
    betPackTokenList:[{
        tokenId: 1,
        tokenTitle: "123"
    }],
    sortOrder: null,
    brand: 'Coral',
    id: '1',
    updatedBy: '',
    updatedAt: '',
    createdBy: '',
    createdAt: '',
    updatedByUserName: '',
    createdByUserName: '',
}
export const NewFilterMockemp : any = {
    filterName: '',
    filterActive: false,
    brand: 'Coral',
    id: '',
    updatedBy: '',
    updatedAt: '',
    createdBy: '',
    createdAt: '',
    updatedByUserName: '',
    createdByUserName: '',
  };
  export const NewFilterMock : any = {
    filterName: 'edeedd!@$',
    filterActive: false,
    brand: 'Coral',
    id: '',
    updatedBy: '',
    updatedAt: '',
    createdBy: '',
    createdAt: '',
    updatedByUserName: '',
    createdByUserName: '',
  };
  export const NewFilterMock1 : any = {
    filterName: 'All',
    filterActive: false,
    brand: 'Coral',
    id: '',
    updatedBy: '',
    updatedAt: '',
    createdBy: '',
    createdAt: '',
    updatedByUserName: '',
    createdByUserName: '',
  };
  export const EditNewFilterMock : any =  {
    filterName: 'aLL',
    filterActive: true,
    isLinkedFilter :true,
    linkedFilterWarningText:'test'
}
export const EditNewFilterMock1 : any =  {
  filterName:undefined,
  filterActive: true,
  isLinkedFilter :true,
  linkedFilterWarningText:'test'
}
export const EditNewFilterMock2 : any =  {
  filterName:'@',
  filterActive: true,
  isLinkedFilter :true,
  linkedFilterWarningText:'test'
}
export const ValidBP: any = {
  betPackId: '1',
  betPackPurchaseAmount: 2,
  betPackEndDate: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString(),
  betPackFreeBetsAmount: 1,
  betPackStartDate: new Date().toISOString(),
  triggerID: '1',
  betPackFrontDisplayDescription: 'qwertyui',
  betPackTitle: 'qwertyui',
  betPackTokenList: ['1'],
  sportsTag: ['1', '2'],
  filterBetPack: false,
  filterList: [],
  betPackMoreInfoText: 'qwerty',
  maxClaims:1,
  maxTokenExpirationDate: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString(),

}
export const BetpackData: any = {
  betPackId: null,
  betPackTitle: '',
  betPackPurchaseAmount: null,
  betPackFreeBetsAmount: null,
  betPackFrontDisplayDescription: '',
  betPackMoreInfoText: '',
  betPackSpecialCheckbox: false,
  sportsTag: [],
  betPackStartDate: null,
  betPackEndDate: null,
  maxTokenExpirationDate: new Date().toISOString(),
  futureBetPack: false,
  filterBetPack: false,
  filterList: [],
  betPackActive: false,
  triggerID: null,
  betPackTokenList: [],
  sortOrder: null,
  brand: 'Coral',
  id: '',
  updatedBy: '',
  updatedAt: '',
  createdBy: '',
  createdAt: '',
  updatedByUserName: '',
  createdByUserName: '',

}
export const onboardImageDataModel: any = {
  isActive: true,
  images: [{ id: '1' }]
}
export const onboardFormArray: any = [{
  onboardImageDetails: [{
    filename: 'qwe',
    originalname: 'qwe',
    path: '/',
    filetype: 'sdf',
    size: 12,
  }],
  id : '1',
  isAdd : false,
  onboardImg: 'xyz',
  imageType: 'abc',
  imageLabel: 'efg',
  nextCTAButtonLabel: '123'
}]
export const onboardFormDataModel: any = {
  id: '1',
  isAdd : false,
  onboardImageDetails: [],
  onboardImg: '',
  imageType: '',
  imageLabel: '',
  nextCTAButtonLabel: ''
}
export const onboardFormDataModelNoId: any = {
  id : '2',
  isAdd : true,
  onboardImageDetails: [],
  onboardImg: '',
  imageType: '',
  imageLabel: '',
  nextCTAButtonLabel: ''
}
export const onboardFormDataModelNoId1: any = {
  id : '1',
  isAdd : true,
  onboardImageDetails: [],
  onboardImg: '',
  imageType: '',
  imageLabel: '',
  nextCTAButtonLabel: ''
}
export const onboardFormArray1: any = [{
  onboardImageDetails: [{
    filename: 'qwe',
    originalname: 'qwe',
    path: '/',
    filetype: 'sdf',
    size: 12,
  }],
  id : '1',
  isAdd : false,
  onboardImg: 'xyz',
  imageType: 'abc',
  imageLabel: 'efg',
  nextCTAButtonLabel: '123'
}]
