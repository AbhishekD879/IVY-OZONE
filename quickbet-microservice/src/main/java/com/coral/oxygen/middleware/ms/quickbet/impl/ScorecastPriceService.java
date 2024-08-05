package com.coral.oxygen.middleware.ms.quickbet.impl;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputPrice;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Component;

@Component
public class ScorecastPriceService {

  private String fileName;
  private List<ScorecastData> scorecastDataList;

  public ScorecastPriceService(@Value("${scorecast.table.csv:empty_file}") String fileName) {
    this.fileName = fileName;
  }

  enum ScorecastType {
    W,
    D,
    L;

    static ScorecastType generate(int csHome, int csAway, String fsResult) {
      if (csHome > csAway) {
        return fsResult.equals("H") ? W : L;
      } else if (csHome < csAway) {
        return fsResult.equals("A") ? W : L;
      } else {
        return D;
      }
    }
  }

  private class ScorecastData {
    ScorecastType type;
    Double csLowPrice;
    Double csHighPrice;
    Double fgLowPrice;
    Double fgHighPrice;
    int priceNum;
    int priceDen;
  }

  public Optional<OutputPrice> calculate(
      Double correctPrice, Double scorerPrice, ScorecastType type) {

    if (scorecastDataList == null) {
      try (BufferedReader br =
          new BufferedReader(
              new InputStreamReader(new ClassPathResource(fileName).getInputStream()))) {
        // skip the header of the csv
        scorecastDataList =
            br.lines().skip(1).map(this::mapToScorecast).collect(Collectors.toList());

      } catch (IOException e) {
        return Optional.empty();
      }
    }
    return scorecastDataList.stream()
        .filter(
            x ->
                x.type.equals(type)
                    && x.csLowPrice.compareTo(correctPrice) < 0
                    && x.csHighPrice.compareTo(correctPrice) >= 0
                    && x.fgLowPrice.compareTo(scorerPrice) < 0
                    && x.fgHighPrice.compareTo(scorerPrice) >= 0)
        .findFirst()
        .map(this::convertToPrice);
  }

  private OutputPrice convertToPrice(ScorecastData x) {
    OutputPrice price = new OutputPrice();
    price.setPriceDen(x.priceDen);
    price.setPriceNum(x.priceNum);
    return price;
  }

  private ScorecastData mapToScorecast(String line) {
    String[] p = line.split(" \\|");
    ScorecastData item = new ScorecastData();
    item.type = ScorecastType.valueOf(p[1]);
    item.csLowPrice = Double.valueOf(p[2]);
    item.csHighPrice = Double.valueOf(p[3]);
    item.fgLowPrice = Double.valueOf(p[4]);
    item.fgHighPrice = Double.valueOf(p[5]);
    item.priceNum = Integer.parseInt(p[6]);
    item.priceDen = Integer.parseInt(p[7]);
    return item;
  }
}
