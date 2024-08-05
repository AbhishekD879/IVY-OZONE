export class QuestionEngineQuestionDetailsModel {
  public awayTeamName: string;
  public awayTeamSvgFilePath: string;
  public channelSvgFilePath: string;
  public description: string;
  public homeTeamName: string;
  public homeTeamSvgFilePath: string;
  public middleHeader: string;
  public signposting: string;
  public topLeftHeader: string;
  public topRightHeader: string;

  constructor(
    awayTeamName: string,
    awayTeamSvgFilePath: string,
    channelSvgFilePath: string,
    description: string,
    homeTeamName: string,
    homeTeamSvgFilePath: string,
    middleHeader: string,
    signposting: string,
    topLeftHeader: string,
    topRightHeader: string
  ) {
    this.awayTeamName = awayTeamName;
    this.awayTeamSvgFilePath = awayTeamSvgFilePath;
    this.channelSvgFilePath = channelSvgFilePath;
    this.description = description;
    this.homeTeamName = homeTeamName;
    this.homeTeamSvgFilePath = homeTeamSvgFilePath;
    this.middleHeader = middleHeader;
    this.signposting = signposting;
    this.topLeftHeader = topLeftHeader;
    this.topRightHeader = topRightHeader;
    }
}


