export interface IDateRangeObject {
  startDate: string;
  endDate?: string;
}

export interface IPreviousResults {
  id? : string | number;
  balls ? : [];
  noOfBalls? : string | number;
  drawAt? : string;
  bonusBall? : string;
  drawName : string;

}
