package com.coral.oxygen.middleware.ms.quickbet.impl;

import static org.assertj.core.api.Assertions.assertThat;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputPrice;
import com.coral.oxygen.middleware.ms.quickbet.impl.ScorecastPriceService.ScorecastType;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class ScorecastPriceServiceTest {

  @Nested
  class Calculate {

    @Nested
    class WhenFileNameIsNotCorrect {
      @Test
      void shouldReturnEmpty() {
        ScorecastPriceService calculator = new ScorecastPriceService("incorrectFilename");

        Optional<OutputPrice> result = calculator.calculate(0.0, 10.0, ScorecastType.W);

        assertThat(result).isEmpty();
      }
    }

    @Nested
    public class WhenFileNameIsCorrect {

      ScorecastPriceService calculator;

      @BeforeEach
      void setUp() {
        calculator = new ScorecastPriceService("scorecastTableTest.csv");
      }

      @ParameterizedTest
      @CsvSource({
        "W, 9.5,   45.4,      250, 1",
        "W, 8.6,   24.9,      125, 1",
        "D, 5.6,   16.999999, 66,  1",
        "L, 8.501, 67.001,    500, 1"
      })
      void shouldReturnNotEmpty(
          ScorecastType type,
          double correctPrice,
          double scorerPrice,
          int expectedPriceNum,
          int expectedPriceDen) {

        Optional<OutputPrice> result = calculator.calculate(correctPrice, scorerPrice, type);

        assertThat(result).isNotEmpty();
        assertThat(result.get().getPriceNum().intValue()).isEqualTo(expectedPriceNum);
        assertThat(result.get().getPriceDen().intValue()).isEqualTo(expectedPriceDen);
      }

      @Test
      void whenScorerPriceIsOutOfRange_ShouldReturnEmpty() {

        Optional<OutputPrice> result = calculator.calculate(9.5, 105.00, ScorecastType.W);

        assertThat(result).isEmpty();
      }

      @Test
      void whenCorrectPriceIsOutOfRange_ShouldReturnEmpty() {

        Optional<OutputPrice> result = calculator.calculate(105.00, 100.00, ScorecastType.W);

        assertThat(result).isEmpty();
      }
    }
  }

  @Nested
  class GenerateScorecastType {
    @Test
    void whenCsHomeMoreThenCsAwayAndFsResultIsH_ShouldReturnW() {
      ScorecastType result = ScorecastType.generate(2, 0, "H");
      assertThat(result).isEqualTo(ScorecastType.W);
    }

    @Test
    void whenCsHomeMoreThenCsAwayAndFsResultIsNotH_ShouldReturnL() {
      ScorecastType result = ScorecastType.generate(2, 1, "A");
      assertThat(result).isEqualTo(ScorecastType.L);
    }

    @Test
    void whenCsHomeLessThenCsAwayAndFsResultIsA_ShouldReturnW() {
      ScorecastType result = ScorecastType.generate(0, 1, "A");
      assertThat(result).isEqualTo(ScorecastType.W);
    }

    @Test
    void whenCsHomeLessThenCsAwayAndFsResultIsNotA_ShouldReturnL() {
      ScorecastType result = ScorecastType.generate(0, 1, "H");
      assertThat(result).isEqualTo(ScorecastType.L);
    }

    @Test
    void whenCsHomeEqualsCsAway_ShouldReturnD() {
      ScorecastType result = ScorecastType.generate(0, 0, "H");
      assertThat(result).isEqualTo(ScorecastType.D);
    }
  }
}
