import { Injectable } from "@angular/core";

@Injectable()
export class ScorecastDataService {
  scorecastData: any;
  setScorecastData(value: any) {
    this.scorecastData = value;
  }
  getScorecastData(): any {
    return this.scorecastData;
  }
}
