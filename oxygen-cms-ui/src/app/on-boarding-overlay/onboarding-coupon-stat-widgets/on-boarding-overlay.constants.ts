import { IMyStable } from "../onboarding-mystable/onboarding-my-stable.model";
import { ICouponStatWidget } from "./onboarding-coupon-stat-widgets.model";

export const onboarding_stat_widget = {
    onBoarding: 'Coupon Stats Widget',
    headerTitle: 'Image label',
}
export const onboarding_ms_widget = {
  onBoarding: 'Coupon/Market Switcher Page',
  headerTitle: 'Image label',
}
export const ONBOARDING_OVERLAY_DEFAULT_VALUES: ICouponStatWidget = {
    id: '',
    updatedBy: '',
    updatedAt: '',
    createdBy: '',
    createdAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    brand: 'ladbrokes',
    imageLabel: "",
    buttonText: "",
    imageUrl: '',
    isEnable: false,
    directFileUrl: '',
    fileName: ''
}
export const ONBOARDING_OVERLAY_MyStable_DEFAULT_VALUES: IMyStable = {
  id: '',
  updatedBy: '',
  updatedAt: '',
  createdBy: '',
  createdAt: '',
  updatedByUserName: '',
  createdByUserName: '',
  brand: 'ladbrokes',
  buttonText: "",
  imageUrl: '',
  isActive: false,
  fileName: '',
  onboardImageDetails:{
    filename: '',
    originalname: '',
    path: '',
    filetype: ''
   }
}

export const onboarding_my_stable = {
  onBoarding: 'My Stable',
  headerTitle: 'Image label',
  enableOnboarding:'Enable Onboarding',
  useUploadedImage:'Use Uploaded image*',
  ctaButtonLabel:'CTA Button Label*',
  ctaButtonLabelErrMsg:'*The CTA button Label Should be filled with max of 12 characters',
  dialogTitle:'Error occurred',
  dialogMessage:'Ooops... Something went wrong, please contact support team',
  titleSuccess:'Success',
  saveFailed:'Error on saving',
  messageSuccess:'Your changes have been saved',
  errUnsupportedTitle:'Error. Unsupported file type.',
  errUnsupportedMessage:'Supported \"jpeg\" ,\"jpg\",\"svg\" and \"png\".',
  imageUploadMessage:'Image Was Uploaded.',
  imageRemovedMessage:'Image Was Removed.',

}