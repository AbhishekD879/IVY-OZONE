export class QuizPopupModel {
  public iconSvgPath: string;
  public header: string;
  public description: string;
  public submitCTAText: string;
  public closeCTAText: string;

  constructor(
    iconSvgPath: string,
    header: string,
    description: string,
    submitCTAText: string,
    closeCTAText: string
  ) {
    this.iconSvgPath = iconSvgPath;
    this.header = header;
    this.description = description;
    this.submitCTAText = submitCTAText;
    this.closeCTAText = closeCTAText;
    }
}


