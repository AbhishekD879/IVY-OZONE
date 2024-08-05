export interface myBetsPayload{
  brand:string;
  type: string;
  noBetText:string;
  addDiscText:string;
  defaultImgLink:string;
  brandedImageList: brandedImageList[];

}
export interface brandedImageList{
    imgLink: string;
    fromDate: string,
    toDate: string,
}